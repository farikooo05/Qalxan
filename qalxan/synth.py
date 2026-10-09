"""Synthetic SMS generator: fills templates, applies scammer obfuscation, builds train/test sets."""
import random
import string

from .synth_templates import LEGIT, NOVEL_SCHEMES, SCAM

BANKS = ["Kapital Bank", "Birbank", "ABB", "PASHA Bank", "Leobank", "Unibank"]
BANK_TOKENS = {"Kapital Bank": "kapitalbank", "Birbank": "birbank", "ABB": "abb-bank", "PASHA Bank": "pashabank",
               "Leobank": "leobank", "Unibank": "unibank"}
BANK_OFFICIAL = {"Kapital Bank": "kapitalbank.az", "Birbank": "birbank.az", "ABB": "abb-bank.az",
                 "PASHA Bank": "pashabank.az", "Leobank": "leobank.az", "Unibank": "unibank.az"}
BANK_SHORT = {"Kapital Bank": "196", "Birbank": "196", "ABB": "937", "PASHA Bank": "967", "Leobank": "151",
              "Unibank": "117"}
OPERATORS = ["Azercell", "Bakcell", "Nar"]
OPERATOR_TOKENS = {"Azercell": "azercell", "Bakcell": "bakcell", "Nar": "narmobile"}
OPERATOR_OFFICIAL = {"Azercell": "azercell.com", "Bakcell": "bakcell.com", "Nar": "nar.az"}
SCHEME_TOKENS = {
    "parcel_delivery": ["azerpost", "azerpoct", "az-post", "azpost-delivery", "poct-az"],
    "fine_government": ["egov", "e-gov-az", "dyp-cerime", "asan-odenis", "vergi-az", "cerime"],
    "marketplace_buyer": ["tapaz", "tap-az", "tapaz-deal", "tapaz-safe"],
    "investment_job": ["invest-az", "crypto-profit", "earn-az", "work-online", "baku-invest"],
    "number_disconnect": ["sim-qeydiyyat", "nomre-az", "rabite-gov", "sim-verify"],
    "social_benefit": ["sosial-odenis", "dovlet-yardim", "kompensasiya", "social-az"],
}
TLDS = ["com", "online", "info", "xyz", "top", "site", "cc", "live", "club", "icu", "vip", "link", "pro"]
PATTERNS = ["{t}-az.{tld}", "{t}-secure.{tld}", "my-{t}.{tld}", "{t}.az-verify.{tld}", "{t}-bonus.{tld}",
            "az-{t}.{tld}", "{t}24.{tld}", "{t}-online.{tld}", "{t}-kart.{tld}", "{t}.az-{tld}.com"]
SHORT = ["bit.ly", "cutt.ly", "is.gd", "clck.ru", "t.ly", "rb.gy"]
PRIZES = ["iPhone 17", "500 AZN", "1000 AZN", "Samsung Galaxy S26", "50 GB internet", "PlayStation 5", "MacBook Air",
          "Chery Tiggo"]
MERCHANTS = ["BRAVO", "Araz Market", "Wolt", "Bolt", "Bazarstore", "Kontakt Home", "Baku Electronics", "Bolt Food",
             "Starbucks Port Baku", "Oba Market"]
ITEMS = ["divan", "velosiped", "iPhone 13", "soyuducu", "kondisioner", "noutbuk", "uşaq arabası",
         "PlayStation", "paltaryuyan"]
NAMES = ["Aysel", "Elvin", "Nigar", "Rashad", "Leyla", "Murad", "Gunel", "Tural", "Sevinc", "Orxan", "Ruslan",
         "Aytac"]
BRANCHES = ["Nərimanov AZ1025", "Yasamal AZ1073", "Səbail AZ1000", "Xətai AZ1031", "Sumqayıt AZ5000",
            "Gəncə AZ2000"]

# Cyrillic look-alikes scammers swap into Latin words, and digits that look like letters.
TO_CYR = {"a": "а", "e": "е", "o": "о", "p": "р", "c": "с", "x": "х", "y": "у", "k": "к", "i": "і"}
TO_LEET = {"o": "0", "i": "1", "e": "3", "a": "@"}
AZ_STRIP = str.maketrans({"ə": "e", "Ə": "E", "ı": "i", "ö": "o", "Ö": "O", "ü": "u", "Ü": "U", "ş": "s",
                          "Ş": "S", "ç": "c", "Ç": "C", "ğ": "g", "İ": "I"})


