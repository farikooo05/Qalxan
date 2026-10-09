"""Turn real SMS collected by the team into a labelled test set.

Input: data/real_sms.txt — one SMS per line; scams as-is, genuine messages prefixed with "OK|".
Output: data/real.jsonl. Then: python scripts/evaluate.py --test data/real.jsonl --tag real
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from qalxan.normalize import detect_language, has_mixed_script  # noqa: E402


def main():
    src = ROOT / "data" / (sys.argv[1] if len(sys.argv) > 1 else "real_sms.txt")
    out = ROOT / "data" / (sys.argv[2] if len(sys.argv) > 2 else "real.jsonl")
    rows = []
    for line in src.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        legit = line.upper().startswith("OK|")
        text = line[3:].strip() if legit else line
        rows.append({"text": text, "label": 0 if legit else 1, "scheme": "real_legit" if legit else "real_scam",
                     "lang": detect_language(text), "template_id": "real", "split": "real",
                     "obfuscated": has_mixed_script(text), "novel": False})
    with open(out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} real SMS ({sum(r['label'] for r in rows)} scam) -> {out}")


if __name__ == "__main__":
    main()
