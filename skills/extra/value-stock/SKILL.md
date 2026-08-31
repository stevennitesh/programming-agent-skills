---
name: value-stock
description: Research and value a publicly traded company from current primary evidence. Use for fair value, intrinsic value, DCF or reverse DCF, residual income, forward P/E or PEG, comparable-company valuation, earnings or guidance tied to valuation, margin of safety, or a fundamental thesis. Route unsupported methods to explicit capability gaps. Do not use for technical analysis, short-term price forecasts, trade execution, portfolio sizing, or personalized investment advice.
---

# Value stock

Estimate a defensible value range, state what the market price assumes, and show
what evidence would change the conclusion. Use public information and provide
impersonal research, not personalized investment advice.

For an actual valuation, read the matching section of
[analyst-runbook.md](references/analyst-runbook.md) when that phase begins. Load
branch references only when their stated condition applies.

## Non-negotiable boundaries

- Browse current sources. Do not treat remembered prices, filings, guidance,
  estimates, rates, or news as current.
- Keep reported facts, management guidance, third-party estimates, analyst
  assumptions, bounds, and calculations distinct.
- Every load-bearing fact needs an owning source, cutoff relevance, definition,
  unit, currency, and admitted use. Missing evidence is not zero.
- The analyst selects evidence, method, assumptions, scenarios, confidence, and
  conclusion. Deterministic code validates typed inputs and owns material
  arithmetic when a supported path exists.
- Do not install a package, data vendor, or connector as a side effect.

## Common path

1. Lock the exact security, legal and reporting issuer, valuation date,
   information cutoff, target claim, output currency, horizon, and price
   timestamp when price matters. Stop if different plausible identities would
   change the claim or denominator.
2. Screen methods by business economics and target claim. Mark each plausible
   method `admit`, `cross-check`, `bound`, or `reject`.
3. Resolve the exact calculator operation before building its inputs. Use the
   current repository's public path and contract when available. Never combine
   it with a bundled or manual formula path. If the operation is absent, state
   the capability gap and unlock condition.
4. Collect only evidence that can change method fit, forecast drivers, claim
   bridge, required return, range, confidence, or thesis breakers.
5. Freeze admitted calculator inputs in one immutable Model Lock. The Evidence
   Pack owns sourced facts; the Model Lock owns the calculation inputs. A
   load-bearing change creates a new lock version.
6. Calculate through the resolved public path. Treat its receipt as authority
   for normalized inputs, arithmetic, assertions, and reproducibility.
7. Interpret the result, reconcile material alternatives, and return the
   Compact report by default. Use Full only when requested.

## Method and market discipline

Choose the primary method from the economics, not the sector label. Do not
force P/E, PEG, EBITDA, or industrial FCFF onto an unsuitable denominator,
capital structure, or lifecycle. Relative valuation may challenge an intrinsic
result but is not intrinsic value. A reverse valuation explains price-implied
expectations; it does not establish fair value.

For a price-dependent or explicitly relative request, read
[market-context.md](references/market-context.md). Select peers, history,
industry, broad market, metric, and statistic policy before inspecting their
valuation outcomes. Use apples-to-apples evidence and keep the subject out of
comparison cohorts. Account for `own_history`, `competitive_peers`,
`economic_peers`, `industry`, and `broad_market` through the repository-owned
typed path when that exact metric is supported. Otherwise report a lane-level
gap. For price-free intrinsic work, do not collect market context.

Operating scenarios vary linked business causes. Sensitivities vary one fixed
parameter or convention around a locked case. Do not blend them. Run an
optional scenario, sensitivity, reverse solve, peer comparison, or analyst
target comparison only when requested or when it can change the range, status,
confidence, or conclusion.

## Status and output

`mechanical_status: pass` proves only that the declared calculation ran. It
does not prove method fit, assumption quality, evidence completeness, or an
investment conclusion. A mechanical failure excludes the affected result.

Return:

- `complete` when the method fits, all load-bearing evidence and claim bridges
  are resolved, the result reproduces, and material alternatives are reconciled;
- `partial` when a justified finite bound supports a narrower claim and its
  full valuation effect is shown; or
- `blocked` when identity, required current primary evidence, or an unbounded
  load-bearing gap prevents a defensible number.

Do not invent a universal hurdle, margin of safety, normalized earnings level,
exit multiple, PEG target, or investment action. A user-supplied hurdle may
produce formal pass/fail or an entry-price calculation. Otherwise describe
price only relative to the supported value estimate.

Use verdict mode by default. Stop after the supported report. Persist or audit
a run only when the user asks for a durable or independently verified artifact.
When the repository's `persist_run()` already audits before commit, do not run
an immediate duplicate audit.
