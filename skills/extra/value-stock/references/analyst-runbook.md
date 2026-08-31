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
pre-existing decision hurdle and authority, if any:
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

Freeze the selected intrinsic Model Lock through the public repository freezer.
Bind it to the exact security, dates, currency, sealed Evidence Pack, historical
and claim receipts, and method-required rate evidence or receipt. Never author
derived totals or substitute a test helper, fixture-shaped lock, placeholder
identity, or direct serialized lock for live authoring receipts.

Calculate through the resolved public path. If the intrinsic freezer, calculator,
or required upstream receipt fails or is unsupported, stop dependent numerical
work and assemble the blocked report required by `SKILL.md` from the typed gap.
Do not try dependent optional operations or substitute calculation paths.
Otherwise repair nonterminal contract failures before interpretation. Keep
causal scenarios separate from parameter sensitivities.

For FCFF work in the active `stockval` repository, the live gate is:

1. `seal_evidence_pack()` over preserved source artifacts;
2. `reconcile_historical_fcff()` and `reconcile_security_claims()`;
3. `build_wacc()` when WACC is issuer-built;
4. `freeze_fcff_model_lock()` followed by `calculate()`;
5. `calculate_scenarios()` for causal cases and typed sensitivity functions for fixed-parameter stress tests;
6. `freeze_price_implied_expectation()` plus `calculate()` for an operating expectation solve, distinct from the conditional rate `calculate_reverse()`;
7. the typed five-lane market-context path or exact lane dispositions when price
   is in scope; and
8. `assemble_valuation_report()` before a supported verdict.

For residual-income work, the proved `residual-income-2` sequence is:

1. `seal_evidence_pack()` over schema-2 point-in-time source artifacts;
2. `reconcile_common_equity_claims()` through the cutoff;
3. `reconcile_residual_income_history()` on one matched common-equity/ROE or tangible-common-equity/ROTCE basis;
4. `freeze_residual_income_model_lock()` followed by shared `calculate()`;
5. when needed, `calculate_residual_income_scenarios()`, `calculate_residual_income_sensitivity()`, and `calculate_residual_income_price_implied()`;
6. the typed `as_of_ptbv` five-lane market-context path when required; and
7. `assemble_valuation_report()` with the passed RI receipts and typed gaps.

Do not project FCFF-specific receipts or WACC semantics onto this direct-common
equity path. Persistence and audit follow only when separately requested.

The Evidence Ledger is the analyst-facing collection view. Every admitted ledger
row must map to an Evidence Pack artifact, reference, claim, and admission; a
derived row must also carry calculator-verifiable input lineage. Unmapped notes or
browser facts remain research leads, not Model Lock support.

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

Use one intrinsic spine in the verdict. Other intrinsic methods are typed
cross-checks or gaps unless a precommitted reconciliation rule owns their use.
Return `complete`, `partial`, or `blocked` under `SKILL.md`. Report mechanical
status separately. Present the strongest report the passed receipts support and
stop.

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

Also confirm that no fixture or placeholder entered the live chain, every
optional number came from its public typed route, conditional rate solves are
not operating expectations, and every report field binds to a receipt or exact
gap.
