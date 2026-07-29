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
  uncertain or the issuer is a sector, life-cycle, or accounting exception.
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
the drivers carrying the forecast. Forecast business drivers before accounting
outputs, and keep growth consistent with reinvestment and returns.

Before calculation, create one internal **Model Lock** containing only
load-bearing:

- security, valuation date, information cutoff, currency, and price timestamp
  when used;
- source-tagged historical facts and forecast anchors;
- method, claim holder, value or cash-flow definition, and matching required
  return;
- material accounting conventions, including cash, leases, acquisitions, and
  stock-based compensation;
- debt, other claims, actual shares, awards, dilution, and the
  enterprise-to-equity or asset-to-security bridge;
- forecast horizon, date map, scenarios, and cash-flow timing; and
- terminal, residual, liquidation, or other realization assumptions.

For a nontrivial numerical valuation, build the typed calculation artifact
defined in `valuation-methods.md`. Lock unknowns explicitly. When two
conventions are defensible, choose one internally consistent base and keep the
other as a sensitivity; never combine pieces of both.

## Five Gates

Run the gates in order. The As-Of, Accounting-Identity, and Security-Claim gates
are pre-calculation gates. A gate passes only with its named evidence; prose
assurance is not a substitute.

### 1. As-Of Gate

**Pass evidence:**

- exact target security, valuation date, information cutoff, and latest
  balance-sheet date;
- authoritative price source, field, timestamp, and timezone for any
  price-dependent conclusion;
- an explicit date map for historical periods, forecast periods, stubs,
  midpoints, discrete events, and terminal or residual value; and
- an evidence-backed bridge for material filings, acquisitions, financing,
  repurchases, distributions, or other events between the balance-sheet and
  valuation dates.

**Safe failure:** If identity or current primary financial evidence is missing,
return `blocked`. If stale balance-sheet data or a missing bridge still permits
a defensible bracket, return `partial` or `indicative` and avoid a precise point
value. Missing authoritative price evidence blocks only price-implied
expectations, observed discount, and hurdle pass/fail, not a standalone
intrinsic valuation.

### 2. Accounting-Identity Gate

**Pass evidence:**

- one filed historical period reconciles to the selected earnings, cash-flow,
  book-value, or asset-value definition;
- a CFO-derived FCFF reconciles financing interest, non-operating income,
  taxes, capex, and cash-flow classification;
- leases are operating or financing under one consistent convention;
- only excess cash and separately valued non-operating assets enter the
  security bridge; and
- material SBC separates existing awards from future grants and reconciles the
  expense, cash-flow, claim, and dilution treatment by cohort.

**Safe failure:** Do not calculate the affected method. Use another method only
when its evidence independently passes these gates; otherwise return `blocked`.

### 3. Security-Claim Gate

**Pass evidence:**

- date-consistent actual common shares and the exact rights or ADR ratio of the
  target security;
- debt, preferred equity, minority interests, options, RSUs, PSUs, warrants,
  convertibles, and other material claims reconcile on a disclosed basis;
- weighted-average EPS shares are not used as a point-in-time equity claim; and
- cash, debt, claims, awards, and shares share one date or an explicit bridge.

**Safe failure:** The equity pool may be reported when supportable, but
per-security value must remain unresolved or be shown only as a bounded range.
Return `partial`, not `complete`, and do not imply a filing-supported diluted
claim count.

### 4. Economics-And-Reproduction Gate

**Pass evidence:**

- the method fits the company and the forecast identifies the few causal
  business or asset drivers carrying value;
- organic and acquired growth are separated when acquisitions materially affect
  the forecast base or stated growth;
- growth, margins, reinvestment, returns, competitive duration, and terminal or
  residual economics are mutually coherent;
- every rate and beta uses the source's exact definition and matches the claim,
  currency, inflation basis, and timing;
- sensitivities change the assumptions that actually drive the range; and
- a separate calculation pass reproduces the locked result and passes the
  deterministic assertions in `valuation-methods.md`.

**Safe failure:** Repair mechanical, timing, sign, unit, identity, or source
definition errors and recompute before interpretation. Preserve defensible
conventions as sensitivities and forecast judgments as causal scenarios. A
failed reproduction or unresolved mechanical discrepancy prevents `complete`.

After deterministic checks pass, apply `model-review.md` when its loading
condition is met. Reviewers challenge judgment, and one assigned reviewer
reproduces the model; they do not replace the gates, vote on value, or average
targets.

### 5. Horizon-And-Decision Gate

**Pass evidence:**

- present fair value is distinct from any future-date value;
- a requested future value either rolls the business, cash, debt, claims,
  distributions, and shares to the future state or labels required-return
  compounding as a subordinate shortcut;
- price-dependent conclusions use authoritative price evidence and name the
  formula:

```text
observed price discount = (estimated value - market price) / estimated value
```

- a formal attractiveness, entry-price, or hurdle pass/fail uses only a rule the
  user supplied; and
- status, range, and numerical precision match the weakest load-bearing input
  and every unresolved gate.

**Safe failure:** Report the intrinsic range or observed discount that is
actually supported, but do not present a shortcut as bottom-up future value,
invent a margin-of-safety hurdle, print arbitrary entry prices, or make a
personalized adequacy judgment.

## Return

Follow the selected Compact or Full return contract. Lead with the range,
price-implied expectations only when supported, confidence, status, and the two
or three assumptions dominating value.

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
