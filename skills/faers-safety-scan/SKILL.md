---
name: faers-safety-scan
description: >
  This skill should be used when the user asks about "FAERS", "adverse event signal",
  "disproportionality", "PRR", "ROR", "safety short", "is there a signal on [drug]",
  "boxed warning risk", "label change risk", or wants to screen post-market safety
  reporting for a marketed drug against a comparator.
metadata:
  version: "0.1.0"
  layer: "Regulatory"
---

# FAERS safety scan

Screen a marketed drug's adverse-event reporting for disproportionate signals, size
the commercial exposure if the signal escalates, and be explicit that this is a
screen rather than a finding.

## Workflow

1. **Define the comparator before you pull anything.** The default of "all other
   drugs in FAERS" is almost always the wrong comparator for an investment question,
   because it confounds the indication. Prefer: other drugs in the same class, or
   drugs treating the same indication. State the comparator in the brief.
2. **Define the event term precisely.** MedDRA preferred terms are narrow. A "liver
   injury" question needs a term list (hepatotoxicity, hepatic failure, ALT increased,
   jaundice, drug-induced liver injury), not one term. Run the list, report per-term
   and aggregated, and show the list in the output.
3. **Set a time window and hold it constant** across drug and comparator. Reporting
   volume grows secularly, so an unwindowed comparison favours older drugs.
4. **Run `scripts/faers_disproportionality.py`.** It builds the 2×2 and returns PRR,
   ROR with 95% CI, chi-square with Yates correction, and the Evans criteria flag.
5. **Apply the Evans screening criteria** (a ≥ 3 cases, PRR ≥ 2, chi-square ≥ 4). All
   three, not one. A PRR of 8 on two cases is noise.
6. **Test for notoriety.** Plot reports by quarter. If the rise begins within a quarter
   of a publication, an FDA communication, a competitor's marketing campaign or
   plaintiff-firm advertising, discount it heavily and say so.
7. **Check what FDA has already done.** Search the current label (openFDA `/drug/label`)
   for the event. If it is already in Warnings and Precautions, the incremental news is
   an escalation to boxed warning or a REMS, not the signal itself — a much higher bar.
8. **Size the exposure.** Which revenue line, what share of it, and what an analogue
   label change did to comparable franchises. This is where the skill earns its keep;
   a signal with no revenue attached is not an investment.
9. Emit the brief.

## What escalation actually looks like

The path from FAERS signal to a stock-moving event is long and mostly does not
complete: signal → FDA screening (FAERS quarterly signal listing) → Drug Safety
Communication → label change → boxed warning → REMS → withdrawal. Each step is
progressively rarer. Position for the step you can name and date, not for the
end of the chain.

The FDA's own quarterly "Potential Signals of Serious Risks" listing is public and is
a far stronger signal than a home-built PRR, because it means the agency is already
looking. Check it before building your own.

## Not-automatic

A disproportionate reporting ratio does not license a causality claim, an incidence
estimate, or a forecast of regulatory action. It licenses a monitor with a named
follow-up observable.

Reference: `references/disproportionality.md`. Contract: `../../references/evidence-brief.md`.