def rand_code(r, n=None):
    return "".join(r.choice(string.digits) for _ in range(n or r.choice([4, 5, 6])))


def mobile(r):
    return f"+994 {r.choice(['50', '51', '55', '70', '77', '99', '10'])} {rand_code(r, 3)} {rand_code(r, 2)} {rand_code(r, 2)}"


def foreign(r):
    return r.choice([f"+44 7{rand_code(r, 9)}", f"+7 9{rand_code(r, 9)}", f"+90 5{rand_code(r, 9)}",
                     f"+380 6{rand_code(r, 8)}", f"+371 2{rand_code(r, 7)}"])


def scam_domain(r, token):
    return r.choice(PATTERNS).format(t=token, tld=r.choice(TLDS))


def scam_url(r, token):
    if r.random() < 0.2:
        return f"{r.choice(SHORT)}/{''.join(r.choice(string.ascii_letters + string.digits) for _ in range(6))}"
    dom = scam_domain(r, token)
    path = r.choice(["", "/login", "/verify", "/pay", "/az", "/odenis", "/bonus", "/kart", "/?id=" + rand_code(r, 6)])
    return ("https://" if r.random() < 0.5 else "") + dom + path


def fill(template, r, scheme=None, campaign=None):
    """Fill template slots. `campaign` pins brand/urls/phones so a campaign shares infrastructure."""
    bank = (campaign or {}).get("bank") or r.choice(BANKS)
    operator = (campaign or {}).get("operator") or r.choice(OPERATORS)
    if campaign and campaign.get("urls"):
        surl = r.choice(campaign["urls"])
    elif scheme in ("bank_card_block", "bank_otp_theft"):
        surl = scam_url(r, BANK_TOKENS[bank])
    elif scheme == "prize_lottery":
        surl = scam_url(r, OPERATOR_TOKENS[operator])
    else:
        surl = scam_url(r, r.choice(SCHEME_TOKENS.get(scheme, ["secure-pay"])))
    phone = r.choice(campaign["phones"]) if campaign and campaign.get("phones") else (
        mobile(r) if r.random() < 0.7 else foreign(r))
    slots = {
        "bank": bank, "operator": operator, "surl": surl, "phone": phone,
        "brand_any": r.choice(OPERATORS + ["Bravo", "Kontakt Home", "Baku Electronics"]),
        "card4": rand_code(r, 4), "card16": " ".join(rand_code(r, 4) for _ in range(4)),
        "amount": r.choice([str(r.randint(5, 900)), f"{r.randint(5, 900)}.{rand_code(r, 2)}"]),
        "balance": f"{r.randint(0, 5000)}.{rand_code(r, 2)}", "fee": r.choice(["1.99", "2.50", "3.20", "4.90", "0.99"]),
        "hours": r.choice(["2", "12", "24", "48"]), "code": rand_code(r), "prize": r.choice(PRIZES),
        "track": r.choice([f"RR{rand_code(r, 9)}AZ", f"AZ{rand_code(r, 8)}", f"CN{rand_code(r, 9)}"]),
        "car": f"{r.choice(['10', '90', '99', '77', '20'])}-{r.choice(['AA', 'BB', 'RR', 'ZZ', 'PL'])}-{rand_code(r, 3)}",
        "item": r.choice(ITEMS), "name": r.choice(NAMES), "merchant": r.choice(MERCHANTS),
        "date": f"{r.randint(1, 28):02d}.{r.randint(1, 12):02d}", "num": rand_code(r, 8), "ussd": rand_code(r, 3),
        "branch": r.choice(BRANCHES), "short": BANK_SHORT.get(bank, "196"),
        "lurl": r.choice([BANK_OFFICIAL[bank], OPERATOR_OFFICIAL[operator]]) + r.choice(["", "/kampaniya", "/az"]),
    }
    return template.format(**slots)


