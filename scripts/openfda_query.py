#!/usr/bin/env python3
"""Generic openFDA client (stdlib only).

Set OPENFDA_API_KEY in the environment to raise the daily limit from 1,000 to
120,000 requests.

Examples
--------
Count reactions for a drug:
    python3 openfda_query.py --endpoint drug/event \
        --search 'patient.drug.openfda.generic_name:"semaglutide"' \
        --count patient.reaction.reactionmeddrapt.exact

Quarterly trend of device malfunction reports for a product code:
    python3 openfda_query.py --endpoint device/event \
        --search 'device.device_report_product_code:"OZO" AND event_type:"Malfunction"' \
        --count date_received

Recent Class I device recalls:
    python3 openfda_query.py --endpoint device/enforcement \
        --search 'classification:"Class I"' --limit 50

Current shortages:
    python3 openfda_query.py --endpoint drug/shortages --limit 100
"""
import argparse, json, os, sys, time, urllib.error, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://api.fda.gov"
ENDPOINTS = ["drug/event", "drug/label", "drug/ndc", "drug/enforcement", "drug/shortages",
             "drug/drugsfda", "device/event", "device/enforcement", "device/510k",
             "device/pma", "device/classification", "device/udi", "device/recall",
             "food/enforcement", "other/nsde"]


def call(endpoint, params, retries=3):
    key = os.environ.get("OPENFDA_API_KEY")
    if key:
        params = dict(params, api_key=key)
    url = f"{BASE}/{endpoint}.json?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={**user_agent("openfda-query")})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"results": [], "meta": {"results": {"total": 0}},
                        "_note": "404 from openFDA means zero matching records for this "
                                 "query. Zero records is NOT evidence of zero events -- "
                                 "check the search syntax and field names first."}
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            sys.stderr.write(f"HTTP {e.code} on {url}\n")
            raise
    return {}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--endpoint", required=True, choices=ENDPOINTS)
    ap.add_argument("--search", default=None, help="openFDA search expression")
    ap.add_argument("--count", default=None, help="field to count on (add .exact for terms)")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--skip", type=int, default=0)
    ap.add_argument("--total-only", action="store_true", help="print meta.results.total and exit")
    a = ap.parse_args()

    params = {"limit": str(min(a.limit, 1000)), "skip": str(a.skip)}
    if a.search:
        params["search"] = a.search
    if a.count:
        params["count"] = a.count
        params.pop("skip", None)

    res = call(a.endpoint, params)
    if a.total_only:
        print(res.get("meta", {}).get("results", {}).get("total", 0))
        return
    json.dump(res, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
