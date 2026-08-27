# fda-safety-signals — standing instructions

**Layers covered:** Regulatory + Clinical (safety, risk).
**Anchor plugin for openFDA.** If a hosted openFDA MCP server is ever adopted, declare
it HERE. `ip-exclusivity` reaches the Orange Book endpoint by co-install and must not
re-declare it.

## What this engine is for

Detecting, sizing and timing post-market safety and regulatory-rejection risk from
free FDA data — the evidence base for safety-driven shorts, label-change monitors and
catalyst invalidation.

## The caveat that governs everything here

**Spontaneous reporting systems measure reporting, not incidence.**

FAERS and MAUDE are voluntary, duplicated, stimulated by litigation and media, and
missing a denominator. There is no exposure figure in either database, so no rate can
be computed from them. Disproportionality statistics compare a drug's reporting
pattern to the rest of the database — they are a *screening* tool that says "look
here", never a causal or quantitative finding.

Consequences you must carry into every brief:

- **Notoriety bias.** Publicity about a possible association generates reports of that
  association. A signal that emerges the month after a journal paper or a plaintiff-firm
  advertising campaign is partly an artefact of the coverage.
- **Indication confounding.** The event may belong to the disease, not the drug.
  Always name a comparator treated for the same indication rather than comparing to
  the whole database when the class allows it.
- **Under-reporting.** A commonly cited estimate is that under 10% of adverse events
  are reported. Absolute counts are floors, not levels.
- **Deduplication.** The same case reaches FAERS through multiple routes. Counts are
  reports, not patients.

A brief that reports a PRR without naming the comparator, the time window and the
notoriety risk is incomplete and should not be sent to the capstone.

## Rate limits

api.fda.gov: without a key, 240 requests/minute and 1,000/day per IP; with a free key,
240/minute and 120,000/day per key. Set `OPENFDA_API_KEY` in the environment. Bulk
zipped-JSON downloads exist for large historical work — use them rather than paging
the API for anything spanning years.

## Chaining

a catalyst engine → readout-handicap and adcom-label (a safety signal changes the
handicap on a label expansion) · a procedure-exposure engine (device revenue at risk) ·
`ip-exclusivity` (Orange Book via the shared connector) · your view layer →
thesis and sell-discipline.
## Connector

Declares **`fda`** (`openpharma-org/fda-mcp`) — this plugin is the openFDA anchor. The
server also carries Orange Book and Purple Book, so `ip-exclusivity` consumes this
session rather than declaring anything of its own.

`OPENFDA_API_KEY` is optional and raises the ceiling from 1,000 to 120,000
requests/day. Disproportionality work burns quota fast — a single PRR screen across a
drug class is hundreds of calls — so get the key.

**Caveat that must reach the brief:** FAERS is refreshed quarterly and lags three
months or more. A signal absent from the current API is not a signal that does not
exist; it may simply not have been published yet. Say which quarter you queried.

## Standard of evidence

This engine is built to **institutional investor standards: rigorous and auditable.**
That is a claim about specific mechanisms, and the full list is in
`references/auditability.md`. The load-bearing ones:

- Every finding carries a source, a retrieval date and the **vintage of the underlying
  data** — a different and usually much earlier date.
- Confidence is gated by vintage, not by conviction.
- Scripts fail loudly on empty result sets. Silence is never a negative finding.
- Known limitations travel with the number, in-line, not in a footnote.
- Evidence and view stay separated. This engine does not issue recommendations.

## Desk conventions (all engines)

- **One connector, one plugin — for plugin-level servers only.** A self-hosted
  stdio server is declared in exactly one plugin's `.mcp.json`; co-installed
  plugins share every server session-wide, so a second declaration buys a
  duplicate process, not extra capability. **Account-level hosted connectors are
  different**: CMS Coverage, PopHIVE, ClinicalTrials.gov, PubMed, ChEMBL,
  bioRxiv and Scholar Gateway are connected once in the directory and are visible
  to every plugin. Plugins reference those; they never declare or own them.
  Full map in `references/mcp-setup.md`.
- **MCP for the analyst, scripts for the watcher.** Both paths ship in every
  plugin and they are not redundant. Interactive query refinement goes through
  the server; unattended scheduled evidence goes through the script, because a
  watcher has to be deterministic and re-runnable against the same vintage.
  Where the two disagree, the script wins for anything entering a brief — you
  cannot cite the internals of a third-party server.
- **Engines produce evidence, not views.** An engine skill ends at the brief. The
  your view layer is the only place a position
  is argued. Do not write a recommendation into an engine output.
- **Open data only.** Every input here is free and public. If an analysis needs
  IQVIA, Symphony, Definitive, EvaluatePharma or Citeline, say so and stop — do
  not silently substitute a proxy for the paid panel and present it as equivalent.
- **Cite the vintage every time.** See `references/evidence-brief.md`.
- **Chain, don't duplicate.** These eight engines cross-reference each other by
  name. Anything outside them — valuation models, single-name research, the
  portfolio view layer — is chained into, never reimplemented here. An engine
  that starts doing valuation has stopped being an engine.
- **Scripts are stdlib-only Python 3.** No pip installs. Every script takes
  `--help`, prints JSON or CSV to stdout, and fails loudly on an empty result set
  rather than returning silence that reads like a negative finding.
