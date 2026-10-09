# Qalxan quality report (documented)

Test set: 70 SMS (40 scam / 30 legit). Phrasings in the test set never appear in training; two scam schemes exist only in the test set.

| System | Precision | Recall | F1 | False alarms (all legit) | False alarms (bank/OTP/gov SMS) | Recall: letter-swapped | Recall: new schemes | ms/SMS |
|---|---|---|---|---|---|---|---|---|
| Keyword filter (today) | 75.0% | 30.0% | 0.429 | 13.3% | 0.0% | 0.0% | 0.0% | 0.00 |
| Classic ML (char n-grams) | 95.0% | 95.0% | 0.950 | 6.7% | 0.0% | 0.0% | 0.0% | 0.16 |
| Qalxan model | 97.1% | 85.0% | 0.907 | 3.3% | 0.0% | 0.0% | 0.0% | 0.35 |

Scam-type accuracy (known schemes): 0.0%

Grey band (0.2 < p < 0.8, sent to the LLM layer): 1 of 70 messages

## Missed scams (Qalxan model)

- p=0.006 [real_scam] Salam, mən bankın təhlükəsizlik şöbəsindənəm. Kartınız ələ keçirilib, pulunuzu qorumaq üçün kartın 16 rəqəmini və arxadakı 3 rəqəmi yazın.
- p=0.14 [real_scam] Kapital Bank: hesabınızı qorumaq üçün AnyDesk tətbiqini yükləyin və ekrandakı kodu mütəxəssisə deyin. Tel: +994 70 512 40 03
- p=0.18 [real_scam] Azercell VIP nömrələr satışı! 050 777 77 77 nömrəsi sizin üçün rezerv olundu. Şəxsiyyət vəsiqəsinin şəklini və 50 AZN beh göndərin WhatsApp: +994 77 340 81 92
- p=0.001 [real_scam] Azercell: эксклюзивный красивый номер закреплён за вами. Пришлите фото паспорта и предоплату 40 AZN на карту 4169 7388 1020 5531
- p=0.185 [real_scam] SOCAR səhmləri ilə ayda 3000 AZN qazanın! Minimum 250 AZN. Telegram: @socar_invest_az
- p=0.007 [real_scam] WhatsApp: hesabınız bloklanacaq. Təsdiq etmək üçün sizə gələn 6 rəqəmli kodu bu nömrəyə göndərin.

## False alarms (Qalxan model)

- p=0.999 [real_legit] Kapital Bank: Payment of 9.99 AZN to NETFLIX.COM approved. Card *4821