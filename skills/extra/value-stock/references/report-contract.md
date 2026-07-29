# Full Valuation Return Contract

Use this contract only for the Full path. Full adds challenge and corroboration,
not mandatory filler. Keep four core sections and insert a branch only when it
can change the method, range, confidence, or a thesis breaker.

## 1. Decision Snapshot

Lead with:

- company, ticker, exchange, exact security, reporting currency, valuation date,
  information cutoff, and price timestamp when price is used;
- present fair-value range and base value at precision supported by the weakest
  load-bearing input;
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
asset-to-security bridge, the resulting range, and its principal limitation.
Show a reverse DCF or equivalent when authoritative current-price evidence
exists. Name the solved variable and fixed assumptions.

Use causal cases and sensitivities for the two or three inputs that materially
move value. Do not average methods unless a weighting rule was fixed before
seeing the results. When an admitted correction or material convention changes
value, bridge from the locked baseline to the recomputed value. If review ran,
state its valid lens coverage and reduced independence, if any.

## 3. Evidence, Economics, And Variant View

Show only evidence that supports or challenges the model:

- the economic engine, variant view, causal value drivers, and observable
  thesis breakers;
- historical and trailing metrics carrying the selected method;
- reported-to-normalized bridges and material accounting, liquidity, dilution,
  claim, country, or control issues;
- forecast anchors, organic versus acquired growth when material, and the
  evidence for growth, margins, reinvestment, and return duration; and
- the price-implied path compared with company history, guidance, industry
  constraints, and relevant base rates.

Separate reported, guided, estimated, assumed, and calculated values. Preserve
conflicts and unknowns rather than merging them.

## 4. Risks, Monitoring, And Decision Boundary

Rank load-bearing risks by valuation effect. For each, name an observable
indicator and the model input it would change. Conclude with the fair-value
range, current-price timestamp, observed discount, and hurdle status when
supported, plus the single most important unknown and the evidence that would
trigger revaluation. Do not invent entry prices or an attractiveness judgment
without a user-supplied rule.

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

Apply the evidence, date, market-price, and citation rules in
[source-protocol.md](source-protocol.md), and the calculation, precision,
future-date, and margin-of-safety rules in
[valuation-methods.md](valuation-methods.md).
