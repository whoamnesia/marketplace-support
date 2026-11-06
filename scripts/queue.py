#!/usr/bin/env python3
"""astudio-marketplace-support · queue.py — READ-ONLY: fetch unanswered reviews and questions.

  WB_TOKEN=... python3 queue.py wb --limit 100 > queue.json
  OZON_CLIENT_ID=... OZON_API_KEY=... python3 queue.py ozon --limit 100 > queue.json

Output is the list route.py expects. Only read methods are called (WB GET feedbacks/questions,
Ozon POST list methods that change nothing). Publishing is a separate, human-approved step:
this plugin never posts on its own. Tokens come from environment variables and are never printed.
WB: one request per second for the whole Feedbacks and Questions category — the script waits 1.1 s
between calls. Ozon: a 403 means the subscription is missing («Управление отзывами» / Premium Pro
for reviews, Premium Plus for questions), not a broken integration.
Endpoints per dev.wildberries.ru and docs.ozon.ru as of 2026-11; re-check them if a call fails.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

def call(method, url, headers, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        hint = {401: "token invalid or expired (WB tokens live 180 days)", 403: "no access: wrong token category or missing subscription", 429: "rate limit: wait and retry later"}.get(e.code, "")
        sys.exit(f"HTTP {e.code} on {url.split('?')[0]}: {hint}")

def wb(limit):
    tok = os.environ.get("WB_TOKEN") or sys.exit("set WB_TOKEN (category: Feedbacks and Questions; read-only is enough)")
    h, base, out = {"Authorization": tok}, "https://feedbacks-api.wildberries.ru", []
    fb = call("GET", f"{base}/api/v1/feedbacks?isAnswered=false&take={limit}&skip=0&order=dateDesc", h)
    for f in (fb.get("data") or {}).get("feedbacks", []):
        text = " ".join(x for x in [f.get("text"), ("Плюсы: " + f["pros"]) if f.get("pros") else "", ("Минусы: " + f["cons"]) if f.get("cons") else ""] if x)
        pd = f.get("productDetails") or {}
        out.append({"id": f.get("id"), "platform": "wb", "kind": "review", "rating": f.get("productValuation"), "text": text,
                    "product": pd.get("productName"), "sku": pd.get("nmId"), "date": f.get("createdDate"), "name": f.get("userName")})
    time.sleep(1.1)
    qs = call("GET", f"{base}/api/v1/questions?isAnswered=false&take={limit}&skip=0&order=dateDesc", h)
    for q in (qs.get("data") or {}).get("questions", []):
        pd = q.get("productDetails") or {}
        out.append({"id": q.get("id"), "platform": "wb", "kind": "question", "rating": None, "text": q.get("text"),
                    "product": pd.get("productName"), "sku": pd.get("nmId"), "date": q.get("createdDate")})
    return out

def ozon(limit):
    cid, key = os.environ.get("OZON_CLIENT_ID"), os.environ.get("OZON_API_KEY")
    if not (cid and key): sys.exit("set OZON_CLIENT_ID and OZON_API_KEY")
    h, base, out = {"Client-Id": cid, "Api-Key": key}, "https://api-seller.ozon.ru", []
    rv = call("POST", f"{base}/v2/review/list", h, {"limit": min(max(limit, 20), 100), "sort_dir": "DESC", "status": "UNPROCESSED"})
    for r in rv.get("reviews", []):
        out.append({"id": r.get("id"), "platform": "ozon", "kind": "review", "rating": r.get("rating"), "text": r.get("text"),
                    "product": None, "sku": r.get("sku"), "date": r.get("published_at")})
    qs = call("POST", f"{base}/v1/question/list", h, {"filter": {"status": "NEW"}, "last_id": ""})
    for q in qs.get("questions", []):
        out.append({"id": q.get("id"), "platform": "ozon", "kind": "question", "rating": None, "text": q.get("text"),
                    "product": q.get("product_name"), "sku": q.get("sku"), "date": q.get("published_at")})
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("platform", choices=["wb", "ozon"]); ap.add_argument("--limit", type=int, default=100)
    a = ap.parse_args()
    print(json.dumps(wb(a.limit) if a.platform == "wb" else ozon(a.limit), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
