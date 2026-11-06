# Compliance reference (checked 2026-11-06)

## Public answers on Wildberries and Ozon: never
- contacts (phones, e-mails, messengers, «напишите в личку»), links, invitations to other sites or marketplaces;
- requests to change, delete or raise a rating; bonuses, gifts or discounts for reviews (WB: the legal tool is the platform's own «Баллы за отзывы»);
- promises of refunds, compensation, replacement or dates that a person or the platform has not confirmed;
- insults, sarcasm, blaming the buyer, veiled threats («вы заказываете и не выкупаете»);
- the buyer's personal data or order details (152-ФЗ);
- medical or cure claims, guaranteed results, dosage advice (ФЗ «О рекламе» ст. 5, 24, 25 for supplements);
- product facts «по памяти»; blaming the marketplace's warehouse or delivery;
- CAPS, strings of emoji or exclamation marks.
Sanctions on Ozon include hiding messages, disabling communication with buyers and blocking the seller.
Sources: Ozon rules as retold by SelSup; Точка guide for WB; checks in `scripts/reply_check.py`.

## Law (ЗоЗПП and 2026 changes)
See `data/rules.json` § law. Key points:
- Remote purchase: refuse within 7 days of delivery, 3 months if return information was not given; refund in 10 days.
- КС РФ 7-П (17.02.2026): the buyer may choose the return method that lets the seller inspect the goods.
- Rules of sale: Постановление 657 of 30.05.2026, in force from 01.09.2026, replaces 2463.
- Defects: ст. 18; deadlines ст. 21 (replacement 7/20 days), ст. 22 (10 days); exchange ст. 25 (14 days).
- Technically complex goods: 15 days for any defect, then only substantial defects (list: Постановление 924, re-check status).
