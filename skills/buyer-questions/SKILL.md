---
name: buyer-questions
description: 'astudio answers to buyer questions on Wildberries and Ozon product cards: a direct answer in the first sentence from card data and documents only, a useful clarification in the second, [уточнить] for unknown facts with a list of what to ask the supplier, no promises of delivery or returns, and a "что добавить в карточку" table from repeated questions. Ozon answers need the SKU and 2-3000 characters. Use for "ответь на вопросы покупателей", "вопросы на карточке", "вопросы по товару", "buyer questions". Part of astudio-marketplace-support.'
argument-hint: "[paste questions or queue.json] [card data / fact sheet]"
---

# astudio · Buyer questions

`<root>` = two levels above this skill's base dir. Check: `reply_check.py --kind question`.

## Answer shape
1. **First sentence answers the question** with the fact: «Да, подходит для индукционной плиты: дно 4 мм с ферромагнитным слоем.»
2. Second sentence: the condition, limit or a useful extra («Диаметр дна — 22 см, для конфорки 18 см тоже подойдёт»).
3. Optional third: what to look at on the card (the photo with the size chart), without links.

## Facts
Only from: the card's characteristics, the product passport or instruction, certificates, the brand fact sheet. If the
fact is missing, write `[уточнить: состав ткани у поставщика]` and add it to a list «Что спросить у поставщика».
Never answer about composition, compatibility, safety, age or medical effect from memory.

## Forbidden
Contacts, links, other platforms; delivery dates and free returns (the platform decides); «сертифицировано» or medical
claims without the document; comparing with a competitor's product by name.

## After a batch
Table «Что добавить в карточку»: question theme · times asked · proposed card text · where (characteristics,
description, photo, size chart). Two or more identical questions mean the card is missing the fact.
