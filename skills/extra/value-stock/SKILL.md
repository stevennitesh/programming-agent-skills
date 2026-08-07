---
name: value-stock
description: Research and value a publicly traded company from current primary evidence. Use when the user asks what a stock is worth, whether it appears overvalued or undervalued, for fair value or intrinsic value, a DCF, reverse DCF, residual-income model, forward P/E or PEG analysis, comparable-company valuation, an earnings or guidance review tied to valuation, a margin-of-safety assessment, or a fundamental investment thesis. Supports ordinary companies, financials, REITs, cyclicals, multi-segment firms, distressed firms, and pre-profit businesses. Do not use for technical analysis, short-term price prediction, trade execution, portfolio sizing, or personalized investment advice.
---

# Value Stock

Estimate a defensible value range, expose the expectations behind it, and show
what evidence would change the conclusion. Treat the agent as a research
analyst, not an oracle or investment adviser.

## Authority And Safety

- Use public information only. Do not request, retain, or analyze material
  non-public information or other confidential information.
- Browse current sources for any live valuation. Never use remembered prices,
  financials, guidance, estimates, rates, or news as if current.
- Use available browsing, filing, finance, spreadsheet, or calculation tools.
  Do not install a data vendor, package, or connector as a side effect.
- Separate reported facts, third-party estimates, management guidance, analyst
  assumptions, and calculations. Never present one class as another.
- Provide impersonal research, uncertainty, and valuation conditions. Do not
  claim suitability, certainty, guaranteed returns, or a personalized buy/sell
  instruction.

## Invoke Upstream Skills Only When Warranted

- If the user explicitly asks to be grilled, Invoke `$grilling` before valuation
  evidence collection or calculation. Pass the valuation mandate as the
  subject, the user as decision and confirmation owner, and `$value-stock` as
  return owner. Proceed only when Confirm closes with the user's explicit
  acceptance and `$grilling` returns without a gap; treat its returned bound and
  confirmed decisions as the mandate. If it returns a gap, return that gap and
  stop; do not duplicate grilling inside this skill.
- Otherwise, do not invoke `$grilling` and do not delay an ordinary valuation
  with grilling questions.
- After normal primary-source collection and any required candidate screen,
  make at most one `$research` handoff per valuation run, only when exactly one
  remaining gap is bounded to one source-answerable question and finite claim
  set, lacks an owning conservative bound over its full valuation effect
  including interactions, and its answer could change the affected candidate's
  disposition, make a primary result available, or materially change the model
  or conclusion. Do not hand off a forecast or valuation judgment, multiple
  independent gaps, an immaterial alternative, the broad stock survey, or
  ownership of this skill's evidence ledger, model, or conclusion. Do not use
  `$research` to rescue a method that fails fit or identity independently of the
  missing evidence; apply the dependent-method failure policy when the handoff
  condition is not met.
- Pass the exact question and exclusions; candidate method and target claim;
  required identity or input; applicable issuer state, as-of date, information
  cutoff, and jurisdiction when relevant; the disposition at stake and
  observable answer condition that would change it; note authority `none`; write
  authority `none`; and `$value-stock` as return owner.
- `$research` owns source work and claim classification for the handed-off gap.
  `$value-stock` owns the evidence ledger, candidate disposition, Model Lock,
  model, valuation status, and conclusion. On return, record one root disposition
  for each load-bearing claim: `admit`, `reject`, or `preserve-conflict`. Admit
  only a supported claim applicable to the resolved security, date, target claim,
  and intended use. A rejected claim cannot satisfy a candidate or Lock
  requirement; retain its unknown or limit in the ledger. A preserved conflict
  cannot satisfy a Lock requirement except through an owning conservative bound
  over its full valuation effect, including interactions. Treat `not-admitted`
  as no new evidence, rescreen the affected candidate once, and derive valuation
  status under this skill's gates and failure policy.

## Lock The Question

Before collecting company-specific financial evidence or selecting a
company-type or valuation branch, create the first company-specific artifact: a
cited **Security Identity** receipt. Identity-only discovery is permitted.
Record the target security's legal issuer; reporting or underlying issuer when
different; class or series and material rights; ticker and listing venue or
status at the cutoff; an owning regulator issuer identifier when one exists; an
authoritative listing or security identifier when available; quote, reporting,
and model currencies when different; and any applicable ADR ratio, depositary,
former name, predecessor, or reorganization chain. Carry this receipt into Gate
1. If supported identities still imply different claims, denominators, or issuer
perimeters, ask or block the dependent work. Absence of a CIK or current
exchange alone is not a failure.

Resolve or state:

- valuation date, information cutoff, and market-price timestamp when price is
  used;
