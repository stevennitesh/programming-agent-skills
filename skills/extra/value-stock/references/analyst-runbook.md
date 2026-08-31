# Analyst runbook

Read one section when its phase begins. `SKILL.md` owns the invariant rules.
This runbook orders the work and points to branch detail.

## 1. Frame the run

Record:

```text
security and target claim:
valuation date and information cutoff:
requested output, currency, and horizon:
price source, timestamp, and timezone when used:
depth: Compact | Full
user-supplied hurdle, if any:
scope exclusions:
```

Perform identity-only research first. Cite the issuer, reporting perimeter,
security class and rights, ticker and venue, regulatory identifier, currencies,
and ADR or reorganization chain when relevant. Stop before financial collection
if unresolved identities imply different claims or denominators.

Set `market_context_scope` before outcome collection. Use `required` when the
request depends on price or relative valuation and `not_requested` for
price-free intrinsic work.

## 2. Select the method and calculation path

Read Method Principles and only the plausible method sections in
[valuation-methods.md](valuation-methods.md). Read
[company-types.md](company-types.md) only when exception economics or multiple
plausible methods make it useful.

For every plausible method, record its target claim, required evidence,
load-bearing gap, and `admit`, `cross-check`, `bound`, or `reject` disposition.
Then resolve each requested numerical operation:

```text
method and operation:
public interface:
owning contract and version:
supported | unsupported | unresolved:
unlock condition when not supported:
```

When the active workspace contains the `stockval` repository, its
`docs/valuation-methodology.md` and named method contracts own capability. Use
its public library functions to freeze inputs and assemble reports. Use
`stockval value <model-lock.json>` for serialized calculation and
`stockval audit <run-dir>` only for a persisted run. The CLI does not research
the company, choose assumptions, build an Evidence Pack, or prove that a model
is economically sound.

Do not use a separate skill-bundled calculator. If no repository-owned path
supports the exact operation, stop that numerical branch with a capability gap.
Independent evidence work may continue.

## 3. Build the evidence foundation

Read the relevant sections of [source-protocol.md](source-protocol.md). Start
with Source Hierarchy, Minimum Evidence Packet, Evidence Ledger, and Freshness
And Stopping. Load price, structured-data, transformed-issuer, guidance, news,
or Full-depth sections only when their trigger applies.

Before forecasting, establish:

- Security Identity, dates, currencies, balance-sheet date, and intervening
  events through the cutoff;
- the reported or reconciled earnings, cash-flow, book-value, or asset base;
- date-consistent cash, debt, senior claims, actual shares, and dilution; and
- enough operating history and current evidence to anchor the forecast.

Seal admitted facts in the repository-owned Evidence Pack when available.
Preserve unsupported items as explicit assumptions, finite full-effect bounds,
or capability gaps. Stop forecasting when an unbounded gap affects the selected
method or target claim.

When market context is required, read
[market-context.md](market-context.md). Freeze price-blind selection evidence
and policy before collecting multiples or other outcomes. Use the exact metric
supported by the active calculation path. An unsupported lane remains visible;
manual peer arithmetic does not repair it.

## 4. Forecast, freeze, and calculate

Forecast operating causes before accounting outputs. Explain the bridge from
the latest reported period to the first forecast period and disposition current
guidance that can change the path. Keep growth, margin, reinvestment, returns,
capital structure, dilution, and terminal economics mutually consistent.

Freeze one Model Lock through the selected repository API. Bind it to the exact
security, valuation date, cutoff, currency, Evidence Pack, and claim receipt.
Do not author calculator-derived totals as analyst facts.

Calculate through the resolved public path. Repair identity, timing, sign,
unit, definition, or reproduction failures before interpretation. A failed
receipt cannot support a partial value. Keep causal scenarios separate from
parameter sensitivities.

Use optional operations only when requested or conclusion-changing:

| Operation | Condition |
| --- | --- |
| Operating scenarios | More than one coherent causal case is supported |
| Sensitivity | One fixed parameter or convention needs stress |
| Reverse solve | An authoritative price or justified target exists |
| Forward P/E or PEG | Requested or able to challenge the primary result |
| Research catalog | One bounded unresolved method or evidence question remains |

For the local research catalog, search metadata for one exact question and open
at most one eligible note. A catalog row cannot supply evidence or a Model Lock
input. No match, conflict, staleness, or ambiguity stays explicit.

## 5. Interpret and report

Read [compact-report.md](compact-report.md) by default or
[report-contract.md](report-contract.md) for an explicitly requested Full
analysis.

Lead with the supported value range or clearly labeled single-case estimate,
current price comparison when supported, confidence, and status. State the
method fit and the assumptions carrying most of the value. Keep intrinsic
value, relative observations, analyst targets, and price-implied expectations
separate.

When market context is required, render all five lane dispositions from the
typed receipt and preserve every gap. Explain disagreement through recorded
differences in forecasts, margins, returns, reinvestment, risk, claims,
denominators, accounting, or market regime. Do not create new arithmetic while
formatting.

Show up to three evidence-backed thesis breakers. Each needs an observable
indicator, issuer-specific trigger, affected model input, and the conclusion it
would change.

Return `complete`, `partial`, or `blocked` under `SKILL.md`. Report mechanical
status separately. Present the verdict and stop.

## 6. Persist only on request

Persistence is not part of an ordinary valuation. When requested, use the
active repository's report, preflight, persistence, and audit contracts. Keep
the Evidence Pack, Model Lock, receipts, report, and run identity aligned.
Prefer a new immutable run after a load-bearing change.

If `persist_run()` performs a staged audit, do not repeat `audit_run()` unless
the user separately asks to verify the stored run.

## Final check

Before returning, confirm that the security, dates, cutoff, currency, and price
timestamp are visible; every load-bearing input is sourced, assumed, bounded,
or gapped; method fit and claim bridge are resolved; the calculation
reproduces; scenarios and sensitivities remain separate; market context has the
required lane dispositions; no hurdle or target was invented; and precision
does not exceed the weakest material evidence.
