# Full Valuation Return Contract

Use this contract only for the Full path. First apply every common rendering gate
and section contract in [compact-report.md](compact-report.md). Full inherits
those rules and adds challenge and corroboration; it never replaces or weakens
them. Keep four core sections and insert a branch only when it can change the
method, range, confidence, or a thesis breaker.

## 1. Decision Snapshot

Use the Compact Snapshot unchanged. Add only the main evidence limit behind
confidence and any market-context or price-implied gap that materially narrows
the typed business-quality or price-demanded conclusion.

## 2. Valuation And Price Expectations

Use one selected intrinsic method as the report spine. Treat every other method
as a typed cross-check, bound, rejection, or capability gap; do not present several
unreconciled intrinsic outputs as interchangeable fair values. For each applicable
method, state why it fits, the assumptions carrying the
value, the reproducible calculation, the enterprise-to-equity or
asset-to-security bridge, the resulting causal range or supported base plus
labeled sensitivity band, and its principal limitation. Show a reverse DCF or
equivalent only when the selected intrinsic spine declares a compatible
operation and authoritative current-price evidence exists. Name the solved
variable and fixed assumptions from the PriceImpliedExpectationReceipt. Keep
exhaustive unique, exhaustive multiple, bounded no-solution, and non-exhaustive
partial states distinct. If that optional reverse operation is
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

When `market_context_scope` is `required`, add one pricing-context table with
exactly `own_history`, `competitive_peers`, `economic_peers`, `industry`, and
`broad_market`. Render each lane's current observation, benchmark, relative
position, explanation, and disposition or exact gap from the receipt.

Add only conclusion-bearing detail: metric-selection rationale, candidate and
peer count funnel, core competitor and economic-peer observations, inclusion
and exclusion reasons in the attached receipt view, applicable LTM, NTM,
normalized and companion fundamentals, own-history structural breaks,
industry and ex-industry context, premium bridge and unexplained residual, and
peer-choice or leave-one-out sensitivity. Do not turn a descriptive cohort
center into a target price or average it with intrinsic value.

Render the `QualityVsPriceAssessment` as two judgments plus the mechanism
reconciliation. Preserve disjoint evidence and the causal bridge for any
mechanism used in both intrinsic and relative reasoning. Add the falsification
ledger with up to three supported thesis breakers, including each observable
indicator, issuer-specific trigger, affected path, current conclusion, and
mind-change condition.

## 4. Risks, Monitoring, And Decision Boundary

Rank load-bearing risks by valuation effect. For each, name an observable
indicator and the model input it would change. Conclude under the Compact gates
with the strongest supported typed intrinsic and price-comparison state, plus
the single most important unknown and the evidence that would trigger
revaluation.

End with one sentence stating that the work is impersonal research, not
personalized investment advice.

## Conditional Inserts

Add the smallest relevant insert:

| Condition | Insert |
| --- | --- |
| Deep normalization changes the value base | Historical and normalization bridge |
| Guidance revisions or delivery are load-bearing | Chronological guidance ledger |
| Required market context can challenge the intrinsic result | Five-lane receipt view, controlled peers, method-fit relative metrics, and explicit gaps |
| A post-period event has a demonstrated value transmission | Dated news or event table |
| A future-date value was requested | Bottom-up horizon roll-forward or clearly subordinate shortcut |
| Independent review ran or a convention changed value | Review coverage and correction bridge |

For forward multiples, render only caller-owned typed receipts with matching
periods, definitions, estimate dates, and peer economics. If PEG is not
meaningful, say `PEG: not applicable`. Do not calculate it in the report. For
news or sentiment, distinguish changed fundamentals from catalysts and
unsupported tone.

Apply only the source and method sections already selected by the runbook from
[source-protocol.md](source-protocol.md) and
[valuation-methods.md](valuation-methods.md). Do not reload either whole reference
while formatting the return. When market context is required, also apply
[market-context.md](market-context.md) without reloading it during formatting.
