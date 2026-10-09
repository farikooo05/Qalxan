# Qalxan quality report (documented)

Test set: 70 SMS (40 scam / 30 legit). Phrasings in the test set never appear in training; two scam schemes exist only in the test set.

| System | Precision | Recall | F1 | False alarms (all legit) | False alarms (bank/OTP/gov SMS) | Recall: letter-swapped | Recall: new schemes | ms/SMS |
|---|---|---|---|---|---|---|---|---|
| Keyword filter (today) | 75.0% | 30.0% | 0.429 | 13.3% | 0.0% | 0.0% | 0.0% | 0.01 |
| Classic ML (char n-grams) | 95.0% | 95.0% | 0.950 | 6.7% | 0.0% | 0.0% | 0.0% | 0.16 |
| Qalxan model | 100.0% | 90.0% | 0.947 | 0.0% | 0.0% | 0.0% | 0.0% | 0.38 |
| Qalxan + Gemini (full cascade) | 100.0% | 97.5% | 0.987 | 0.0% | 0.0% | 0.0% | 0.0% | 197.91 |

Scam-type accuracy (known schemes): 0.0%

Grey band (0.2 < p < 0.8, sent to the LLM layer): 2 of 70 messages

## Missed scams (Qalxan model)

- p=0.152 [real_scam] Kapital Bank: hesabınızı qorumaq üçün AnyDesk tətbiqini yükləyin və ekrandakı kodu mütəxəssisə deyin. Tel: +994 70 512 40 03
- p=0.494 [real_scam] Azercell VIP nömrələr satışı! 050 777 77 77 nömrəsi sizin üçün rezerv olundu. Şəxsiyyət vəsiqəsinin şəklini və 50 AZN beh göndərin WhatsApp: +994 77 340 81 92
- p=0.001 [real_scam] Azercell: эксклюзивный красивый номер закреплён за вами. Пришлите фото паспорта и предоплату 40 AZN на карту 4169 7388 1020 5531
- p=0.163 [real_scam] SOCAR səhmləri ilə ayda 3000 AZN qazanın! Minimum 250 AZN. Telegram: @socar_invest_az

## False alarms (Qalxan model)

- none