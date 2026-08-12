# Analyst Runbook

Read only the section selected by the operation router in `SKILL.md`. A selected
section may route another reference only under its stated condition. The
canonical invariant contract remains in `SKILL.md`; this runbook orders
operation-specific work and must not become a second evidence ledger or formula
owner.

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

When live evidence collection begins, read Source Hierarchy, Minimum Evidence
Packet, Evidence Ledger, and Freshness And Stopping in
[source-protocol.md](source-protocol.md). Read its market-price section only for
a price-dependent output; structured-data, transformed-issuer, guidance, news,
and Full-expansion sections only when their named condition applies. Keep facts,
guidance, estimates, assumptions, and calculations distinct.

Read Method Principles and only the selected or still-plausible method sections
in [valuation-methods.md](valuation-methods.md). Read Future-Date Valuation only
for a future-date output, Margin Of Safety only for a price, attractiveness, or
hurdle comparison, and Calculation Artifact And Assertions only when a
supported deterministic lane is used. Read
[company-types.md](company-types.md) only when multiple methods remain
materially plausible or exception economics could change the cash-flow,
claim-bridge, or method identity.

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

If one exact source-answerable question remains after collection and candidate
screening, run **Conditional Research Resolution** before marking the forecast
foundation ready.

Run Gates 1-3 before forecasting. Record `forecast foundation: ready` only when
all applicable requirements pass or have an owning full-effect bound. Any later
change to their content resets the marker and invalidates dependent work.

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

At the calculation boundary, resolve the caller repository's valuation
methodology, selected method contract, and public interface. Record the owner,
method, requested calculation, contract version, and capability state. Require
the selected path to declare the calculation it will perform. If a caller-owned
path exists, use only it. If none exists, use the
[bundled valuation gateway](../scripts/valuation_gateway.py) only for its
declared FCFF or residual-income `validate`, `calculate`, or explicit reverse
solve route. Never use both paths for one material result. An absent,
conflicting, or unverified calculation is a capability gap with an exact unlock
condition, not authority for manual arithmetic.

When the selected caller path uses a method-specific lock, bind it to the
run-level security, valuation date, cutoff, currency, and upstream evidence
identities. The method lock is not another analyst ledger or authority to mix
run versions.

For supported bundled FCFF or residual-income work, use the matching
[FCFF example](../examples/fcff-model-lock.json) or
[residual-income example](../examples/residual-income-model-lock.json) only as a
schema starter. Replace every example value with the frozen Model Lock and run
only the operation selected under the `SKILL.md` calculation firewall. Never
treat an example as live evidence or as the operation choice.

Treat receipt JSON as authoritative; Markdown is its readable view. Interpret
objective diagnostics without allowing them to alter assumptions, confidence,
range, or status. Repair deterministic identity, timing, sign, unit,
source-definition, or reproduction failures before using the affected result.

After the Model Lock is frozen, run Gates 4 and 5. Keep causal operating
scenarios separate from parameter or convention sensitivities. For a
price-dependent conclusion, use the named convention from Margin Of Safety in
`valuation-methods.md`.

## 4. Trigger Conditional Branches

### Conditional Research Resolution

Use this subsection only for the unresolved question routed from Section 2. If
the caller declares a valuation research catalog, search only its metadata.
Exclude wrong-scope, countercondition, retired, superseded, stale, and
conflicted entries; open exactly one best eligible note and disposition its
answer in the existing ledger. A catalog row cannot satisfy a Model Lock
requirement. Equal eligible matches or no eligible note return a routing gap,
not permission to load the archive.

Only after the catalog is unavailable or returns no eligible answer, make at
most one `$research` handoff when the bounded question could change a candidate
disposition, enable a primary result, or materially change the model or
conclusion, and no owning full-effect bound exists. Do not delegate a forecast,
valuation judgment, broad survey, multiple gaps, or ownership of the ledger or
conclusion. Pass the exact question and exclusions, candidate and claim,
identity, issuer state, cutoff, jurisdiction when relevant, disposition at
stake, observable answer condition, no note or write authority, and
`$value-stock` as return owner. On return, disposition each load-bearing claim
as `admit`, `reject`, or `preserve-conflict`, then rescreen the candidate once.

### Forward P/E Or PEG

Use this subsection only when Forward P/E or PEG is requested or could
materially challenge the primary result. Resolve the caller-owned
forward-multiple calculation and contract under Section 3. If unavailable,
report the capability gap and do not invent a command or manual parallel
calculation.

### Independent Review

Use this subsection only when independent validation is requested or complex
claims, conventions, methods, or alternatives could materially change the
conclusion. First derive one Review Readiness receipt from the existing gate and
assertion results.
Include Model Lock version, calculation artifact identity, scope,
dependency-closed evidence packet status, security and target-claim identity,
price evidence when applicable, selected basis, filed reconciliation,
claim-bridge timing, intervening-event sweep, and root reproduction. A bound is
ready only when its full valuation effect is visible and review does not require
the reviewer to obtain missing evidence. If any applicable item fails, repair
it or return `review: not run - candidate not ready` without loading the review
procedure.

When the matching receipt is `ready: yes`, read
[model-review.md](model-review.md). Repair any later root-owned reproduction
failure before review. Reviewers challenge judgment and one reproduces the
model. They do not replace the gates, construct the candidate, vote on value,
or average targets. Review Readiness is not a sixth gate and cannot upgrade
status.

### Run Feedback

Use this subsection only when the caller explicitly requests process
evaluation, a reusable fixture, or evidence for improving `$value-stock`.
Complete the valuation and applicable review before reading
[run-feedback.md](run-feedback.md).

## 5. Interpret, Report, And Persist

When the output is ready to compose, read exactly one return contract:
[compact-report.md](compact-report.md) for Compact or
[report-contract.md](report-contract.md) for Full.

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
