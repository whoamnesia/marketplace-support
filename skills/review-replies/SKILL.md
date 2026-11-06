---
name: review-replies
description: 'astudio replies to Wildberries and Ozon product reviews: classify each review (thanks, neutral, constructive critique, harsh negative, suspected fake, spam), pick the strategy, write a specific 2-5 sentence reply in the brand voice for future buyers, add "что сделать кроме ответа", batch mode with a summary table and recurring problems, and a compliance check before approval. Use for "ответь на отзывы", "ответы на негатив", "отзывы на WB", "отзывы на Ozon", "что ответить на плохой отзыв", "reply to reviews". Part of astudio-marketplace-support.'
argument-hint: "[paste reviews or queue.json] [wb | ozon]"
---

# astudio · Review replies

`<root>` = two levels above this skill's base dir. Requires `brand-voice.md` (else run `brand-voice` first).
Triage: `<root>/scripts/route.py`. Check: `<root>/scripts/reply_check.py --kind review`.

## Strategy by type
| Type | Goal | Reply |
|---|---|---|
| Thanks (4–5★) | warmth, a detail for future buyers | thank by name; mention the specific thing they praised; one useful tip (care, a matching product from the same shop without a link) |
| Neutral / no text | be present | one or two sentences, never the same text twice in a row |
| Constructive critique (3★, specific) | show the fix | thank for the detail; say what you checked or changed (only true things); how to solve it now through the platform |
| Harsh negative (1–2★) | calm, specific, for readers | acknowledge the exact problem in one sentence; no excuses, no blame; the next step through the platform (return as defect, chat with the seller in the platform); what you do with the batch or card |
| Suspected fake / competitor | do not argue | do not reply in heat: a person decides on a complaint (`/feedbacks/actions` on WB) with evidence |
| Spam / links | none | complaint, no reply |
| Health, safety, counterfeit, legal threat, money dispute | a person decides | escalation brief (`escalation`), optional neutral holding reply for approval |

## Reply shape
1. Name (if given) and the specific point of the review: "Анна, жаль, что крышка не держится уже через неделю."
2. The substance: what is true, what you checked, what will happen. Only facts you have.
3. Next step for the buyer, through the platform: "Оформите возврат в личном кабинете с причиной «брак»".
4. Short close in the brand voice. No contacts, links, ratings talk, promises of money.

2–5 sentences; up to 6 for a negative review. Russian typography: « », em dash with spaces, non-breaking spaces in numbers.

## Batch mode
1. Summary table: № · ★ · type · essence · route · priority.
2. The drafts, each followed by **«Что сделать кроме ответа»** (pass to the warehouse, fix the size chart, ask the supplier).
3. **Повторяющиеся проблемы:** 1–3 themes with counts (≥3 on one product = product or card problem).
4. `reply_check.py --file drafts.json` output; nothing goes for approval with a BLOCK.

## Bad → good
- ✗ «Спасибо за ваш отзыв! Ваше мнение очень важно для нас.» → ✓ «Анна, спасибо, что написали про носик: он и правда не капает, мы долго его подбирали.»
- ✗ «Вы, видимо, неправильно пользовались.» → ✓ «Жаль, что ручка нагревается. Мы передали партию на проверку. Если товар неисправен, оформите возврат в личном кабинете с причиной «брак».»
- ✗ «Напишите нам в телеграм, вернём деньги!» → ✓ «Напишите нам в чат с продавцом на странице заказа — разберёмся по фото.»
