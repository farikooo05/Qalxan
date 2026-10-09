"""Text normalization that undoes the tricks scammers use to slip past keyword filters.

- Azerbaijani letters are folded (ə→e, ş→s, ç→c ...) so "uduş" and "udus" look the same.
- Inside a token that mixes Latin and Cyrillic letters ("Kapitаl" with a Cyrillic а),
  Cyrillic look-alikes are mapped to Latin.
- Digits used as letters inside words ("kap1tal", "bl0k") are mapped back.
- URLs, phone numbers and other numbers become placeholder tokens.
"""
import re
import unicodedata

AZ_FOLD = str.maketrans({"ə": "e", "ı": "i", "ö": "o", "ü": "u", "ş": "s", "ç": "c", "ğ": "g"})

# Cyrillic letters that look like Latin ones.
HOMOGLYPHS = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "к": "k",
    "м": "m", "т": "t", "н": "h", "в": "b", "і": "i", "ј": "j", "ѕ": "s", "ԁ": "d", "ӏ": "l",
})
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})

URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?[a-z0-9][a-z0-9\-]*(?:\.[a-z0-9\-]+)*\.(?:az|com|net|org|info|xyz|top|online|site|"
    r"cc|ru|io|me|ly|gd|at|link|click|shop|store|live|pro|eu|co|biz|icu|vip|club|life|app|pw|su|gy)(?:/[^\s]*)?",
    re.IGNORECASE,
)
PHONE_RE = re.compile(r"(?:\+?\d[\d\-\s()]{7,}\d)")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")
CYR = re.compile(r"[а-яёәғқңөүһіј]", re.IGNORECASE)
LAT = re.compile(r"[a-z]", re.IGNORECASE)


def has_mixed_script(text: str) -> bool:
    """True if any single word mixes Latin and Cyrillic letters — a classic evasion trick."""
    for tok in re.findall(r"\w+", text):
        if CYR.search(tok) and LAT.search(tok):
            return True
    return False


def _fix_token(tok: str) -> str:
    if CYR.search(tok) and LAT.search(tok):
        tok = tok.translate(HOMOGLYPHS)
    if re.search(r"[a-z]", tok) and re.search(r"[0-9@$]", tok) and not tok.isdigit():
        # only treat digits as letters when the token is mostly letters
        letters = sum(c.isalpha() for c in tok)
        if letters >= len(tok) / 2:
            tok = tok.translate(LEET)
    return tok


def fold(text: str) -> str:
    """Lowercase + NFKC + Azerbaijani folding, without touching URLs/numbers."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("İ", "i").lower().replace("i̇", "i")
    return text.translate(AZ_FOLD)


def normalize(text: str) -> str:
    """Full normalization used by the model."""
    text = fold(text)
    text = URL_RE.sub(" _url_ ", text)
    text = PHONE_RE.sub(" _phone_ ", text)
    tokens = re.split(r"(\s+)", text)
    text = "".join(_fix_token(t) if not t.isspace() else t for t in tokens)
    text = NUM_RE.sub(" _num_ ", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_language(text: str) -> str:
    """Rough language guess: 'ru', 'az' or 'en'."""
    cyr = len(CYR.findall(text))
    lat = len(LAT.findall(text))
    if cyr > lat:
        return "ru"
    low = text.lower()
    if re.search(r"[əğışçöü]", low) or re.search(
        r"\b(siz|sizin|ucun|üçün|kart|edin|olunub|olundu|hormetli|hörmətli|salam|var|bu|ve|və|nomre|nömrə|gun|gün|pul|ile|ilə)\b",
        low,
    ):
        return "az"
    return "en"