- requested horizon, whether value is present or future, method, depth, and
  output currency;
- whether the user supplied an explicit margin-of-safety rule or a trigger for
  conditionally deepening the work; and
- material scope exclusions or unavailable sources.

Resolve harmless ambiguity from authoritative sources. Ask only when different
answers would value different securities or materially change the result.

## Choose Depth Without Lowering Rigor

Use `Compact` by default for an ordinary request for fair value, intrinsic
value, or a simple valuation. Use `Full` when the user requests a deep,
comprehensive, or full analysis.

If the user requests Full only when the stock appears attractive:

1. run Compact first;
2. compare the result with the hurdle the user specified in advance;
3. continue directly to Full when the hurdle is met; and
4. otherwise stop after Compact and state why Full did not run.

If no hurdle was supplied, report the Compact result and ask whether to deepen;
do not invent a universal threshold. A user-supplied required
margin-of-safety hurdle may serve as the trigger.

Compact and Full change evidence breadth and answer length, not analytical
honesty. Full adds history, corroboration, detailed bridges, causal scenarios,
guidance delivery, peers, and news only where they can challenge the result.

Treat a factor as material when it can credibly change cash flows, timing,
reinvestment, security claims, required returns, method, range, confidence, or
a thesis breaker. Catalysts, tone, and sentiment affect intrinsic value only
through a demonstrated cash-flow, timing, claim, or risk transmission.

## Load The Right References

- Load [source-protocol.md](references/source-protocol.md) before collecting
  evidence. Apply its source hierarchy and minimum evidence packet in both
  depths and its Full expansion only for Full or a material issue.
- Load Method Principles, the applicable method sections, Margin Of Safety, and
  Calculation Artifact And Assertions from
  [valuation-methods.md](references/valuation-methods.md). Load Future-Date
  Valuation only when a future value is requested.
- Load [company-types.md](references/company-types.md) when initial inspection
  leaves more than one primary method materially plausible for the issuer's
  business economics and target claim; when the issuer is a sector, life-cycle,
  or accounting exception; or when a non-financial issuer has material lending,
  lease-financing,
  custody/customer-funds, insurance-underwriting, or asset-linked funding
  activity that can change the cash-flow definition, claim bridge, or method.
- Load [model-review.md](references/model-review.md) only when independent
  validation is requested or complex claims, conventions, methods, or
  alternative values could materially change the conclusion. A reproduction
  failure is root-owned deterministic repair, not a review trigger.
- Load [run-feedback.md](references/run-feedback.md) only when the caller
  explicitly requests evaluation of this run's valuation process, evidence for
  improving `$value-stock`, or a reusable valuation fixture. Full analysis,
  independent validation, report revision, or an ordinary request for stronger
  evidence is not a trigger. Complete the canonical valuation or blocked
  attempt and any applicable review before running this branch.
- Load [compact-report.md](references/compact-report.md) for Compact or
  [report-contract.md](references/report-contract.md) for Full before composing
  the answer.

## Run The Calculator

For a nontrivial supported FCFF or residual-income valuation, freeze the
admitted Model Lock, use the [FCFF example](examples/fcff-model-lock.json) or
[residual-income example](examples/residual-income-model-lock.json), and follow
[valuation-methods.md](references/valuation-methods.md) for methodology:

```text
python skills/extra/value-stock/scripts/valuation_gateway.py calculate skills/extra/value-stock/examples/fcff-model-lock.json
python skills/extra/value-stock/scripts/valuation_gateway.py calculate skills/extra/value-stock/examples/residual-income-model-lock.json
```

Run these commands from the repository root. Replace the example path with the
frozen Model Lock for the selected method; use `validate` in place of
`calculate` when only normalization and contract validation are needed.

Treat receipt JSON as authoritative for normalized inputs, arithmetic,
assertions, and reproducibility; Markdown is only its compact readable view.
`mechanical_status: fail` excludes the affected result. A
`mechanical_status: pass` result is a mechanical tracer; it neither passes Gate
4 nor determines valuation status. Until Gate 4 passes, report calculation
status and valuation status separately, and do not present the mechanical tracer
as fair value, intrinsic value, or a valuation conclusion. Interpret objective
diagnostics without letting them alter inputs, confidence, range, or status.
When the selected method is unsupported, report an explicit capability gap and
do not improvise material valuation arithmetic.

## Select And Lock The Model

Choose the primary method by the business economics and target claim. Use an
intrinsic or asset-based method when supportable and a reverse valuation when
authoritative current-price evidence exists. Add a relative method only when it
can challenge the primary result or the user requests it. Never force P/E, PEG,
EBITDA, or industrial FCFF onto a company whose denominator or capital structure
makes it misleading.

