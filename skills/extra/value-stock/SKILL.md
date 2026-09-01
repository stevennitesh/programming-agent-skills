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
- Test fixtures, browser facts, hand arithmetic, spreadsheets, standalone
  scripts, placeholder identities, direct serialized locks, and failed receipts
  cannot replace an unsupported or failed repository operation.
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
5. Freeze one selected intrinsic spine in an immutable Model Lock. Keep its
   Evidence Pack and claim receipts distinct from separately typed market-context,
   price-implied, forward-multiple, residual-income, or analyst-comparison locks
   and packs. The Evidence Pack owns sourced facts; every Model Lock owns the
   calculation inputs for its typed calculation. A load-bearing change creates a
   new version of every dependent lock.
6. Calculate through the resolved public path. Treat its receipt as authority
   for normalized inputs, arithmetic, assertions, and reproducibility.
7. Close the request before a supported verdict: disposition every requested or
   conclusion-bearing branch and assemble the active report. A passed calculator
   receipt closes only its mechanical calculation branch. Then interpret the
   assembled result and return Compact by default, or Full when requested.

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

For a bank residual-income valuation, read
[bank-residual-income.md](references/bank-residual-income.md) when that method is
selected. It routes the proved public sequence without owning repository fields
or formulas.

## Status and output

`mechanical_status: pass` proves only that the declared calculation ran. It
does not prove method fit, assumption quality, evidence completeness, or an
investment conclusion. A mechanical failure excludes the affected result.

Return:

- `complete` when the method fits, all load-bearing evidence and claim bridges
  are resolved, a passed intrinsic receipt supports the claim, the result
  reproduces, and material alternatives are reconciled;
- `partial` when a mechanically passed intrinsic spine supports a narrower
  conclusion but a typed material limitation remains, with its exact effect or
  unlock condition shown. A justified finite bound is one valid partial case,
  not a requirement for every partial result; or
- `blocked` when no passed intrinsic receipt exists because identity, required
  evidence, an upstream receipt, the selected freezer or calculator, or method
  support failed.

If the selected intrinsic path is failed or unsupported, go directly to a
blocked report. Omit every intrinsic value, range, sensitivity band, observed
discount, attractiveness statement, entry level, and price verdict that depends
on that path. Retain only sourced nonvaluation facts, exact gaps, and unlock
conditions. Mechanical pass alone does not establish method fit, evidence
sufficiency, a causal range, or an investment conclusion.

Do not invent a universal hurdle, margin of safety, normalized earnings level,
exit multiple, PEG target, or investment action. Formal pass/fail,
attractiveness, entry-price, and action language requires a hurdle supplied
before outcome inspection by the user or by a named pre-existing policy.
Without that authority, state only the typed relative price position and that no
decision was assessed.

Return the strongest actively assembled report the request-wide closure gate
supports; it may be blocked. Stop after that report. Persist or audit a run only
when the user asks for a durable or independently verified artifact. When the
repository's `persist_run()` already audits before commit, do not run an
immediate duplicate audit.
