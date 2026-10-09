"""The current approach we compare against: a keyword blocklist on raw lowercase text."""

KEYWORDS = [
    # Azerbaijani
    "uduş", "uddunuz", "qazandınız", "qalib", "hədiyyə", "bloklanıb", "bloklanib", "dondurulub", "lotereya",
    "kodu göndərin", "kodu deyin", "cvv", "rüsum", "cərimə", "təcili pul", "yeni nömrəm",
    # Russian
    "выиграл", "приз", "заблокирована", "лотере", "код из смс", "пошлин", "штраф", "срочно нужно", "новый номер",
    "заработок", "переведи",
    # English
    "won", "prize", "winner", "blocked", "suspended", "lottery", "customs fee", "share the code", "new number",
    "earn",
    # Known shorteners
    "bit.ly", "cutt.ly", "clck.ru",
]


def keyword_filter(text: str) -> bool:
    low = text.lower()
    return any(k in low for k in KEYWORDS)
