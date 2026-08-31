# Market context procedure

Read this reference when the request uses current price, asks whether a stock
is cheap or expensive, or explicitly asks for relative valuation. Do not load
or collect market context for an intrinsic valuation that does not use price.

## Route the request

Record one scope before market evidence collection:

| Request shape | Market-context scope | Required result |
| --- | --- | --- |
| Price-dependent intrinsic valuation | `required` | Five lane dispositions plus a separate price-implied receipt or exact gap |
| Explicit relative valuation | `required` | Five lane dispositions using a method-fit metric |
| Intrinsic valuation without price | `not_requested` | No market-price, peer-multiple, history-multiple, industry, or broad-market collection |

An unsupported optional diagnostic does not reduce a supported intrinsic
result. It does affect status when the user requested it or the analyst declared
it load-bearing to a conclusion.

## Select a metric before outcomes

Choose one primary relative metric from the target claim, business economics,
denominator quality, lifecycle, cycle, and available deterministic capability.
Add one companion metric only when it catches a different material failure.
Do not invent a universal multiple, peer rule, history window, estimator,
outlier cutoff, or threshold.

A metric is usable only when its contract fixes the numerator and denominator
claims, period, forecast vintage, earnings or cash-flow basis, dilution basis,
currency and FX treatment, calendarization, normalizations, denominator
eligibility, companion fundamentals, and method-fit rationale. A formula named
in a reference does not establish runtime support. Resolve the exact
caller-owned operation before collecting its dependent outcome evidence.

The proven schema-3 runtime supports positive, claim-compatible as-of forward
P/E and exposes typed gaps outside that capability. Do not replace a missing
operation with manual multiple, percentile, premium, discount, PEG, or target
price arithmetic.

## Freeze selection before pricing outcomes

Keep two evidence packages. The selection package contains only candidate
identity, business economics, structural-era facts, taxonomy, and benchmark
membership. It must exclude prices, observed multiples, valuation targets,
hurdles, actions, and later outcomes. The market-context package admits the
later price and denominator evidence.

Use the caller-owned public operations in this order:

1. Seal the outcome-free package with `seal_selection_evidence_pack()`.
2. Freeze the economic-peer policy with `freeze_peer_selection()`.
3. Freeze own-history, competitive-peer, industry, and broad-market policy
   with `freeze_history_selection()`, `freeze_additional_selection()`, and
   `freeze_benchmark_selection()` as applicable.
4. Seal outcome evidence with `seal_market_context_evidence_pack()`.
5. Bind the exact selection locks and market evidence with
   `freeze_market_context()`.
6. Send the frozen lock through the public `calculate()` route.

If the environment cannot separate selection evidence from outcomes, return a
`capability_gap`. An analyst attestation cannot make that lane `used`. Never
change candidates, thresholds, weights, history eras, benchmark membership,
estimators, or outlier policy after inspecting outcomes.

## Enforce apples-to-apples admission

Every candidate needs one final disposition. Admit it only when each material
dimension is `pass`, `normalized`, or `not_applicable`:

- security and claim identity;
- price date, denominator period, estimate vintage, and information cutoff;
- currency, FX date, quote scale, and units;
- accounting treatment and any reproducible normalization bridge;
- business mix, geography, growth, margins, returns, reinvestment, capital
  intensity, lifecycle, cyclicality, and risk for the selected metric; and
- denominator sign, magnitude, missing-data state, and estimator eligibility.

Use price-independent size measures for candidate selection. Exclude the
subject, its other listings or classes, and duplicate consolidated issuers.
One eligible peer is a named observation, not a cohort statistic. Missing
required evidence produces `capability_gap`; a complete observed universe in
which every candidate fails comparability produces `not_comparable`.

## Disposition exactly five lanes

The `MarketContextReceipt` must account for these lanes once each:

| Lane | Question |
| --- | --- |
| `own_history` | Is the current multiple unusual within a declared comparable era or cycle? |
| `competitive_peers` | How are direct rivals priced, and what operating differences explain the spread? |
| `economic_peers` | How are companies with similar multiple drivers priced? |
| `industry` | Is the classification cohort historically rich or cheap, and is the spread explained? |
| `broad_market` | Is the issuer or industry premium unusual in the current market regime? |

Each lane ends as `used`, `not_applicable`, `not_comparable`,
`capability_gap`, or `mechanical_failure`. Preserve the reason, exact unlock,
candidate funnel, exclusions, missing and invalid observations, denominator
coverage, forecast-contributor dispersion, transformed multiple interval, and
leave-one-out influence supplied by the receipt. Do not hide a failed lane or
turn it into a neutral comparison.

The broad-market metric must have the same economic meaning as the issuer
metric. Do not force broad P/E onto a bank P/TBV, REIT P/FFO, or asset-level
biotech valuation. An industry aggregate does not establish intrinsic value,
and a published benchmark containing the target remains
`subject_influenced`, not independent support.

## Keep price-implied expectations separate

When current price is in scope and the caller supports it, declare one bounded
operating variable or coupled path with `freeze_price_implied_expectation()`
and calculate it through the public gateway. Use only the typed receipt's fixed
leaves, equation, bounds, solver, residual, roots, completeness proof, and
solution-set status.

Report exhaustive unique, exhaustive multiple, bounded no-solution, and
non-exhaustive partial results distinctly. A solved path states what would
satisfy the observed price while other declared inputs stay fixed. It does not
show that the path is reasonable, likely, unique outside its bounded proof, or
an intrinsic value.

## Reconcile quality and price

Keep two typed judgments:

- `business_quality` covers operating durability, returns, competitive
  position, balance-sheet resilience, cash conversion, reinvestment runway,
  and counterevidence;
- `price_demanded` binds the observed-price evidence, price-implied receipt or
  exact gap, all five lane receipt identities, and the demanded growth, margin,
  reinvestment, risk, or duration paths.

Disposition every quality mechanism as `intrinsic_forecast`,
`relative_premium_interpretation`, `both_distinct_evidence`, or
`rejected_double_count`. Using one mechanism in both lenses requires disjoint
evidence sets and an explicit causal bridge. Quality does not imply an
attractive price.

Carry no more than three supported thesis breakers. Each must name an
observable indicator, current evidence, issuer-specific trigger, affected
Model Lock or MarketContextLock path, expected direction, causal rationale,
current conclusion, a result or gate that would change the conclusion, new-run
evidence, and a review or expiry condition. "Reassess" is not a mind-change
condition.

## Render receipts, not new analysis

Compact and Full use the same validated receipts. Compact shows the five-lane
pricing table, one primary metric and optional companion, price-implied result
or exact gap, forecast dispersion and instability, the two quality and price
judgments, and supported thesis breakers. Full may add the candidate funnel,
peer tables, inclusion and exclusion reasons, structural breaks, industry and
ex-industry context, premium bridge and unexplained residual, leave-one-out
sensitivity, and the falsification ledger when those items carry the
conclusion.

Render no arithmetic or explanatory claim that is absent from a typed receipt
or analyst judgment. Never average intrinsic and relative results. Explain a
disagreement through the recorded forecast, margin, return, reinvestment,
risk, claim, denominator, accounting, or regime differences.
