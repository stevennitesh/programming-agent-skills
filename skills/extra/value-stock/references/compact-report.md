# Compact Valuation Return Contract

Use this contract for the default Compact path. Compact changes the breadth of
research and reporting, not the minimum evidence needed to call a range fair
value.

## 1. Snapshot

Lead with:

- company, ticker, exchange, exact security, and reporting currency;
- valuation date, information cutoff, and current-price timestamp when used;
- present causal fair-value range and base value per target security when
  supported; otherwise a supported base plus a narrowly labeled sensitivity
  band and an explicit statement that no causal range was established;
- observed price discount to estimated value using the named formula when
  authoritative price evidence exists;
- required margin-of-safety hurdle and pass/fail when the user supplied one,
  otherwise `required hurdle: not supplied; pass/fail: not assessed`;
- confidence, status (`complete`, `partial`, or `blocked`), and any failed gate.

Do not lead with a generic company description.

## 2. Load-Bearing Valuation

State the selected primary method and why it fits. Show:

- the three to five assumptions carrying most of the value;
- a short reproducible calculation and enterprise-to-equity or
  asset-to-security bridge;
- current-price-implied expectations from a reverse DCF or equivalent only
  when the selected intrinsic spine declares a compatible operation and
  authoritative price evidence exists; and
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

## 3. Material Evidence And Quality

Include only the historical, latest-reporting, guidance, accounting, dilution,
peer, and post-period evidence needed to support or challenge the model.
Identify any unresolved conflict or missing input. Do not include a generic
business overview, broad news digest, peer table, PEG, or sentiment section
unless it changes value, method, range, confidence, or a thesis breaker.

## 4. Future Value When Requested

Keep present fair value distinct from a future-date value. Name the horizon,
show the roll-forward mechanics or label a shortcut, and report either the
future holder value plus distributions or its annualized holder return. Never
compare a future value directly with today's price as current upside.

## 5. Thesis Breakers And Next Depth

Give the three most important observable thesis breakers and the model input
each would change. If the user requested Full analysis only after a stated
attractiveness hurdle, say whether that hurdle was met and either continue to
Full or stop here. If no hurdle was supplied, do not invent one.

End with one sentence stating that the work is impersonal research, not
personalized investment advice.

Apply only the source and method sections already selected by the runbook from
[source-protocol.md](source-protocol.md) and
[valuation-methods.md](valuation-methods.md). Do not reload either whole
reference while formatting the return.
