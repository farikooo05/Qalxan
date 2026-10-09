# Сценарий видео Qalxan (до 2 минут)

**Как записать:** откройте http://localhost:8000 в Chrome во весь экран (F11), нажмите `Win + Alt + R`
(Xbox Game Bar), повторно `Win + Alt + R`, чтобы остановить. Видео сохранится в «Видео → Клипы».
Перед записью нажмите **Reset** на дашборде. Говорите спокойно; текст можно читать с телефона.

Озвучка дана на английском (для международного жюри) и в переводе на русский. Время ориентировочное.

---

## 0:00–0:15. Проблема
**Экран:** дашборд, ничего не запущено.

> EN: Every day, scam SMS pretending to be Kapital Bank, Azerpost or the traffic police reach thousands of people
> in Azerbaijan. Operators block them with keyword lists, and scammers beat those lists by swapping a single letter.

> RU: Каждый день мошеннические SMS от имени Kapital Bank, Азерпочты или дорожной полиции получают тысячи
> людей в Азербайджане. Операторы блокируют их списками ключевых слов, а мошенники обходят их, меняя одну букву.

## 0:15–0:35. Поток и запуск атаки
**Экран:** нажмите **▶ Start network traffic**, через 3 секунды выберите «Fake bank: card blocked» и
нажмите **⚡ Launch scam campaign**.

> EN: This is Qalxan, a scam radar for mobile operators. Here is normal SMS traffic: bank codes, payments, chats.
> Now a scam campaign hits the network: sixty messages, three rotating domains, letters swapped to dodge filters.

> RU: Это Qalxan, радар мошенничества для мобильных операторов. Вот обычный поток SMS: коды банков, оплаты,
> переписка. А теперь в сеть заходит мошенническая кампания: шестьдесят сообщений, три сменяющихся домена,
> подменённые буквы.

## 0:35–1:00. Кампания найдена
**Экран:** наведите курсор на карточку кампании слева, затем на полосы сравнения вверху.

> EN: Within seconds Qalxan groups them into one campaign: fake Kapital Bank, these domains, this many messages per
> minute. Look at the bars: Qalxan caught every scam, the keyword filter operators use today caught about a third.
> And zero false alarms on real bank codes.

> RU: За секунды Qalxan собирает их в одну кампанию: поддельный Kapital Bank, вот домены, столько-то сообщений
> в минуту. Посмотрите на полосы: Qalxan поймал все, а фильтр по словам, который используют сегодня, около трети.
> И ни одной ложной тревоги на настоящих банковских кодах.

## 1:00–1:15. Действие аналитика
**Экран:** нажмите **Block campaign**, затем **Warn recipients**. Покажите, как новые сообщения в ленте
помечаются BLOCKED.

> EN: The analyst blocks the campaign in one click, and everyone who already received it gets a warning SMS.

> RU: Аналитик блокирует кампанию одним кликом, а все, кто уже получил SMS, получают предупреждение.

## 1:15–1:40. Почему это мошенничество
**Экран:** прокрутите вниз, нажмите пример «Fake bank», затем «Real bank code», переключите язык на AZ.

> EN: Every verdict is explained in Azerbaijani, Russian or English: who is impersonated, why the link is fake,
> what not to do. A real bank code is recognised as safe. Subscribers get the same answer from our Telegram bot.

> RU: Каждый вердикт объясняется на азербайджанском, русском или английском: кого подделывают, почему ссылка
> фальшивая, чего не делать. Настоящий код банка распознаётся как безопасный. Абоненты получают такой же ответ
> в нашем Telegram-боте.

## 1:40–2:00. Как это работает и почему реально внедрить
**Экран:** нажмите пример «New scheme» (новая схема, которой не было в обучении).

> EN: Under the hood is our own model, trained by us: it runs on the operator's servers in milliseconds, so SMS
> never leave the network. Only the rare unclear cases go to Gemini for a second opinion. Even schemes it has never
> seen are caught. Qalxan: one shield for every subscriber.

> RU: Внутри наша собственная модель, которую мы обучили сами. Она работает на серверах оператора за миллисекунды,
> поэтому SMS не покидают сеть. Только редкие спорные случаи уходят в Gemini за вторым мнением. Ловятся даже
> схемы, которых модель никогда не видела. Qalxan: один щит для каждого абонента.