Validate the selected or requested method under Gate 2. When more than one
primary candidate remains materially plausible, screen them before forecasting
or calculation. For each, record the target claim, required identity, owning
evidence, load-bearing gaps, and disposition as `admit`, `cross-check`, `bound`,
or `reject`. `Admit` only when claim and identity fit and load-bearing inputs are
supported. `Bound` may carry only a partial method result when owning evidence
brackets the gap's full valuation effect, including interactions. A
`cross-check` cannot carry the conclusion; reject a candidate that fails fit or
has an unbounded load-bearing gap. Rejected or cross-check alternatives do not
force `partial` when an admitted primary passes and material alternatives are
reconciled.

Before forecasting, initialize one internal **Model Lock** with the five sections
below. Mark sections not yet reached as pending and record each gate result,
unresolved item, conservative bound when available, and final status as it
becomes available. Each gate validates its section; the Lock is the canonical
evidence object, not a second narrative checklist. Do not admit or report any
pre-Lock target as a valuation result.

| Gate and Lock section | Required pass evidence |
| --- | --- |
| **1. As-Of** | Cited Security Identity receipt; valuation date, cutoff, currency, latest balance-sheet date; authoritative price field, timestamp, and timezone when price is used; a map of historical periods, stubs, forecast periods and realization dates; and a completed intervening-event sweep with every material effect bridged or bounded. |
| **2. Accounting-Identity** | Selected or requested method and target claim; selected starting value or cash-flow identity and matching return convention; one filed starting period or balance-sheet date reconciled to that identity; and consistent treatment conventions for financing interest, non-operating income, taxes, capex, leases, excess cash, acquisitions, and material existing-award versus future-grant SBC. Forecast drivers, assumptions, projected amounts, and economics belong to Gate 4. |
| **3. Security-Claim** | Date-consistent actual common shares; debt, preferred, minority interests, awards, options, warrants, convertibles and other material claims; no weighted-average EPS shares as a point-in-time claim; and one-date or explicitly bridged cash, debt, claims, awards, and shares. |
| **4. Economics-And-Reproduction** | Source-tagged facts and anchors; causal business or asset drivers and scenario definitions; organic versus acquired growth when material; coherent growth, margins, reinvestment, returns and competitive duration; exact rate definitions; terminal or other realization economics; useful sensitivities; and a separate pass that reproduces the typed calculation artifact and its deterministic assertions. |
| **5. Horizon-And-Decision** | Present value separated from future-date value; a future-state roll-forward or a clearly subordinate required-return shortcut; authoritative price evidence for price-dependent outputs; the named observed-discount formula; only a user-supplied hurdle for formal pass/fail or entry price; and precision and status no stronger than the weakest load-bearing input. |

Run Gates 1-3 in order before constructing any forecast. Record the derived
marker `forecast foundation: ready` in the Model Lock only when every applicable
requirement either passes or has an owning conservative bound over its full
valuation effect, including interactions. The foundation includes the date
spine, target claim and applicable claim bridge, selected starting value or
cash-flow identity and matching return convention, and its filed starting-
period or balance-sheet-date reconciliation. A bound does not pass a failed gate
or strengthen status; every dependent result remains `partial`. Security
Identity and required current primary financial evidence must pass and cannot
be replaced by a bound. The marker is not another gate or receipt.

Only after the foundation is ready, reconstruct enough history to normalize the
selected value base and expose the drivers carrying the forecast. Construct the
forecast from causal business drivers before accounting outputs; direct
cash-flow growth may summarize that derivation but cannot replace it. Keep
growth consistent with reinvestment and returns. Any later change to Gate 1-3
content resets the marker and invalidates its dependent work.

Before freezing forecast assumptions, disposition every applicable current
management guidance item or long-term target that could materially change a
forecast premise or terminal or realization state. Trace the first explicit
period and terminal or realization state from reported or guided
method-appropriate drivers through the economics required by the selected method.
Preserve any unexplained material conflict as pending. Usable dated consensus
may challenge this path, but is neither required nor a forecast input by
default.

Before calculation or review, resolve or conservatively bound every known
pending item that could change load-bearing content; an explicit forecast
assumption is not unresolved evidence solely because it is uncertain. Freeze
that content under one immutable run-local Model Lock version. Bind the forecast
and every resulting calculation artifact and gate result to that version. When
review is required, bind its Review Readiness receipt and dependency-closed
review evidence packet to the same version. The packet contains only evidence
already admitted into the frozen candidate or Lock, plus preserved conflicts
consumed by the candidate or assigned lenses, precise source identities and
locations, enough captured context to test source meaning, semantic
dependencies, and owning bounds. It is Lock-bound, not separately versioned.

