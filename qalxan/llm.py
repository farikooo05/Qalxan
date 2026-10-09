"""Optional second opinion from Gemini for messages our model is unsure about (the grey band).

Works only if GEMINI_API_KEY is set; otherwise every call returns None and the model decides alone.
"""
import json
import os
import time
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

PROMPT = """You are an anti-fraud analyst at a mobile operator in Azerbaijan.
Decide whether this SMS is a scam. Messages can be in Azerbaijani, Russian or English, may mix scripts,
and scammers swap letters to dodge filters. Genuine banks send OTP codes and payment alerts but never ask
anyone to send, tell or type a code, PIN or CVV, and only link to their official domains.

Return JSON with:
- is_scam: boolean
- confidence: number 0..1
- scam_type: one of bank_card_block, bank_otp_theft, prize_lottery, parcel_delivery, fine_government,
  marketplace_buyer, relative_emergency, investment_job, other, none
- reason_az, reason_ru, reason_en: one short sentence each explaining the decision to a subscriber

SMS:
\"\"\"{text}\"\"\""""

SCHEMA = {
    "type": "object",
    "properties": {
        "is_scam": {"type": "boolean"},
        "confidence": {"type": "number"},
        "scam_type": {"type": "string"},
        "reason_az": {"type": "string"},
        "reason_ru": {"type": "string"},
        "reason_en": {"type": "string"},
    },
    "required": ["is_scam", "confidence", "scam_type", "reason_az", "reason_ru", "reason_en"],
}


def available() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


@lru_cache(maxsize=1)
def _client():
    from google import genai
    from google.genai import types
    return genai.Client(api_key=os.environ["GEMINI_API_KEY"], http_options=types.HttpOptions(timeout=15000))


_cache: dict[str, dict] = {}


def llm_verdict(text: str):
    """Return dict verdict from Gemini, or None if unavailable or failed. Only successes are cached."""
    if not available():
        return None
    if text in _cache:
        return _cache[text]
    from google.genai import types
    # If one model is overloaded (503) or rate-limited (429), fall back to the next one.
    models = list(dict.fromkeys([os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest"), "gemini-flash-lite-latest",
                                 "gemini-flash-latest"]))
    for attempt, model in enumerate(models * 2):  # two passes: demand spikes are short
        if attempt == len(models):
            time.sleep(1.5)
        try:
            resp = _client().models.generate_content(
                model=model,
                contents=PROMPT.format(text=text),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_json_schema=SCHEMA,
                    temperature=0,
                ),
            )
            out = json.loads(resp.text)
            out["model"] = model
            _cache[text] = out
            return out
        except Exception as e:  # network, quota, parsing: try the next model, else the model's verdict stands
            print(f"[llm] {model} failed: {str(e)[:120]}")
    return None
