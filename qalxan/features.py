"""Rule-based signal extraction: links, phones, impersonated brand, requested action, red flags.

These signals feed the model as extra features and drive the human-readable explanation.
"""
import re
from urllib.parse import urlparse

from .brands import BRANDS, SHORTENERS, is_official, registered_domain
from .normalize import PHONE_RE, URL_RE, fold, has_mixed_script

# Keyword groups, written in folded form (ə→e, ş→s ...). Matched as substrings of folded text.
FLAG_WORDS = {
    "urgency": ["tecili", "derhal", "24 saat", "1 saat", "bu gun", "son gun", "srochno", "срочно", "немедленно",
                "в течение", "сегодня", "urgent", "immediately", "within 24", "today", "asap", "son xeberdarliq"],
    "threat": ["blok", "bloklan", "dondurul", "legv", "sondurul", "baglanacaq", "deaktiv", "заблок", "блокир",
               "отключ", "аннулир", "suspend", "blocked", "disconnect", "deactivat", "cerime", "штраф", "fine",
               "mehkeme", "суд", "court", "borc", "долг", "debt", "arrest", "hebs"],
    "prize": ["udus", "udmusunuz", "qazandiniz", "qalib", "hediyye", "bonus", "приз", "выиграл", "подар",
              "победител", "won", "winner", "prize", "gift", "reward", "lotereya", "лотере", "lottery"],
    "asks_code": ["kodu gonder", "kodu bildir", "kodu deyin", "kodu yaz", "sms kodu", "sifreni", "назовите код",
                  "сообщите код", "продиктуйте", "код из смс", "пришлите код", "send the code", "share the code",
                  "tell us the code", "reply with the code", "cvv", "pin kod", "пин-код", "card number",
                  "kart nomresi", "номер карты", "16 reqem", "16-digit", "16 цифр", "arxadaki 3", "3 цифры",
                  "fin kod", "bitme tarixi", "expiry", "срок действия карты", "reqemli kodu", "kodu bu nomreye",
                  "код подтверждения, который", "пришлите код", "send the code", "otp kodu", "otp you"],
    "personal_data": ["sexsiyyet vesiqesinin sekli", "vesiqenin sekli", "фото паспорта", "паспортные данные",
                      "passport photo", "photo of your id", "kart melumatlarini", "данные карты", "card details",
                      "melumatlarinizi daxil", "введите карту", "введите данные"],
    "remote_access": ["anydesk", "teamviewer", "rustdesk", "ekrandaki kod", "ekrani paylas", "демонстрац",
                      "удалённый доступ", "удаленный доступ", "screen share", "screen sharing", "quicksupport"],
    "money_request": ["pul kocur", "pul gonder", "kocurun", "odenis edin", "odeyin", "переведи", "переведите",
                      "скинь", "оплатите", "send money", "transfer", "pay the fee", "pay a fee", "rusum", "пошлин",
                      "customs fee", "komissiya", "комисси", "depozit", "депозит"],
    "new_number": ["yeni nomre", "yeni nomrem", "новый номер", "мой новый", "new number", "telefonum xarab",
                   "телефон сломал", "phone broke", "telefonum itib", "потерял телефон"],
    "easy_money": ["qazanc", "gunde", "gelir elde", "заработ", "доход", "в день", "earn", "per day", "invest",
                   "kripto", "крипт", "crypto", "passiv", "пассив", "is teklifi", "вакансия", "remote job"],
}

CALL_WORDS = ["zeng edin", "zeng et", "позвоните", "звоните", "call ", "call:", "elaqe", "свяжитесь", "contact"]
CLICK_WORDS = ["kecid", "linke", "kecin", "daxil olun", "перейдите", "по ссылке", "click", "visit", "tap ",
               "open the link", "follow the link"]
PAY_WORDS = ["odenis", "odeyin", "оплат", "pay", "rusum", "пошлин", "fee"]


def extract_urls(text: str):
    out = []
    for m in URL_RE.finditer(text):
        raw = m.group(0).rstrip(".,!?)")
        host = urlparse(raw if "://" in raw else "http://" + raw).hostname or ""
        if not host or "." not in host:
            continue
        out.append({"url": raw, "host": host.lower(), "domain": registered_domain(host)})
    return out


