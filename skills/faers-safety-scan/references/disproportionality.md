# Disproportionality analysis — methods and reporting standards

## The 2×2

For drug D and event E across a defined FAERS window:

|             | Event E | Not E |
|-------------|---------|-------|
| Drug D      | a       | b     |
| Comparator  | c       | d     |

- **PRR** = [a/(a+b)] / [c/(c+d)] — proportional reporting ratio (MHRA tradition)
- **ROR** = (a/b)/(c/d) = ad/bc — reporting odds ratio (Netherlands/EMA tradition);
  95% CI = exp(ln ROR ± 1.96·sqrt(1/a + 1/b + 1/c + 1/d))
- **chi-square** with Yates correction on the same table
- **Evans criteria** for a signal of disproportionate reporting: a ≥ 3, PRR ≥ 2,
  chi-square ≥ 4. Treat all three as jointly necessary.

Bayesian shrinkage methods (BCPNN's IC, and the MGPS EBGM used by FDA) behave better
in sparse cells, which is exactly where naive PRR explodes. If a is small, say the
frequentist estimate is unstable rather than reporting a large PRR with a straight face.

## Reporting standard

Follow **READUS-PV** (*Drug Safety*, 2024), the reporting guideline for
disproportionality studies. The minimum a brief must state:

1. Database and version, and the exact extraction date.
2. The time window, applied identically to drug and comparator.
3. The comparator group, and why it was chosen.
4. The event definition — every MedDRA PT in the list.
5. Whether deduplication was attempted, and how.
6. The 2×2 counts themselves, not just the ratios.
7. A statement that no incidence, risk or causality can be inferred.

## Structural biases, in the order they bite

1. **Notoriety / stimulated reporting** — publicity generates reports. The single
   biggest source of false signals in a litigation-heavy market.
2. **Indication confounding (channelling)** — sicker patients get the newer drug.
3. **Masking / competition bias** — one drug with a huge number of reports for an
   event suppresses the measured disproportionality of every other drug for it.
4. **Time on market (Weber effect)** — reporting peaks in the first two years post
   launch then declines regardless of true risk. Never compare a year-two drug to a
   year-ten drug without windowing.
5. **Duplicates** — the same case arrives via manufacturer, physician and consumer.

## Turning a signal into an investment question

The useful question is rarely "is there a signal" — it is "what would have to be true
for the label to change, and what is that worth". Work backwards:

- Which revenue line carries the indication, and what share of group revenue is it?
- Is there a same-class competitor without the signal that takes the share?
- Has FDA already listed the drug-event pair in its quarterly potential-signals report?
- Is there an AdCom scheduled? a catalyst engine → adcom-label owns that handicap.
- For a device analogue, what did the comparable Class I recall do to the franchise?
