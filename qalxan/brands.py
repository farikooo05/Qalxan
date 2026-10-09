"""Brands that scammers impersonate in Azerbaijan, with their official domains.

Aliases are written in normalized form (lowercase, Azerbaijani letters folded: ə→e, ş→s ...).
`domain_tokens` are substrings that betray a lookalike domain (kapitalbank-az.com).
"""

BRANDS = [
    {"name": "Kapital Bank", "aliases": ["kapital bank", "kapitalbank", "birbank", "капитал банк", "капиталбанк"],
     "domains": ["kapitalbank.az", "birbank.az"], "domain_tokens": ["kapital", "birbank"]},
    {"name": "ABB", "aliases": ["abb bank", "abb", "абб"],
     "domains": ["abb-bank.az"], "domain_tokens": ["abb"]},
    {"name": "PASHA Bank", "aliases": ["pasha bank", "pashabank", "паша банк"],
     "domains": ["pashabank.az"], "domain_tokens": ["pasha"]},
    {"name": "Leobank", "aliases": ["leobank", "леобанк"],
     "domains": ["leobank.az"], "domain_tokens": ["leobank"]},
    {"name": "Unibank", "aliases": ["unibank", "унибанк"],
     "domains": ["unibank.az"], "domain_tokens": ["unibank"]},
    {"name": "Azercell", "aliases": ["azercell", "азерселл", "азерсел"],
     "domains": ["azercell.com"], "domain_tokens": ["azercell", "azercel"]},
    {"name": "Bakcell", "aliases": ["bakcell", "бакселл"],
     "domains": ["bakcell.com"], "domain_tokens": ["bakcell"]},
    {"name": "Nar", "aliases": ["nar mobile", "narmobile"],
     "domains": ["nar.az"], "domain_tokens": ["narmobile"]},
    {"name": "Azerpoct", "aliases": ["azerpoct", "azerpost", "azer poct", "азерпочт", "азерпочта"],
     "domains": ["azerpost.az"], "domain_tokens": ["azerpo", "az-post", "azpost"]},
    {"name": "ASAN Xidmet", "aliases": ["asan xidmet", "asan imza", "asan odenis", "асан хидмет", "асан"],
     "domains": ["asan.gov.az", "e-gov.az"], "domain_tokens": ["asan", "egov", "e-gov"]},
    {"name": "Traffic Police (DYP)", "aliases": ["dyp", "ypx", "yol polisi", "дорожная полиция", "гаи", "дпс"],
     "domains": ["dyp.gov.az", "e-gov.az"], "domain_tokens": ["dyp", "ypx", "cerime", "jarima"]},
    {"name": "Tax Service", "aliases": ["vergi xidmeti", "dovlet vergi", "налоговая", "налоговой"],
     "domains": ["taxes.gov.az"], "domain_tokens": ["vergi", "taxes"]},
    {"name": "Tap.az", "aliases": ["tap.az", "tapaz", "тап.аз", "тапаз"],
     "domains": ["tap.az"], "domain_tokens": ["tapaz", "tap-az", "tap.az-"]},
]

SHORTENERS = {"bit.ly", "tinyurl.com", "cutt.ly", "t.ly", "is.gd", "clck.ru", "goo.su", "rb.gy", "shorturl.at", "tiny.cc"}

OFFICIAL_DOMAINS = {d for b in BRANDS for d in b["domains"]} | {
    "gov.az", "bolt.eu", "wolt.com", "azerpost.az", "my.gov.az",
    # well-known merchants that appear in genuine payment alerts ("Payment to NETFLIX.COM")
    "netflix.com", "spotify.com", "apple.com", "google.com", "youtube.com", "amazon.com", "aliexpress.com",
    "trendyol.com", "temu.com", "wildberries.ru", "ozon.ru", "uber.com", "booking.com", "steampowered.com",
    "microsoft.com", "openai.com", "anthropic.com", "claude.ai", "airbnb.com",
}


def registered_domain(host: str) -> str:
    """Return the registrable part of a host (last two labels, or three for *.gov.az style)."""
    host = host.lower().strip(".")
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in {"gov", "com", "org", "net", "edu"} and parts[-1] == "az":
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def is_official(host: str) -> bool:
    host = host.lower()
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)
