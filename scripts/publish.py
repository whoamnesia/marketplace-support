#!/usr/bin/env python3
"""astudio-marketplace-support · publish.py — publish replies a HUMAN has approved.

  python3 publish.py approved.json            # dry run: shows exactly what would be sent
  python3 publish.py approved.json --yes      # sends, one by one

approved.json: [{"id": "...", "platform": "wb|ozon", "kind": "review|question", "text": "...",
                 "sku": 123 (Ozon questions), "approved": true, "approved_by": "Имя"}]
Rules enforced here, not only in the prompt:
- an item without "approved": true and "approved_by" is skipped;
- every text passes reply_check.py again (a human edit can add a problem);
- WB: 1 request per second for the category (1.1 s pause); answers can be edited only once in 60 days;
- Ozon: there is no edit method, only delete and create again;
- nothing is sent without --yes. Tokens: WB_TOKEN (Feedbacks and Questions, not read-only),
  OZON_CLIENT_ID + OZON_API_KEY. Endpoints per platform docs as of 2026-11; re-check on failure.
"""
import argparse, json, os, sys, time, pathlib, urllib.request, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reply_check import check  # noqa: E402

def req(method, url, headers, body):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), method=method, headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")[:300]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")[:300]

def plan(it):
    if it["platform"] == "wb":
        h = {"Authorization": os.environ.get("WB_TOKEN", "")}; b = "https://feedbacks-api.wildberries.ru"
        if it["kind"] == "review":
            return "POST", f"{b}/api/v1/feedbacks/answer", h, {"id": it["id"], "text": it["text"]}
        return "PATCH", f"{b}/api/v1/questions", h, {"id": it["id"], "answer": {"text": it["text"]}, "state": "wbRu"}
    h = {"Client-Id": os.environ.get("OZON_CLIENT_ID", ""), "Api-Key": os.environ.get("OZON_API_KEY", "")}; b = "https://api-seller.ozon.ru"
    if it["kind"] == "review":
        return "POST", f"{b}/v1/review/comment/create", h, {"review_id": it["id"], "text": it["text"], "mark_review_as_processed": True}
    return "POST", f"{b}/v1/question/answer/create", h, {"question_id": it["id"], "sku": it.get("sku"), "text": it["text"]}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file"); ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    items = json.loads(pathlib.Path(a.file).read_text(encoding="utf-8"))
    sent = skipped = 0
    for it in items:
        if not (it.get("approved") is True and it.get("approved_by")):
            print(f"skip {it.get('id')}: not approved by a named person"); skipped += 1; continue
        bad = [i for i in check(it["text"], it["platform"], it["kind"]) if i["level"] == "block"]
        if bad:
            print(f"skip {it['id']}: " + "; ".join(f"{i['code']} «{i['match']}»" for i in bad)); skipped += 1; continue
        if it["platform"] == "ozon" and it["kind"] == "question" and not it.get("sku"):
            print(f"skip {it['id']}: Ozon question answers need sku"); skipped += 1; continue
        m, url, h, body = plan(it)
        if not a.yes:
            print(f"DRY {m} {url}\n    {json.dumps(body, ensure_ascii=False)}"); continue
        code, resp = req(m, url, h, body)
        print(f"{'✓' if code < 300 else '✗'} {it['id']} HTTP {code} {'' if code < 300 else resp}")
        sent += code < 300
        if it["platform"] == "wb": time.sleep(1.1)
    print(f"\nsent {sent}, skipped {skipped}" + ("" if a.yes else " — dry run, add --yes after the human confirms"))
    print("Check the answers in the seller account after publishing.")

if __name__ == "__main__":
    main()
