# Qalxan quality report (synthetic)

Test set: 873 SMS (594 scam / 279 legit). Phrasings in the test set never appear in training; two scam schemes exist only in the test set.

| System | Precision | Recall | F1 | False alarms (all legit) | False alarms (bank/OTP/gov SMS) | Recall: letter-swapped | Recall: new schemes | ms/SMS |
|---|---|---|---|---|---|---|---|---|
| Keyword filter (today) | 95.2% | 30.1% | 0.458 | 3.2% | 0.0% | 28.3% | 11.7% | 0.00 |
| Classic ML (char n-grams) | 91.5% | 94.6% | 0.930 | 18.6% | 18.8% | 93.5% | 100.0% | 0.16 |
| Qalxan model | 100.0% | 96.1% | 0.980 | 0.0% | 0.0% | 99.5% | 100.0% | 0.33 |
| Qalxan + Gemini (full cascade) | 100.0% | 98.5% | 0.992 | 0.0% | 0.0% | 100.0% | 100.0% | 79.88 |

Scam-type accuracy (known schemes): 86.7%

Grey band (0.2 < p < 0.8, sent to the LLM layer): 21 of 873 messages

## Missed scams (Qalxan model)

- p=0.233 [bank_otp_theft] Kartınızdan pul çıxarılmasının qаrşısını almаq üçün SMS кodu cavab olarаq yazın. Kapital Bank
- p=0.233 [bank_otp_theft] Kartinizdan pul cixarilmasinin qarsisini almaq ucun SMS kodu cavab olaraq yazin. ABB
- p=0.231 [bank_otp_theft] Kartinizdan pul cixarilmasinin qarsisini almaq ucun SMS kodu cavab olaraq yazin. PASHA Bank
- p=0.231 [bank_otp_theft] Kartınızdan pul çıxarılmasının qarşısını almaq üçün SMS kodu cavab olaraq yazın. PASHA Bank
- p=0.242 [bank_otp_theft] Kartinizdan pul cixarilmasinin qarsisini almaq ucun SMS kodu cavab olaraq yazin. Kapital Bank
- p=0.242 [bank_otp_theft] Kartınızdan pul çıxarılmasının qarşısını almaq üçün SMS kodu cavab olaraq yazın. Kapital Bank
- p=0.235 [bank_otp_theft] Kartınızdan pul çıxarılmasının qarşısını almaq üçün SMS kodu cavab olaraq yazın. Unibank
- p=0.148 [bank_otp_theft] Kapital Bank: hesabinizi qorumaq ucun operatora zeng edin +994 10 138 32 19 ve tesdiq kodunu deyin
- p=0.396 [bank_otp_theft] ABB: hesabinizi qorumaq ucun operatora zeng edin +90 5114541269 ve tesdiq kodunu deyin
- p=0.396 [bank_otp_theft] ABB: hesabınızı qorumaq üçün operatora zəng edin +90 5916881500 və təsdiq kodunu deyin
- p=0.144 [bank_otp_theft] Birbank: hesabinizi qorumaq ucun operatora zeng edin +994 10 635 44 86 ve tesdiq kodunu deyin
- p=0.144 [bank_otp_theft] Unibank: hesabınızı qorumaq üçün operatora zəng edin +994 70 498 07 47 və təsdiq kodunu deyin
- p=0.243 [bank_otp_theft] ABB: подтвердите личность. Пришлите код из смс в ответ на это сообщение
- p=0.244 [bank_otp_theft] Leobank: подтвердите личность. Пришлите код из смс в ответ на это сообщение
- p=0.25 [bank_otp_theft] Birbank: подтвердите личность. Пришлите код из смс в ответ на это сообщение

## False alarms (Qalxan model)

- none