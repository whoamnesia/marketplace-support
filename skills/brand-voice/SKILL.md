---
name: brand-voice
description: 'astudio brand voice for marketplace replies: interview the seller (8 questions) or infer the voice from 10-20 of their best past replies, write brand-voice.md (address, tone, words we use and never use, how we apologise, what we can and cannot offer, where product facts live, example replies) and test it on two sample replies. Required before any reply is drafted. Use for "голос бренда", "тон ответов", "как нам отвечать покупателям", "шаблоны ответов магазина". Part of astudio-marketplace-support.'
argument-hint: "[shop name] [paste past replies, optional]"
---

# astudio · Brand voice

Template: `<root>/templates/brand-voice.md` (`<root>` = two levels above this skill's base dir).

## Interview (one message, eight questions)
1. «Вы» или «ты»? Обращаемся по имени?
2. Тон в трёх словах. Пример бренда, который пишет так, как вам нравится.
3. Эмодзи: никогда / один в позитивных ответах?
4. Фразы, которые вы ненавидите в ответах продавцов.
5. Как вы извиняетесь, когда виноваты?
6. Что вы реально можете предложить недовольному покупателю (только то, что делается через площадку)?
7. Чего вы не обещаете никогда?
8. Где лежат факты о товарах: карточки, паспорта, сертификаты, таблицы размеров. Пришлите 2–3 ответа, которыми гордитесь.

If the seller sends past replies instead, infer the same eight points and show them for confirmation.

## Output
Write `brand-voice.md` from the template. Then test it with two sample replies: a 5★ thank-you with a detail and a
harsh 1★ about a defect. Run both through `reply_check.py`. The seller approves the file.

## Rules
- The voice never overrides platform rules or the law (`<root>/data/rules.json`): no contacts or links even if "that is
  how we always did it". Say so politely and record it in «Не говорим никогда».
- Keep the file short (one screen). Update it when the seller corrects a reply twice in the same way.
