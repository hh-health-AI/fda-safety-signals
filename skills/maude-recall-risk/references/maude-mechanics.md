# MAUDE mechanics and device recall reading

## What is in the database

Medical Device Reports from three streams with very different behaviour:

- **Manufacturer reports** — mandatory, the bulk of volume, filed on a deadline.
- **Importer reports** — mandatory, smaller.
- **Voluntary reports** — clinicians, patients, hospitals; low volume, high signal
  quality when they describe a novel failure mode.

Also present: summary reporting programmes (alternative summary reporting historically
hid large volumes of well-known malfunctions; FDA has since moved these into the
public voluntary malfunction summary reporting programme). A step change in a series
is often a change in **reporting programme**, not in device behaviour. Check the FDA
programme history before writing up a step change.

## Recall classes

- **Class I** — reasonable probability of serious adverse health consequences or death.
  The class that moves revenue and triggers hospital switching.
- **Class II** — temporary or medically reversible consequences. Common; usually not
  thesis-changing on its own, but a cluster of them at one plant is.
- **Class III** — unlikely to cause adverse consequences. Mostly labelling.

Note that a "recall" in FDA terms frequently means a correction or a field safety
notice, not a physical return. Read the enforcement record's action description before
assuming units came off the market.

## Pathway risk

- **510(k)** — cleared on substantial equivalence to a predicate. Fast, cheap, and
  carries predicate-chain risk: if a predicate was itself recalled, the descendants
  inherit scrutiny.
- **De Novo** — for novel low-to-moderate risk devices with no predicate; creates a
  new classification others can then use as a predicate.
- **PMA** — full premarket approval with clinical evidence; slower, and supplements
  are needed for design changes.

Published analysis (JAMA Network Open, 2021, among others) has found higher recall
rates among 510(k)-cleared devices than PMA-approved ones. Treat pathway as a prior on
recall risk, not as a prediction.

## Leading indicators worth monitoring

1. Repeat Form 483 observations at the manufacturing site.
2. A warning letter naming design controls or CAPA.
3. Import alerts on a foreign plant.
4. A competitor's Class I recall in the same product code — hospitals re-evaluate the
   whole category, which can be an opportunity as often as a risk.
5. Rising malfunction reports with stable procedure volume disclosed on calls.
