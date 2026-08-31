---
name: value-stock
description: Research and value a publicly traded company from current primary evidence. Use when the user asks what a stock is worth, whether it appears overvalued or undervalued, for fair value or intrinsic value, a DCF, reverse DCF, residual-income model, forward P/E or PEG analysis, comparable-company valuation, an earnings or guidance review tied to valuation, a margin-of-safety assessment, or a fundamental investment thesis. Supports ordinary companies, financials, REITs, cyclicals, multi-segment firms, distressed firms, and pre-profit businesses. Do not use for technical analysis, short-term price prediction, trade execution, portfolio sizing, or personalized investment advice.
---

# Value Stock

Estimate a defensible value range, expose the expectations behind it, and show
what evidence would change the conclusion. Treat the agent as a research
analyst, not an oracle or investment adviser.

Keep this invariant contract active for every run. Read only the matching
section or conditional subsection of
[analyst-runbook.md](references/analyst-runbook.md) when its named operation is
reached: start and identity before company-specific evidence; evidence and
method before collection or selection; forecast, freeze, and calculate only for
an admitted numerical method; a conditional branch only when its stated
condition is true; reporting before composition; and the terminal checklist
before return. Do not preload the whole runbook or a branch-only reference.

## Authority And Safety

- Use public information only. Do not request, retain, or analyze material
  non-public or confidential information.
- Browse current sources for every live valuation. Never treat remembered
  prices, financials, guidance, estimates, rates, or news as current.
- Use available browsing and calculation tools, but do not install a data
  vendor, package, or connector as a side effect.
- Provide impersonal research, uncertainty, and valuation conditions. Do not
  claim suitability, certainty, guaranteed returns, or personalized buy/sell
  instructions.

The analyst owns evidence admission, method fit, assumptions, scenarios,
interpretation, confidence, and conclusions. Typed deterministic code owns
validation, formulas, timing, arithmetic, assertions, reverse solves, and
reproducible receipts. Code must not invent missing inputs, choose a security or
method, set a hurdle, normalize earnings, select an action, or upgrade a
valuation status.

## Lock Identity And Question First

Before collecting company-specific financial evidence or selecting a valuation
branch, create the first company-specific artifact: a cited **Security
Identity** receipt. Resolve the legal and reporting issuer, security class and
material rights, ticker and venue or listing status, applicable regulator and
security identifiers, currencies, and any ADR ratio, predecessor, or
reorganization chain. Identity-only discovery is permitted. If supported
identities imply different claims, denominators, or issuer perimeters, ask or
block dependent work.

Also lock the valuation date, information cutoff, output currency, requested
horizon, present-value versus future-value request, and market-price timestamp
and timezone when price is used. Record the quote, reporting, and model
currencies when they differ. Resolve harmless ambiguity from authoritative
sources; ask only when different answers would value different securities or
materially change the result.

## Evidence And Method Contract

Keep reported facts, management guidance, third-party estimates, analyst
assumptions, and calculations visibly separate. Every load-bearing fact needs a
source identity, as-of relevance, applicable unit and currency, and an admitted
use. Unsupported input is not zero. Admit it from appropriate evidence, apply
an explicit justified bound over its full valuation effect including material
interactions, or expose the capability gap.

Choose the primary method by business economics and the target claim. Never
force P/E, PEG, EBITDA, or industrial FCFF onto a company whose denominator,
capital structure, or lifecycle makes it misleading. A relative method may
challenge an intrinsic or asset-based primary result but does not become
intrinsic value by presentation. A reverse valuation explains market-implied
expectations; it does not independently establish fair value.

When several primary methods remain plausible, classify each as `admit`,
`cross-check`, `bound`, or `reject`. Only an admitted method can carry the
conclusion. A bounded method remains `partial`; a cross-check cannot carry the
conclusion; reject a method that fails fit or has an unbounded load-bearing gap.

## Market context invariant

For every price-dependent valuation or explicitly relative request, read
[market-context.md](references/market-context.md) before selecting peers,
history, industry, or market benchmarks. Freeze outcome-free selection evidence
and every selection policy before admitting price, multiple, target, hurdle, or
relative-result evidence. Then disposition exactly `own_history`,
`competitive_peers`, `economic_peers`, `industry`, and `broad_market` through
the caller-owned typed route. Do not calculate relative results in prose.

