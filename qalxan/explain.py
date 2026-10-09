"""Human-readable verdict explanations in Azerbaijani, Russian and English."""

TYPE_NAMES = {
    "bank_card_block": {"az": "saxta bank bildirişi (kart bloklanıb)", "ru": "фальшивое уведомление банка о блокировке карты",
                        "en": "fake bank card-block notice"},
    "bank_otp_theft": {"az": "SMS kodun oğurlanması", "ru": "кража кода из СМС", "en": "SMS code theft"},
    "prize_lottery": {"az": "saxta uduş / lotereya", "ru": "фальшивый выигрыш / лотерея", "en": "fake prize / lottery"},
    "parcel_delivery": {"az": "saxta bağlama ödənişi", "ru": "фальшивая оплата посылки", "en": "fake parcel delivery fee"},
    "fine_government": {"az": "saxta cərimə / dövlət borcu", "ru": "фальшивый штраф / долг перед госорганом",
                        "en": "fake fine / government debt"},
    "marketplace_buyer": {"az": "saxta alıcı (Tap.az)", "ru": "фальшивый покупатель (Tap.az)",
                          "en": "fake marketplace buyer"},
    "relative_emergency": {"az": "\"yeni nömrə\" qohum fırıldağı", "ru": "мошенничество «мама, это мой новый номер»",
                           "en": "\"new number\" relative scam"},
    "investment_job": {"az": "saxta investisiya / iş təklifi", "ru": "фальшивые инвестиции / работа",
                       "en": "fake investment / job offer"},
    "other": {"az": "fırıldaqçılıq", "ru": "мошенничество", "en": "scam"},
}

FLAG_TEXT = {
    "urgency": {"az": "təcililik və vaxt təzyiqi", "ru": "давление срочностью", "en": "urgency pressure"},
    "threat": {"az": "hədə (bloklama, cərimə, məhkəmə)", "ru": "угроза (блокировка, штраф, суд)",
               "en": "threat (block, fine, court)"},
    "prize": {"az": "gözlənilməz uduş vədi", "ru": "обещание неожиданного выигрыша", "en": "unexpected prize promise"},
    "asks_code": {"az": "SMS kod, PIN və ya kart məlumatı istəyir", "ru": "просят код из СМС, PIN или данные карты",
                  "en": "asks for SMS code, PIN or card data"},
    "personal_data": {"az": "kart məlumatı və ya şəxsiyyət sənədi istəyir", "ru": "просят данные карты или документы",
                      "en": "asks for card details or ID documents"},
    "remote_access": {"az": "telefona uzaqdan giriş proqramı (AnyDesk və s.) quraşdırmağı istəyir",
                      "ru": "просят установить программу удалённого доступа (AnyDesk и т.п.)",
                      "en": "asks to install a remote-access app (AnyDesk etc.)"},
    "money_request": {"az": "ödəniş və ya pul köçürmə tələbi", "ru": "просят оплатить или перевести деньги",
                      "en": "asks to pay or transfer money"},
    "new_number": {"az": "\"yeni nömrə\" bəhanəsi", "ru": "предлог «новый номер»", "en": "\"new number\" pretext"},
    "easy_money": {"az": "asan qazanc vədi", "ru": "обещание лёгкого заработка", "en": "easy money promise"},
    "mixed_script": {"az": "hərflər gizlicə dəyişdirilib (latın/kiril qarışığı)",
                     "ru": "буквы подменены (смесь латиницы и кириллицы)", "en": "letters swapped (mixed Latin/Cyrillic)"},
    "lookalike_domain": {"az": "rəsmi sayta oxşayan saxta link", "ru": "ссылка на поддельный сайт, похожий на официальный",
                         "en": "lookalike fake website"},
    "shortener": {"az": "qısaldılmış link əsl ünvanı gizlədir", "ru": "сокращённая ссылка скрывает адрес",
                  "en": "shortened link hides the destination"},
    "foreign_phone": {"az": "xarici nömrə", "ru": "иностранный номер", "en": "foreign phone number"},
}

BRAND_LINK = {"az": "{brand} adından yazılıb, amma link onun rəsmi saytı deyil",
              "ru": "пишут от имени {brand}, но ссылка ведёт не на официальный сайт",
              "en": "claims to be {brand}, but the link is not its official site"}

ADVICE = {
    "click_link": {"az": "Linkə keçməyin və kart məlumatlarını daxil etməyin.",
                   "ru": "Не переходите по ссылке и не вводите данные карты.",
                   "en": "Do not open the link or enter card details."},
    "send_code": {"az": "Kodu heç kimə deməyin: bank heç vaxt kodu soruşmur.",
                  "ru": "Никому не сообщайте код: банк никогда его не спрашивает.",
                  "en": "Never share the code: banks never ask for it."},
    "call": {"az": "Bu nömrəyə zəng etməyin. Təşkilatın rəsmi nömrəsinə özünüz zəng edin.",
             "ru": "Не звоните на этот номер. Позвоните в организацию по официальному номеру сами.",
             "en": "Don't call this number. Call the organisation's official number yourself."},
    "send_money": {"az": "Pul köçürməyin. Əvvəlcə həmin şəxsə köhnə nömrəsindən zəng edin.",
                   "ru": "Не переводите деньги. Сначала перезвоните человеку на его старый номер.",
                   "en": "Don't send money. Call the person on their known number first."},
    "none": {"az": "Heç bir məlumat göndərməyin.", "ru": "Не отправляйте никаких данных.",
             "en": "Don't send any personal data."},
}
ADVICE["pay_link"] = ADVICE["click_link"]

HEAD = {
    "scam": {"az": "FIRILDAQ", "ru": "МОШЕННИЧЕСТВО", "en": "SCAM"},
    "suspicious": {"az": "ŞÜBHƏLİ", "ru": "ПОДОЗРИТЕЛЬНО", "en": "SUSPICIOUS"},
    "safe": {"az": "Təhlükə əlaməti tapılmadı.", "ru": "Признаков мошенничества не найдено.",
             "en": "No scam signs found."},
}
SIGNS = {"az": "Əlamətlər", "ru": "Признаки", "en": "Signs"}


def red_flags(sig: dict) -> list:
    """Ordered list of flag keys that are present (most telling first)."""
    order = ["brand_unofficial_link", "remote_access", "asks_code", "personal_data", "lookalike_domain",
             "mixed_script", "shortener", "threat",
             "prize", "money_request", "new_number", "easy_money", "urgency", "foreign_phone"]
    return [f for f in order if sig["flags"].get(f)]


def flag_text(flag: str, lang: str, brand: str | None) -> str:
    if flag == "brand_unofficial_link":
        return BRAND_LINK[lang].format(brand=brand or "?")
    return FLAG_TEXT[flag][lang]


def explain(verdict: str, scam_type: str | None, sig: dict, lang: str) -> str:
    if verdict == "safe":
        return HEAD["safe"][lang]
    flags = red_flags(sig)
    type_name = TYPE_NAMES.get(scam_type or "other", TYPE_NAMES["other"])[lang]
    parts = [f"{HEAD[verdict][lang]}: {type_name}."]
    if flags:
        parts.append(f"{SIGNS[lang]}: " + "; ".join(flag_text(f, lang, sig.get('brand')) for f in flags[:4]) + ".")
    parts.append(ADVICE.get(sig["action"], ADVICE["none"])[lang])
    return " ".join(parts)


def explain_all(verdict, scam_type, sig):
    return {lang: explain(verdict, scam_type, sig, lang) for lang in ("az", "ru", "en")}
