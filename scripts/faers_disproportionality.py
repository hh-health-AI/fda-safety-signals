#!/usr/bin/env python3
"""FAERS disproportionality: PRR, ROR (95% CI), chi-square (Yates), Evans criteria.

Stdlib only. Builds the 2x2 from openFDA /drug/event total counts.

Example
-------
    python3 faers_disproportionality.py \
        --drug semaglutide \
        --comparator-drugs liraglutide dulaglutide tirzepatide \
        --events "PANCREATITIS" "PANCREATITIS ACUTE" \
        --from 2020-01-01 --to 2026-06-30

If --comparator-drugs is omitted the comparator is the whole database for the same
window. That confounds the indication and is usually the WRONG comparator for an
investment question -- the script will warn you.

Reports counts, not patients. No incidence, risk or causality can be inferred.
"""
import argparse, datetime, json, math, os, sys, time, urllib.error, urllib.parse, urllib.request

from _ua import user_agent

BASE = "https://api.fda.gov/drug/event.json"


def total(search):
    params = {"search": search, "limit": "1"}
    key = os.environ.get("OPENFDA_API_KEY")
    if key:
        params["api_key"] = key
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={**user_agent("faers-disproportionality")})
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode("utf-8"))
            return int(d.get("meta", {}).get("results", {}).get("total", 0))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 0
            if e.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(2 ** attempt); continue
            raise
    return 0


def drug_clause(names):
    inner = " OR ".join(f'patient.drug.openfda.generic_name:"{n}"' for n in names)
    return f"({inner})"


def event_clause(events):
    inner = " OR ".join(f'patient.reaction.reactionmeddrapt:"{e}"' for e in events)
    return f"({inner})"


def date_clause(d_from, d_to):
    f = d_from.replace("-", "")
    t = d_to.replace("-", "")
    return f"receivedate:[{f}+TO+{t}]"


def stats(a, b, c, d):
    out = {"a": a, "b": b, "c": c, "d": d}
    if min(a, b, c, d) <= 0:
        out["note"] = ("A zero cell makes the frequentist estimates unstable or "
                       "undefined. Report the raw counts and stop; do not present a "
                       "ratio computed on a zero cell.")
        return out
    prr = (a / (a + b)) / (c / (c + d))
    ror = (a * d) / (b * c)
    se = math.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    lo, hi = math.exp(math.log(ror) - 1.96 * se), math.exp(math.log(ror) + 1.96 * se)
    n = a + b + c + d
    chi2 = (n * (abs(a * d - b * c) - n / 2) ** 2) / ((a + b) * (c + d) * (a + c) * (b + d))
    out.update({
        "PRR": round(prr, 3),
        "ROR": round(ror, 3),
        "ROR_95CI": [round(lo, 3), round(hi, 3)],
        "chi2_yates": round(chi2, 2),
        "evans_criteria_met": bool(a >= 3 and prr >= 2 and chi2 >= 4),
        "evans_detail": {"a>=3": a >= 3, "PRR>=2": prr >= 2, "chi2>=4": chi2 >= 4},
    })
    if a < 10:
        out["stability_warning"] = ("Fewer than 10 cases in cell a. Frequentist "
                                    "disproportionality is unstable here; a Bayesian "
                                    "shrinkage estimate (IC / EBGM) would be lower. "
                                    "Do not headline the PRR.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drug", required=True, help="generic name of the drug of interest")
    ap.add_argument("--events", required=True, nargs="+", help="MedDRA preferred term(s)")
    ap.add_argument("--comparator-drugs", nargs="*", default=[],
                    help="generic names forming the comparator group")
    ap.add_argument("--from", dest="d_from", default="2015-01-01")
    ap.add_argument("--to", dest="d_to",
                    default=datetime.date.today().isoformat())
    a = ap.parse_args()

    dc = date_clause(a.d_from, a.d_to)
    drug = drug_clause([a.drug])
    ev = event_clause(a.events)

    a_ct = total(f"{drug} AND {ev} AND {dc}")
    drug_all = total(f"{drug} AND {dc}")
    b_ct = drug_all - a_ct

    if a.comparator_drugs:
        comp = drug_clause(a.comparator_drugs)
        c_ct = total(f"{comp} AND {ev} AND {dc}")
        comp_all = total(f"{comp} AND {dc}")
        comparator_desc = "named comparator drugs: " + ", ".join(a.comparator_drugs)
    else:
        all_ev = total(f"{ev} AND {dc}")
        all_rep = total(dc)
        c_ct = all_ev - a_ct
        comp_all = all_rep - drug_all
        comparator_desc = ("WHOLE DATABASE -- confounded by indication. Prefer a "
                           "same-class or same-indication comparator for any "
                           "investment conclusion.")
    d_ct = comp_all - c_ct

    res = {
        "drug": a.drug,
        "events": a.events,
        "window": {"from": a.d_from, "to": a.d_to},
        "comparator": comparator_desc,
        "extracted": datetime.date.today().isoformat(),
        "statistics": stats(a_ct, b_ct, c_ct, d_ct),
        "mandatory_caveats": [
            "FAERS counts reports, not patients, and has no exposure denominator: no "
            "incidence or risk can be computed.",
            "Voluntary reporting is subject to notoriety bias -- check whether the rise "
            "begins after publicity, an FDA communication or litigation advertising.",
            "Duplicates are present; deduplication was not attempted by this script.",
            "Disproportionality is a screening signal, never evidence of causality.",
            "Report per READUS-PV (Drug Safety 2024): database, extraction date, window, "
            "comparator, full event term list, and the raw 2x2.",
        ],
    }
    json.dump(res, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
