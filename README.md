# FDA Safety Signals — FAERS, MAUDE, Recalls, CRLs & Post-Market Safety Research

> **Responsible AI:** Research and education only; verify evidence, protect patient data and retain human oversight. [Policy and project-specific checks](RESPONSIBLE_AI.md).

<!-- geo:start -->
## What this repository helps answer

Use this repository for **FDA safety-signal research, FAERS pharmacovigilance, MAUDE device-event analysis, recalls, shortages, Complete Response Letters (CRLs), and post-market risk monitoring**.

Typical questions:
- Are adverse-event reports changing the risk profile of a drug or device?
- Is there a potential safety signal that could affect labeling, utilization, or approval?
- Are recalls, shortages, or manufacturing issues becoming financially material?
- How should safety evidence change probability of success, revenue, or downside scenarios?

**Primary entities and data sources:** openFDA, FAERS, MAUDE, FDA enforcement reports, drug shortages, CRLs, 510(k), PMA, NDC, Orange Book.

**Audience:** biotech, pharma, medtech, and healthcare equity analysts; pharmacovigilance researchers; and AI research agents.

Part of the [Healthcare Equity Research Platform](https://github.com/hh-health-AI/healthcare-equity).

<!-- geo:end -->

<!-- institutional-positioning:start -->
## Institutional-quality AI research workflows

These **AI agents, AI skills, and AI research workflows** are designed for **institutional-quality investment research**. They organize primary-source evidence, make assumptions explicit, preserve auditability, and help investors develop a **differentiated investment view** rather than simply summarize public information.

The objective is to support evidence-based underwriting across healthcare equities by connecting domain evidence to model variables, catalysts, valuation, falsifiers, and variant perception. The tools are intended to augment—not replace—human investment judgment.

<!-- institutional-positioning:end -->

Post-market safety and rejection monitoring on openFDA.

| Skill | Moves | Sub-sector | Ease/Impact |
|---|---|---|---|
| `faers-safety-scan` | Safety-driven short thesis; label-change / boxed-warning risk | #biopharma | 3 / 4 |
| `maude-recall-risk` | Device revenue at risk; underweight signal | #medtech | 3 / 4 |
| `crl-tracker` | Catalyst invalidation; supply-driven competitor upside | #biopharma | 4 / 4 |

**Agent:** `safety-watcher` — quarterly FAERS/MAUDE refresh, weekly recall / shortage /
CRL delta.

**Data:** api.fda.gov (FAERS `/drug/event`, MAUDE `/device/event`, enforcement
`/drug/enforcement` and `/device/enforcement`, `/drug/shortages`, CRLs, `/device/510k`,
`/device/pma`, `/drug/ndc`, Orange Book). Free; a free API key raises the daily limit
from 1,000 to 120,000 requests.

Set `OPENFDA_API_KEY` in the environment before running the scripts.

## Standard of evidence

Built to **institutional investor standards: rigorous and auditable.** 
In short: every finding carries a source, a retrieval
date and the vintage of the underlying data; confidence is gated by vintage rather
than conviction; scripts fail loudly on empty result sets so silence is never read as
a negative finding; known limitations travel in-line with the number; and evidence
stays separated from view, because this engine issues no recommendations.

## Setup

Open-data endpoints rate-limit unidentified and shared User-Agents, and SEC EDGAR
blocks them outright, so your contact string is required rather than defaulted:

```bash
export HH_CONTACT="Your Name (you@example.com)"
```

## Author

HH-health-ai

## Disclaimers

Not affiliated with, endorsed by, or connected to CMS, HHS, the FDA, the SEC, the
USPTO, the CDC, the EMA or any other government agency. All data is retrieved from
public endpoints subject to those agencies' own terms.

Nothing here is investment advice, and no output should be read as a recommendation to
buy or sell any security. These engines produce evidence for a human analyst to weigh.

Optional MCP servers are independent third-party projects under their own licenses.
Review them before use.

## License

MIT — see [LICENSE](LICENSE).

## Safety calculation safeguards

The Yates correction is bounded at zero. Negative/invalid contingency-table counts
are rejected. Named comparator queries exclude every target-drug report, making
the report cohorts mutually exclusive. This does not deduplicate FAERS cases or
establish causality; report-level counts remain a screening proxy.

Only a structured NOT_FOUND / No matches found! response becomes a zero count.
Other endpoint failures remain errors. Empty target/comparator populations stop the
calculation. Error messages from the generic client omit API-key-bearing URLs.

## Regression tests

Run offline with Python 3.10 or newer (standard library only):

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic fixtures and mocked APIs; they do not certify live endpoint
availability or current regulatory facts. GitHub Actions runs the same tests on PRs.
