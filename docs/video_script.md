# Qalxan: video script (up to 2:00) and recording guide

## Before you record (5 minutes)

1. **Server running:** open http://localhost:8000 in Chrome. If it does not open, double-click
   `start_qalxan.bat` in the project folder and wait for the dashboard.
2. **Clean screen:** close other tabs; Chrome zoom 100% (`Ctrl + 0`); full screen `F11`.
3. **No pop-ups:** turn on Do Not Disturb (Windows: Notifications → Do not disturb); mute Telegram/WhatsApp.
4. **Clean state:** press **Reset** on the dashboard. Language switch top right: **EN**.
5. **Microphone:** quiet room, laptop mic or headset; do one 10-second test recording and listen to it.
6. Keep this script open on your **phone** to read from.

## How to record (Windows 11)

**Option A, Xbox Game Bar (simplest):**
1. Click on the Chrome window so it is active.
2. `Win + G` → in the Capture widget, check that the **microphone icon is ON** (not crossed out).
3. `Win + Alt + R` starts recording; `Win + Alt + R` again stops it.
4. The file is saved in **Videos → Captures** (Видео → Клипы).

**Option B, Snipping Tool:** `Win + Shift + R` → select the whole screen → Start. Turn the microphone on in
the toolbar before starting.

**Trim to 2:00:** open the video in **Clipchamp** (built into Windows 11) or Photos → Edit → Trim. The video
must be **2 minutes or shorter**.

**Upload and get the link:**
- **YouTube:** Create → Upload video → visibility **Unlisted** → copy the link; or
- **Google Drive:** upload → Share → General access: **Anyone with the link** → copy the link.
- Open the link in a private/incognito window to make sure it plays without logging in.

## Script (about 1:55)

Narration in English for the international jury; Russian translation under each block. Speak calmly: if a
step takes longer, pause; do not rush.

---

### 0:00–0:12 · The problem
**Screen:** the dashboard after Reset, nothing running.

> EN: Every day, scam SMS pretending to be Kapital Bank, Azerpost or the traffic police reach thousands of people
> in Azerbaijan. Operators block them with keyword lists, and scammers beat those lists by changing one letter.

> RU: Каждый день мошеннические SMS от имени Kapital Bank, Азерпочты или дорожной полиции получают тысячи людей
> в Азербайджане. Операторы блокируют их списками слов, а мошенники обходят их, меняя одну букву.

### 0:12–0:30 · Traffic and the attack
**Screen:** click **▶ Start network traffic**. Wait 3 seconds. In the list choose **Fake bank: card blocked**,
click **⚡ Launch scam campaign**.

> EN: This is Qalxan, a scam radar for mobile operators. Here is normal traffic: bank codes, payments, chats.
> Now a scam campaign hits the network: sixty messages, rotating fake domains, letters swapped.

> RU: Это Qalxan, радар мошенничества для мобильных операторов. Вот обычный поток: коды банков, оплаты,
> переписка. А теперь в сеть заходит мошенническая кампания: шестьдесят сообщений, меняющиеся поддельные домены,
> подменённые буквы.

### 0:30–0:55 · The campaign is caught
**Screen:** point the mouse at the campaign card on the left, then at the two bars at the top
(Qalxan vs Keyword filter), then at "False alarms on genuine SMS: 0".

> EN: Within seconds Qalxan groups them into one campaign: which bank is faked, which domains, how fast it spreads.
> Look at the bars: Qalxan catches every scam message, today's keyword filter only about a third.
> And zero false alarms on real bank codes.

> RU: За секунды Qalxan собирает их в одну кампанию: какой банк подделан, какие домены, как быстро она
> распространяется. Посмотрите на полосы: Qalxan ловит каждое мошенническое сообщение, сегодняшний фильтр по
> словам только около трети. И ноль ложных тревог на настоящих кодах банков.

### 0:55–1:08 · The analyst acts
**Screen:** click **Block campaign**, then **Warn … recipients**. Show new messages in the stream marked
**BLOCKED**.

> EN: The analyst blocks the campaign in one click, and everyone who already received it gets a warning.

> RU: Аналитик блокирует кампанию одним кликом, а все, кто уже получил сообщение, получают предупреждение.

### 1:08–1:35 · Why it is a scam
**Screen:** scroll down to **Check a message**. Click the example **Fake bank** → show the verdict.
Click **Real bank code** → SAFE. Switch the language at the top to **AZ** for 2 seconds, then back to **EN**.

> EN: Every verdict is explained: who is being faked, why the link is fake, what not to do. A real bank code is
> recognised as safe. And the explanation comes in Azerbaijani, Russian or English. Subscribers get the same
> answer from our Telegram bot.

> RU: Каждый вердикт объяснён: кого подделывают, почему ссылка фальшивая, чего не делать. Настоящий код банка
> распознаётся как безопасный. Объяснение на азербайджанском, русском или английском. Абоненты получают такой же
> ответ в нашем Telegram-боте.

### 1:35–1:55 · How it works and the close
**Screen:** click the example **New scheme** → SCAM.

> EN: This scheme was never in our training data, and it is still caught. Under the hood is our own model,
> trained by us: it runs on the operator's servers in milliseconds, so messages never leave the network. Only rare
> unclear cases go to Gemini for a second opinion. Qalxan: one shield for every subscriber.

> RU: Этой схемы не было в обучающих данных, и она всё равно поймана. Внутри наша собственная модель, которую мы
> обучили сами: она работает на серверах оператора за миллисекунды, поэтому сообщения не покидают сеть. Только
> редкие спорные случаи уходят в Gemini за вторым мнением. Qalxan: один щит для каждого абонента.

---

## If something goes wrong

- Mistake while talking: keep going, then cut it out in Clipchamp, or press **Reset** and record again.
- The campaign card did not appear after 10 seconds: check that traffic is running (button shows **❚❚ Pause**).
- Dashboard empty or frozen: refresh the page (`F5`) and press **Reset**.
- Longer than 2:00: cut pauses at the start and between scenes first.
