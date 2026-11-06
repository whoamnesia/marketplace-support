# Third-party notices / Сторонние источники

astudio-marketplace-support is written by **astudio.one**. Its rules, workflows and tools are original work. The projects below were studied in full; ideas, structures and checklists were adapted from them with credit. Where text was translated or adapted from an Apache-2.0 project, that project's notice is reproduced below.

astudio-marketplace-support написан **astudio.one**. Правила, сценарии и инструменты — собственная работа. Проекты ниже изучены целиком; идеи, структура и чек-листы взяты из них с указанием авторства. Где текст переведён или адаптирован из проекта под Apache-2.0, его уведомление приведено ниже.

## Studied and adapted / Изучены и использованы

| Project | Licence | What we took |
|---|---|---|
| [ilyautov/marketplaces-mcp-ru](https://github.com/ilyautov/marketplaces-mcp-ru) | MIT | WB/Ozon support endpoint map, read/write/destructive gate idea, 'cluster recurring complaints by product' recipe |
| [DeviceIngineering/wb-mcp-server](https://github.com/DeviceIngineering/wb-mcp-server) | MIT | WB claim actions, replySign, token diagnostics, PII masking principle |
| [DeviceIngineering/ozon-mcp-server](https://github.com/DeviceIngineering/ozon-mcp-server) | MIT | Ozon review/question/chat/return method map, 403 = subscription, no edit = delete and recreate |
| [codebywater/WB-OZON-AI-TEAM](https://github.com/codebywater/WB-OZON-AI-TEAM) | MIT | brand-voice gate and interview, review type table, [уточнить], «что добавить в карточку», returns output shape (its contact-sharing contradiction removed) |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | customer-support: reply structure, internal notes, P1–P4 triage, escalation criteria and brief |

## Studied, ideas only (no code or text copied) / Только идеи, без копирования

| Project | Licence | Why ideas only |
|---|---|---|
| [anymasoft/marketplace-reviews-ai](https://github.com/anymasoft/marketplace-reviews-ai) | no licence | never-auto-answer routing and regex compliance checks — re-implemented from scratch in route.py and reply_check.py |
| [composio-community/support-skills](https://github.com/composio-community/support-skills) | no licence | anger classification idea only |

## Apache-2.0 notices

- anthropics/knowledge-work-plugins (customer-support) — Copyright Anthropic, PBC. Licensed under the Apache License 2.0. Triage and escalation ideas were adapted and rewritten for marketplaces in Russian; no file was copied.

## Public documentation / Открытая документация

- Wildberries API: Customer Communication, API information (dev.wildberries.ru)
- Ozon Seller API OpenAPI (docs.ozon.ru/api/seller), snapshot 2026-10-18
- Закон РФ «О защите прав потребителей» ст. 18, 20–22, 25, 26.1 (КонсультантПлюс)
- Постановление КС РФ № 7-П от 17.02.2026; Постановление Правительства РФ № 657 от 30.05.2026; № 924 от 10.11.2011
- ФЗ «О рекламе»; 152-ФЗ «О персональных данных»
