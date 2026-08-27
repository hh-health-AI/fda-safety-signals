---
name: crl-tracker
description: >
  This skill should be used when the user asks about "complete response letter",
  "CRL", "why was it rejected", "refuse to file", "drug shortage", "supply
  disruption", "who benefits from the shortage", or wants to monitor FDA rejection
  and supply events across the coverage universe.
metadata:
  version: "0.1.0"
  layer: "Regulatory"
---

# CRL and shortage tracker

Monitor two event streams that invalidate catalysts and create competitor upside:
FDA Complete Response Letters, and drug shortages.

## Complete Response Letters

FDA began publishing CRLs in 2025, so the corpus is shallow and skewed to recent and
historical batch releases. **The absence of a CRL in the dataset is not evidence that
no CRL was issued** — this is the single most important caveat and belongs in every
brief from this skill.

Workflow:

1. Pull recent CRL publications and filter to the coverage universe and to competitors.
2. Classify the deficiency. The classification is what carries the read-across:
   - **CMC / manufacturing** — often resolvable in 6–12 months with a Class 2 resubmission;
     third-party manufacturing sites can affect several sponsors at once, so check who
     else uses the plant.
   - **Clinical / efficacy** — usually requires a new trial. Reset the timeline by
     years, not quarters, and re-run the probability of success.
   - **Safety** — may be fatal to the programme in that indication.
   - **Inspection-related** — a foreign site classified OAI. Look for other sponsors
     with products at the same site; this is where the cross-read money is.
3. Read across to the class. A CRL citing a mechanism-level safety concern raises the
   bar for every competitor with the same mechanism; a CMC CRL says nothing about them.
4. Hand the timeline reset to a catalyst engine → catalyst-calendar, and the
   probability revision to `readout-handicap`.

## Drug shortages

1. Pull `/drug/shortages` and filter to molecules where the coverage universe has an
   approved or filed product.
2. Classify the cause where stated: manufacturing quality, demand increase,
   discontinuation, raw-material supply.
3. Identify the beneficiary. A shortage of a sole-source injectable transfers volume
   to whoever has capacity, and the transfer often persists after resolution because
   hospital contracts are sticky.
4. Watch the flip side: a shortage caused by the covered name's own quality problem is
   a revenue hole plus a warning-letter risk. Cross-check `/drug/enforcement` and the
   FDA warning-letter database for the same site.

## Not-automatic

A published CRL does not license a conclusion about resubmission timing unless the
letter itself states the deficiency type; a shortage listing does not license a market-
share conclusion without capacity evidence from the beneficiary's disclosures.

Contract: `../../references/evidence-brief.md`.
