---
name: value-stock
description: Research and value a publicly traded company from current primary evidence. Use when the user asks what a stock is worth, whether it appears overvalued or undervalued, for fair value or intrinsic value, a DCF, reverse DCF, residual-income model, forward P/E or PEG analysis, comparable-company valuation, an earnings or guidance review tied to valuation, a margin-of-safety assessment, or a fundamental investment thesis. Supports ordinary companies, financials, REITs, cyclicals, multi-segment firms, distressed firms, and pre-profit businesses. Do not use for technical analysis, short-term price prediction, trade execution, portfolio sizing, or personalized investment advice.
---

# Value Stock

Estimate a defensible value range, expose the expectations behind it, and show
what evidence would change the conclusion. Treat the agent as a research
analyst, not an oracle or investment adviser.

Read [analyst-runbook.md](references/analyst-runbook.md) completely at the start
of every valuation run. It owns the chronological procedure and routes the
conditional references. This file owns the invariant valuation contract.

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

For supported FCFF and residual-income work, send the frozen Model Lock through
the typed calculator described by the runbook. Its receipt is authoritative for
normalized inputs, arithmetic, assertions, and reproducibility. Markdown is a
view of that receipt, not an alternate calculation path.

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

## Depth Router

Use `Compact` by default and `Full` only when requested. If Full is conditional
on attractiveness, run Compact first and deepen only against a hurdle the user
specified in advance. If none was supplied, report Compact and ask whether to
deepen. Depth changes evidence breadth and answer length, never rigor, gate
requirements, or status semantics.
