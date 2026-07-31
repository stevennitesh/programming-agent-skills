# Value-Stock Excess-Return Duration Regression Fixture

Status: admitted existing-contract regression fixture; sampling not started.

## Behavior

For a Full residual-income valuation of a historically high-return company under
a material temporary disruption, make competitive-advantage duration visible
when it controls value. When current analyst targets materially challenge the
present-value result, compare usable targets on a common date and keep opaque or
incompatible targets as dispersion or sentiment evidence.

This fixture exercises existing requirements in:

- [`value-stock` Gate 4](../../../../../../skills/extra/value-stock/SKILL.md);
- [Residual Income And Excess Return](../../../../../../skills/extra/value-stock/references/valuation-methods.md#residual-income-and-excess-return); and
- [analyst-target reconciliation](../../../../../../skills/extra/value-stock/references/source-protocol.md#earnings-and-guidance).

## Entry-Positive Fixture

Task: perform a Full present-value residual-income valuation and explain a
material disagreement with current analyst targets.

Worker-visible synthetic facts:

- The issuer historically earned 20%-25% common ROE, but a disclosed temporary
  operating disruption reduced current ROE materially.
- Current primary evidence supports an operating recovery, while its duration
  and the fade back to sustainable returns remain judgmental.
- The model's near-term earnings are close to disclosed analyst estimates, but
  its value is materially lower because excess returns fade sooner.
- Usable analyst targets disclose publication date, 12-month horizon, forecast
  earnings period and definition, and a 20x-23x forward-earnings operator.
- Other targets omit a usable horizon or method.
- Near-term operating assumptions and the required return can be held fixed
  while alternative excess-return fade durations are calculated.

Expected behavior:

1. Show an explicit excess-return fade-duration sensitivity without silently
   changing near-term operations or the required return.
2. Identify duration, rather than next-period earnings alone, as the principal
   source of the valuation disagreement when the calculations support it.
3. Record each usable target's date, horizon, method, forecast period, and
   earnings definition, then compare it with intrinsic value on a common date.
4. Treat methodless or horizonless targets only as dispersion or sentiment
   evidence; do not average them into intrinsic value.
5. Preserve the stronger recovery path as forecast judgment, not a mechanical
   correction or an automatic replacement for the base case.

## Closest Wrong Condition

The issuer has stable low excess returns, no material disruption or recovery
thesis, and analyst targets are stale, opaque, or not materially different from
the intrinsic result.

Expected behavior: do not add an excess-return duration sensitivity or detailed
target bridge. Opaque targets may be mentioned only when they materially inform
dispersion or sentiment, with no new gate, weaker status, or report bulk.

## Evaluation

Score each entry-positive run on the five expected behaviors above. Any direct
comparison of present value with an unadjusted future target, averaging of
incompatible targets, hidden change to near-term operations or required return,
or categorical conclusion that suppresses the supported alternative is a
critical failure.

Before claiming behavioral efficacy, freeze control and candidate packages and
run the current behavioral-evaluation protocol with at least five fresh
entry-positive samples and separate wrong-condition pairs. This fixture proves
neither prevalence nor wording efficacy by itself.
