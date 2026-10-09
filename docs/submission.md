# NeuroBridge submission: texts to paste

Copy each block into the matching field on neurobridge.si/dashboard/project.

---

## TRACK

AI Enterprise Solutions

## TITLE

Qalxan: scam campaign radar for mobile operators

(If the title field must stay your team name, keep "La Furia Roja" and put the line above at the start of
"The user and the problem".)

## THE USER AND THE PROBLEM

The user is the anti-fraud analyst at an Azerbaijani mobile operator (Azercell, Bakcell, Nar). Scam SMS reach
thousands of subscribers before anyone reacts: fake Kapital Bank "your card is blocked" links, the fake Azerpost
10.2 AZN customs fee, fake Tap.az buyers, "Mom, this is my new number". Today the defence is a keyword blocklist,
updated by hand after complaints, with hours to days of lag. Scammers beat it by swapping one letter (ə→e, a
Cyrillic "а" inside "Kapitаl"), rotating domains and rephrasing. In our tests the keyword approach catches only
30% of scams. Subscribers lose money, and the operator takes the complaints, the brand damage and the regulator
pressure.

Qalxan reads every SMS like an analyst. It catches the scheme whatever the wording, groups messages into a
campaign within seconds (brand impersonated, domains, phones, messages per minute), and lets the analyst block
the campaign and warn everyone who already received it in one click. Every verdict is explained in Azerbaijani,
Russian and English. Subscribers can forward a suspicious SMS to a Telegram bot and get the same explanation.

## SETUP INSTRUCTIONS

Windows: double-click start_qalxan.bat. It creates a virtual environment, installs requirements.txt, trains the
model (about 10 seconds) and opens http://localhost:8000.
Other OS: python -m venv .venv → .venv/bin/pip install -r requirements.txt → .venv/bin/python scripts/train.py →
.venv/bin/python -m uvicorn qalxan.api:app --port 8000.
Demo: press "Start network traffic", then "Launch scam campaign"; block the campaign; use "Check a message" with
any SMS (example buttons included).
Optional: put GEMINI_API_KEY and TELEGRAM_BOT_TOKEN in .env (see .env.example). Without them the system runs fully
on our own model.
Known limitations: training data is synthetic, and the independent test set is reconstructed from official
warnings, not real subscriber traffic. The Gemini free tier sometimes returns 503 under load, in which case the
model's verdict stands. Dashboard state is in memory and resets on restart.

## DISCLOSURE: MODELS

Our own model: TF-IDF character 2–5-grams + word 1–2-grams + rule features → logistic regression (scikit-learn),
trained by us during the hackathon. Google Gemini (gemini-flash-lite-latest, falling back to gemini-flash-latest)
gives an optional second opinion on grey-zone/risky messages only (2–6% of traffic). Claude (Anthropic, via Claude
Code) was used as an AI coding assistant.

## DISCLOSURE: DATA

Synthetic: 2,714 labelled SMS (AZ/RU/EN) generated from our own templates of documented Azerbaijani scam schemes,
plus hard negatives (bank OTP codes, payment alerts, operator promos, genuine fines). Test split by template; 2
schemes are test-only. Independent test: 70 SMS reconstructed from official warnings (Electronic Security Service,
Ministry of Internal Affairs, Kapital Bank, Azercell). No real subscriber data.

## DISCLOSURE: COMPONENTS

FastAPI, Uvicorn, scikit-learn, NumPy, SciPy, joblib, google-genai, aiogram (Telegram bot), matplotlib,
python-dotenv; fonts Inter and JetBrains Mono (Google Fonts). No templates or prior code.

## QUALITY TESTING: WHAT DID YOU TEST, AND WHAT BROKE?

Baseline = keyword blocklist (how operators filter today).

1) Independent test, 70 SMS: 40 scams reconstructed from official warnings about real Azerbaijani campaigns (the
fake Azerpost 10.2 AZN customs fee, fake "Receive payment" pages for sellers, the fake IBA gift, a "bank specialist"
asking for CVV/OTP/FIN, AnyDesk takeover, a fake "VIP number" sale, WhatsApp code theft) + 30 genuine-looking SMS.
Many of these schemes were never in training.
- Keyword filter: 30% of scams caught, 13% false alarms.
- Our model v1: 85% caught, 3.3% false alarms.
- What broke in v1: it missed every unseen scheme that asks for data instead of a click ("tell us the 16 digits
  and the 3 on the back", "install AnyDesk", "send a passport photo", "send the 6-digit code"). The model was
  confidently wrong (p < 0.2), so the Gemini layer was never asked. It also flagged a genuine payment alert to
  NETFLIX.COM as a suspicious link.
- Fix: risk signals (card/ID data requests, remote-access apps) that always trigger a Gemini second opinion, plus
  trusted merchant domains and an exception for genuine "we never ask for your code" notices.
- After the fix: model 90% caught / 0 false alarms; model + Gemini 97.5% (39/40) / 0 false alarms. This is
  optimistic because it was measured on the same set; v1 is the unbiased number. Still missed: a "SOCAR shares"
  investment pitch with only a Telegram handle.

2) Held-out synthetic set, 873 SMS. Test phrasings never appear in training, 2 schemes exist only in test, and
there are hard negatives (OTP codes, payment alerts, a genuine "card blocked after 3 wrong PINs", fines payable at
e-gov.az).
- Keyword filter: 30.1% caught; on letter-swapped scams 28%.
- Classic char n-gram ML: 94.6% caught, but 18.8% false alarms on genuine bank/OTP SMS.
- Qalxan model: 96.1% caught, 0% false alarms, 99.5% of letter-swapped scams.
- Qalxan + Gemini: 98.5% caught, 0% false alarms; Gemini called for only 2.4% of messages.
- Remaining failures: "bank OTP theft" phrased almost like a genuine OTP SMS; scheme-type labels are 86.7% accurate
  (parcel vs fine confusion).

Speed: ~0.3 ms per SMS on a laptop CPU for our model. Full reports and charts: reports/eval_documented.md,
reports/eval_documented_v1_before_fixes.md, reports/eval_synthetic.md.

---

## Fields that need a decision from the team

- **DEMO LINK:** optional per the form. Can stay empty.
- **GITHUB / GITLAB LINK:** judges must be able to open the code. Your decision: a public repo, or another host
  (for example a shared Google Drive folder with a zip of the project).
- **VIDEO:** needs a link: YouTube (Unlisted) or Google Drive with "anyone with the link can view". Script:
  docs/video_script.md.
- **PITCH DECK:** PDF or PowerPoint up to 30 MB, or a link.
- **Checkbox "built after the hackathon started":** true; nothing was built before.
