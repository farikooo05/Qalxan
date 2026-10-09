Create a 14-slide pitch deck in English for a hackathon project. Clean, modern, dark-navy security style with red
(scam), amber (keyword filter) and green/blue (our product) accents. One idea per slide, big numbers, little text,
no stock clichés. Every slide must stay readable as plain text, because the FIRST ROUND OF JUDGING IS DONE BY AI
MODELS (GPT and Claude) READING THE DECK: state every claim and number explicitly in text, not only in images,
and label each slide with the judging criterion it answers.

Context: NeuroBridge.SI AI hackathon, Baku, 9–10 October 2026. Track: AI Enterprise Solutions. Judging card
(100 points): Value for the user 25, Prototype and use of AI 30, Quality testing 20, Feasibility 15,
Originality 10. Team name: La Furia Roja. Product name: Qalxan ("shield" in Azerbaijani).

Use ONLY the facts below. Do not invent numbers, customers or partnerships.

SLIDE 1. Title
- Qalxan: scam campaign radar for mobile operators
- Tagline: "One shield for every subscriber."
- Team La Furia Roja · Track: AI Enterprise Solutions · NeuroBridge.SI Baku 2026

SLIDE 2. The problem [Value for the user]
- Scam SMS in Azerbaijan: fake Kapital Bank "your card is blocked" links, the fake Azerpost 10.2 AZN customs fee
  (officially warned about by the Electronic Security Service), fake Tap.az buyers, "Mom, this is my new number".
- They reach thousands of subscribers before the operator reacts.
- Today: keyword blocklists, updated by hand after complaints, with hours to days of lag.
- Scammers beat them by swapping one letter (ə→e, a Cyrillic "а" inside "Kapitаl", 0 instead of o), rotating
  domains and rephrasing.
- Big number: the keyword approach catches only 30% of scams in our tests.

SLIDE 3. The user and their workflow [Value for the user]
- User: the anti-fraud / security analyst at a mobile operator (Azercell, Bakcell, Nar).
- Today: complaints → manual search → add keywords → hours or days later.
- With Qalxan: the campaign is detected and grouped within seconds → one click to block → one click to warn
  everyone who already received it.
- Secondary user: the subscriber, who forwards a suspicious SMS to a Telegram bot and gets a verdict with an
  explanation in Azerbaijani, Russian or English.