def extract_phones(text: str):
    phones = []
    for m in PHONE_RE.finditer(text):
        digits = re.sub(r"\D", "", m.group(0))
        if len(digits) < 9 or len(digits) == 16:  # 16 digits is a card number, not a phone
            continue
        phones.append(digits)
    return phones


def find_brand(folded: str, urls):
    for b in BRANDS:
        for alias in b["aliases"]:
            if re.search(r"(?<![a-zа-я])" + re.escape(alias) + r"(?![a-zа-я])", folded):
                return b
    for u in urls:
        for b in BRANDS:
            if any(tok in u["host"] for tok in b["domain_tokens"]):
                return b
    return None


def extract(text: str) -> dict:
    folded = fold(text)
    urls = extract_urls(text)
    phones = extract_phones(URL_RE.sub(" ", text))
    brand = find_brand(folded, urls)

    link_kinds = []
    for u in urls:
        if u["domain"] in SHORTENERS or u["host"] in SHORTENERS:
            kind = "shortener"
        elif is_official(u["host"]):
            kind = "official"
        elif any(tok in u["host"] for b in BRANDS for tok in b["domain_tokens"]):
            kind = "lookalike"
        else:
            kind = "unknown"
        u["kind"] = kind
        link_kinds.append(kind)

    body = fold(URL_RE.sub(" ", text))  # words inside links ("-bonus.online") are not the message's words
    flags = {name: any(w in body for w in words) for name, words in FLAG_WORDS.items()}
    flags["mixed_script"] = has_mixed_script(text)
    flags["lookalike_domain"] = "lookalike" in link_kinds
    flags["shortener"] = "shortener" in link_kinds
    flags["unknown_link"] = "unknown" in link_kinds
    flags["official_link"] = "official" in link_kinds
    flags["foreign_phone"] = any(not p.startswith("994") and len(p) > 10 for p in phones)
    flags["mobile_phone"] = any(len(p) >= 9 for p in phones)
    # A brand that writes with a link that is not its own site is the strongest single signal.
    flags["brand_unofficial_link"] = bool(brand) and any(k in ("lookalike", "shortener", "unknown") for k in link_kinds)

    if flags["asks_code"]:
        action = "send_code"
    elif urls and (any(w in folded for w in CLICK_WORDS) or not phones):
        action = "pay_link" if any(w in folded for w in PAY_WORDS) else "click_link"
    elif phones and any(w in folded for w in CALL_WORDS):
        action = "call"
    elif flags["money_request"]:
        action = "send_money"
    elif phones:
        action = "call"
    else:
        action = "none"

    return {
        "urls": urls,
        "phones": phones,
        "brand": brand["name"] if brand else None,
        "action": action,
        "flags": flags,
    }


BANK_BRANDS = {"Kapital Bank", "ABB", "PASHA Bank", "Leobank", "Unibank"}


def rule_type(sig: dict) -> str | None:
    """Scheme implied by who is impersonated and what is asked, when that is unambiguous."""
    f, brand = sig["flags"], sig["brand"]
    if f["new_number"] and f["money_request"]:
        return "relative_emergency"
    if brand == "Azerpoct":
        return "parcel_delivery"
    if brand == "Tap.az":
        return "marketplace_buyer"
    if brand in {"Traffic Police (DYP)", "Tax Service"}:
        return "fine_government"
    if brand in BANK_BRANDS and sig["action"] in ("send_code", "call"):
        return "bank_otp_theft"
    if f["prize"]:
        return "prize_lottery"
    return None


FLAG_ORDER = ["urgency", "threat", "prize", "asks_code", "personal_data", "remote_access", "money_request",
              "new_number", "easy_money",
              "mixed_script", "lookalike_domain", "shortener", "unknown_link", "official_link",
              "foreign_phone", "mobile_phone", "brand_unofficial_link"]
ACTIONS = ["none", "click_link", "pay_link", "call", "send_code", "send_money"]


def feature_vector(sig: dict) -> list:
    """Numeric vector of rule signals for the model."""
    vec = [1.0 if sig["flags"].get(f) else 0.0 for f in FLAG_ORDER]
    vec += [1.0 if sig["action"] == a else 0.0 for a in ACTIONS]
    vec.append(1.0 if sig["brand"] else 0.0)
    vec.append(min(len(sig["urls"]), 3) / 3)
    return vec
