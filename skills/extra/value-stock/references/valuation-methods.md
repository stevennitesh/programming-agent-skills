# Valuation Methods

## Contents

- [Method Principles](#method-principles)
- [Future-Date Valuation](#future-date-valuation)
- [FCFF DCF](#fcff-dcf)
- [Cash-Flow And Accounting Identities](#cash-flow-and-accounting-identities)
- [Management-Defined And Analyst-Constructed Cash Flow](#management-defined-and-analyst-constructed-cash-flow)
- [Stock-Based Compensation Reconciliation](#stock-based-compensation-reconciliation)
- [FCFE And Dividend Models](#fcfe-and-dividend-models)
- [Discount Rates, Country Risk, And Timing](#discount-rates-country-risk-and-timing)
- [Growth, Reinvestment, And Terminal Value](#growth-reinvestment-and-terminal-value)
- [Reverse DCF](#reverse-dcf)
- [Residual Income And Excess Return](#residual-income-and-excess-return)
- [Relative Valuation](#relative-valuation)
- [Forward P/E](#forward-pe)
- [PEG](#peg)
- [SOTP, NAV, And Distress](#sotp-nav-and-distress)
- [Margin Of Safety](#margin-of-safety)
- [Calculation Artifact And Assertions](#calculation-artifact-and-assertions)

## Method Principles

Value cash flows to the correct claim holder at a matching required return.
Keep currency, inflation basis, tax treatment, and timing consistent. Reserve
fair-value range endpoints for named coherent operating, financing,
asset-realization, claim-path, or outcome cases. A fixed-case sweep of required
return, terminal growth, cap rate, continuing spread, or market multiple remains
a separately labeled sensitivity band unless each endpoint is a coherent causal
case. A causal case may change required return when its supported transmission
changes risk or funding.

Report no more precision than the weakest load-bearing input supports;
approximate claims, stale bridges, and broad sensitivities do not support
cents-level fair value.

When multiple load-bearing bounds affect one per-security result, record each
bound's affected layer, held-constant scope, unlock condition, and direction on
the numerator, denominator, and final metric. Label the combined result upper
or lower only when its direction is proven over the full bound ranges. Opposing
effects remain `partial` and directionally unresolved unless their combined
direction is proven.

Valuation is uncertain even when carefully executed; sensitivity, scenarios,
and decision trees expose uncertainty but do not remove it:
[Damodaran: An Introduction to Valuation](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/background/valintro.htm).

Keep cases causal. If probabilities are supportable, make them exhaustive and
sum to 100%. Expected scenario cash flows still require a risk-consistent
discount rate. Do not penalize the same risk again because a simulation also
shows a wide value distribution:
[Damodaran: Probabilistic Valuation](https://pages.stern.nyu.edu/~adamodar/pdfiles/DSV2/Ch3.pdf).

## Future-Date Valuation

Present-value estimates and future-date values are different outputs. A
defensible future-date value rolls the model to that state rather than merely
compounding today's fair value:

1. remove elapsed forecast cash flows from the remaining valuation;
2. roll cash, debt, debt-like claims, awards, share count, and other claims
   through retained cash, distributions, buybacks, issuance, financing,
   acquisitions, and other explicitly modeled uses;
3. update the remaining operating drivers, terminal economics, and required
   returns to assumptions appropriate for the future state;
4. discount the remaining cash flows from the future date and rebuild the
   enterprise-to-equity or asset-to-security bridge; and
5. cross-check the result against normalized forward earnings, cash flow, book
   value, NAV, or another method appropriate to the business.

Do not automatically add the elapsed year's FCFF to cash: it may fund
reinvestment, debt service, acquisitions, distributions, or repurchases. Trace
the modeled use and avoid counting it in both cash flow and the equity bridge.

If evidence supports only a shortcut, label it. Under the simplest one-period
equity relation:

```text
future ex-distribution value
  = present value x (1 + required return) - interim holder distributions
```

This is a required-return roll-forward, not a new bottom-up fair-value estimate.
For either approach, state the horizon and translate the result into present
value or an annualized return that includes modeled holder distributions:

```text
annualized holder return = IRR(
  -current price,
  interim per-share cash distributions,
  future value plus final distribution
)
```

Use actual dates when timing is irregular. Do not count buybacks as cash paid to
a continuing holder; reflect their modeled effect through share count and value
per share.

## FCFF DCF

Use for non-financial operating businesses when debt is a financing claim rather
than an operating raw material.

```text
NOPAT = EBIT x (1 - normalized operating tax rate)
FCFF = NOPAT + D&A - capital expenditures - change in operating working capital
enterprise value = PV(explicit FCFF) + PV(terminal value)
common equity pool = enterprise value
                     + excess cash and non-operating assets
                     - debt and debt-like claims
                     - preferred equity
                     - non-controlling interest
                     - unfunded obligations
target common value = common equity pool
                      - option, warrant, and conversion-right claim value
common value per share = target common value
                         / actual date-consistent common shares
```

Adjust consistently for leases, capitalized R&D, acquisitions, pensions,
cross-holdings, options, and stock-based compensation when material. Do not add
back stock-based compensation while ignoring future grants or the resulting
dilution and equity claim.

When material, value employee options, warrants, and conversion rights as
separate claims on equity before dividing by common shares. A fully diluted
share count is a shortcut, not an equivalent treatment, because it can miss
exercise proceeds, vesting, and option time value:
[Damodaran: Dealing with Options, Warrants and Convertibles](https://pages.stern.nyu.edu/adamodar/New_Home_Page/lectures/eqshare.htm).

Decompose material non-controlling interests by subsidiary or economic
component. For a listed subsidiary, use dated minority ownership, market price,
and the applicable foreign-exchange rate. For private components, require a
supported economic value or finite conservative bound. Treat carrying value as
a labeled proxy unless it is reconciled to attributable cash flows or equity
value. Apply the dependent status policy to any material residual component: a
finite bound may support `partial`; an unbounded load-bearing gap blocks the
affected numerical result.

Discount FCFF at WACC using market-value capital weights and a cost of capital
consistent with the cash-flow currency. Do not use a stale universal risk-free
rate, equity risk premium, beta, or debt spread.

At Full depth, each explicit FCFF forecast phase must trace revenue or volume
and price through operating margin, cash operating tax, reinvestment, and the
economically matching return driver. Use incremental ROIC when meaningful;
otherwise state why it is not meaningful and use the applicable driver.
Reconcile sustainable growth with reinvestment and return on new invested
capital, or an economically matching terminal driver, in the terminal state.
Separate organic and acquired contribution when material. Direct FCFF growth
may summarize a completed path; otherwise it is only a labeled sensitivity and
cannot establish a causal range or pass Gate 4.

Select the perpetual-growth terminal branch explicitly. Prefer
`stable_economics` when the Lock admits next-period NOPAT, stable growth, stable
return on new invested capital, and WACC: the calculator derives reinvestment
rate as `growth / return on new invested capital`, reinvestment, next-period
FCFF, and terminal value. `direct_fcff_growth` is a labeled shortcut that grows
the last explicit FCFF; use it only when that direct scalar path is consistent
with the admitted terminal economics and keep its analytical limit visible.

When an admitted reported or guided cash-flow measure materially anchors the
first explicit forecast period, reconcile modeled FCFF to it by definition and
timing. Trace the difference through tax, interest classification, D&A, capex,
working capital, acquisitions, prior-period growth investment, utilization, or
other identified sources and uses. A growth-and-return reinvestment identity is
a consistency check, not a substitute for this bridge. An unexplained material
difference fails Gate 4; apply the main skill's dependent `partial` or `blocked`
policy.

## Cash-Flow And Accounting Identities

Declare each historical FCFF base as `EBIT-derived FCFF` or `CFO-derived FCFF`;
do not blend branches or switch between them to conceal a failed
reconciliation. An EBIT-derived base must bridge filed operating income to
normalized operating EBIT and reconcile cash operating tax, D&A, fixed-capital
investment, operating working-capital change, and material lease, acquisition,
or classification adjustments. A CFO-derived base must reconcile one filed
period under the identity below:

```text
FCFF = CFO + financing interest
       - cash tax benefit attributable to financing interest
       - fixed-capital investment
       +/- disclosed classification and non-operating adjustments
```

This starts from the standard CFO conversion summarized by
[CFA Institute](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation),
but it is a reconciliation, not a license to add total interest expense.
Identify the financing-interest amount the CFO treatment requires, then trace
cash paid, accruals, non-cash interest, lease interest, capitalized interest,
tax effects, and the issuer's cash-flow classification. Use the cash tax benefit
from financing interest actually available under applicable losses, limits, and
classifications; do not mechanically apply a reported effective tax rate.
Remove after-tax non-operating interest income when its cash or investment asset
is separately added in the enterprise-to-equity bridge. Under IFRS or another
policy choice, adapt the formula to where interest and dividends were actually
classified:
[Damodaran: Valuing Cash](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/lectures/cash.html).

A second derivation is optional and must pass independently. Reject only the
dependent FCFF result when its selected branch has a load-bearing unbounded gap;
an owning conservative full-effect bound may carry only a bounded partial
result.

Choose one lease convention. Either treat leases as operating and leave the
matching rent in operating cash flow, or capitalize the financing claim and
restate operating cash flow consistently. Do not subtract lease debt while also
leaving the full financing component in operating expense.

Add only **excess cash** and separately valued non-operating assets to operating
value. Estimate the liquidity and working-capital reserve needed to run the
business; when that reserve is uncertain and material, show a sensitivity
instead of labeling all cash excess.

Apply one disclosed liquidity-reserve convention to cash and economically
equivalent marketable securities after separately classifying restricted,
regulatory, customer, and non-operating balances. Do not reserve one while
treating the other as fully excess without support.

## Management-Defined And Analyst-Constructed Cash Flow

Before a management-defined or analyst-constructed cash-flow measure carries a
method result, reconcile at least one filed period from the nearest reported
measure to its exact definition and target claim, and test material adjustments
for recurrence over the admitted history. Classify each material adjustment as
recurring owner cost, reinvestment, financing or security claim, non-operating
or timing, or finite source or use.

Deduct omitted recurring owner costs and model all reinvestment required by the
forecast without forcing growth investment into a maintenance or steady-state
denominator. Treat stock-based compensation and acquisitions consistently
through cash flow, claims or dilution, and acquired-growth economics without
double counting. Distinguish generated from distributable cash after minimum
liquidity, regulatory or reserve requirements, covenants, debt service, and
stable leverage.

Opening cash is a dated bridge asset. Asset-sale proceeds and finite funding are
dated realization or financing flows, never recurring or terminal cash flow.
Bound an unsupported maintenance-versus-growth split over its full valuation
effect. Reject only the dependent measure when a load-bearing adjustment remains
unreconciled and unbounded; then apply the main status policy.

## Stock-Based Compensation Reconciliation

Separate two economic questions:

- **existing awards and overhang:** claims already granted as of the valuation
  date; and
- **future employee services:** compensation expected to be granted or paid
  during the forecast.

This separation follows the distinct current-award and future-grant valuation
questions identified by
[Damodaran: Management Options and Value](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/mgtoption.htm).
Financial statements recognize share-based payment as compensation cost, so a
non-cash label does not make it economically free:
[FASB: Accounting for Share-Based Payment](https://fasb.org/page/getarticle?uid=fasb_NEWS_RELEASE_12_16_04Body_0228221200).

Choose and disclose one internally consistent treatment for each:

- Starting from GAAP EBIT, stock-based compensation is already an operating
  expense. Do not subtract that same expense again from FCFF.
- Starting from cash flow from operations, the non-cash stock-based
  compensation add-back is embedded in cash flow. Reverse the add-back for an
  owner-economic cash-flow measure, or model the economically equivalent future
  dilution or equity claim explicitly.
- Treat material existing options, restricted units, and similar awards as
  separate equity claims or in a date-consistent diluted-share bridge. Do not
  use both for the same award population.
- Model future grants as recurring compensation expense, a cash-equivalent
  cost, or explicit future dilution. Do not also subtract the same forecast
  grant cohort as a separate current claim.

Reconcile award cohorts, vesting, forfeitures, exercise proceeds, tax effects,
and forecast share count when material. Never subtract recurring stock-based
compensation from cash flow and then deduct all related unvested awards from
equity without showing why the two adjustments represent different service
periods or claims. Repurchases offset dilution only through the cash spent and
shares retired; they are not a free adjustment.

## FCFE And Dividend Models

Use equity cash flow when debt policy is stable and estimable:

```text
FCFE = net income + D&A - capex - change in working capital + net borrowing
equity value = PV(FCFE discounted at cost of equity)
```

Use a dividend discount model only when dividends reasonably approximate
residual distributable cash or regulation makes dividends the observable equity
cash flow. A low payout does not by itself make a stock cheap.

## Discount Rates, Country Risk, And Timing

Build discount rates from current, named inputs:

- a default-free rate in the cash-flow currency and on the same nominal or real
  basis;
- an equity risk premium and a risk measure suited to the business;
- a pre-tax cost of debt reflecting current default risk, then the applicable
  tax treatment; and
- market-value capital weights or an economically defensible target structure.

Preserve the source's exact rate and beta definitions. Distinguish raw,
levered, unlevered, cash-corrected, bottom-up, and adjusted betas; unlever or
relever them explicitly when required. Never relabel a cash-corrected unlevered
beta as the target equity beta:
[Damodaran: Dataset Variable Definitions](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/variable.htm).

Assess country risk from where revenue, production, assets, funding, and legal
claims are exposed, not simply where the company is incorporated or traded.
Avoid using a risky sovereign yield as the risk-free rate and then adding a
country premium again. Adjust expected cash flows or the discount rate
consistently, and explain the choice:
[Damodaran: Measuring Company Exposure to Country Risk](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/CountryRisk.htm).

Use a disclosed midyear convention when cash flow is earned throughout a year.
Use explicit timing for acquisitions, milestones, debt maturities, binary
events, and stub periods. Align fiscal years, calendar years, next fiscal year,
and next twelve months before discounting or comparing estimates.

## Growth, Reinvestment, And Terminal Value

Connect growth to investment economics:

```text
operating-income growth ~= reinvestment rate x return on new invested capital
stable reinvestment rate = stable growth / stable return on capital
```

Growth funded below the cost of capital can destroy value. Damodaran's
definitions and growth discussion make reinvestment and return on capital the
fundamental drivers:

- [Financial measures and ratios](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html)
- [Fundamental determinants of growth](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/invfables/growthdeterminants.htm)

For a going concern:

```text
terminal value at year n = FCFF(n+1) / (WACC - stable growth)
```

Require `WACC > stable growth`. Converge risk, margins, reinvestment, and returns
toward sustainable levels. Stable nominal growth should not exceed the
corresponding long-run economy indefinitely. An exit multiple imports current
market pricing and is therefore a relative-value cross-check, not an intrinsic
terminal-value method:
[Damodaran: Terminal Value](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/terminalvalue.htm).

Report the share of enterprise value from terminal value as a sensitivity
diagnostic, not an automatic pass/fail rule.

## Reverse DCF

Hold a transparent set of non-growth assumptions and solve for the revenue
growth, margin, reinvestment efficiency, or terminal economics required for the
current price. State which variable was solved and what stayed fixed.

Describe a reverse result as a minimum or maximum only relative to the named
bound and stated held-constant assumptions. Do not extend that direction across
other unresolved bounds.

Treat a one-variable solve as a conditional sensitivity, not the market's
unique thesis. When multiple economically linked drivers can plausibly explain
price and the price-implied expectation is load-bearing, also show one coherent
joint path or state that the expectation is not uniquely identified. Do not
present an extreme held-constant solution as the singular market implication.

Compare implied expectations with:

- company history and current guidance;
- addressable-market and share constraints;
- peer economics and industry base rates;
- required reinvestment and capital availability; and
- competitive erosion and steady-state limits.

Reverse DCF explains what price requires; it does not prove that expectation is
likely.

## Residual Income And Excess Return

Use residual income when book value and earnings are meaningful but dividends or
free cash flow are difficult to forecast, especially for regulated financial
firms:

```text
residual income(t) = net income(t)
                     - cost of equity x beginning common book value(t)
equity value = current common book value
               + PV(expected future residual income)
```

The equivalent driver is `(ROE - cost of equity) x beginning book value`.
Forecast continuing residual income from sustainable ROE, growth, payout, and
competition; do not assume excess returns persist forever.

Use exactly one accounting basis. Pair `reported_common_equity` with common
earnings and ROE, or pair `tangible_common_equity` with ROTCE-compatible common
earnings and a reconciled TCE basis. Do not apply ROTCE to reported common book,
consume an opaque adjusted return, or create an arbitrary adjusted-book basis.
TCE starts from reported common equity and separately reconciles goodwill,
identifiable intangibles, related tax effects, and each issuer-specific
exclusion.

The historical receipt must close clean surplus through common income,
dividends, gross repurchases, issuance, employee-equity effects, AOCI or other
comprehensive-income effects, other direct-to-common adjustments, and every
basis-specific change. Preserve reported and adjusted earnings separately. Each
normalization identifies gross amount, tax effect, common attribution,
accounting location, recurrence disposition, and evidence. An unexplained
material difference or irreproducible return denominator blocks the dependent
valuation.

Each forecast period declares direct common earnings or a matched return-derived
path, an explicit beginning, admitted-average, or reproducible simple-average
capital convention, common cost of equity, and one owner-distribution or
ending-capital driver. Keep dividends, repurchases, issuance, employee-equity
effects, and other direct-equity movements separate. The calculator derives the
dependent earnings, distribution, ending capital, equity charge, residual
income, retention, and payout; do not supply those outputs as assumptions.

The continuing state declares sustainable return, common cost of equity, book
growth, zero direct-equity adjustment, and either franchise support or a finite
fade. The calculator derives next-period capital, earnings, retention, payout,
residual income, and terminal value. Require `cost of equity > growth`; perpetual
excess return needs explicit franchise support. If distributable capital is
load-bearing, the payout and growth path must pass the declared regulatory-
capital constraint. This arithmetic does not judge whether the economics are
plausible.

Reconcile the clean-surplus relation: ending common book value should equal
beginning book value plus comprehensive income attributable to common less
dividends and repurchases plus issuances, with other direct-to-equity changes
identified. Adjust book value and earnings consistently for material accounting
distortions, write-offs, reserve changes, acquisitions, and other-comprehensive-
income items. Pair the model with justified P/B or P/TBV, asset quality, and
capital adequacy:
[CFA Institute: Residual Income Valuation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/residual-income-valuation).

Residual income starts from common-equity book value, so do not repeat FCFF's
debt, preferred, or noncontrolling-interest bridge. After calculating common
equity, apply only separately valued existing awards/options and explicit
target-security add/subtract adjustments. Declare existing awards in exactly
one place: either the dated share count or the RI claim bridge, never both.

## Relative Valuation

Use [market-context.md](market-context.md) for selection timing,
apples-to-apples admission, exact lane dispositions, and caller-owned
calculation. The table below guides metric fit. It does not authorize manual
multiple, premium, percentile, PEG, or target-price arithmetic.

Match numerator and denominator:

| Multiple | Appropriate use | Major controls |
| --- | --- | --- |
| Forward P/E | Positive sustainable equity earnings | EPS definition, growth, duration, risk, payout, ROE |
| EV/EBIT | Operating earnings across leverage | tax/capital intensity, growth, risk |
| EV/EBITDA | Similar capital intensity and lease policy | capex, D&A, leases, margins |
| EV/Sales | Pre-profit or margin-transition firms | normalized margin, growth, reinvestment, risk |
| Price/FCF or FCF yield | Mature cash generators | FCF definition, maintenance capex, working capital |
| P/B or P/TBV | Financial firms and asset economics | ROE, asset quality, growth, cost of equity |
| P/FFO or P/AFFO | REITs | recurring capex, leverage, property mix, NAV |

Use consistent forward or trailing periods for target and peers. The frozen
StatisticContract owns the estimator and outlier policy. A comparable is
similar in growth, risk, and cash-flow economics, not merely sector label:

- [Damodaran: What is a comparable firm?](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/comparables.htm)
- [Controlling for differences](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/controldifferences.htm)

Relative valuation can show cheapness versus peers while the whole group remains
overvalued. Preserve disagreements with intrinsic value rather than averaging
them away:
[Reconciling DCF and relative valuation](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/reconcilingdcfandrelative.htm).

## Forward P/E

The typed MetricContract fixes current equity price, forecast diluted EPS,
named period, estimate vintage, earnings basis, and dilution basis. Use the
caller-owned receipt. Do not calculate it in the report. A P/E is not meaningful
with negative earnings. Its fundamental drivers include growth, risk, payout or
reinvestment, and return on equity:
[Damodaran: Price Earnings Ratio](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/invfables/peratio.htm).

Compare forward P/E only with the same earnings definition and horizon. Rebase
historical comparisons for changed rates, business mix, leverage, accounting,
tax, margins, or growth duration.

## PEG

Use PEG only when a caller-owned typed contract fixes the forward P/E, growth
definition, scale, estimate vintage, and matched horizon. Do not calculate it
manually. Reject PEG for negative, near-zero, highly cyclical, or
one-off-recovery growth. `PEG < 1` is not a universal bargain rule. PEG does not
fully control for risk, payout, growth quality, or the nonlinear relationship
between growth and value:
[Damodaran: PEG Ratios](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/lectures/peg.htm).

## SOTP, NAV, And Distress

- **SOTP:** value economically distinct segments with suitable methods, then
  subtract central costs and common claims. Avoid double-counting segment cash.
- **NAV:** mark separable assets and liabilities using supportable values,
  taxes, costs, and ownership; use for property, resources, or holding companies.
- **Distress:** probability-weight going-concern and failure/recovery outcomes;
  model refinancing, covenant, dilution, and senior-claim paths explicitly.

Damodaran provides model variants for financial services, troubled firms,
high-growth firms, and other exceptions:
[Valuation spreadsheets and model selection](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/eqspread.htm).

## Margin Of Safety

Distinguish:

```text
upside versus price = (value - price) / price
price discount to value = (value - price) / value
```

Always report the second measure as the **observed price discount to estimated
value**. Market practice sometimes calls this observed discount a margin of
safety, so answer that usage directly when the user asks, but keep it distinct
from the decision hurdle below. Always name the formula because conventions
vary.

A **required margin-of-safety hurdle** is a decision rule layered on an
uncertain valuation, not another valuation method. Apply the authority and
language boundary in `SKILL.md`. Keep any observed price discount distinct from
the hurdle decision state, and do not characterize a blocked comparison.

Do not invent one threshold for every company or automatically print arbitrary
entry-price thresholds. A wider hurdle is generally warranted when value is more
uncertain, the balance sheet or business is fragile, terminal value dominates
plausible cases, or catalysts are weak. Diversification and the source of
uncertainty also matter:
[Damodaran: Margin of Safety](https://pages.stern.nyu.edu/~adamodar/pdfiles/blog/MOS.pdf).

## Calculation Artifact And Assertions

For a supported nontrivial FCFF or residual-income valuation, serialize the
admitted frozen Model Lock through the calculator. Its authoritative JSON
receipt supplies the deterministic arithmetic and assertions represented by
the selected typed calculation path; it does not prove every derivation behind
an admitted scalar assumption. Do not reproduce the receipt-owned arithmetic
manually in the valuation report. If the selected method is unsupported, keep
the capability gap explicit instead of improvising material arithmetic. For
each admitted input the selected path consumes and each derived output it owns,
the receipt gives:

| Field | Required content |
| --- | --- |
| ID | Stable input or calculation name |
| Class | Reported / estimated / guided / assumed / calculated |
| Source date | Publication date and observation or balance-sheet date |
| Period | Historical, stub, forecast, terminal, or valuation date |
| Unit | Currency, scale, per-share basis, nominal or real |
| Claim basis | Enterprise, debt, preferred, common pool, or target security |
| Scenario | Base or named causal alternative |
| Timing | For each discounted item, value or represented-realization date and calculated discount factor or exponent; record valuation origin and applicable compounding, day-count, and rate basis once per artifact |
| Source or formula | Owning citation or reproducible expression |
| Result | Value at disclosed precision |

Before relying on the result, assert:

- one historical period ties from the filing to the selected earnings, cash-flow,
  book-value, or asset-value definition;
- for residual-income models, each explicit modeled period and continuing-state
  anchor reconciles beginning to ending selected common-equity book value, and
  any adjusted basis to reported common book value, under the clean-surplus
  relation above; earnings, OCI, and other direct-to-equity movements stay on
  that basis, and each earnings or book-value normalization has a quantified
  bridge without double counting or an assertion-tested reason it affects no
  modeled period;
- no cash flow that elapsed before the valuation date remains in the forecast;
- when a discrete continuing-value formula defines value at date `T` from a
  numerator flow represented one modeled interval later, that flow's recorded
  date equals `T + interval`, and its midpoint or year-end representation
  matches the numerator and discount factor; other continuing-value formulas
  use their formula-specific timing instead;
- CFO-derived FCFF reconciles financing interest, non-operating income, tax,
  capex, and classification without counting cash returns twice;
- the declared FCFF derivation and its filed-period bridge reproduce the
  applicable EBIT- or CFO-derived identity; no failed branch is silently blended
  or replaced;
- any admitted reported or guided cash-flow anchor material to the first
  forecast period has a quantified definition-and-timing bridge to modeled FCFF;
- cash, debt, claims, awards, and shares use one date or an explicit
  post-balance-sheet bridge;
- actual point-in-time common shares, not weighted-average EPS shares, own the
  per-security denominator;
- the enterprise-to-equity or asset-to-security bridge includes every material
  claim and only excess cash;
- existing awards and future grants reconcile without double counting;
- organic and acquired growth are distinguished when acquisitions materially
  affect the forecast base or stated growth;
- any historical payout or retention ratio used to anchor the forecast uses the
  same attributable earnings, distributions, and investee population as the
  forecast, or has a quantified bridge;
- every material contractual or potentially finite income stream has an
  explicit terminal or realization disposition as continuing, fading, or
  expiring; no finite stream continues into perpetuity by omission;
- growth, reinvestment, returns, terminal economics, and required returns are
  coherent, including `discount rate > growth` where applicable;
- each sensitivity point or case records every input or convention intentionally
  varied from the Lock, the applicable formulas or identities, and every linked
  quantity mechanically recomputed; it satisfies those identities and leaves
  every other locked input and convention unchanged;
- source variable definitions, signs, units, currency, fiscal periods, and
  timing match the Model Lock; and
- a separate calculation pass reproduces the locked result within the disclosed
  rounding.

Repair a failed deterministic assertion before interpretation or review.
Keep uncertainty classes separate: operating scenarios vary causally linked
business drivers while holding accounting, claim-bridge, non-operating-asset,
and required-return conventions fixed. Show defensible convention changes as
separate sensitivities unless the stated business scenario itself causes them
to change. Never blend alternatives into a mechanically inconsistent base.
