"""SMS templates for synthetic data. Disclosed in the submission as synthetic, generated in-session.

SCAM[scheme][lang] and LEGIT[category][lang] are lists of templates with {slots}.
Templates are split into train/test by index (see synth.py), so test phrasing is never seen in training.
NOVEL_SCHEMES never appear in training at all.
"""

SCAM = {
    "bank_card_block": {
        "az": [
            "{bank}: Kartınız *{card4} təhlükəsizlik səbəbi ilə bloklanıb. Bərpa etmək üçün {hours} saat ərzində keçid edin: {surl}",
            "Hörmətli müştəri, {bank} kartınızda şübhəli əməliyyat aşkarlandı. Kart dondurulub. Təsdiqləmək üçün: {surl}",
            "{bank} XƏBƏRDARLIQ! Hesabınız müvəqqəti məhdudlaşdırılıb. Məlumatlarınızı yeniləyin: {surl}",
            "Kartiniz bloklanib. Kartin aktivlesdirilmesi ucun daxil olun {surl} {bank}",
            "{bank}: {amount} AZN məbləğində əməliyyat dayandırıldı. Siz deyilsinizsə, dərhal ləğv edin: {surl}",
            "Diqqət! {bank} kartınızın müddəti bitir, kart bloklanacaq. Yeniləmək üçün linkə keçin {surl}",
        ],
        "ru": [
            "{bank}: Ваша карта *{card4} заблокирована в целях безопасности. Для разблокировки перейдите: {surl}",
            "Уважаемый клиент! По вашей карте {bank} зафиксирована подозрительная операция на {amount} AZN. Отменить: {surl}",
            "{bank}: доступ к счету ограничен. Подтвердите данные в течение {hours} часов: {surl}",
            "Ваша карта будет заблокирована сегодня. Срочно обновите данные {bank} по ссылке {surl}",
            "Внимание! Списание {amount} AZN с карты *{card4}. Если это не вы, отмените операцию: {surl}",
            "{bank}: обнаружен вход в ваш личный кабинет с нового устройства. Если это не вы, заблокируйте доступ: {surl}",
        ],
        "en": [
            "{bank}: Your card *{card4} has been blocked for security reasons. Restore access here: {surl}",
            "Dear customer, suspicious transaction of {amount} AZN detected on your {bank} card. Cancel now: {surl}",
            "{bank} ALERT: your account is suspended. Verify your details within {hours} hours: {surl}",
            "Your {bank} card will be deactivated today. Update your information immediately at {surl}",
            "{bank}: new login to your online banking from an unknown device. Not you? Secure your account: {surl}",
            "Payment of {amount} AZN from card *{card4} is on hold. Confirm or cancel at {surl}",
        ],
    },
    "bank_otp_theft": {
        "az": [
            "{bank} təhlükəsizlik xidməti: kartınızı qorumaq üçün sizə gələn SMS kodu bu nömrəyə göndərin {phone}",
            "Salam, {bank} əməkdaşıyam. Hesabınızda problem var, telefonunuza gələn kodu deyin ki, əməliyyatı ləğv edək. Zəng: {phone}",
            "Kartınızdan pul çıxarılmasının qarşısını almaq üçün SMS kodu cavab olaraq yazın. {bank}",
            "{bank}: kartınız təsdiq gözləyir. Kart nömrəsi və CVV kodunu {phone} nömrəsinə WhatsApp ilə göndərin",
            "Sizin adınıza kredit rəsmiləşdirilir. Ləğv etmək üçün {bank} mütəxəssisinə SMS kodu bildirin: {phone}",
            "{bank}: hesabınızı qorumaq üçün operatora zəng edin {phone} və təsdiq kodunu deyin",
        ],
        "ru": [
            "Служба безопасности {bank}: для защиты карты сообщите код из смс по номеру {phone}",
            "Здравствуйте, это {bank}. На ваше имя оформляется кредит. Чтобы отменить, продиктуйте код из смс оператору: {phone}",
            "{bank}: подтвердите личность. Пришлите код из смс в ответ на это сообщение",
            "Для отмены подозрительного перевода назовите код из смс специалисту {bank}. Тел: {phone}",
            "{bank}: ваша карта под угрозой. Сообщите номер карты и CVV специалисту по номеру {phone}",
        ],
        "en": [
            "{bank} security team: to protect your card, reply with the code you just received.",
            "This is {bank} fraud department. Someone is taking a loan in your name. Call {phone} and share the code from SMS to stop it.",
            "{bank}: confirm your identity, send the card number and CVV to {phone} on WhatsApp.",
            "{bank}: to cancel the suspicious transfer, tell our specialist the code from SMS. Call {phone}",
        ],
    },
    "prize_lottery": {
        "az": [
            "TƏBRİKLƏR! {operator} lotereyasında {prize} uddunuz! Hədiyyəni almaq üçün: {surl}",
            "{operator} yubiley aksiyası: siz qalib seçildiniz! {prize} qazandınız. Ətraflı: {surl}",
            "Hörmətli abunəçi, nömrəniz {prize} uduşu qazandı. Çatdırılma rüsumu {fee} AZN ödəyin: {surl}",
            "Siz {brand_any} aksiyasının qalibisiniz! Hədiyyə {hours} saat ərzində götürülməlidir: {surl}",
            "{operator}: təsadüfi seçimdə nömrəniz qalib gəldi. {prize} sizi gözləyir {surl}",
            "Təbriklər! {brand_any} müştəriləri arasında keçirilən tirajda {prize} uddunuz. Təsdiqləyin: {surl}",
        ],
        "ru": [
            "ПОЗДРАВЛЯЕМ! Ваш номер выиграл {prize} в лотерее {operator}! Получите приз: {surl}",
            "{operator}: Вы стали победителем розыгрыша. Ваш подарок {prize}. Оплатите доставку {fee} AZN: {surl}",
            "Вы выиграли {prize}! Подтвердите получение приза сегодня по ссылке {surl}",
            "Акция {brand_any}: ваш номер выбран победителем. Заберите {prize} в течение {hours} часов: {surl}",
            "{operator} дарит {prize} случайным абонентам. Вы в списке победителей! {surl}",
        ],
        "en": [
            "CONGRATULATIONS! Your number won {prize} in the {operator} anniversary lottery. Claim: {surl}",
            "{operator}: you are our lucky winner of {prize}! Pay {fee} AZN delivery to receive your gift: {surl}",
            "You have won {prize}! Claim your reward within {hours} hours: {surl}",
            "{brand_any} giveaway: your number was selected. Collect your {prize} here {surl}",
        ],
    },
    "parcel_delivery": {
        "az": [
            "Azərpoçt: Bağlamanız {track} gömrükdə saxlanılıb. Rüsum {fee} AZN ödəyin: {surl}",
            "Bağlamanız ünvanın düzgün olmaması səbəbindən çatdırılmadı. Ünvanı yeniləyin: {surl}",
            "AZERPOCT: Sizin bağlama anbarda gözləyir. {hours} saat ərzində ödəniş edilməsə geri qaytarılacaq {surl}",
            "Azərpoçt: {track} bağlamasının çatdırılması dayandırılıb. Əlavə ödəniş {fee} AZN: {surl}",
            "Kuryer sizi tapa bilmədi. Bağlamanın yenidən çatdırılması üçün {fee} AZN ödəyin {surl}",
        ],
        "ru": [
            "Азерпочта: Ваша посылка {track} задержана на таможне. Оплатите пошлину {fee} AZN: {surl}",
            "Не удалось доставить посылку: неверный адрес. Обновите данные: {surl}",
            "Ваша посылка ожидает на складе. Оплатите доставку {fee} AZN до конца дня: {surl}",
            "Курьер не смог вас застать. Для повторной доставки оплатите {fee} AZN: {surl}",
        ],
        "en": [
            "Azerpost: your parcel {track} is held at customs. Pay the {fee} AZN fee: {surl}",
            "We could not deliver your package due to an incomplete address. Update it here: {surl}",
            "Your parcel is waiting at our warehouse. Pay {fee} AZN redelivery fee today: {surl}",
            "Delivery failed for parcel {track}. Reschedule and pay {fee} AZN at {surl}",
        ],
    },
    "fine_government": {
        "az": [
            "DYP: {car} nömrəli avtomobiliniz üzrə ödənilməmiş cərimə {amount} AZN. Ödənilməsə məhkəməyə veriləcək. Ödəniş: {surl}",
            "ASAN Ödəniş: Sizin {amount} AZN vergi borcunuz var. Bu gün ödəyin, əks halda hesabınız dondurulacaq: {surl}",
            "e-gov: Sizin adınıza cərimə yazılıb. Ətraflı məlumat və ödəniş: {surl}",
            "Vergi xidməti: {amount} AZN borcunuz var. {hours} saat ərzində ödənilməsə hesablarınıza həbs qoyulacaq {surl}",
            "Yol polisi: radar cəriməniz {amount} AZN. 50% endirimlə ödəmək üçün bu gün keçid edin {surl}",
        ],
        "ru": [
            "ДПС: По автомобилю {car} неоплаченный штраф {amount} AZN. Оплатите сегодня, иначе дело передадут в суд: {surl}",
            "Налоговая служба: у вас задолженность {amount} AZN. Оплатите в течение {hours} часов: {surl}",
            "У вас неоплаченный штраф. Проверьте и оплатите: {surl}",
            "Дорожная полиция: штраф {amount} AZN по {car}. Оплатите со скидкой 50% только сегодня: {surl}",
        ],
        "en": [
            "Traffic Police: unpaid fine of {amount} AZN for vehicle {car}. Pay today to avoid court: {surl}",
            "Tax Service: you have an outstanding debt of {amount} AZN. Pay within {hours} hours: {surl}",
            "e-gov notice: a fine was issued in your name. Details and payment: {surl}",
        ],
    },
    "marketplace_buyer": {
        "az": [
            "Salam, {item} elanınıza görə yazıram. Pulu artıq köçürdüm, kartınıza almaq üçün linkə keçin: {surl}",
            "Tap.az: Alıcı elanınız üçün ödəniş etdi. Vəsaiti əldə etmək üçün kart məlumatlarını daxil edin {surl}",
            "Salam, {item} hələ satılır? Kuryerlə götürəcəm, ödənişi Tap.az təhlükəsiz ödəniş ilə etdim, təsdiqlə: {surl}",
            "Tap.az təhlükəsiz sövdələşmə: {amount} AZN sizin üçün rezerv edilib. Almaq üçün kartınızı təsdiqləyin {surl}",
        ],
        "ru": [
            "Здравствуйте, по объявлению {item}. Я уже оплатил, получите деньги по ссылке: {surl}",
            "Tap.az: покупатель оплатил ваш товар. Чтобы получить средства, введите данные карты: {surl}",
            "Добрый день, беру {item}. Оплатил через безопасную сделку Tap.az, подтвердите получение: {surl}",
        ],
        "en": [
            "Hi, about your {item} ad. I already paid via Tap.az safe deal, receive the money here: {surl}",
            "Tap.az: buyer has paid for your item. Enter your card details to receive funds: {surl}",
            "Hello, I'll take the {item}. Payment of {amount} AZN is waiting for you, confirm here {surl}",
        ],
    },
    "relative_emergency": {
        "az": [
            "Ana, bu mənim yeni nömrəmdir. Telefonum xarab oldu. Təcili {amount} AZN lazımdır, bu karta köçür: {card16}",
            "Salam, mənəm, telefonum itib, dostumun nömrəsindən yazıram. Təcili pul lazımdır, zəhmət olmasa {amount} AZN göndər",
            "Ata, problemim var, zəng edə bilmirəm. {amount} manat köçür bu karta {card16}, sonra izah edərəm",
            "Ana, yeni nömrəmdir bu. Təcili ödəniş etməliyəm, {amount} AZN at bu karta {card16}, axşam qaytaracam",
        ],
        "ru": [
            "Мама, это мой новый номер, старый телефон сломался. Срочно нужно {amount} AZN, переведи на карту {card16}",
            "Привет, это я, пишу с чужого номера. Попал в неприятность, срочно скинь {amount} манат, потом объясню",
            "Пап, у меня проблемы, не могу говорить. Переведи {amount} AZN на эту карту {card16}, срочно",
        ],
        "en": [
            "Mom, this is my new number, my phone broke. I urgently need {amount} AZN, please transfer to {card16}",
            "Hi it's me, writing from a friend's phone. I'm in trouble, send {amount} AZN now, I'll explain later",
            "Dad, I can't call right now. Please transfer {amount} AZN to this card {card16} urgently",
        ],
    },
    "investment_job": {
        "az": [
            "Evdən işləyərək gündə {amount} AZN qazanc! Təcrübə tələb olunmur. WhatsApp: {phone}",
            "Səhmlərə investisiya edin, ayda 300% gəlir! Qeydiyyat: {surl}",
            "Onlayn iş təklifi: gündə 2 saat, həftəlik {amount} AZN. Ətraflı: {surl}",
            "Kriptovalyuta ilə passiv gəlir! 100 AZN qoy, həftədə {amount} AZN qazan. Yaz: {phone}",
        ],
        "ru": [
            "Заработок от {amount} AZN в день без опыта! Пишите в WhatsApp {phone}",
            "Инвестиции в крипту с доходом 40% в неделю. Регистрация: {surl}",
            "Удалённая работа: лайки и отзывы, оплата {amount} AZN в день. Подробнее {surl}",
            "Пассивный доход от {amount} AZN в неделю. Вложите 100 AZN, остальное сделает робот: {surl}",
        ],
        "en": [
            "Earn {amount} AZN per day from home, no experience needed! WhatsApp {phone}",
            "Invest in crypto and get 40% profit weekly. Register now: {surl}",
            "Part-time online job: like videos and earn {amount} AZN daily. Details: {surl}",
        ],
    },
    # Novel schemes: test only, never seen in training.
    "number_disconnect": {
        "az": [
            "Rabitə Nazirliyi: nömrəniz qeydiyyatdan keçmədiyi üçün {hours} saat ərzində söndürüləcək. Qarşısını almaq üçün: {surl}",
            "{operator}: SİM kartınızın qeydiyyatı başa çatıb. Nömrəniz bağlanacaq. Şəxsiyyət vəsiqəsini təsdiqləyin {surl}",
            "Nömrəniz {hours} saatdan sonra deaktiv ediləcək. Məlumatları yeniləmək üçün zəng edin {phone}",
        ],
        "ru": [
            "Министерство связи: ваш номер будет отключен через {hours} часа из-за отсутствия регистрации. Подтвердите: {surl}",
            "{operator}: регистрация SIM-карты истекла. Номер будет заблокирован. Подтвердите паспорт: {surl}",
        ],
        "en": [
            "Ministry of Communications: your number will be disconnected in {hours} hours due to missing registration. Confirm: {surl}",
            "{operator}: your SIM registration expired and the line will be suspended. Verify your ID at {surl}",
        ],
    },
    "social_benefit": {
        "az": [
            "Dövlət sosial ödənişi: Sizə {amount} AZN birdəfəlik yardım təyin olunub. Almaq üçün kart məlumatlarını daxil edin: {surl}",
            "Sizə {amount} AZN kompensasiya hesablanıb. Kartınıza köçürmək üçün: {surl}",
            "Əmək Nazirliyi: {amount} AZN müavinət almaq hüququnuz var. Bu gün müraciət edin {surl}",
        ],
        "ru": [
            "Вам начислена социальная выплата {amount} AZN. Для получения введите данные карты: {surl}",
            "Государственная компенсация {amount} AZN. Оформите получение до конца дня: {surl}",
        ],
        "en": [
            "You are eligible for a one-time state payment of {amount} AZN. Enter your card details to receive it: {surl}",
            "Government compensation of {amount} AZN has been assigned to you. Claim today: {surl}",
        ],
    },
}

