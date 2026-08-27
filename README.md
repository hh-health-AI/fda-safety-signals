# fda-safety-signals

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
