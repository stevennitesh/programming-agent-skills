# Analyst Runbook

Use this procedure for each `$value-stock` run. The canonical contract remains
in `SKILL.md`; this runbook orders the work and routes detail to the existing
reference owners. Do not turn the runbook into a second evidence ledger or copy
method formulas into it.

## 1. Start The Run And Lock The Mandate

Create a run card containing the requested security, valuation date,
information cutoff, output currency, present- or future-value request, horizon,
depth, requested methods, and any user-supplied hurdle. Record price source,
timestamp, and timezone only when a price-dependent output is in scope. State
material exclusions and unavailable sources.

Before company-specific financial collection or method selection, perform
identity-only discovery and create the cited Security Identity receipt. Record:

- legal issuer and reporting or underlying issuer when different;
- class or series, material rights, ticker, venue, and listing status at cutoff;
- owning regulator issuer identifier when one exists and an authoritative
  security or listing identifier when available;
- quote, reporting, model, and output currencies when different; and
- ADR ratio, depositary, former name, predecessor, or reorganization chain when
  applicable.

Carry the receipt into Gate 1. Absence of a CIK or current exchange alone is not
a failure. If supported identities imply different claims, share denominators,
or issuer perimeters, ask the user or block the dependent result.

Use `Compact` for an ordinary valuation and `Full` for an explicitly deep or
comprehensive request. When Full is conditional on attractiveness, first run
Compact, compare it only with the user's predeclared hurdle, and deepen if the
hurdle is met. Without a supplied hurdle, finish Compact and ask whether to
deepen.

If the user explicitly asks to be grilled, invoke `$grilling` before evidence
collection or calculation. Pass the valuation mandate as the subject, the user
as decision and confirmation owner, and `$value-stock` as return owner. Proceed
only after explicit acceptance and a no-gap return. Otherwise do not invoke it
or delay an ordinary valuation with grilling questions.

## 2. Build The Evidence Foundation

Read [source-protocol.md](source-protocol.md) before evidence collection. Apply
its source hierarchy and minimum evidence packet at both depths; apply its Full
expansion only for Full or a material issue. Keep reported facts, guidance,
third-party estimates, assumptions, and calculations distinct in the evidence
ledger.

Read Method Principles, the selected method sections, Margin Of Safety, and
Calculation Artifact And Assertions in
[valuation-methods.md](valuation-methods.md). Read Future-Date Valuation only
when requested. Read [company-types.md](company-types.md) when initial
inspection leaves multiple materially plausible primary methods, the issuer is
a sector, lifecycle, or accounting exception, or material financing,
underwriting, custody, or asset-linked activity could change the cash-flow
definition, claim bridge, or method.

Choose the primary method from the business economics and target claim. Use an
intrinsic or asset-based method when supportable and a reverse valuation when
authoritative current-price evidence exists. Add relative valuation only when
requested or able to challenge the primary result. For each materially
plausible candidate, record target claim, required identity, owning evidence,
load-bearing gaps, and `admit`, `cross-check`, `bound`, or `reject` disposition.

Initialize the Model Lock and run the gates in order. Keep unreached sections
pending.

| Gate | Required evidence |
| --- | --- |
| **1. As-Of** | Security Identity; dates, cutoff, currencies, latest balance sheet; authoritative timestamped price when used; historical, stub, forecast, and realization date spine; intervening-event sweep with material effects bridged or bounded. |
| **2. Accounting-Identity** | Method and target claim; starting value or cash-flow identity with matching return convention; filed starting-period reconciliation; consistent conventions for interest, non-operating income, taxes, capex, leases, excess cash, acquisitions, and material existing-award versus future-grant SBC. |
| **3. Security-Claim** | Date-consistent actual common shares; debt, preferred, minority interests, awards, options, warrants, convertibles, and other material claims; one date or an explicit bridge for cash, debt, claims, awards, and shares. Do not use weighted-average EPS shares as a point-in-time claim. |
| **4. Economics-And-Reproduction** | Source-tagged anchors; causal drivers and scenarios; acquired versus organic growth when material; coherent growth, margins, reinvestment, returns, and competitive duration; exact rate definitions; terminal or realization economics; useful sensitivities; independently reproduced typed artifact and assertions. |
| **5. Horizon-And-Decision** | Present value separate from future-date value; future-state roll-forward or subordinate required-return shortcut; authoritative price for price-dependent outputs; named discount formula; only user-supplied hurdle for pass/fail or entry price; precision and status no stronger than the weakest load-bearing input. |

Run Gates 1-3 before forecasting. Record `forecast foundation: ready` only when
all applicable requirements pass or have an owning full-effect bound. Any later
change to their content resets the marker and invalidates dependent work.

After normal primary-source collection and candidate screening, make at most
one `$research` handoff only when one remaining bounded, source-answerable
question could change a candidate disposition, enable a primary result, or
materially change the model or conclusion, and no owning conservative bound
covers the full effect. Do not delegate a forecast, valuation judgment, broad
survey, multiple gaps, or ownership of the ledger or conclusion. Pass the exact
question and exclusions, candidate and claim, identity, issuer state, cutoff,
jurisdiction when relevant, disposition at stake, and observable answer
condition; set note and write authority to `none`, with `$value-stock` as return
owner. On return, disposition each load-bearing claim as `admit`, `reject`, or
`preserve-conflict`, then rescreen the affected candidate once.

## 3. Forecast, Freeze, And Calculate

Once the foundation is ready, reconstruct only enough history to normalize the
selected value base and expose forecast drivers. Build forecasts from causal
business or asset drivers before accounting outputs. Keep growth consistent
with reinvestment and returns. Direct cash-flow growth may summarize the
derivation but cannot replace it.

