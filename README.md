# astudio-marketplace-support — customer support for Wildberries and Ozon sellers

**English** · [Русский](README.ru.md)

Author: **astudio.one** — [astudio.one](https://astudio.one) · License: MIT · Version 1.0.0

A plugin that runs a seller's customer care on Wildberries and Ozon the way a careful head of support would: reviews, buyer questions, chats, returns and claims — in the brand's voice, within marketplace rules and the 2026 Russian consumer law, with a compliance check on every draft and a named person approving anything that gets published.

## What it does

- Brand-voice gate: no reply is written until brand-voice.md exists
- Rule-based triage: health, safety, counterfeit, legal threats and money disputes always go to a person
- Review replies by type, buyer-question answers from card data only, in-platform chat replies within Ozon's 48/72-hour windows
- Returns and claims under ЗоЗПП with the 2026 changes (КС РФ 7-П, Постановление 657 instead of 2463) and a deadline calculator
- Deterministic compliance checker for Russian replies: contacts, links, rating manipulation, compensation promises, medical claims, tone, length
- Read-only queue fetch from WB/Ozon APIs and a publisher that sends only items approved by a named person
- Weekly insights: complaint themes per product and what to fix in the card

## Install

In Claude Code:

```
/plugin marketplace add whoamnesia/astudio-marketplace-support
/plugin install astudio-marketplace-support@astudio-marketplace-support
```

Restart Claude Code. Skills appear in the `/` menu as `astudio-marketplace-support:astudio-marketplace-support` …

Pinned install (what aiocenter.ru does): clone the repository, check out the published commit, then `/plugin marketplace add ~/.aiocenter/packages/astudio-marketplace-support`.

Other agents (Cursor, Codex, Gemini CLI): every skill is a plain `skills/<name>/SKILL.md` with references; point the agent at the folder or copy it into the agent's rules.

## Skills

| Skill | What it does |
|---|---|
| `astudio-marketplace-support` | Main skill: queue → triage → draft → check → approval → publish → insights |
| `brand-voice` | Interview or inference of the shop's voice into brand-voice.md |
| `review-replies` | Replies to reviews by type, batch mode, «что сделать кроме ответа» |
| `buyer-questions` | Answers to card questions from facts only; «что добавить в карточку» |
| `buyer-chat` | Platform chat replies, windows, de-escalation |
| `returns-claims` | Returns, marketplace disputes and supplier claims under 2026 law |
| `escalation` | P1–P4 triage and a one-screen escalation brief |
| `support-insights` | Weekly report: themes, card fixes, supplier issues |

## Tools

Python 3.9+, standard library only. They read what you pass them and write nothing unless you redirect the output.

| Script | Purpose |
|---|---|
| `scripts/queue.py` | Read-only fetch of unanswered WB/Ozon reviews and questions |
| `scripts/route.py` | Rule-based triage, priorities and repeated issues per product |
| `scripts/reply_check.py` | Compliance check of a reply (RU/EN), Cyrillic-safe |
| `scripts/publish.py` | Sends only approved, re-checked replies; dry run by default |
| `scripts/deadlines.py` | Consumer-law dates for a remote purchase |

## Safety

- Nothing is published, sent, accepted or rejected without a named person's approval; publish.py refuses unapproved items and re-runs the compliance check.
- Queue fetch needs only a read-only token; tokens come from environment variables and are never printed.
- WB rate limit (1 request/second for the category) is respected; Ozon 403s are reported as subscription issues.
- Reference on consumer law, not legal advice; disputes go to a person.

## Layout

```
astudio-marketplace-support/
  .claude-plugin/plugin.json, marketplace.json
  skills/<8 skills>/SKILL.md
  data/rules.json        platform limits and consumer law, dated
  reference/             compliance.md · api.md
  templates/brand-voice.md
  scripts/               queue.py · route.py · reply_check.py · publish.py · deadlines.py
  README.md · README.ru.md · LICENSE · NOTICE.md
```

## Training track

This plugin is the package of the aiocenter.ru track «Поддержка клиентов маркетплейса»: digests, agent memo and an exam with a signed certificate — https://aiocenter.ru/tracks/marketplace-support/

## Credits

Built by astudio.one on ideas from the best open-source projects in this field; see [NOTICE.md](NOTICE.md) for sources and licences.