NOVEL_SCHEMES = {"number_disconnect", "social_benefit"}

LEGIT = {
    "bank_otp": {
        "az": [
            "{code} - {bank} təsdiq kodunuz. Kodu heç kimə deməyin, bank əməkdaşlarına da.",
            "Birbank: Giriş kodu {code}. Bu kodu heç kimlə paylaşmayın.",
            "Kod: {code}. {bank} əməliyyatı təsdiqləmək üçün. Kodu heç kimə verməyin.",
            "{bank}: {amount} AZN ödənişi təsdiqləmək üçün kod {code}. Kodu heç kimə deməyin.",
        ],
        "ru": [
            "Код подтверждения {bank}: {code}. Никому не сообщайте этот код, даже сотрудникам банка.",
            "{code} — ваш код для входа в {bank}. Не передавайте его третьим лицам.",
            "{bank}: код {code} для подтверждения платежа {amount} AZN. Никому его не сообщайте.",
        ],
        "en": [
            "{code} is your {bank} verification code. Do not share it with anyone.",
            "Your one-time password is {code}. {bank} will never ask for it.",
            "{bank}: use code {code} to confirm payment of {amount} AZN. Never share this code.",
        ],
    },
    "bank_payment": {
        "az": [
            "Kart *{card4}: -{amount} AZN, {merchant}. Balans: {balance} AZN",
            "{bank}: Hesabınıza {amount} AZN mədaxil olundu. Balans {balance} AZN",
            "Kart *{card4} ilə {merchant} ödənişi: {amount} AZN. {date}",
            "{bank}: *{card4} kartından {amount} AZN nağdlaşdırıldı. Balans {balance} AZN",
        ],
        "ru": [
            "Карта *{card4}: покупка {amount} AZN, {merchant}. Доступно {balance} AZN",
            "{bank}: зачисление {amount} AZN. Баланс {balance} AZN",
            "{bank}: снятие наличных {amount} AZN, карта *{card4}. Остаток {balance} AZN",
        ],
        "en": [
            "Card *{card4}: purchase {amount} AZN at {merchant}. Available balance {balance} AZN",
            "{bank}: {amount} AZN received to your account. Balance {balance} AZN",
            "{bank}: cash withdrawal {amount} AZN, card *{card4}. Balance {balance} AZN",
        ],
    },
    "bank_info": {
        "az": [
            "{bank}: Kartınız 3 dəfə səhv PIN daxil edildiyi üçün bloklanıb. Ətraflı məlumat üçün {short} nömrəsinə zəng edin.",
            "Hörmətli müştəri, *{card4} kartınızın müddəti {date} tarixində bitir. Yeni kartı filialdan götürə bilərsiniz. {bank}",
            "{bank}: Kredit ödənişinizin tarixi {date}. Məbləğ {amount} AZN. Ödənişi Birbank tətbiqində edə bilərsiniz.",
            "{bank} heç vaxt SMS kod, PIN və ya CVV soruşmur. Belə zənglərə cavab verməyin.",
            "{bank}: yeni kampaniya, kartla ödənişlərə 5% keşbek. Ətraflı: {lurl}",
            "{bank}: şübhəli əməliyyat səbəbindən kartınız müvəqqəti dayandırılıb. Zəhmət olmasa {short} nömrəsinə zəng edin və ya filiala yaxınlaşın.",
        ],
        "ru": [
            "{bank}: карта *{card4} заблокирована после 3 неверных вводов PIN. Справки по телефону {short}.",
            "Срок действия карты *{card4} истекает {date}. Новую карту можно получить в отделении {bank}.",
            "{bank}: напоминаем о платеже по кредиту {amount} AZN до {date}.",
            "{bank} никогда не запрашивает коды из СМС. Не сообщайте их никому.",
            "{bank}: кешбэк 5% на все покупки картой в этом месяце. Подробнее: {lurl}",
        ],
        "en": [
            "{bank}: card *{card4} is blocked after 3 wrong PIN attempts. For help call {short}.",
            "Your {bank} card *{card4} expires on {date}. Pick up the new card at any branch.",
            "{bank} will never ask for your SMS code or PIN. Stay alert.",
            "{bank}: loan payment of {amount} AZN is due on {date}. Pay in the app.",
        ],
    },
    "operator_promo": {
        "az": [
            "{operator}: 5 AZN-ə 10 GB internet! Aktivləşdirmək üçün *{ussd}# yığın.",
            "{operator}: Balansınız 0.50 AZN-dən azdır. Balansı artırmaq üçün {lurl}",
            "{operator}: Rouminq paketi aktivləşdi. Uğurlu səfər!",
            "{operator}: Yeni tarif! Limitsiz zənglər ayda {amount} AZN. Ətraflı: {lurl}",
            "{operator}: 2 GB bonus internet hədiyyə olaraq hesabınıza əlavə edildi. Müddət: 7 gün.",
            "{operator}: Paketinizin müddəti sabah bitir. Yeniləmək üçün *{ussd}# yığın.",
        ],
        "ru": [
            "{operator}: 10 ГБ интернета за 5 AZN! Наберите *{ussd}#",
            "{operator}: на вашем балансе меньше 0.50 AZN. Пополнить: {lurl}",
            "{operator}: вам подарено 2 ГБ бонусного интернета на 7 дней.",
            "{operator}: роуминг-пакет активирован. Приятной поездки!",
        ],
        "en": [
            "{operator}: 10 GB for 5 AZN! Dial *{ussd}# to activate.",
            "{operator}: your roaming package is active. Have a nice trip!",
            "{operator}: 2 GB bonus internet added to your account as a gift. Valid 7 days.",
        ],
    },
    "delivery": {
        "az": [
            "Azərpoçt: {track} nömrəli bağlamanız {branch} poçt şöbəsinə çatıb. İş saatı 09:00-18:00.",
            "Wolt: Sifarişiniz yoldadır, kuryer 15 dəqiqəyə çatacaq.",
            "Bolt: Sürücünüz {name} 3 dəqiqəyə çatacaq. Avtomobil: {car}",
            "Kuryer bu gün 14:00-18:00 arası bağlamanızı gətirəcək. Sual üçün: {short}",
        ],
        "ru": [
            "Азерпочта: посылка {track} прибыла в отделение {branch}.",
            "Wolt: ваш заказ в пути, курьер будет через 15 минут.",
            "Bolt: водитель {name} приедет через 3 минуты. Машина {car}",
        ],
        "en": [
            "Azerpost: parcel {track} has arrived at {branch} post office.",
            "Wolt: your order is on the way, courier arrives in 15 min.",
            "Bolt: your driver {name} arrives in 3 minutes. Car {car}",
        ],
    },
    "gov": {
        "az": [
            "ASAN Xidmət: {num} nömrəli müraciətiniz hazırdır. Sənədi 3 iş günü ərzində götürə bilərsiniz.",
            "DYP: {car} avtomobili üzrə {amount} AZN cərimə yazılıb. Ödəniş: e-gov.az və ya ASAN Ödəniş terminalları.",
            "Vergi xidməti: bəyannamənin təqdim edilməsinin son tarixi {date}. Ətraflı: taxes.gov.az",
            "ASAN İmza sertifikatınızın müddəti {date} bitir. Yeniləmək üçün ASAN Xidmət mərkəzinə müraciət edin.",
        ],
        "ru": [
            "ASAN Хидмет: ваше обращение №{num} готово. Документ можно забрать в течение 3 рабочих дней.",
            "ДПС: на автомобиль {car} выписан штраф {amount} AZN. Оплата через e-gov.az.",
            "Налоговая служба: срок подачи декларации до {date}. Подробнее: taxes.gov.az",
        ],
        "en": [
            "ASAN Service: your application {num} is ready for pickup.",
            "Traffic Police: fine of {amount} AZN issued for {car}. Pay at e-gov.az.",
        ],
    },
    "personal": {
        "az": [
            "Salam, axşam gəlirsən?",
            "Ana, gec gələcəm, narahat olma",
            "Sabah saat 10-da görüşürük, unutma",
            "Telefonum oturmuşdu, indi gördüm. Zəng edərəm",
            "Qardaş, {amount} manatı sabah qaytaracam, sağ ol",
            "Ad günün mübarək, {name}! Hər şey ürəyincə olsun",
            "Mağazadan çörək və süd al zəhmət olmasa",
            "Bu mənim yeni nömrəmdir, köhnəni sil. {name}",
            "Toyda görüşərik, saat 7-də restoranın qabağında",
            "Uşaqları məktəbdən sən götürə bilərsən? Mən işdə gecikirəm",
        ],
        "ru": [
            "Привет, ты где? Позвони, как освободишься",
            "Мама, я дома, все хорошо",
            "Встреча перенесена на 15:00",
            "С днем рождения, {name}! Счастья и здоровья",
            "Купи хлеб по дороге домой",
            "Это мой новый номер, сохрани. {name}",
            "Скинь, пожалуйста, фото документов, которые вчера обсуждали",
        ],
        "en": [
            "Hey, are we still meeting at 7?",
            "Running late, be there in 10 min",
            "Happy birthday {name}! Have a great day",
            "This is my new number, save it. {name}",
            "Can you send me the presentation before the meeting?",
        ],
    },
    "marketplace": {
        "az": [
            "Tap.az: Elanınız dərc olundu. Elan №{num}.",
            "Tap.az: Elanınızın müddəti {date} bitir. Uzatmaq üçün tətbiqə daxil olun.",
            "Salam, {item} hələ satılır? Sabah baxmağa gələ bilərəm?",
            "Salam, {item} üçün son qiymət nə qədərdir?",
        ],
        "ru": [
            "Здравствуйте, {item} еще продается? Могу завтра посмотреть",
            "Tap.az: ваше объявление №{num} опубликовано.",
            "Добрый день, за {item} торг уместен?",
        ],
        "en": [
            "Hi, is the {item} still available? Can I see it tomorrow?",
            "Tap.az: your ad {num} has been published.",
        ],
    },
    "service_otp": {
        "az": [
            "Sizin Wolt təsdiq kodunuz: {code}",
            "Bolt kodu: {code}. Paylaşmayın.",
            "myGov giriş kodu: {code}. Kodu heç kimə verməyin.",
        ],
        "ru": [
            "Ваш код для входа в Telegram: {code}. Не давайте код никому.",
            "Код подтверждения: {code}",
        ],
        "en": [
            "Your Google verification code is {code}",
            "{code} is your WhatsApp code. Don't share it.",
        ],
    },
}