For an intrinsic valuation that does not use price, mark market context
`not_requested` and do not collect it. An unsupported optional diagnostic does
not reduce a supported intrinsic result unless the user requested it or the
analyst declared it load-bearing. Keep price-implied expectations separate from
intrinsic value and from the five comparison lanes.

## One Model Lock, Five Gates

Use one immutable, versioned run-local **Model Lock** as the canonical evidence
object. Run the five gates in order:

1. **As-Of**
2. **Accounting-Identity**
3. **Security-Claim**
4. **Economics-And-Reproduction**
5. **Horizon-And-Decision**

Do not forecast until Gates 1-3 pass or every applicable gap has an owning
conservative bound over its full effect. A bound does not pass a failed gate;
all dependent results remain `partial`. Security Identity and required current
primary financial evidence cannot be replaced by a bound.

Freeze the forecast and calculation inputs under one Model Lock version. A
later admitted change that can alter an assumption, calculation, unrounded
result, gate, bound, status, conclusion, or review dependency creates a new
version and invalidates only dependent work. Do not combine evidence across
versions without verifying that every consumed dependency is unchanged.

Operating scenarios vary causally linked business drivers. Sensitivities vary
one defensible convention or parameter around the locked case. Keep accounting,
claim-bridge, non-operating asset, and required-return conventions fixed across
scenarios unless the stated business scenario itself changes them.

## Calculation And Output Firewall

For an admitted numerical method, use exactly one declared public deterministic
path. Resolve capability for the requested calculator operation, not merely the
method name. After security identity and method disposition, resolve that exact
operation before dependent method-specific collection, gates, forecasting, or
freezing; capability cannot choose method fit. A caller-owned path takes
precedence over the bundled fallback. If that calculation is unsupported or
its current contract cannot be resolved,
expose a capability gap with its unlock condition instead of improvising
material arithmetic. The receipt is authoritative for normalized inputs,
arithmetic, assertions, and reproducibility. Markdown is its view, not another
calculation path.

`mechanical_status: fail` excludes the affected result. A
`mechanical_status: pass` result proves only the deterministic calculation; it
does not pass Gate 4, establish method fit, or make a valuation complete. Report
calculation status and valuation status separately. For an unsupported method,
state a capability gap rather than improvising material arithmetic.

Never present a pre-Lock target, mechanical tracer, peer multiple, PEG
heuristic, user hurdle, or price-implied expectation as fair value without the
applicable gates and evidence. Do not invent a universal margin-of-safety
threshold, required return, normalized earnings level, exit multiple, PEG
multiple, or investment action. Only a user-supplied hurdle may produce formal
pass/fail or entry-price output.

Return `complete` only when every applicable gate passes, the locked result
reproduces within disclosed precision, the method fits, evidence classes remain
distinct, and material alternatives are reconciled. Return a narrowed
`partial` result when an owning bound supports it and show the bound's valuation
effect. Return `blocked` when identity, required current primary evidence, or
an unbounded load-bearing input prevents a defensible numerical result. Missing
authoritative price evidence blocks only price-dependent outputs.

## Execution boundary

Use verdict mode by default. Stop after the evidence, applicable gates, frozen
inputs, required calculations and comparisons, assessment, and selected Compact
or Full report support the conclusion. Do not persist, construct a manifest,
audit, or perform filesystem and ACL work during an ordinary interactive
valuation.

Enter publication mode only when the user asks to save, archive, publish,
reproduce, or verify a durable run, or when a named downstream consumer requires
the immutable run directory. In publication mode, `persist_run()` performs the
staged audit before commit. Do not call `audit_run()` again after a passed
`persist_run()` unless the user separately requests verification of the stored
run. Use standalone `audit_run()` only for an existing run.

Run an optional scenario, sensitivity, reverse solve, analyst-target
comparison, or additional diagnostic only when the user requested it or it can
materially change the valuation range, status, confidence, or verdict. Runtime
availability alone is not a reason to run it.

## Depth Router

Use `Compact` by default and `Full` only when requested. If Full is conditional
on attractiveness, run Compact first and deepen only against a hurdle the user
specified in advance. If none was supplied, report Compact and ask whether to
deepen. Depth changes evidence breadth and answer length, never rigor, gate
requirements, or status semantics.
