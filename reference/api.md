# WB and Ozon support APIs (as of 2026-11; re-check on dev.wildberries.ru and docs.ozon.ru)

## Wildberries (separate token categories, 180 days, can be read-only)
| Task | Method |
|---|---|
| anything new? | GET feedbacks-api /api/v1/new-feedbacks-questions |
| unanswered counts | GET /api/v1/feedbacks/count-unanswered, /api/v1/questions/count-unanswered |
| list reviews | GET /api/v1/feedbacks?isAnswered=false&take≤5000&skip |
| answer / edit review | POST / PATCH /api/v1/feedbacks/answer (2–5000 chars; edit once within 60 days) |
| list / answer questions | GET /api/v1/questions; PATCH /api/v1/questions (answer, edit once within 60 days, reject, mark viewed) |
| return from a review | POST /api/v1/feedbacks/order/return (only if isAbleReturnProductOrders=true) |
| complaint on a review | /api/v1/feedbacks/actions (once per review, ≤1000 chars) |
| chats | buyer-chat-api: GET /api/v1/seller/chats (replySign), GET /api/v1/seller/events, POST /api/v1/seller/message (≤1000 chars) |
| claims | returns-api: GET /api/v1/claims?is_archive=false (last 14 days), PATCH /api/v1/claim {id, action, comment} |
Limit: 1 request/second for the whole Feedbacks and Questions category per seller; >3 rps blocks for 60 s.

## Ozon (Client-Id + Api-Key; 50 rps per Client-Id by default)
| Task | Method | Access |
|---|---|---|
| reviews | POST /v2/review/list, /v2/review/info, /v2/review/count, /v2/review/change-status | «Управление отзывами» or Premium Pro |
| answer review | POST /v1/review/comment/create {review_id, text, mark_review_as_processed}; delete: /v2/review/comment/delete; no edit | same |
| questions | POST /v1/question/list, /v1/question/answer/create {question_id, sku, text 2–3000} | Premium Plus |
| chats | /v3/chat/list, /v3/chat/history, /v1/chat/send/message (1–1000 chars, windows 48/72 h) | Premium Plus / Pro |
| returns | /v1/returns/list (FBO, FBS); rFBS: /v2/returns/rfbs/list, /v1/returns/rfbs/action/set | — |

## Ready MCP servers (optional, install separately; MIT)
- ilyautov/marketplaces-mcp-ru — wide WB/Ozon coverage with a confirm gate. Note: in the version studied the WB review
  answer method was marked `read` and skipped the gate, so this plugin always asks a person before any answer call.
- DeviceIngineering/wb-mcp-server and ozon-mcp-server — narrow, well-described tools and token diagnostics; no confirm gate.
