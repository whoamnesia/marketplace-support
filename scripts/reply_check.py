#!/usr/bin/env python3
"""astudio-marketplace-support · reply_check.py — deterministic compliance check of a reply
before it is shown to a human for approval. Russian and English.

  python3 reply_check.py --platform wb --kind review "Текст ответа"
  python3 reply_check.py --platform ozon --kind question --file drafts.json   # [{"id":..,"text":..}, ...]

Exit code 1 if any blocking issue is found. Never sends anything anywhere.
Codes: contact, link, other_platform, rating_manipulation, compensation_promise,
hostile_tone, personal_data, medical_claim, guaranteed_result, blame_logistics,
placeholder, length, stock_phrase (warn), caps (warn), emoji (warn).
"""
import argparse, json, re, sys, pathlib

# Cyrillic-safe word boundaries: \b does not treat Cyrillic consistently in every engine, so use lookarounds.
L = r"(?<![а-яёa-z0-9])"
R = r"(?![а-яёa-z0-9])"

def w(p):  # whole-word pattern
    return re.compile(L + p + R, re.I | re.U)

BLOCK = [
    ("contact", re.compile(r"(\+7|8)[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-]*\d{2}[\s\-]*\d{2}|[\w.+-]+@[\w-]+\.[\w.]+|(?<!\w)@[a-z0-9_]{4,}|whats\s?app|телеграм|telegram|вайбер|viber|ватсап|напишите (нам )?в (личку|лс|директ)", re.I), "contacts, e-mails or messengers are not allowed in public answers"),
    ("link", re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(ru|com|рф|net|org|shop|store)\b", re.I), "links are not allowed"),
    ("other_platform", w(r"(озон|ozon|вайлдберриз|wildberries|вб|wb|яндекс\s?маркет|мегамаркет|авито|avito|aliexpress|алиэкспресс|lamoda|ламода)"), "naming marketplaces in a reply (check: allowed only for the platform you answer on, never to send buyers elsewhere)"),
    ("rating_manipulation", re.compile(L + r"(измен|поменя|исправ|удал|повыс|подним|подня|пересмотр)\w*\s+(\w+\s+){0,2}(оценк|отзыв|звезд|рейтинг)|оценк\w*\s+на\s+(5|пять)|поставьте\s+(5|пять)|(бонус|подарок|скидк\w*|кешбэк|кэшбэк|баллы)\s+за\s+(отзыв|оценк)|change (your )?rating|remove (your )?review", re.I | re.U), "asking to change a rating or rewarding reviews is forbidden"),
    ("compensation_promise", re.compile(L + r"(мы\s+)?(верн[её]м|вернем|перечисл(им|ю)|компенсиру(ем|ю)|возмест(им|им вам)|отправим (вам )?(новый|замену|бесплатно)|вышлем замену|гарантируем возврат)" + R + r"|we will refund|we.ll refund|we will send (you )?a replacement", re.I | re.U), "promise of money or replacement: only a human may confirm it; rephrase as the procedure"),
    ("hostile_tone", re.compile(L + r"(сами виноваты|читайте внимательн|надо было|нужно было (смотреть|читать)|вы не правы|не выдумывайте|вы ошибаетесь|видимо, вы|неадекват|не умеете)" + R + r"|your own fault|you should have read", re.I | re.U), "blaming or sarcastic tone"),
    ("personal_data", re.compile(r"(номер\s+(вашего\s+)?заказа\s*№?\s*\d{5,}|\b\d{10,}\b|паспорт|адрес доставки:)", re.I), "do not publish order numbers or personal data"),
    ("medical_claim", w(r"(вылеч\w*|лечит|излеч\w*|исцел\w*|от (диабета|рака|давления|простатит\w*)|избав\w+ от болезн\w*|cures?|treats? (the )?disease)"), "medical or cure claims are not allowed (ФЗ «О рекламе» ст. 5, 24, 25)"),
    ("guaranteed_result", w(r"(100\s?% (результат|эффект|гарантия)|гарантированн\w+ (результат|эффект)|guaranteed results?)"), "guaranteed results cannot be promised"),
    ("blame_logistics", re.compile(L + r"(виноват\w*|вина)\s+(\w+\s+){0,3}(склад\w*|доставк\w*|курьер\w*|пвз|маркетплейс\w*)|(склад|доставка|курьер|пвз)\s+(\w+\s+){0,2}(виноват\w*|испортил\w*|повредил\w*)", re.I | re.U), "do not blame the warehouse, delivery or marketplace in public; say what you will check"),
    ("placeholder", re.compile(r"\[(уточнить|todo|tbd|имя|name)[^\]]*\]|\{\{|\}\}", re.I), "unfilled placeholder: get the fact from a human before publishing"),
]
WARN = [
    ("stock_phrase", re.compile(r"(ваш (отзыв|мнение) (очень )?важ(ен|но) для нас|спасибо за (ваш )?отзыв[.!]?\s*$|приносим извинения за доставленные неудобства|your feedback is important to us)", re.I | re.M), "stock phrase: say something specific to this review"),
    ("caps", re.compile(r"\b[А-ЯЁA-Z]{6,}\b"), "words in CAPS read as shouting"),
    ("emoji", re.compile(r"[\U0001F300-\U0001FAFF☀-➿]{3,}"), "three or more emoji in a row"),
    ("exclaim", re.compile(r"!{2,}|\?{2,}"), "repeated punctuation"),
]
LIMITS = {("wb", "review"): (2, 5000), ("wb", "question"): (2, 5000), ("wb", "chat"): (1, 1000), ("wb", "claim"): (10, 1000),
          ("ozon", "review"): (2, 3000), ("ozon", "question"): (2, 3000), ("ozon", "chat"): (1, 1000)}
STYLE_MAX = {"review": 900, "question": 600, "chat": 700, "claim": 1000}


def check(text, platform, kind, allow_platform_name=True):
    issues = []
    for code, rx, why in BLOCK:
        m = rx.search(text)
        if not m:
            continue
        if code == "other_platform" and allow_platform_name:
            names = {"wb": r"(вайлдберриз|wildberries|вб|wb)", "ozon": r"(озон|ozon)"}
            if re.fullmatch(names[platform], m.group(1) or m.group(0), re.I):
                continue
        issues.append({"level": "block", "code": code, "match": m.group(0)[:60], "why": why})
    for code, rx, why in WARN:
        m = rx.search(text)
        if m:
            issues.append({"level": "warn", "code": code, "match": m.group(0)[:60], "why": why})
    lo, hi = LIMITS.get((platform, kind), (1, 5000))
    n = len(text.strip())
    if n < lo or n > hi:
        issues.append({"level": "block", "code": "length", "match": str(n), "why": f"{n} characters; the platform allows {lo}–{hi}"})
    elif n > STYLE_MAX.get(kind, 900):
        issues.append({"level": "warn", "code": "length", "match": str(n), "why": f"{n} characters; aim for 2–5 sentences (≤{STYLE_MAX.get(kind)})"})
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?"); ap.add_argument("--file")
    ap.add_argument("--platform", choices=["wb", "ozon"], required=True)
    ap.add_argument("--kind", choices=["review", "question", "chat", "claim"], default="review")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.file).read_text(encoding="utf-8")) if a.file else [{"id": "1", "text": a.text or sys.stdin.read()}]
    out, blocked = [], 0
    for it in items:
        iss = check(it["text"], a.platform, a.kind)
        if any(i["level"] == "block" for i in iss):
            blocked += 1
        out.append({"id": it.get("id"), "ok": not any(i["level"] == "block" for i in iss), "issues": iss})
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for o in out:
            print(f"{'✓' if o['ok'] else '✗'} {o['id']}")
            for i in o["issues"]:
                print(f"   {'BLOCK' if i['level'] == 'block' else 'warn '} {i['code']}: «{i['match']}» — {i['why']}")
        print(f"\n{len(out) - blocked} of {len(out)} ready for human approval")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
