# Valuation Methods

## Contents

- [Method Principles](#method-principles)
- [Future-Date Valuation](#future-date-valuation)
- [FCFF DCF](#fcff-dcf)
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
- [Audit Checklist](#audit-checklist)

## Method Principles

Value cash flows to the correct claim holder at a matching required return.
Keep currency, inflation basis, tax treatment, and timing consistent. Prefer a
range tied to causal cases over a false-precision point estimate.

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

Discount FCFF at WACC using market-value capital weights and a cost of capital
consistent with the cash-flow currency. Do not use a stale universal risk-free
rate, equity risk premium, beta, or debt spread.

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

Reconcile the clean-surplus relation: ending common book value should equal
beginning book value plus comprehensive income attributable to common less
dividends and repurchases plus issuances, with other direct-to-equity changes
identified. Adjust book value and earnings consistently for material accounting
distortions, write-offs, reserve changes, acquisitions, and other-comprehensive-
income items. Pair the model with justified P/B or P/TBV, asset quality, and
capital adequacy:
[CFA Institute: Residual Income Valuation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/residual-income-valuation).

## Relative Valuation

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

Use consistent forward or trailing periods for target and peers. Prefer medians
when outliers are material, but inspect the distribution. A comparable is
similar in growth, risk, and cash-flow economics, not merely sector label:

- [Damodaran: What is a comparable firm?](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/comparables.htm)
- [Controlling for differences](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/controldifferences.htm)

Relative valuation can show cheapness versus peers while the whole group remains
overvalued. Preserve disagreements with intrinsic value rather than averaging
them away:
[Reconciling DCF and relative valuation](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/littlebook/reconcilingdcfandrelative.htm).

## Forward P/E

Define explicitly:

```text
forward P/E = current equity price / forecast diluted EPS for a named period
```

State whether the denominator is next fiscal year, next twelve months, GAAP, or
adjusted; name the estimate source and date. A P/E is not meaningful with
negative earnings. Its fundamental drivers include growth, risk, payout or
reinvestment, and return on equity:
[Damodaran: Price Earnings Ratio](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/invfables/peratio.htm).

Compare forward P/E only with the same earnings definition and horizon. Rebase
historical comparisons for changed rates, business mix, leverage, accounting,
tax, margins, or growth duration.

## PEG

Define the convention, commonly:

```text
PEG = forward P/E / expected annual EPS growth expressed as a whole percent
```

Example: `P/E 20 / growth 10 = PEG 2.0`, not `20 / 0.10`.

Use the same EPS definition and a matched growth horizon. Do not use PEG for
negative, near-zero, highly cyclical, or one-off-recovery growth. `PEG < 1` is
not a universal bargain rule. PEG does not fully control for risk, payout,
growth quality, or the nonlinear relationship between growth and value:
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
uncertain valuation, not another valuation method. Report its pass/fail only
when the user or a stated policy supplies the hurdle. Without one, report the
observed discount and `required hurdle: not supplied; pass/fail: not assessed`.
Do not invent one threshold for every company or automatically print arbitrary
entry-price thresholds. A wider hurdle is generally warranted when value is
more uncertain, the balance sheet or business is fragile, terminal value
dominates plausible cases, or catalysts are weak. Diversification and the
source of uncertainty also matter:
[Damodaran: Margin of Safety](https://pages.stern.nyu.edu/~adamodar/pdfiles/blog/MOS.pdf).

## Audit Checklist

- Historical model ties to filed totals and segment disclosures.
- Formulas use consistent signs, scale, units, periods, and currency.
- Forecast drivers reconcile to revenue, margins, taxes, reinvestment, and cash.
- Growth is feasible relative to market size and capital needs.
- Discount rates match claim holder, currency, and inflation basis.
- Country risk follows operating and claim exposure and is not double-counted.
- Fiscal, calendar, stub-period, and discount timing are aligned.
- Terminal economics are internally consistent and economically sustainable.
- Enterprise-to-equity bridge includes every material non-operating claim.
- Options, warrants, convertibles, ADR ratios, and common shares reconcile to
  the exact security; any diluted-share shortcut is disclosed.
- Existing SBC awards and future grants are separated; cash-flow, claim-value,
  and diluted-share treatments do not count the same award cohort twice.
- A future-date value rolls forward cash, distributions, claims, and shares or
  is explicitly labeled as a required-return shortcut.
- Sensitivities change the intended inputs and preserve `discount rate > growth`.
- Scenario differences are causal; probabilities sum to 100% when used; risk
  adjustments are mapped and residual uncertainty is separated from them.
- Every material input is reported, estimated, guided, or assumed and cited.
