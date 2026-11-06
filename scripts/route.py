#!/usr/bin/env python3
"""astudio-marketplace-support · route.py — deterministic triage of reviews / questions / chats.

  python3 route.py queue.json            # [{"id","platform","kind","rating","text","product","sku"}, ...]
  python3 route.py queue.json --json

Every item gets: type (thanks / neutral / critique / harsh / suspected_fake / spam / question),
route (draft = agent drafts for approval, human = a person decides before any reply),
priority P1–P4, and the rule that fired. A model asked to "answer the buyer" finds it hard not to
answer; these rules decide first. Also reports repeated issues per product (≥3 = product problem).
"""
import argparse, json, re, sys, pathlib
from collections import Counter, defaultdict

L, R = r"(?<![а-яёa-z])", r"(?![а-яёa-z])"
def rx(p): return re.compile(L + p, re.I | re.U)

HUMAN_RULES = [
    ("health_safety", rx(r"(аллерг|ожог|отравл|сып[ья]|травм|порезал|загорел|задымил|искрит|удар(ило)? током|взорвал|больниц|врач|дерматит|зуд)"), "P1", "health or safety harm: a person answers and checks the batch"),
    ("counterfeit", rx(r"(подделк|фейк|контрафакт|не оригинал|неоригинал|паль|копия бренда|китайская копия)"), "P2", "counterfeit claim: needs documents and a person"),
    ("legal_threat", rx(r"(роспотребнадзор|суд|прокуратур|претензи|юрист|адвокат|заявлени\w* в полиц|жалоб\w* в)"), "P1", "legal threat: a person decides"),
    ("money_dispute", rx(r"(верните деньги|возврат денег|деньги не (вернули|пришли)|списали дважды|не вернули|отказали в возврате|возврат не принимают|компенсац)"), "P2", "money or return dispute: only a person may promise money"),
    ("wrong_item", rx(r"(пришл\w* не (тот|та|то)|другой (товар|цвет|размер)|пуст\w* коробк|недоложил|некомплект|не хватает)"), "P2", "wrong or incomplete item: check the order before replying"),
    ("damaged", rx(r"(брак|сломан|разбит|трещин|не работает|не включается|порван|протек|бракован)"), "P3", "defect: reply with the procedure; a person checks repeats"),
]
FAKE = rx(r"(конкурент|заказной отзыв|купите лучше у|у других дешевле|ссылк[аи] в профиле)")
SPAM = re.compile(r"https?://|@[a-z0-9_]{4,}|t\.me/", re.I)
QUESTION = re.compile(r"\?\s*$|^(подскажите|скажите|а есть|какой|какая|какие|сколько|можно ли|будет ли)", re.I | re.M)


def classify(it):
    text = (it.get("text") or "").strip()
    rating = it.get("rating")
    kind = it.get("kind", "review")
    for code, r, prio, why in HUMAN_RULES:
        if r.search(text):
            t = "harsh" if (rating or 5) <= 2 else "critique"
            route = "human" if code != "damaged" or (rating or 5) <= 2 else "draft"
            return {"type": t, "route": route, "priority": prio, "rule": code, "why": why}
    if SPAM.search(text):
        return {"type": "spam", "route": "human", "priority": "P4", "rule": "spam", "why": "links or handles: consider a complaint, not a reply"}
    if FAKE.search(text):
        return {"type": "suspected_fake", "route": "human", "priority": "P3", "rule": "fake", "why": "possible competitor review: file a complaint with evidence, do not argue in public"}
    if kind in ("question", "chat") or (kind == "review" and QUESTION.search(text) and rating is None):
        return {"type": "question", "route": "draft", "priority": "P3", "rule": "question", "why": "answer from the card and fact sheet; [уточнить] what is missing"}
    if rating is None:
        return {"type": "neutral", "route": "draft", "priority": "P4", "rule": "default", "why": "no rating"}
    if rating <= 2:
        return {"type": "harsh" if len(text) > 0 else "neutral", "route": "human" if not text else "draft", "priority": "P2", "rule": "low_rating", "why": "1–2★: draft carefully; a person approves" if text else "1–2★ without text: a short reply, a person approves"}
    if rating == 3:
        return {"type": "critique", "route": "draft", "priority": "P3", "rule": "mid_rating", "why": "3★: find what went wrong"}
    return {"type": "thanks" if text else "neutral", "route": "draft", "priority": "P4", "rule": "positive", "why": "4–5★: thank with a specific detail"}


THEMES = {"размер": r"(маломер|большемер|размер)", "качество": r"(брак|сломал|порвал|не работает|трещин)", "упаковка": r"(упаковк|помят|коробк)",
          "описание": r"(не соответств|на фото|в описании|не как на)", "запах": r"(запах|воняет)", "комплект": r"(некомплект|не хватает|пришл\w* не)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.file).read_text(encoding="utf-8"))
    rows, per_product = [], defaultdict(Counter)
    for it in items:
        c = classify(it); rows.append({**{k: it.get(k) for k in ("id", "platform", "kind", "rating", "product")}, **c})
        for theme, p in THEMES.items():
            if re.search(p, it.get("text") or "", re.I):
                per_product[it.get("product") or it.get("sku") or "?"][theme] += 1
    repeats = [{"product": p, "theme": t, "count": n} for p, c in per_product.items() for t, n in c.items() if n >= 3]
    order = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
    rows.sort(key=lambda r: order[r["priority"]])
    if a.json:
        print(json.dumps({"items": rows, "repeated_issues": repeats}, ensure_ascii=False, indent=2)); return 0
    print("| # | id | ★ | type | route | priority | why |\n|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['id']} | {r['rating'] if r['rating'] is not None else '–'} | {r['type']} | {r['route']} | {r['priority']} | {r['why']} |")
    print(f"\nto a person: {sum(r['route'] == 'human' for r in rows)} · agent drafts for approval: {sum(r['route'] == 'draft' for r in rows)}")
    if repeats:
        print("\nRepeated issues (≥3 on one product: fix the product or the card, not only the replies):")
        for x in repeats: print(f"- {x['product']}: {x['theme']} × {x['count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
