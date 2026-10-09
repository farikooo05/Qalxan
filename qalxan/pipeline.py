"""The cascade: rules + our model decide most messages; Gemini is asked only in the grey band."""
import time

from . import llm
from .baseline import keyword_filter
from .explain import TYPE_NAMES, explain_all, red_flags
from .features import extract, rule_type
from .model import MODEL_PATH, QalxanModel
from .normalize import detect_language, fold

SCAM_AT = 0.8   # model probability at or above which we call it a scam outright
SAFE_AT = 0.2   # at or below which we call it safe outright
RISK_FLAGS = ("asks_code", "personal_data", "remote_access", "brand_unofficial_link", "lookalike_domain")
SAFETY_NOTICE = ("hec vaxt", "hec kime", "hec kimle", "demeyin", "vermeyin", "paylasmayin", "никогда не", "никому не",
                 "не сообщайте", "не передавайте", "never ask", "will never", "do not share", "don't share",
                 "never share")


class Analyzer:
    def __init__(self, model: QalxanModel | None = None):
        if model is None:
            try:
                model = QalxanModel.load()
            except Exception:  # missing file or a different scikit-learn version: retrain (~10 s)
                from .synth import build_dataset
                rows = [r for r in build_dataset() if r["split"] == "train"]
                model = QalxanModel().fit([r["text"] for r in rows], [r["label"] for r in rows],
                                          [r["scheme"] for r in rows])
                try:
                    model.save()
                except OSError:
                    pass
        self.model = model

    def analyze(self, text: str, use_llm: bool = True) -> dict:
        t0 = time.perf_counter()
        sig = extract(text)
        prob, scam_type, type_conf = self.model.predict([text])[0]
        scam_type = rule_type(sig) or scam_type
        source = "model"
        llm_reason = None

        # Signals that should never be waved through on the model's word alone: send them for a second opinion.
        risky = any(sig["flags"].get(f) for f in RISK_FLAGS) or (sig["flags"]["new_number"] and sig["flags"]["money_request"])
        if risky and not sig["flags"]["unknown_link"] and any(w in fold(text) for w in SAFETY_NOTICE):
            risky = False  # "we never ask for your CVV" / "do not share this code" is a genuine notice
        if prob >= SCAM_AT:
            verdict = "scam"
        elif prob <= SAFE_AT and not risky:
            verdict = "safe"
        else:
            verdict = "suspicious"
            v = llm.llm_verdict(text) if use_llm else None
            if v is not None:
                source = "model+gemini"
                verdict = "scam" if v["is_scam"] else "safe"
                prob = (prob + float(v.get("confidence", 0.5) if v["is_scam"] else 1 - float(v.get("confidence", 0.5)))) / 2
                if v.get("scam_type") in TYPE_NAMES:
                    scam_type = v["scam_type"]
                llm_reason = {"az": v.get("reason_az"), "ru": v.get("reason_ru"), "en": v.get("reason_en")}

        explanation = explain_all(verdict, scam_type if verdict != "safe" else None, sig)
        if llm_reason and verdict != "safe":
            explanation = {k: f"{explanation[k]} {llm_reason[k] or ''}".strip() for k in explanation}
        elif llm_reason:
            explanation = {k: llm_reason[k] or explanation[k] for k in explanation}

        return {
            "text": text,
            "verdict": verdict,
            "is_scam": verdict == "scam",
            "probability": round(prob, 4),
            "scam_type": scam_type if verdict != "safe" else None,
            "brand": sig["brand"],
            "action": sig["action"],
            "red_flags": red_flags(sig),
            "domains": sorted({u["domain"] for u in sig["urls"] if u["kind"] != "official"}),
            "hosts": sorted({u["host"] for u in sig["urls"] if u["kind"] != "official"}),
            "phones": sig["phones"],
            "lang": detect_language(text),
            "explanation": explanation,
            "source": source,
            "keyword_filter_hit": keyword_filter(text),
            "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
        }
