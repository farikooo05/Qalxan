# Qalxan — scam campaign radar for mobile operators

*Qalxan* means "shield" in Azerbaijani.

**NeuroBridge.SI Baku 2026 · Track: AI Enterprise Solutions**

Scam SMS in Azerbaijan ("your Kapital Bank card is blocked", "pay 1.99 AZN customs fee", "Mom, this is my new
number") reach thousands of subscribers before an operator reacts. Today's defence is a keyword blocklist,
updated by hand after complaints. Scammers beat it with letter swaps (`ə→e`, Cyrillic `а` inside Latin words,
`0` for `o`), fresh domains and rephrasing.

Qalxan reads every SMS the way an analyst would, catches the scheme whatever the wording, **groups messages into
campaigns within seconds**, and lets the anti-fraud analyst block a campaign and warn its recipients in one click.
Subscribers can forward a suspicious SMS to a Telegram bot and get a verdict with an explanation in Azerbaijani,
Russian or English.

## Who it is for

- **Primary user:** the anti-fraud / security analyst at a mobile operator (Azercell, Bakcell, Nar).
- **Secondary:** subscribers who want to check a message before they click.

## Results

### Test 1: documented real-world schemes (70 SMS, independent of training)

Scams reconstructed from official warnings about real campaigns in Azerbaijan (Electronic Security Service,
Ministry of Internal Affairs, Kapital Bank, Azercell): the fake Azerpost 10.2 AZN customs fee, fake
"Receive payment" pages for online sellers, the fake IBA gift, "bank specialist" asking for CVV/OTP/FIN, AnyDesk
takeover, fake sale of "VIP numbers", WhatsApp code theft. Written after training, in different wording; many of
these schemes never appear in training. 30 genuine-looking SMS as hard negatives. File:
[data/documented_cases.txt](data/documented_cases.txt).

| System | Precision | Recall | False alarms |
|---|---|---|---|
| Keyword filter (today's approach) | 75.0% | **30.0%** | 13.3% |
| Classic ML (char n-grams only) | 95.0% | 95.0% | 6.7% |
| Qalxan model, first version | 97.1% | 85.0% | 3.3% |
| Qalxan model, after fixing the failures below | 100% | 90.0% | 0.0% |
| **Qalxan model + Gemini (full cascade)** | **100%** | **97.5%** | **0.0%** |

Gemini was consulted for only 4 of 70 messages.

**What we learned from the first version (and fixed):** it missed every scheme it had never seen that asks for
data instead of a click ("tell us the 16 digits and the 3 on the back", "install AnyDesk", "send a photo of your
passport", "send the 6-digit code") because the model was confidently wrong (p < 0.2), so the Gemini layer was never
asked. Fix: new risk signals (card/ID data requests, remote-access apps) that always trigger a second opinion, plus
an exception for genuine "we never ask for your code" notices. It also flagged a genuine payment alert to
`NETFLIX.COM` because a merchant name looked like a link; well-known merchant domains are now trusted.
Caveat: the "after" rows were measured on the same 70 messages that revealed the failures, so they are optimistic;
the first-version row is the unbiased one ([reports/eval_documented_v1_before_fixes.md](reports/eval_documented_v1_before_fixes.md)).
The one scam still missed: a "SOCAR shares" investment pitch with only a Telegram handle.

### Test 2: large synthetic held-out set (873 SMS)

| System | Precision | Recall | False alarms on genuine bank/OTP/gov SMS | Recall on letter-swapped scams | Recall on never-seen schemes |
|---|---|---|---|---|---|
| Keyword filter (today's approach) | 95.2% | **30.1%** | 0.0% | 28.3% | 11.7% |
| Classic ML (char n-grams only) | 91.5% | 94.6% | **18.8%** | 93.5% | 100% |
| Qalxan model | 100% | 96.1% | 0.0% | 99.5% | 100% |
| **Qalxan model + Gemini (full cascade)** | **100%** | **98.5%** | **0.0%** | **100%** | **100%** |

Gemini was consulted for 21 of 873 messages (2.4% of traffic); the other 97.6% were decided by our own model.

- Test phrasings never appear in training (split by template), and two whole scam schemes (fake SIM
  disconnection, fake state payment) exist **only** in the test set.
- Hard negatives are deliberately included: real-looking bank OTP codes ("never share this code"), payment alerts,
  a genuine "card blocked after 3 wrong PINs" notice, operator promos with links, real traffic fines with
  e-gov.az, "this is my new number" from a friend.
- Speed: ~0.3 ms per SMS on a laptop CPU (batch), 2–7 ms end to end per request.
- Full report with failure examples: [reports/eval_synthetic.md](reports/eval_synthetic.md), chart:
  [reports/chart_synthetic.png](reports/chart_synthetic.png).

### Honest failures

- On the synthetic set the model alone misses ~23 of 594 scams, almost all "bank OTP theft" phrased like a genuine
  OTP SMS ("to stop the debit, reply with the SMS code"). They land in the grey zone or carry a risk signal, which is
  exactly where the Gemini layer is consulted.
- Scheme-type accuracy is 86.7%: parcel vs fine messages share "pay a fee" wording.
- The data is synthetic (see Disclosure). A real-world check on SMS collected by the team is in
  `scripts/import_real.py` → `reports/eval_real.md`.

## How it works

```
SMS ─► normalize ─► rule signals ─► Qalxan model ─┬─ p ≥ 0.8 → SCAM ─► campaign grouping ─► dashboard / block / warn
       (ə→e,        (brand, links,   (char + word  ├─ p ≤ 0.2 → SAFE
        homoglyphs,  lookalike       n-grams +     └─ grey zone → Gemini second opinion (optional)
        URLs, nums)  domains, asks   rule features,
                     for code, …)    logistic reg.)        explanation in AZ / RU / EN
```

1. **Normalization** (`qalxan/normalize.py`) undoes evasion: Azerbaijani letter folding, Cyrillic look-alikes inside
   Latin words, digits used as letters, URLs/phones/numbers replaced with tokens.
2. **Rule signals** (`qalxan/features.py`): impersonated brand, official vs lookalike vs shortened links, what the
   message asks for (click, pay, call, send code, send money), urgency, threats, prizes, "new number" pretext.
3. **Our own model** (`qalxan/model.py`): character n-grams survive letter swaps, word n-grams carry meaning, rule
   signals add domain knowledge. Trained by us on CPU in seconds. Two heads: scam probability and scheme type.
4. **Gemini layer** (`qalxan/llm.py`), optional: only messages in the grey zone (≈2–3% of traffic) are sent to
   Gemini for a second opinion. The system works fully without it.
5. **Campaign grouping** (`qalxan/campaigns.py`): shared domains or phones, same impersonated brand within
   10 minutes, or near-identical wording → one campaign, with live per-minute rate.
6. **Explanations** (`qalxan/explain.py`) in Azerbaijani, Russian and English for subscribers and analysts.

## Feasibility

- **Privacy:** the model runs on the operator's own servers, so SMS content never leaves the network. Only the
  grey zone may go to an LLM, and in production that would be a self-hosted model.
- **Cost:** no per-message API cost for ~97% of traffic; a laptop CPU classifies thousands of SMS per second.
- **Data sources that exist today:** A2P / bulk SMS already inspected by operator SMS firewalls, plus messages
  subscribers forward voluntarily (bot or short number).
- **Next step:** a 4-week pilot on subscriber-forwarded reports with one operator, then shadow mode on A2P traffic.

## Run it

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows (use .venv/bin/pip on macOS/Linux)
.venv/Scripts/python scripts/train.py             # builds data/ and models/qalxan.joblib
.venv/Scripts/python scripts/evaluate.py          # writes reports/
.venv/Scripts/python -m uvicorn qalxan.api:app --port 8000
```

Open http://localhost:8000, press **Start network traffic**, then **Launch scam campaign**.
Optional: copy `.env.example` to `.env` and set `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN`.

## Disclosure (models, data, components)

- **Our model:** scikit-learn TF-IDF (character 2–5-grams, word 1–2-grams) + logistic regression, trained by the team
  during the hackathon on the data below.
- **LLM:** Google Gemini (`gemini-flash-latest`) via the `google-genai` SDK, used only for grey-zone messages and
  only when an API key is configured. Prompt in `qalxan/llm.py`.
- **AI coding assistant:** Claude (Anthropic) via Claude Code helped write the code and the synthetic SMS templates.
- **Data:** 2,714 synthetic SMS generated from hand-written templates (`qalxan/synth_templates.py`) modelled on
  publicly reported scam schemes in Azerbaijan, filled with random brands, amounts, lookalike domains and phones,
  with programmatic obfuscation. No real subscriber data. Real SMS collected by the team from their own phones are
  used only as an extra test set (`data/real_sms.txt`).
- **Libraries:** FastAPI, Uvicorn, scikit-learn, NumPy, SciPy, joblib, aiogram (Telegram), google-genai,
  matplotlib, python-dotenv. Fonts: Inter, JetBrains Mono (Google Fonts).
- Nothing was built before the hackathon started.
