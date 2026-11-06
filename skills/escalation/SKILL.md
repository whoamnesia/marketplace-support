---
name: escalation
description: 'astudio triage and escalation for marketplace support: P1-P4 priority with bump rules, what the agent may draft vs what a person must decide (health and safety, counterfeit, legal threats, money disputes, suspected fakes, 3+ same complaints on one product, compliance failures, missing facts, subscription 403s), and a one-screen escalation brief with impact, evidence, what was tried, the decision needed and the deadline. Use for "эскалация", "что передать менеджеру", "срочные отзывы", "приоритеты обращений", "triage". Part of astudio-marketplace-support.'
argument-hint: "[items routed to a person]"
---

# astudio · Escalation

`<root>` = two levels above this skill's base dir. Rules engine: `<root>/scripts/route.py` (decides first; the model
does not override a **human** route).

## Priorities
| P | When | Reaction |
|---|---|---|
| P1 | health or safety harm, legal threat (Роспотребнадзор, суд, претензия), public scandal risk | a person within 4 working hours; check the batch |
| P2 | money or return dispute, counterfeit claim, wrong or incomplete item, 1–2★ with a specific defect | same day |
| P3 | 3★ critique, questions, suspected fake | within 2 days |
| P4 | thanks, neutral | within 3 days (WB archives unanswered reviews after 30 days) |
Bump one level when: the same issue appears in 3+ items on one product; the buyer wrote again; the answer window
closes soon (Ozon chat 48/72 h); a regulator or court is mentioned.

## Escalation brief (one screen)
```
Кому: <роль>            Приоритет: P1      Срок решения: <дата, время>
Что случилось: <1–2 предложения, факты>
Масштаб: <сколько обращений, товар/nmId/SKU, период>
Доказательства: <ссылки на отзывы/чаты по id, фото, номер поставки>
Что уже сделано: <проверки, черновик ответа на согласовании>
Что нужно решить: <конкретный вопрос: вернуть деньги? снять партию? жалоба на отзыв?>
Черновик ответа покупателю (если нужен): <текст, прошедший reply_check>
```

## Rules
- Quantify; do not dramatise. Separate facts from guesses.
- A 403 from Ozon is a subscription question for the owner, not a technical incident.
- After the decision, record it in `brand-voice.md` § «Что можем предложить» if it becomes a rule.
