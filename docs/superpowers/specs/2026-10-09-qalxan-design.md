# Qalxan — Scam Campaign Radar for Telecom Operators

Date: 2026-10-09 · NeuroBridge.SI Baku · Track: AI Enterprise Solutions

## Problem
Scam SMS in Azerbaijan (fake bank "card blocked", fake fines, parcel fees, Tap.az buyer links,
"mom, new number") reach thousands of subscribers before an operator reacts. Today detection is
keyword blocklists updated manually after complaints: hours to days of lag, and scammers defeat
keywords with letter swaps (ə→e, Latin/Cyrillic homoglyphs), new domains and rephrasing.

## User
Operator anti-fraud / security analyst (Azercell, Bakcell, Nar). Secondary: subscribers who
forward a suspicious SMS to a bot and get a verdict + explanation in AZ/RU/EN.

## Outcome / metric
Detect and group a new scam campaign within minutes; catch rate vs keyword filter; false-positive
rate on genuine bank SMS (OTP codes, payment alerts) — must stay near zero.

## Architecture (cascade)
1. `normalize` — NFKC, lowercase, Azerbaijani letters folded, homoglyphs in mixed-script tokens
   mapped to Latin, URLs/phones/numbers replaced with tokens.
2. `features` — rule extraction: URLs + domains (official vs lookalike vs shortener), phones,
   impersonated brand, requested action (click link / call / send code / pay), red flags
   (urgency, threat, prize, mixed scripts).
3. `model` — our own model, trained by us on CPU: char n-gram TF-IDF + word TF-IDF + rule
   features → logistic regression (scam probability) and a scam-type classifier.
4. `llm` — Gemini (free tier) only for uncertain cases (probability in the grey band) and novel
   schemes; optional, system works without it.
5. `explain` — verdict explanation in AZ/RU/EN from detected brand/action/red flags.
6. `campaigns` — online clustering of scam messages by shared domain/phone or text similarity
   within the same scheme; spike detection.

## Surfaces
- FastAPI backend: `/api/analyze`, live SSE stream, campaigns, stats, simulator controls,
  block/warn actions. Serves the dashboard.
- Dashboard "Radar" (single-page HTML/JS): live feed, campaign cards, keyword-filter vs Qalxan
  comparison, "check a message" box.
- Simulator: normal traffic + "launch scam campaign" with mutated variants.
- Telegram bot: forward an SMS, get verdict + explanation in the user's language.

## Data
- Synthetic labelled SMS generated in this session (disclosed), AZ/RU/EN/mixed, scam schemes +
  hard negatives (real-looking bank OTP/payment SMS, operator promos with links, personal chats).
- Train/test split by template family; two scheme types exist only in test (novel schemes).
- Real scam SMS collected by the team from their phones → extra real-world test set.

## Quality testing
Baselines: keyword filter (current approach), char TF-IDF only. Ours: full model, model + LLM.
Metrics: precision, recall, F1, FPR on genuine bank SMS, recall on obfuscated messages, recall on
novel schemes. Report with charts + failure examples → goes into the deck.

## Feasibility
Own model runs on operator premises (SMS content never leaves), ms latency, ~zero marginal cost;
LLM sees only the grey band. Data sources: A2P/bulk traffic already inspected by SMS firewalls +
subscriber-forwarded reports. Next step: pilot on forwarded reports with one operator.

## Out of scope (next steps slide)
Voice-call scam detection, on-device app, production SMS-firewall integration.
