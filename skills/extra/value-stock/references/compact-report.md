# Compact Valuation Return Contract

Use this contract for the default Compact path. Compact changes the breadth of
research and reporting, not the minimum evidence needed to call a range fair
value.

These rendering gates apply to both Compact and Full. Render only fields owned
by compatible typed receipts or exact typed gaps; do no valuation or comparison
arithmetic while formatting. A failed or unsupported intrinsic path renders a
blocked report with no intrinsic value, range, sensitivity band, observed
discount, attractiveness statement, entry level, or price verdict. A passed
single case may be labeled only as a conditional estimate; only passed coherent
causal cases support a fair-value range, and a sensitivity band stays labeled as
sensitivity. The renderer owns conclusion language and analyst prose cannot
override the typed intrinsic, price-comparison, or decision state.

## 1. Snapshot

Lead with:

- company, ticker, exchange, exact security, and reporting currency;
- valuation date, information cutoff, and current-price timestamp when used;
- present causal fair-value range and base value per target security when
  supported; otherwise a supported base plus a narrowly labeled sensitivity
  band and an explicit statement that no causal range was established;
- observed price discount to estimated value using the named formula when
  authoritative price evidence exists;
- the hurdle decision state authorized under `SKILL.md`, or otherwise
  `required hurdle: not supplied; pass/fail: not assessed`;
- confidence, status (`complete`, `partial`, or `blocked`), and any failed gate.

When `market_context_scope` is `required`, also show the separate
business-quality and price-demanded conclusions. A quality conclusion cannot
stand in for price attractiveness.

Do not lead with a generic company description.

## 2. Load-Bearing Valuation

State the selected primary method and why it fits. Show:

- the three to five assumptions carrying most of the value;
- a short reproducible calculation and enterprise-to-equity or
  asset-to-security bridge;
- current-price-implied expectations from a reverse DCF or equivalent only
  when the selected intrinsic spine declares a compatible operation and
  authoritative price evidence exists, using the typed
  PriceImpliedExpectationReceipt's solution and gap fields; and
- sensitivities for the two or three inputs that can materially move the range.

If that optional reverse operation is unsupported, show a separate adjunct
capability gap and its unlock condition. It does not downgrade an otherwise
complete intrinsic result unless the user explicitly requested it or it is
load-bearing to the requested conclusion.

Use a causal range when coherent endpoints are supported. Otherwise, only when
the base remains supportable, show the base plus a narrowly labeled sensitivity
band; the band does not establish a causal fair-value range. Full bear/base/bull
narratives are optional unless asymmetric outcomes materially change the
conclusion.

When an admitted correction or material alternative changes value, show a
short bridge from the locked baseline through each correction, convention, or
scenario to the recomputed value. Otherwise omit the internal lock and review
ceremony.

## 3. Market context, evidence, and quality

When `market_context_scope` is `required`, render this table from the typed
receipt. Keep all five rows even when a lane is unavailable.

| Lens | Current observation | Benchmark | Relative position | What explains it | Status or gap |
| --- | --- | --- | --- | --- | --- |
| Own history | | | | | |
| Competitive peers | | | | | |
| Economic peers | | | | | |
| Industry | | | | | |
| Broad market | | | | | |

Show one primary relative metric and one companion only when the companion
catches a different material failure. Include forecast-contributor count,
dispersion, transformed multiple interval, and any unstable relative claim
supplied by the receipt. Do not calculate or infer a missing value while
rendering.

Include only the historical, latest-reporting, guidance, accounting, dilution,
peer, and post-period evidence needed to support or challenge the model.
Identify any unresolved conflict or missing input. Do not include a generic
business overview, broad news digest, peer table, PEG, or sentiment section
unless it changes value, method, range, confidence, or a thesis breaker.

Render `business_quality`, `price_demanded`, and every mechanism disposition
from `QualityVsPriceAssessment`. A mechanism used in both intrinsic and
relative reasoning must carry disjoint evidence and an explicit causal bridge.

## 4. Future Value When Requested

Keep present fair value distinct from a future-date value. Name the horizon,
show the roll-forward mechanics or label a shortcut, and report either the
future holder value plus distributions or its annualized holder return. Never
compare a future value directly with today's price as current upside.

## 5. Thesis Breakers And Next Depth

Give up to three supported thesis breakers. For each, render its observable
indicator, issuer-specific trigger, affected model path, current conclusion,
and mind-change condition. Omit unsupported prose that only says to reassess.
If the user made Full conditional on the authorized hurdle state, render that
state and either continue to Full or stop.

End with one sentence stating that the work is impersonal research, not
personalized investment advice.

Apply only the source and method sections already selected by the runbook from
[source-protocol.md](source-protocol.md) and
[valuation-methods.md](valuation-methods.md). Do not reload either whole reference
while formatting the return. When market context is required, also apply
[market-context.md](market-context.md) without reloading it during formatting.