A later root-admitted change is load-bearing when it can change a forecast
premise, calculation or unrounded result, gate disposition, bound, status,
conclusion, or assigned-lens dependency. Create a new Lock version and
invalidate only the dependent forecast, calculation, assertions, gates, Review
Readiness receipt, evidence packet, and lenses; recompute or rerun them before
reuse. Carry an unaffected result forward only after verifying every dependency
it consumed is unchanged. A fact outside every load-bearing and review
dependency may be recorded without a new version or rerun. Do not combine
evidence across versions without that verification.

After the forecast foundation is ready and the Lock version is frozen, run
Gates 4 and 5 in order. A gate passes only with its named evidence. For a
nontrivial supported FCFF or residual-income valuation, calculate the frozen
Model Lock through the gateway before Gate 4. For another method, report the
capability gap instead of silently performing material arithmetic.

Apply failure narrowly:

- Repair any deterministic identity, timing, sign, unit, source-definition, or
  reproduction failure before using the affected calculation.
- An evidence gap may return `partial` when owning evidence supports a
  conservative bound. Show the full valuation effect, narrow any conclusion the
  bound could reverse, and do not imply that the unresolved fact was observed.
- Block only the dependent method or per-security output when the missing item
  is load-bearing and cannot be bounded without fabrication. Security identity
  or missing current primary financial evidence blocks any dependent numerical
  result; missing price evidence blocks only price-dependent outputs.

When two conventions are defensible, choose one internally consistent base and
show the other as a separate sensitivity. Operating scenarios vary causally
linked business drivers while holding accounting, claim-bridge, non-operating
asset, and required-return conventions fixed, unless the stated business
scenario itself causes one of those items to change.

Before dispatching review, define the stable candidate and review scope, then
record one run-local **Review Readiness** receipt:

```text
model lock version:
calculation artifact identity:
review scope:
review evidence packet for scope: dependency-closed | fail
security and target-claim identity: pass | fail
authoritative price source when price-dependent: pass | not applicable | fail
selected value or cash-flow basis: <type>; pass | fail
historical FCFF reconciliation basis: not applicable | EBIT-derived | CFO-derived
filed starting-period reconciliation: pass | fail
cash, debt, shares, awards, and claims: one date | explicit bridge | bounded | fail
intervening-event sweep through cutoff: pass | fail
root calculation reproduction: pass | fail
ready: yes | no
```

Derive the receipt from existing gate and assertion results; record their
references and dispositions, not copied evidence or values. Bind both identities
to the frozen candidate. `ready: yes` requires every item applicable to the
candidate and review scope to have a passing disposition and no unresolved
deterministic discrepancy. `bounded` passes only when the Lock shows the gap's
full valuation effect and reviewers can inspect a stable candidate without
owning the missing evidence. Excluded failed components retain their own
`partial` or `blocked` status. Otherwise do not dispatch review: repair
deterministic failures or return the dependent `partial` or `blocked` result and
state `review: not run - candidate not ready`. The receipt is not a sixth gate
and cannot pass a gate or upgrade valuation status.

After readiness passes, apply `model-review.md` when its loading condition is
met. Reviewers challenge judgment, and one assigned reviewer reproduces the
model; they do not replace the gates, construct the candidate, vote on value, or
average targets.

For price-dependent conclusions, name the formula:

```text
observed price discount = (estimated value - market price) / estimated value
```

## Return

Follow the selected Compact or Full return contract. Lead with the range,
price-implied expectations only when supported, confidence, status, and the two
or three assumptions dominating value.

When the intervening-event sweep finds a material event, show a dated
latest-balance-sheet-to-information-cutoff bridge for every affected
load-bearing Lock field, plus any separately evidenced or explicitly assumed
bridge from the cutoff to the valuation date. Label each item with its evidence
class and show the full valuation effect of any estimate or conservative bound
that could change the range or conclusion.

Return:

- `complete` only when every applicable gate passes, the locked result
  reproduces within disclosed precision, the method fits, evidence classes
  remain distinct, and material alternatives are classified and reconciled;
- `partial` when a named failed gate or unavailable component still permits a
  useful bounded result; narrow the claim and state the valuation effect; or
- `blocked` when security identity, current primary evidence, or a load-bearing
  input prevents any defensible numerical result.

Completion requires one canonical valuation, visible uncertainty and thesis
breakers, no unresolved deterministic discrepancy, and an answer that does not
outrun its evidence.

When run feedback was requested, return `valuation status` and `feedback status`
separately. Feedback cannot upgrade, relabel, or suppress the canonical
valuation. Return the combined response only after both requested outputs reach
terminal status; do not collapse them into one.
