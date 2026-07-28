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
- valuation date, information cutoff, and market-price timestamp;
- requested horizon, whether value is present or future, method, depth, and
  output currency;
- whether the user supplied an explicit margin-of-safety rule; and
- material scope exclusions or unavailable sources.

Resolve harmless ambiguity from authoritative sources. Ask only when different
answers would value different securities or materially change the result.

## Load The Right References

- Always load [source-protocol.md](references/source-protocol.md) before
  collecting evidence.
- Always load [valuation-methods.md](references/valuation-methods.md) before
  selecting or calculating a method.
- Load [company-types.md](references/company-types.md) when choosing the model
  or handling a sector, life-cycle, or accounting exception.
- Load [report-contract.md](references/report-contract.md) before composing the
  answer.

## Valuation Spine

### 1. Establish The Evidence Date

Record the latest fiscal year, latest reported quarter, all material filings
and company updates after that quarter, the market-price timestamp, and the
publication date of every forward estimate. Use only information available by
the stated cutoff; never use later outcomes to make an earlier valuation appear
better informed. If current primary evidence is unavailable, stop numerical
valuation or return a clearly bounded partial analysis; do not fill gaps from
memory.

### 2. Explain The Business Economically

Identify revenue segments, customer and geographic concentration, pricing,
volume, unit economics, cost structure, capital intensity, reinvestment needs,
competitive advantages, industry structure, and key regulatory or commodity
exposures. Assess country and currency risk from revenue, production, assets,
funding, and legal exposure rather than incorporation or listing venue alone.
Connect each claimed advantage to observable evidence and a value driver such
as growth duration, margin, reinvestment efficiency, or risk.

### 3. Reconstruct And Normalize History

Use at least three to five annual periods when available and the latest
trailing period. Reconcile the income statement, balance sheet, cash-flow
statement, statement of equity, segment data, and footnotes.

Normalize only with an explicit bridge. Examine:

- acquisitions, divestitures, discontinued operations, restructuring, and
  genuinely non-recurring items;
- stock-based compensation, future grants, dilution, buybacks, options,
  warrants, convertibles, and other claims on common equity;
- capitalized versus expensed investment, including R&D where material;
- leases, pensions, minority interest, preferred claims, and off-balance-sheet
  commitments;
- working-capital swings, maintenance versus growth capex, taxes, and cyclicality;
- GAAP or local-GAAP results versus management-defined non-GAAP measures;
- per-share growth versus aggregate growth;
- receivables, inventory, reserves, capitalized costs, related-party activity,
  auditor changes, and internal-control weaknesses when material; and
- capital allocation at the prices and terms actually paid, not merely the
  amount spent.

Show revenue growth, margins, cash conversion, ROIC or the appropriate sector
return measure, incremental returns when supportable, leverage, interest
coverage, reinvestment, and share-count change. A high growth rate is not value
creation unless its return on incremental capital exceeds its opportunity cost.

### 4. Build A Driver Forecast

Forecast business drivers before earnings:

```text
market or unit volume x share x price
-> revenue
-> operating margin
-> after-tax operating profit
-> reinvestment
-> free cash flow
```

Anchor near-term ranges to reported backlog, contracts, capacity, company
guidance, consensus estimates, and industry evidence, while labeling each
source and recording estimate date, dispersion, and revisions when available.
Align fiscal and calendar periods, model any stub period explicitly, and avoid
mixing next-twelve-month and next-fiscal-year inputs. Fade growth, margins, risk,
and returns toward economically coherent steady-state levels. Make growth
consistent with reinvestment and returns on capital. Do not extrapolate a
temporary margin, tax rate, commodity price, or working-capital benefit forever.

Construct bear, base, and bull cases from distinct causal assumptions. Do not
create cosmetic percentage offsets. Assign probabilities only when evidence
supports them; otherwise present unweighted cases. Make assigned probabilities
sum to 100%. Map each risk explicitly and do not hide the same adjustment in
scenario odds, a cash-flow haircut, and a discount-rate premium. Reserve the
margin-of-safety threshold for residual valuation and decision uncertainty.

### 5. Choose Methods By Economics

Use the model-selection matrix in `company-types.md`. For a typical
non-financial operating company, default to:

1. FCFF DCF for intrinsic value;
2. reverse DCF to expose what the current price implies; and
3. a fundamentals-controlled comparable valuation as a market-pricing
   cross-check.

