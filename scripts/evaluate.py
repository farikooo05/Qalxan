"""Quality testing: compare the keyword filter (today's approach), a classic char n-gram model and Qalxan.

Usage: python scripts/evaluate.py [--llm] [--real data/real.jsonl]
Writes reports/eval.md, reports/metrics.json and charts.
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from qalxan.baseline import keyword_filter  # noqa: E402
from qalxan.model import QalxanModel  # noqa: E402

DATA = ROOT / "data"
REPORTS = ROOT / "reports"
HARD_NEG = {"bank_otp", "bank_info", "bank_payment", "operator_promo", "gov", "service_otp"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def metrics(y, p):
    tp = sum(1 for a, b in zip(y, p) if a == 1 and b == 1)
    fp = sum(1 for a, b in zip(y, p) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y, p) if a == 1 and b == 0)
    tn = sum(1 for a, b in zip(y, p) if a == 0 and b == 0)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {"precision": prec, "recall": rec, "f1": f1, "fpr": fpr, "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def recall_on(rows, preds, cond):
    idx = [i for i, r in enumerate(rows) if r["label"] == 1 and cond(r)]
    return (sum(preds[i] for i in idx) / len(idx) if idx else 0.0), len(idx)


def fpr_on(rows, preds, cond):
    idx = [i for i, r in enumerate(rows) if r["label"] == 0 and cond(r)]
    return (sum(preds[i] for i in idx) / len(idx) if idx else 0.0), len(idx)


def evaluate_system(name, rows, preds, latency_ms):
    y = [r["label"] for r in rows]
    m = metrics(y, preds)
    m["recall_obfuscated"], n_obf = recall_on(rows, preds, lambda r: r["obfuscated"])
    m["recall_novel"], n_nov = recall_on(rows, preds, lambda r: r["novel"])
    m["fpr_hard_negatives"], n_hard = fpr_on(rows, preds, lambda r: r["scheme"] in HARD_NEG)
    for lang in ("az", "ru", "en"):
        sub = [i for i, r in enumerate(rows) if r["lang"] == lang]
        m[f"f1_{lang}"] = metrics([y[i] for i in sub], [preds[i] for i in sub])["f1"]
    m["latency_ms"] = latency_ms
    m["name"] = name
    m["n"] = {"total": len(rows), "obfuscated": n_obf, "novel": n_nov, "hard_negatives": n_hard}
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", action="store_true", help="also run the Gemini layer on the grey band")
    ap.add_argument("--test", default=str(DATA / "test.jsonl"))
    ap.add_argument("--tag", default="synthetic")
    args = ap.parse_args()

    train = load(DATA / "train.jsonl")
    test = load(args.test)
    texts = [r["text"] for r in test]
    results = []

    t = time.perf_counter()
    kw = [1 if keyword_filter(x) else 0 for x in texts]
    results.append(evaluate_system("Keyword filter (today)", test, kw, (time.perf_counter() - t) * 1000 / len(test)))

    char_only = QalxanModel(use_rules=False, use_words=False).fit(
        [r["text"] for r in train], [r["label"] for r in train], [r["scheme"] for r in train])
    t = time.perf_counter()
    co = [1 if p >= 0.5 else 0 for p, _, _ in char_only.predict(texts)]
    results.append(evaluate_system("Classic ML (char n-grams)", test, co, (time.perf_counter() - t) * 1000 / len(test)))

    model = QalxanModel.load()
    t = time.perf_counter()
    out = model.predict(texts)
    lat = (time.perf_counter() - t) * 1000 / len(test)
    probs = [p for p, _, _ in out]
    qa = [1 if p >= 0.5 else 0 for p in probs]
    results.append(evaluate_system("Qalxan model", test, qa, lat))

    if args.llm:
        # The full production cascade: grey zone and risk signals go to Gemini.
        from qalxan.pipeline import Analyzer
        analyzer = Analyzer(model)
        final, calls, failed = [], 0, 0
        t = time.perf_counter()
        for i, x in enumerate(texts):
            r = analyzer.analyze(x, use_llm=True)
            if r["source"] == "model+gemini":
                calls += 1
                time.sleep(2)  # stay under the free-tier rate limit
            elif r["verdict"] == "suspicious":
                failed += 1
            final.append(1 if r["verdict"] == "scam" or (r["verdict"] == "suspicious" and probs[i] >= 0.5) else 0)
        m = evaluate_system("Qalxan + Gemini (full cascade)", test, final, (time.perf_counter() - t) * 1000 / len(test))
        m["llm_calls"], m["llm_failed"] = calls, failed
        results.append(m)

    # type accuracy on known schemes
    from qalxan.features import extract, rule_type
    known = [i for i, r in enumerate(test) if r["label"] == 1 and not r["novel"]]
    type_acc = sum(1 for i in known if (rule_type(extract(texts[i])) or out[i][1]) == test[i]["scheme"]) / len(known) \
        if known else 0.0

    failures = {
        "missed_scams": [{"text": test[i]["text"], "scheme": test[i]["scheme"], "p": round(probs[i], 3)}
                         for i in range(len(test)) if test[i]["label"] == 1 and qa[i] == 0][:15],
        "false_alarms": [{"text": test[i]["text"], "category": test[i]["scheme"], "p": round(probs[i], 3)}
                         for i in range(len(test)) if test[i]["label"] == 0 and qa[i] == 1][:15],
        "grey_band": sum(1 for p in probs if 0.2 < p < 0.8),
    }

    REPORTS.mkdir(exist_ok=True)
    with open(REPORTS / f"metrics_{args.tag}.json", "w", encoding="utf-8") as f:
        json.dump({"results": results, "type_accuracy": type_acc, "failures": failures}, f, ensure_ascii=False, indent=2)

    lines = [f"# Qalxan quality report ({args.tag})", "",
             f"Test set: {len(test)} SMS ({sum(r['label'] for r in test)} scam / "
             f"{len(test) - sum(r['label'] for r in test)} legit). Phrasings in the test set never appear in training; "
             f"two scam schemes exist only in the test set.", "",
             "| System | Precision | Recall | F1 | False alarms (all legit) | False alarms (bank/OTP/gov SMS) | "
             "Recall: letter-swapped | Recall: new schemes | ms/SMS |",
             "|---|---|---|---|---|---|---|---|---|"]
    for m in results:
        lines.append(f"| {m['name']} | {m['precision']:.1%} | {m['recall']:.1%} | {m['f1']:.3f} | {m['fpr']:.1%} | "
                     f"{m['fpr_hard_negatives']:.1%} | {m['recall_obfuscated']:.1%} | {m['recall_novel']:.1%} | "
                     f"{m['latency_ms']:.2f} |")
    lines += ["", f"Scam-type accuracy (known schemes): {type_acc:.1%}", "",
              f"Grey band (0.2 < p < 0.8, sent to the LLM layer): {failures['grey_band']} of {len(test)} messages", "",
              "## Missed scams (Qalxan model)", ""]
    lines += [f"- p={x['p']} [{x['scheme']}] {x['text']}" for x in failures["missed_scams"]] or ["- none"]
    lines += ["", "## False alarms (Qalxan model)", ""]
    lines += [f"- p={x['p']} [{x['category']}] {x['text']}" for x in failures["false_alarms"]] or ["- none"]
    (REPORTS / f"eval_{args.tag}.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:12 + len(results)]))

    try:
        make_chart(results, REPORTS / f"chart_{args.tag}.png")
    except ImportError:
        print("matplotlib not installed, skipping chart")


def make_chart(results, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = results[0]["n"]
    pairs = [("Scams caught\n(recall)", "recall"), ("Precision", "precision"),
             ("False alarms\n(all genuine SMS)", "fpr")]
    if n["obfuscated"]:
        pairs.append(("Scams caught:\nletter-swapped", "recall_obfuscated"))
    if n["novel"]:
        pairs.append(("Scams caught:\nnever-seen schemes", "recall_novel"))
    if n["hard_negatives"]:
        pairs.append(("False alarms on\nbank/OTP/gov SMS", "fpr_hard_negatives"))
    labels, keys = [p[0] for p in pairs], [p[1] for p in pairs]
    colors = ["#9aa0a6", "#c8a35a", "#1f6feb", "#2da44e"]
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=150)
    w = 0.8 / len(results)
    for k, m in enumerate(results):
        xs = [i + k * w for i in range(len(keys))]
        vals = [m[key] * 100 for key in keys]
        bars = ax.bar(xs, vals, w * 0.92, label=m["name"], color=colors[k % len(colors)])
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.0f}%", ha="center", fontsize=8)
    ax.set_xticks([i + w * (len(results) - 1) / 2 for i in range(len(keys))])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 110)
    ax.set_ylabel("%")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper center", ncol=len(results))
    fig.tight_layout()
    fig.savefig(path)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--chart-only":
        tag = sys.argv[2]
        with open(REPORTS / f"metrics_{tag}.json", encoding="utf-8") as f:
            make_chart(json.load(f)["results"], REPORTS / f"chart_{tag}.png")
    else:
        main()
