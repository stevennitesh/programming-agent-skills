# Market context

Read this reference when the request uses current price, asks whether a stock is
cheap or expensive, or explicitly requests relative valuation. Do not collect
market context for price-free intrinsic work.

## Set scope and capability first

Set `market_context_scope` before collecting outcomes:

| Request | Scope |
| --- | --- |
| Price-dependent intrinsic valuation | `required` |
| Explicit relative valuation | `required` |
| Intrinsic valuation without price | `not_requested` |

Select one primary relative metric from the target claim, denominator quality,
business economics, lifecycle, cyclicality, and the active calculator's exact
capability. A companion metric is useful only when it catches a different
material failure.

The metric contract must fix claim identity, period, estimate vintage,
accounting basis, dilution, currency, calendarization, normalization,
denominator eligibility, and statistic policy. Read the active repository's
valuation methodology and method contract before collecting dependent outcome
evidence. A formula in this reference is not runtime support.

If the repository does not support the chosen metric or lane, return the exact
capability gap. Do not substitute manual premium, discount, percentile, PEG, or
target-price arithmetic.

The current `stockval` market-context engine proves positive, claim-compatible
as-of forward P/E and `as_of_ptbv`. Every other formula family remains a typed
capability gap until its complete public path is proved.

For bank `as_of_ptbv`, use synchronized common-equity market capitalization over
normalized tangible common equity. Choose one book-timing convention per lane:
`latest_public_as_of` uses the latest TCE available by each price time;
`same_period_ex_post` is hindsight and must be labeled unavailable to an as-of
investor at that price date. Do not mix the conventions in one lane. Peer prices
use one declared session and synchronized measurement policy.

Reconcile every TCE observation from issuer-reported common equity. Preserve the
treatment of preferred equity, noncontrolling interests, goodwill, identifiable
intangibles, related tax effects, mortgage-servicing rights, and issuer-specific
exclusions. An unresolved material definition difference is `not_comparable`.
Keep reported, issuer-adjusted, and analyst-normalized ROTCE distinct; a
conclusion-bearing cohort uses one earnings basis, return period, and average-TCE
definition. ROTCE explains P/TBV economics but does not choose a target multiple.

## Freeze selection before outcomes

Choose candidates and policies without seeing their prices, multiples, targets,
or later results. Preserve two evidence groups:

- selection evidence contains identity, business economics, structural era,
  taxonomy, and benchmark membership;
- outcome evidence contains price, denominator, estimate, and calculated
  market observations.

Use the repository's public selection, evidence, freeze, and calculation path.
Lock the peer policy, history window and structural era, industry membership,
broad-market benchmark, statistic, weighting, outlier rule, and subject
exclusion before admitting outcomes. If the environment cannot enforce that
separation, stop the affected lane with a capability gap.

## Require apples-to-apples evidence

Give every candidate a final inclusion or exclusion disposition. Admit it only
when material differences are passed, reproduced through a disclosed
normalization, or irrelevant to the chosen metric. Check:

- security, issuer perimeter, and target claim;
- price date, denominator period, estimate vintage, and cutoff;
- currency, FX date, units, and quote scale;
- accounting, dilution, and normalization;
- business mix, geography, growth, margins, returns, reinvestment, capital
  intensity, lifecycle, cyclicality, and risk; and
- denominator sign, magnitude, missing-data state, and estimator eligibility.

Use price-independent size measures for candidate selection. Exclude the
subject, duplicate listings or classes, and duplicate consolidated issuers.
One eligible peer is an observation, not a cohort statistic. A fully examined
universe with no comparable candidates is `not_comparable`; missing evidence is
a `capability_gap`.

For banks, label candidates as whole-firm competitors, segment competitors, or
economic peers. A segment competitor cannot enter a whole-firm P/TBV statistic
unless it independently passes that lane's frozen policy. Industry P/TBV is
aggregate common market capitalization divided by aggregate normalized TCE, not
a mean or median of constituent ratios. Broad-market P/E is not comparable with
bank P/TBV and produces no premium, discount, or forced ratio.

## Account for five lanes

The typed result must disposition each lane exactly once:

| Lane | Question |
| --- | --- |
| `own_history` | Is the current metric unusual within a comparable era or cycle? |
| `competitive_peers` | How are direct rivals priced, and what explains the spread? |
| `economic_peers` | How are firms with similar multiple drivers priced? |
| `industry` | Is the industry itself rich or cheap against comparable history? |
| `broad_market` | Is the issuer or industry premium unusual in the current regime? |

Each lane ends as `used`, `not_applicable`, `not_comparable`,
`capability_gap`, or `mechanical_failure`. Preserve the candidate funnel,
exclusions, missing observations, denominator coverage, dispersion,
instability, influence, reason, and unlock condition supplied by the receipt.
Do not hide a failed lane or turn it into a neutral result.

The benchmark metric must carry the same economic meaning as the issuer metric.
Do not compare a bank P/TBV, REIT P/FFO, or asset-level biotech valuation with a
broad P/E simply because that benchmark is available. Relative cheapness does
not establish intrinsic value, and the whole comparison group may be expensive.

## Separate price-implied expectations

When current price is in scope and the repository supports the operation,
solve only the declared operating variable or coupled path through its public
typed route. Report the bounds, fixed assumptions, residual, solution-set
status, and completeness limits from the receipt.

A solved path states what satisfies the observed price while other declared
inputs stay fixed. It does not prove that the path is reasonable, likely, or
unique outside the tested bounds.

Keep two reverse questions distinct. `calculate_reverse()` conditionally solves
WACC or terminal growth while the operating forecast stays fixed.
`freeze_price_implied_expectation()` plus `calculate()` solves the declared
operating variable or coupled path while the named fixed leaves stay fixed. Never
rename the conditional rate solution as the market's operating expectation.

Keep business quality separate from price demanded. If one mechanism supports
both the intrinsic forecast and relative-premium explanation, use distinct
evidence and state the causal bridge so it is not double counted.

## Report without new arithmetic

Render the five lanes, price-implied result or gap, quality judgment, price
judgment, instability warnings, and up to three supported thesis breakers from
the typed receipts and analyst assessment. Full may add the candidate funnel,
peer exclusions, structural breaks, industry and ex-industry context, premium
bridge, and leave-one-out sensitivity when they affect the conclusion.

Never average intrinsic and relative values. Explain disagreement through the
recorded differences in forecast, margin, return, reinvestment, risk, claim,
denominator, accounting, or regime.
