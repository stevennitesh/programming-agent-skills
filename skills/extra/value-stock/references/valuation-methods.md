# Valuation Methods

## Contents

- [Method Principles](#method-principles)
- [FCFF DCF](#fcff-dcf)
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

Present-value estimates and future target values are different outputs. If
returning a future value, state the horizon and translate it into present value
or an annualized return that includes modeled holder distributions:

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

Use the second definition when reporting the price-to-value gap in this skill.
Always name the formula because market practice varies.

A required margin of safety is a decision rule layered on an uncertain
valuation, not another valuation method. Do not invent one threshold for every
company. A wider cushion is generally warranted when value is more uncertain,
the balance sheet or business is fragile, terminal value dominates plausible
cases, or catalysts are weak. Diversification and the source of uncertainty also
matter:
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
- Sensitivities change the intended inputs and preserve `discount rate > growth`.
- Scenario differences are causal; probabilities sum to 100% when used; risk
  adjustments are mapped and residual uncertainty is separated from them.
- Every material input is reported, estimated, guided, or assumed and cited.
