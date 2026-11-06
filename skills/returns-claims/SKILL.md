---
name: returns-claims
description: 'astudio returns and claims for marketplace sellers under Russian law (2026): buyer return requests (WB claims with approve1/approve2/autorefund1/reject actions, Ozon FBO/FBS/rFBS returns), consumer-law deadlines (ЗоЗПП ст. 18, 21, 22, 25, 26.1; КС РФ 7-П of 17.02.2026; Постановление 657 instead of 2463), drafts of answers and disputes with the marketplace (fines, lost or damaged goods) and supplier claims - each with chances, text, attachments and "если откажут". Use for "возврат", "претензия покупателя", "заявка на возврат WB", "спор с маркетплейсом", "претензия поставщику", "сроки возврата". Part of astudio-marketplace-support.'
argument-hint: "[buyer | marketplace | supplier] [facts, dates, photos]"
---

# astudio · Returns and claims

`<root>` = two levels above this skill's base dir. Law and platform facts: `<root>/data/rules.json` § law.
Dates: `<root>/scripts/deadlines.py`. Reference: `<root>/reference/compliance.md` § law.
This is reference work, not legal advice. Every decision about money is a person's.

## Three modes
**1. Buyer return request** (WB claim, Ozon return, chat).
- Facts: delivery date, whether written return information was given at delivery, reason (defect / not fitting /
  wrong item), photos, product type (technically complex? non-returnable list of Постановление 657? individually made?).
- Run `deadlines.py`. State the buyer's rights neutrally: 7 days for a remote purchase (3 months if return information
  was not given), refund within 10 days; defects under ст. 18; the buyer may choose the return method if the seller can
  inspect the goods (КС 7-П, 2026).
- Recommend a WB action (approve1 check at WB warehouse / approve2 take the goods back / autorefund1 refund without
  return / reject1–3 / rejectcustom with a 10–1000 character comment) with the reason; a person decides.
- Never discourage a lawful return. A rejection needs a legal ground in the comment, not «не положено».

**2. Dispute with the marketplace** (fines, lost or damaged goods at the warehouse, wrong acceptance): collect the
supply number, acceptance act, photos/video of packing, the offer clause **as the person shows it** (never invent clause
numbers), amounts.

**3. Claim to a supplier**: contract, batch, defect rate with numbers (from `support-insights`), photos, demand.

## Output for every case
1. **Оценка ситуации**: chances (high / medium / low) and what is missing.
2. **Текст** (answer, appeal or claim) — dated facts, the norm, the demand, the deadline.
3. **Приложить**: list of files.
4. **Если откажут**: the next step (appeal in the seller account, written claim, Роспотребнадзор for buyers, court).

## Rules
- Cite the current acts: Постановление 657 (from 01.09.2026), not 2463; КС 7-П; never "возврат только 7 дней" without the
  3-month case.
- Never falsify evidence or dates; never advise hiding a defect.
- Escalate to a person: legal threats, health harm, counterfeit claims, sums above the threshold in `brand-voice.md`.