def obfuscate(text, r):
    """Apply the evasion tricks scammers use. Returns (text, applied?)."""
    words = text.split(" ")
    applied = False
    for i, w in enumerate(words):
        if "." in w or "/" in w or any(c.isdigit() for c in w) or len(w) < 4:
            continue
        if r.random() < 0.35:
            chars = list(w)
            idx = [j for j, c in enumerate(chars) if c.lower() in TO_CYR]
            if idx:
                j = r.choice(idx)
                chars[j] = TO_CYR[chars[j].lower()] if chars[j].islower() else TO_CYR[chars[j].lower()].upper()
                applied = True
            words[i] = "".join(chars)
        elif r.random() < 0.12:
            chars = list(w)
            idx = [j for j, c in enumerate(chars) if c.lower() in TO_LEET]
            if idx:
                j = r.choice(idx)
                chars[j] = TO_LEET[chars[j].lower()]
                applied = True
            words[i] = "".join(chars)
    return " ".join(words), applied


def render(template, r, label, scheme, lang, tid, split, campaign=None, obf_p=0.4):
    text = fill(template, r, scheme if label else None, campaign)
    obf = False
    if r.random() < 0.3:
        text = text.translate(AZ_STRIP)  # many people type without Azerbaijani letters
    if label and r.random() < obf_p:
        text, obf = obfuscate(text, r)
    return {"text": text, "label": label, "scheme": scheme, "lang": lang, "template_id": tid, "split": split,
            "obfuscated": obf, "novel": scheme in NOVEL_SCHEMES}


def template_split(idx):
    return "test" if idx % 3 == 2 else "train"


def build_dataset(seed=7, per_scam_template=14, per_legit_template=14):
    r = random.Random(seed)
    rows = []
    for scheme, langs in SCAM.items():
        for lang, temps in langs.items():
            for i, t in enumerate(temps):
                split = "test" if scheme in NOVEL_SCHEMES else template_split(i)
                for _ in range(per_scam_template):
                    rows.append(render(t, r, 1, scheme, lang, f"{scheme}/{lang}/{i}", split))
    for cat, langs in LEGIT.items():
        for lang, temps in langs.items():
            for i, t in enumerate(temps):
                split = template_split(i)
                n = per_legit_template if "{" in t else 3
                for _ in range(n):
                    rows.append(render(t, r, 0, cat, lang, f"{cat}/{lang}/{i}", split))
    # dedupe exact duplicates
    seen, out = set(), []
    for row in rows:
        if row["text"] not in seen:
            seen.add(row["text"])
            out.append(row)
    return out


def new_campaign(scheme, r):
    """Infrastructure for a live scam campaign: one brand, 2-3 domains, 1-2 phones."""
    bank = r.choice(BANKS)
    operator = r.choice(OPERATORS)
    if scheme in ("bank_card_block", "bank_otp_theft"):
        token = BANK_TOKENS[bank]
    elif scheme == "prize_lottery":
        token = OPERATOR_TOKENS[operator]
    else:
        token = r.choice(SCHEME_TOKENS.get(scheme, ["secure-pay"]))
    urls = ["https://" + scam_domain(r, token) + r.choice(["/login", "/verify", "/pay", ""]) for _ in range(r.randint(2, 3))]
    phones = [mobile(r) for _ in range(r.randint(1, 2))]
    return {"scheme": scheme, "bank": bank, "operator": operator, "urls": urls, "phones": phones}


def campaign_messages(scheme, n, r):
    """Mutated variants of one scam campaign, using test-only phrasings where possible."""
    camp = new_campaign(scheme, r)
    temps = [(lang, i, t) for lang, ts in SCAM[scheme].items() for i, t in enumerate(ts)]
    msgs = []
    for _ in range(n):
        lang, i, t = r.choice(temps)
        msgs.append(render(t, r, 1, scheme, lang, f"{scheme}/{lang}/{i}", "live", campaign=camp, obf_p=0.6))
    return camp, msgs


def legit_stream(r):
    """Endless generator of ordinary SMS traffic."""
    temps = [(cat, lang, i, t) for cat, ls in LEGIT.items() for lang, ts in ls.items() for i, t in enumerate(ts)]
    while True:
        cat, lang, i, t = r.choice(temps)
        yield render(t, r, 0, cat, lang, f"{cat}/{lang}/{i}", "live")