Add or substitute FCFE, DDM, residual-income or excess-return, NAV, SOTP,
normalized mid-cycle, liquidation, or probability-adjusted methods when the
business requires them. Never force P/E, EBITDA, or a standard FCFF model onto a
company for which the denominator or capital structure has no economic meaning.

### 6. Calculate And Audit

- Match cash flow to discount rate, currency, inflation basis, and claim holder.
- Bridge enterprise value to the exact target security completely. When
  material, value employee options, warrants, and conversion rights as separate
  claims on equity; use a fully diluted share-count shortcut only as a disclosed
  approximation that handles exercise proceeds consistently.
- Match discount timing to cash-flow timing. Use a disclosed midyear convention
  only for cash generated through the year; use actual or explicit timing for
  discrete events and stub periods.
- Keep terminal growth below the matching discount rate and consistent with
  long-run economic limits. Make terminal reinvestment and returns coherent.
- Treat an exit multiple as relative valuation, not an intrinsic terminal value.
- Show sensitivities for the assumptions that actually drive value.
- State formulas, units, dates, source cells or lines, and calculation choices
  sufficiently for another analyst to reproduce the result.
- Run arithmetic, sign, unit, period, and identity checks. Reconcile historical
  values back to the filings before trusting forecasts.
- If reporting a future fair value, do not compare it directly with today's
  price as current upside. Show the horizon and either discount it to present
  value or calculate a cash-distribution-consistent annualized return.

Do not mechanically average methods. Explain disagreements: intrinsic value and
relative value answer different questions and may diverge because a peer group
or entire sector is mispriced.

### 7. Interpret Forward Multiples Carefully

Use forward P/E only with positive, sustainable, consistently defined forward
diluted EPS and a named forecast period and source. Interpret it through growth,
growth duration, risk, payout or reinvestment, and return on equity.

Use PEG only as a contextual cross-check among sufficiently comparable firms.
State the P/E basis, growth metric, horizon, and percent convention. Do not use
PEG with negative or near-zero growth, treat `PEG < 1` as a law, or assume PEG
fully controls for risk, payout, or reinvestment quality.

Apply the same denominator definition and time basis to the target and peers.
Select peers by similar cash-flow economics, growth, risk, margins, capital
intensity, and geography - not industry label alone.

### 8. Process Earnings, Guidance, News, And Sentiment

Maintain a dated guidance ledger: original metric and range, later revisions,
reported outcome, and management explanation. Compare like-for-like definitions.
Use this to assess forecasting evidence and execution, not character.

For each material news item or transcript change, classify it as:

- new fundamental information that changes cash flow, reinvestment, or risk;
- a catalyst or timing signal that may close a price-value gap;
- market sentiment or positioning with no demonstrated value change; or
- duplicate or immaterial noise.

Do not double-count one event across guidance, news, and scenarios. Treat tone,
evasion, analyst questions, and social sentiment as hypotheses requiring
corroboration. Positive language is not intrinsic value.

### 9. Challenge The Thesis

Use a pre-mortem. Identify the assumptions carrying the most value, evidence
against them, base rates or relevant history, accounting red flags, financing
or dilution paths, competitive responses, and observable thesis breakers.
Compare the modeled expectations with those implied by the market price.

Compute:

```text
price-to-value gap = (estimated value - market price) / estimated value
```

Call this a margin of safety only when the user or a stated policy supplies the
required threshold. Otherwise report `margin of safety: not assessed - threshold
not supplied`; do not characterize the gap as an adequate, inadequate,
meaningful, or absent margin of safety, and do not substitute equivalent
`cushion` language. Explain instead how valuation uncertainty, balance-sheet
risk, business fragility, diversification, and catalyst uncertainty should
inform a user-chosen threshold.

## Return

Follow `report-contract.md`. Lead with the valuation range, current price and
timestamp, price-implied expectations, confidence, and the two or three
assumptions that dominate the result. Cite every material current fact and
number adjacent to its claim.

Return `complete`, `partial`, or `blocked`.

- `complete`: current evidence, applicable methods, calculations, challenges,
  and citations satisfy the contract.
- `partial`: useful analysis is possible, but named data or a method is
  unavailable; narrow the claims and state the effect.
- `blocked`: security identity, current primary evidence, or a load-bearing
  input cannot be resolved without fabricating a result.

Complete only when the result is reproducible; model choice fits the company;
reported, estimated, guided, and assumed values remain distinct; valuation
differences are reconciled; uncertainty and thesis breakers are visible; and
the answer does not outrun the evidence.