SLIDE 4. The solution [Prototype]
Four capabilities:
1. Detect: reads every SMS in AZ/RU/EN and catches the scheme whatever the wording.
2. Group: groups messages into campaigns (impersonated brand, domains, phones, messages per minute).
3. Act: one-click "Block campaign" and "Warn recipients".
4. Explain: every verdict is explained in AZ/RU/EN ("claims to be Kapital Bank but the link is not its official
   site; do not open the link").

SLIDE 5. Live demo: the core scenario [Prototype]
- Normal traffic flows: bank codes, payments, chats.
- A scam campaign hits: 60 SMS, 3 rotating lookalike domains, letters swapped.
- Within seconds, one campaign card: "Fake bank: card blocked · impersonates Kapital Bank · 3 domains".
- Side by side: Qalxan caught 100% of the campaign; the keyword filter caught about a third.
- Analyst clicks Block, then Warn. A subscriber checks a message in the bot and gets an explanation.

SLIDE 6. How the AI works [Use of AI]
Cascade (draw as a left-to-right flow):
SMS → Normalize (undo letter swaps, ə→e, Cyrillic look-alikes, digits as letters) → Risk signals (impersonated
brand, lookalike / shortened links, asks for code / card / ID, remote-access apps, urgency, threats) → OUR OWN
MODEL (character + word n-grams + rule signals → logistic regression, trained by us) →
  - confident → verdict in ~0.3 ms
  - grey zone or risk signal → Gemini second opinion (only 2.4% of traffic)
→ Campaign grouping → Dashboard / Block / Warn / Explanation in AZ-RU-EN.

SLIDE 7. What AI actually contributes [Use of AI]
- Understands the scheme, not the keywords: catches rephrased and letter-swapped scams (99.5% of letter-swapped
  scams vs 28% for keywords).
- Generalizes to never-seen schemes (fake SIM disconnection and fake state payments were never in training:
  100% caught).
- Turns thousands of messages into a few campaigns an analyst can act on.
- Explains each decision in the subscriber's language.

SLIDE 8. Quality testing 1: documented real-world schemes [Quality testing]
Independent test: 70 SMS. 40 scams reconstructed from official warnings about real campaigns in Azerbaijan
(Electronic Security Service, Ministry of Internal Affairs, Kapital Bank, Azercell): the fake Azerpost customs
fee, fake "Receive payment" pages for sellers, the fake IBA gift, a "bank specialist" asking for CVV/OTP/FIN,
AnyDesk takeover, fake "VIP number" sales, WhatsApp code theft. Plus 30 genuine-looking SMS.
Table:
| System | Scams caught | False alarms |
| Keyword filter (today) | 30% | 13% |
| Our model, first version | 85% | 3.3% |
| Our model + Gemini, final | 97.5% (39 of 40) | 0% |
Note: the final numbers were measured on the same set that revealed the failures, so they are optimistic; the
first-version number is the unbiased one.

SLIDE 9. Quality testing 2: large held-out test [Quality testing]
873 SMS; test phrasings never appear in training; 2 scheme types only in test; hard negatives include real-looking
bank OTP codes, payment alerts, a genuine "card blocked after 3 wrong PINs" notice and fines payable at e-gov.az.
| System | Scams caught | False alarms on genuine bank/OTP SMS |
| Keyword filter (today) | 30.1% | 0% |
| Classic ML (character n-grams only) | 94.6% | 18.8% |
| Qalxan model | 96.1% | 0% |
| Qalxan + Gemini | 98.5% | 0% |
Gemini called for only 2.4% of messages. Speed: ~0.3 ms per SMS on a laptop CPU.
(Leave space for a bar chart image: the team will insert chart_synthetic.png.)

SLIDE 10. What broke, and what we did [Quality testing]
- First version missed every unseen scheme that asks for data instead of a click ("tell us the 16 digits and
  the 3 on the back", "install AnyDesk", "send a passport photo"). The model was confidently wrong, so Gemini was
  never asked.
  → Fix: risk signals that always trigger a second opinion.
- It flagged a genuine payment alert to NETFLIX.COM as a suspicious link.
  → Fix: trusted merchant domains.
- Still failing: an investment pitch with only a Telegram handle; "bank code theft" phrased almost like a real OTP
  SMS; scheme labels 86.7% accurate.

SLIDE 11. Feasibility [Feasibility]
- Privacy: our model runs on the operator's own servers, so SMS content never leaves the network; only the grey
  zone may go to an LLM (a self-hosted model in production).
- Cost: no API cost for ~97.6% of traffic; a laptop CPU classifies thousands of SMS per second.
- Data that exists today: A2P / bulk SMS already inspected by operator SMS firewalls, plus messages subscribers
  forward voluntarily.
- Next step: a 4-week pilot with one operator on subscriber-forwarded reports, then shadow mode on A2P traffic.
  Success metrics: time from campaign start to block, % scams caught vs blocklist, false alarms on bank SMS.

SLIDE 11b. Business model [Feasibility]
Title: "Business model: the operator pays, brands join"
1. Operator license (core revenue): an annual on-premise license priced by subscriber base, plus setup and
   support. Buyer: head of fraud / CTO. Why they pay: fewer scam complaints to the call center, brand trust and
   churn, regulator expectations.
2. Brand protection feed (banks, post, marketplaces): real-time alerts when a brand is impersonated (campaign,
   lookalike domains, phone numbers) for faster takedowns. Monthly subscription per brand.
3. Scam Shield add-on (subscribers, revenue share): the operator bundles warnings and the bot into a tariff or
   loyalty program as a value-added service.
- Unit economics: our model runs on CPU at ~0.3 ms per SMS with no API cost for 97.6% of traffic; the LLM is
  needed for 2.4%.
- Go-to-market: pilot with one Azerbaijani operator → paid license → the same schemes hit Central Asia, Türkiye
  and the GCC. Pricing is validated in the pilot (do not invent prices).

SLIDE 12. Why it is different [Originality]
- Campaign-level, not message-level: analysts act on waves, not single texts.
- Built for Azerbaijan: AZ/RU/EN, Azerbaijani letter folding, Latin/Cyrillic homoglyphs, local brands and
  schemes.
- Explainable: every verdict says why, in the subscriber's language.
- Small own model first, big LLM only when needed: cheap, fast and private.

SLIDE 13. Disclosure and what's next
- Models: our own TF-IDF + logistic regression model (trained during the hackathon); Google Gemini
  (flash-lite / flash) for grey-zone second opinions; Claude used as a coding assistant.
- Data: 2,714 synthetic SMS from our templates of documented schemes; 70-SMS independent test reconstructed from
  official warnings. No real subscriber data.
- Components: FastAPI, scikit-learn, google-genai, aiogram (Telegram), matplotlib.
- Next: voice-call scam detection, on-device version, pilot with an operator.
- Closing line: "Qalxan: one shield for every subscriber."