Before freezing assumptions, disposition each current management guidance item
or long-term target that could materially affect a forecast premise or terminal
state. Trace the first explicit period and terminal or realization state from
reported or guided method-appropriate drivers. Preserve unexplained material
conflicts as pending. Dated consensus may challenge the path but is not a
required forecast input.

Resolve or conservatively bound load-bearing pending items. Freeze one immutable
Model Lock version. Bind forecasts, calculation artifacts, assertions, gates,
and any review packet to it. An uncertain but explicit analyst assumption is
not automatically an unresolved evidence gap.

For nontrivial supported FCFF or residual-income work, start from the
[FCFF example](../examples/fcff-model-lock.json) or
[residual-income example](../examples/residual-income-model-lock.json), replace
the example with the frozen Model Lock, and run from the repository root:

```text
python skills/extra/value-stock/scripts/valuation_gateway.py calculate skills/extra/value-stock/examples/fcff-model-lock.json
python skills/extra/value-stock/scripts/valuation_gateway.py calculate skills/extra/value-stock/examples/residual-income-model-lock.json
```

Use `validate` instead of `calculate` for normalization and contract validation
only. Treat receipt JSON as authoritative; Markdown is its readable view.
Interpret objective diagnostics without allowing them to alter assumptions,
confidence, range, or status. Repair deterministic identity, timing, sign, unit,
source-definition, or reproduction failures before using the affected result.
For unsupported methods, expose a capability gap.

After the Model Lock is frozen, run Gates 4 and 5. Keep causal operating
scenarios separate from parameter or convention sensitivities. For a
price-dependent conclusion, name the formula:

```text
observed price discount = (estimated value - market price) / estimated value
```

## 4. Trigger Conditional Branches

| Condition | Action |
| --- | --- |
| Forward P/E or PEG is requested or could materially challenge the primary result | Load the caller-owned forward-multiple contract only when its public calculation path is implemented. Otherwise report the live capability state and do not invent a command or manual parallel calculation. |
| Independent validation requested, or complex claims, conventions, methods, or alternatives could materially change the conclusion | Read [model-review.md](model-review.md). First repair root-owned reproduction failures. |
| Compact output | Read [compact-report.md](compact-report.md) before composing. |
| Full output | Read [report-contract.md](report-contract.md) before composing. |
| Caller explicitly requests process evaluation, reusable fixture, or evidence for improving `$value-stock` | Complete the valuation and applicable review, then read [run-feedback.md](run-feedback.md). |
| One exact methodology, provider, event, or empirical question remains after identity and method screening, and the caller repository declares a valuation research catalog | Search only that catalog's metadata, exclude wrong-scope, countercondition, retired, superseded, stale, and conflicted entries, then open exactly one best eligible note. Record its disposition in the existing ledger and stop the branch. No match, equal eligible matches, staleness, or unresolved conflict returns a routing gap; a catalog row cannot satisfy a Model Lock requirement. |

Before review, derive one Review Readiness receipt from the existing gate and
assertion results. Include Model Lock version, calculation artifact identity,
scope, dependency-closed evidence packet status, security and target-claim
identity, price evidence when applicable, selected basis, filed reconciliation,
claim-bridge timing, intervening-event sweep, and root reproduction. Dispatch
only when all applicable items pass and no deterministic discrepancy remains.
A bound is ready only when its full valuation effect is visible and review does
not require the reviewer to obtain missing evidence. Otherwise repair or return
the dependent status with `review: not run - candidate not ready`.

Reviewers challenge judgment and one reproduces the model. They do not replace
the gates, construct the candidate, vote on value, or average targets. Review
Readiness is not a sixth gate and cannot upgrade status.

## 5. Interpret, Report, And Persist

Lead with the value range, supported price-implied expectations, confidence,
valuation status, and the two or three assumptions dominating value. Explain
method fit, causal scenarios, useful sensitivities, uncertainty, and thesis
breakers. Do not convert a target, peer multiple, PEG heuristic, hurdle, or
mechanical tracer into fair value by wording.

If the intervening-event sweep finds a material event, show dated bridges from
the latest balance sheet through the cutoff, and from cutoff to valuation date
when needed, for every affected load-bearing field. Label each bridge item by
evidence class and show the full valuation effect of estimates or bounds that
could change the conclusion.

Use `complete`, `partial`, and `blocked` exactly as defined in `SKILL.md`. A
partial result must name the failed gate or unavailable component, narrow the
claim, and show the bound's effect. A blocked result must state the precise
unlock condition. Report calculation status separately from valuation status.

Persist or present only artifacts authorized by the caller. Keep the evidence
ledger, Security Identity, Model Lock versions, calculation receipts, and any
review receipt traceable to the same run. Do not create a second ledger,
silently combine versions, or retain unsupported conclusions.

If run feedback was requested, report `valuation status` and `feedback status`
separately after both reach a terminal state. Feedback cannot upgrade, relabel,
or suppress the valuation.

## 6. Terminal Checklist

Before returning, verify:

- the security, claim, dates, currencies, cutoff, and price timestamp are clear;
- every material input is sourced, explicitly assumed, conservatively bounded,
  or exposed as a gap;
- evidence classes remain separate and method fit is explicit;
- all applicable gates have dispositions and the immutable result reproduces;
- scenario, sensitivity, mechanical status, and valuation status are distinct;
- alternatives, uncertainty, thesis breakers, and unlock conditions are visible;
- precision and conclusion do not outrun the weakest load-bearing evidence; and
- no automated hurdle, normalization, target, or investment action was invented.
