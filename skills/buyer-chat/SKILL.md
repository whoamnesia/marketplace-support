---
name: buyer-chat
description: 'astudio buyer chats on Wildberries and Ozon: reply to buyer messages inside the platform chat within its rules (WB 1000 characters with replySign, Ozon 1-1000 characters, Premium Plus/Pro, FBO 48-hour and FBS/rFBS 72-hour windows), ask for photos of a defect, explain the return procedure, de-escalate angry buyers, and never move the conversation off the platform. Use for "чат с покупателем", "ответь в чате", "сообщение покупателю", "покупатель пишет в чат", "buyer chat". Part of astudio-marketplace-support.'
argument-hint: "[chat history] [order context]"
---

# astudio · Buyer chat

`<root>` = two levels above this skill's base dir. Windows and limits: `<root>/data/rules.json`. Check:
`reply_check.py --kind chat`.

## Before writing
- Platform and window: Ozon FBO — reply only within 48 h of the buyer's last message; FBS/rFBS — you may write within
  72 h after delivery, then only reply within 48 h. If the window is closed, say so and do not draft.
- Read the whole chat and the order status. Classify the buyer's state: frustrated, hostile, anxious, confused.
  Find the root cause: defect, wrong item, delay, unmet expectation, misunderstanding of the procedure.

## Reply shape (1–4 sentences)
Acknowledge the specific problem → the one thing we need or do now → the next step and who does it → short close.
Example: «Понимаю, неприятно получить чайник с вмятиной. Пришлите, пожалуйста, два фото: коробку и вмятину крупно. Мы
проверим и в течение дня напишем, как оформить замену или возврат через площадку.»
Promise only what the brand voice file and a person allow; timeframes only for your own actions.

## De-escalation
Do not match anger; name the problem in their words; one apology for a real failure, no apologies for things that are
not yours; offer a concrete next step; never «успокойтесь». If the buyer threatens a regulator or court, stop and
escalate (`escalation`).

## Never
Phone, e-mail, messengers, links, «давайте перейдём в WhatsApp», asking for card details or passport data, payment
outside the platform.
