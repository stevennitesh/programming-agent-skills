# Full Valuation Return Contract

Use this contract only for the Full path. Full adds challenge and corroboration,
not mandatory filler. Keep four core sections and insert a branch only when it
can change the method, range, confidence, or a thesis breaker.

## 1. Decision Snapshot

Lead with:

- company, ticker, exchange, exact security, reporting currency, valuation date,
  information cutoff, and price timestamp when price is used;
- present causal fair-value range and base value when supported; otherwise a
  supported base plus a narrowly labeled sensitivity band and an explicit
  statement that no causal range was established;
- observed price discount using the named formula when authoritative price
  evidence exists;
- the user-supplied margin-of-safety hurdle and pass/fail, or
  `required hurdle: not supplied; pass/fail: not assessed`;
- confidence with its main evidence limit; and
- status (`complete`, `partial`, or `blocked`) plus any failed gate.

Do not lead with a generic company description or imply a precise per-share
claim when the security bridge is unresolved.

## 2. Valuation And Price Expectations

For each applicable method, state why it fits, the assumptions carrying the
value, the reproducible calculation, the enterprise-to-equity or
asset-to-security bridge, the resulting causal range or supported base plus
labeled sensitivity band, and its principal limitation. Show a reverse DCF or
equivalent only when the selected intrinsic spine declares a compatible
operation and authoritative current-price evidence exists. Name the solved
variable and fixed assumptions. If that optional reverse operation is
unsupported, show a separate adjunct capability gap and its unlock condition.
It does not downgrade an otherwise complete intrinsic result unless the user
explicitly requested it or it is load-bearing to the requested conclusion.

When more than one coherent causal case is supported, show a distinct
**Operating Cases** table with the base and named alternatives, intentionally
varied business, financing, asset-realization, claim-path, or outcome drivers,
and recomputed value. Hold accounting, claim-bridge, non-operating-asset,
required-return, and realization conventions fixed unless the named causal
transmission changes one. If only one case is supported, report the base and
state that no causal range was established; do not invent alternatives.

When a second defensible convention or fixed-case parameterization materially
changes the result, show a separate **Convention Sensitivities** table that holds
the base causal case fixed, names each changed convention, and recomputes value.
Otherwise omit it. Never create a bull or bear operating case from a
convention-only change.

Do not average methods unless a weighting rule was fixed before seeing the
results. When an admitted correction or material convention changes value,
bridge from the locked baseline to the recomputed value. If review ran, state
its valid lens coverage and reduced independence, if any.

## 3. Evidence, Economics, And Variant View

Show only evidence that supports or challenges the model:

- the economic engine, variant view, causal value drivers, and observable
  thesis breakers;
- historical and trailing metrics carrying the selected method;
- reported-to-normalized bridges and material accounting, liquidity, dilution,
  claim, country, or control issues;
- forecast anchors, organic versus acquired growth when material, and the
  evidence for growth, margins, reinvestment, return duration, and any Full FCFF
  phase paths required by [valuation-methods.md](valuation-methods.md); and
- the price-implied path compared with company history, guidance, industry
  constraints, and relevant base rates.

Separate reported, guided, estimated, assumed, and calculated values. Preserve
conflicts and unknowns rather than merging them.

## 4. Risks, Monitoring, And Decision Boundary

Rank load-bearing risks by valuation effect. For each, name an observable
indicator and the model input it would change. Conclude with the causal
fair-value range, or supported base plus labeled sensitivity band, current-price
timestamp, observed discount, and hurdle status when supported, plus the single
most important unknown and the evidence that would trigger revaluation. When
explicitly requested and supported, characterize price only relative to the
present-value estimate and any causal range or labeled sensitivity band;
without a supplied rule, do not state formal pass/fail, an entry price, or a
rule-derived threshold.

End with one sentence stating that the work is impersonal research, not
personalized investment advice.

## Conditional Inserts

Add the smallest relevant insert:

| Condition | Insert |
| --- | --- |
| Deep normalization changes the value base | Historical and normalization bridge |
| Guidance revisions or delivery are load-bearing | Chronological guidance ledger |
| Relative valuation can challenge the intrinsic result | Controlled peers, forward multiples, or PEG |
| A post-period event has a demonstrated value transmission | Dated news or event table |
| A future-date value was requested | Bottom-up horizon roll-forward or clearly subordinate shortcut |
| Independent review ran or a convention changed value | Review coverage and correction bridge |

For forward multiples, use matching periods, definitions, estimate dates, and
peer economics. If PEG is not meaningful, say `PEG: not applicable`. For news
or sentiment, distinguish changed fundamentals from catalysts and unsupported
tone.

Apply only the source and method sections already selected by the runbook from
[source-protocol.md](source-protocol.md) and
[valuation-methods.md](valuation-methods.md). Do not reload either whole
reference while formatting the return.
