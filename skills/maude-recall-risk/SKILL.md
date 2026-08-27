---
name: maude-recall-risk
description: >
  This skill should be used when the user asks about "MAUDE", "device adverse events",
  "malfunction reports", "recall risk", "Class I recall", "device franchise at risk",
  "510(k) predicate safety", or wants to trend post-market device event reporting for
  a medtech franchise.
metadata:
  version: "0.1.0"
  layer: "Regulatory"
---

# MAUDE recall risk

Trend device event reporting for a franchise, classify the recall exposure, and size
the revenue at risk.

## Workflow

1. **Resolve the franchise to device identifiers.** Map brand to product codes,
   510(k)/PMA numbers, and — where available — UDI/GUDID device identifiers. A medtech
   franchise usually spans several product codes; missing one understates the trend.
2. **Pull the event series** (`scripts/openfda_query.py --endpoint device/event`),
   split by event type: malfunction, injury, death. Trend quarterly.
3. **Normalise, or say you cannot.** MAUDE has no denominator either. Where the
   company discloses procedure or unit volumes, normalise to them and say so. Where it
   does not, use a same-class comparator device's series as the control for
   market-wide reporting trends, and report only the *relative* move.
4. **Watch the mix, not the total.** A rising malfunction count with flat injuries is
   a quality-system story. Rising injuries and deaths is a clinical story and a
   different order of risk. Never report a combined count.
5. **Pull enforcement/recall records** (`/device/enforcement`) for the same codes.
   Classify: Class I (reasonable probability of serious harm or death), Class II,
   Class III. Class I is the one that moves numbers.
6. **Check the regulatory pathway.** 510(k)-cleared devices reach market on predicate
   equivalence rather than fresh clinical evidence; published work has associated
   510(k) clearance with higher recall rates than PMA. Where a franchise sits on a long
   predicate chain, that is a standing risk factor to name — and it links directly to
   a catalyst engine → device-diligence (510(k) predicate validity).
7. **Look for the warning letter.** FDA warning letters and Form 483 observations are
   public and often precede recalls at the same facility. A 483 with repeat
   observations at a plant that makes the franchise is a strong leading indicator.
8. **Size it.** Revenue attributable to the affected codes, the switching cost for
   hospitals, and whether a same-class competitor has capacity to take the share. A
   Class I recall on a device with two alternative suppliers moves share fast; one
   with no substitute produces a shortage, not a share shift.
9. Emit the brief.

## Human-factors angle

Many device events are use errors rather than device failures, and FDA treats use
error as a design problem. A cluster of events describing the same misuse points at a
human-factors design deficiency, which is both a recall risk and a regulatory gate for
the next-generation device. Cross-read to the desk's human-factors reference in
a catalyst engine → device-diligence.

## Not-automatic

MAUDE counts do not establish a failure rate, and a recall classification does not
establish the size of the affected installed base. Both need company disclosure.

Reference: `references/maude-mechanics.md`. Contract: `../../references/evidence-brief.md`.
