---
name: support-insights
description: 'astudio support insights for marketplace sellers: turn reviews, questions and chats into a weekly report - rating trend, share answered and response time, top complaint themes per product with counts and quotes, what to fix in the product card (photos, size chart, description), what to tell the supplier or warehouse, and which questions to pre-empt. Use for "отчёт по отзывам", "аналитика отзывов", "что улучшить в карточке", "частые жалобы", "еженедельный отчёт поддержки". Part of astudio-marketplace-support.'
argument-hint: "[queue.json or export] [period]"
---

# astudio · Support insights

`<root>` = two levels above this skill's base dir. Themes and repeats: `<root>/scripts/route.py --json`.

## Weekly report
1. **Цифры** (each with its source and period): new reviews and questions, average rating, share answered, median
   time to answer, items escalated.
2. **Темы жалоб** by product: theme · count · 1–2 short quotes (no names) · trend vs last week.
3. **Исправить в карточке**: card element · current text · proposed text · which complaints/questions it removes.
4. **Передать поставщику / на склад**: defect themes with counts, batch if known.
5. **Ответить заранее**: questions to add to the description or to pin as answered.
6. **Что поменять в голосе бренда**: replies the seller edited the same way twice.

## Rules
- A theme counts only with ≥3 items on one product in the period; below that, list it as "наблюдаем".
- Never quote personal data. Never estimate numbers you did not count; mark missing data as «нет данных».
