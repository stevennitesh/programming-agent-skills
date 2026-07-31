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
- Invoke `$research` only when one bounded, source-answerable uncertainty remains
  after normal primary-source collection and could materially change the model,
  method, or conclusion. Pass the exact question, scope, as-of date,
  jurisdiction when relevant, note authority `none`, write authority `none`, and
  `$value-stock` as return owner. Integrate supported claims and preserve
  conflicts and unknowns. Return `partial` when supported alternatives can be
  bracketed; return `blocked` when the unresolved input is load-bearing and any
  number would be fabricated. Do not use `$research` for the broad stock survey
  or to outsource this skill's evidence ledger, model, or conclusion.

## Lock The Question

Resolve or state:

- legal company name, ticker, exchange, security class, economic and voting
  rights, and any ADR-to-ordinary-share ratio;
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
- Load [company-types.md](references/company-types.md) when model selection is
  uncertain, the issuer is a sector, life-cycle, or accounting exception, or a
  non-financial issuer has material lending, lease-financing,
  custody/customer-funds, insurance-underwriting, or asset-linked funding
  activity that can change the cash-flow definition, claim bridge, or method.
- Load [model-review.md](references/model-review.md) only when independent
  validation is requested, exact reproduction fails, or complex claims,
  conventions, methods, or alternative values could materially change the
  conclusion.
- Load [compact-report.md](references/compact-report.md) for Compact or
  [report-contract.md](references/report-contract.md) for Full before composing
  the answer.

## Select And Lock The Model

Choose the primary method by the business economics and target claim. Use an
intrinsic or asset-based method when supportable and a reverse valuation when
authoritative current-price evidence exists. Add a relative method only when it
can challenge the primary result or the user requests it. Never force P/E, PEG,
EBITDA, or industrial FCFF onto a company whose denominator or capital structure
makes it misleading.

Reconstruct only enough history to normalize the selected value base and expose
the drivers carrying the forecast. Derive forecast cash flow from causal
business drivers before accounting outputs; direct cash-flow growth may
summarize that derivation but cannot replace it. Keep growth consistent with
reinvestment and returns.

Before calculation, create one internal **Model Lock** with the five sections
below. Each gate validates its section; the Lock is the canonical evidence
object, not a second narrative checklist. Record each gate result, unresolved
item, conservative bound when available, and final status in the Lock.
Do not admit or report any pre-Lock target as a valuation result.

| Gate and Lock section | Required pass evidence |
| --- | --- |
| **1. As-Of** | Exact security, rights or ADR ratio, valuation date, cutoff, currency, latest balance-sheet date, authoritative price field, timestamp and timezone when used, a map of historical periods, stubs, forecast periods and realization dates, and a bridge for material intervening events. |
| **2. Accounting-Identity** | Method, target claim, value or cash-flow definition and matching return; one filed historical period reconciled to that definition; consistent treatment of financing interest, non-operating income, taxes, capex, leases, excess cash, acquisitions, and material existing-award versus future-grant SBC. |
| **3. Security-Claim** | Date-consistent actual common shares; debt, preferred, minority interests, awards, options, warrants, convertibles and other material claims; no weighted-average EPS shares as a point-in-time claim; and one-date or explicitly bridged cash, debt, claims, awards, and shares. |
| **4. Economics-And-Reproduction** | Source-tagged facts and anchors; causal business or asset drivers and scenario definitions; organic versus acquired growth when material; coherent growth, margins, reinvestment, returns and competitive duration; exact rate definitions; terminal or other realization economics; useful sensitivities; and a separate pass that reproduces the typed calculation artifact and its deterministic assertions. |
| **5. Horizon-And-Decision** | Present value separated from future-date value; a future-state roll-forward or a clearly subordinate required-return shortcut; authoritative price evidence for price-dependent outputs; the named observed-discount formula; only a user-supplied hurdle for formal pass/fail or entry price; and precision and status no stronger than the weakest load-bearing input. |

Before calculation or review, freeze the Lock's load-bearing model content under
an immutable run-local version; reuse that version while the content is
unchanged, and bind the calculation artifact, gate results, and review evidence
to it. A root-admitted load-bearing change creates a new version: recompute
every dependent output and rerun its deterministic assertions and gates. Do not
combine evidence across versions unless unchanged dependencies are verified.

Run the gates in order; the first three are pre-calculation gates. A gate passes
only with its named evidence. For a nontrivial numerical valuation, build the
typed calculation artifact in `valuation-methods.md` before Gate 4.

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

After deterministic checks pass, apply `model-review.md` when its loading
condition is met. Reviewers challenge judgment, and one assigned reviewer
reproduces the model; they do not replace the gates, vote on value, or average
targets.

For price-dependent conclusions, name the formula:

```text
observed price discount = (estimated value - market price) / estimated value
```

## Return

Follow the selected Compact or Full return contract. Lead with the range,
price-implied expectations only when supported, confidence, status, and the two
or three assumptions dominating value.

When material intervening events change cash, debt, claims, awards, or shares
between the latest balance-sheet date and valuation date, show a dated
opening-to-valuation bridge. Label each item with its evidence class, state any
conservative bound, and show the valuation effect of any estimate or bound that
could change the range or conclusion.

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
