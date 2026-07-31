# Source Protocol

Use this protocol for a live public-stock valuation. Adapt filing names and
regulators to the issuer's jurisdiction.

## Contents

- [Source Hierarchy](#source-hierarchy)
- [Market-Price Evidence](#market-price-evidence)
- [Minimum Evidence Packet](#minimum-evidence-packet)
- [Full Diligence Expansion](#full-diligence-expansion)
- [Evidence Ledger](#evidence-ledger)
- [Structured Filing Data](#structured-filing-data)
- [Transformed Issuers](#transformed-issuers)
- [Earnings And Guidance](#earnings-and-guidance)
- [News And Sentiment](#news-and-sentiment)
- [Freshness And Stopping](#freshness-and-stopping)

## Source Hierarchy

Prefer the source that owns the claim:

1. securities-regulator filings and audited financial statements;
2. company-filed earnings exhibits, investor-relations releases, presentations,
   transcripts, and explicit guidance;
3. official government, regulator, exchange, and industry data;
4. identified consensus or estimate datasets with dates and definitions;
5. reputable reporting for independent context and event verification;
6. aggregators, search snippets, newsletters, and social media for discovery or
   sentiment only.

For U.S. issuers, start with the latest 10-K, subsequent 10-Q, material later
8-Ks, and filed earnings exhibits. Inspect the latest proxy when compensation,
dilution, governance, ownership, or security rights are material. The SEC
explains that a 10-K covers the business, risks, and annual operating and
financial results; 10-Q statements are quarterly and unaudited; and 8-Ks
disclose major current events. Read MD&A and footnotes, not just headline
statements:

- [SEC: How to Read a 10-K](https://www.sec.gov/answers/reada10k.htm)
- [SEC: Beginners' Guide to Financial Statements](https://www.sec.gov/about/reports-publications/beginners-guide-financial-statements)
- [Investor.gov: 8-K](https://www.investor.gov/introduction-investing/investing-basics/glossary/8-k)

For foreign private issuers, inspect the home-market filings plus applicable
20-F, 40-F, and later 6-K filings. For an ADR or ADS, inspect the Form F-6,
deposit agreement, and registered-security description for the ratio, fees,
voting, distribution, conversion, and withdrawal rights:

- [SEC: International Business Rules, Regulations and Forms](https://www.sec.gov/about/divisions-offices/division-corporation-finance/international-business-rules-regulations-forms)
- [SEC: Why the ADR deposit agreement matters](https://www.sec.gov/rules-regulations/2002/05/mandated-edgar-filing-foreign-issuers)

Treat company disclosures as primary evidence of what management reported, not
independent proof that the claim is correct. Treat news as primary evidence of
what the outlet reported, not of an underlying fact it did not independently
establish.

## Market-Price Evidence

Use an exchange or an authoritative market-data feed for a price that carries a
valuation conclusion. Record the exact security, quote currency, exchange,
field used (last trade, official close, or another defined field), timestamp,
and timezone. Use aggregators only to discover a stronger source or to assess
sentiment.

If authoritative current-price evidence is unavailable, a standalone intrinsic
fair-value estimate may still be complete when its own evidence gates pass.
Omit price-implied expectations, observed discount, and hurdle pass/fail, or
mark those specifically requested components `partial`; do not let a weak quote
own the claim.

## Minimum Evidence Packet

Answer length does not lower the evidence standard. Before calling a numerical
range fair value, collect and date enough owning evidence to establish:

- the exact security, valuation date, information cutoff, latest
  balance-sheet date, and a current-price timestamp when a price-dependent
  conclusion is requested;
- a date map for every historical period, forecast period, stub, discount
  midpoint, discrete event, and terminal or residual value, plus a bridge for
  material events between the latest balance sheet and valuation date;
- the latest annual filing, latest interim filing, and every later event known
  to be material to cash flows, risk, capital structure, or security claims;
- enough history to normalize the business and cover relevant economics -
  normally at least three annual periods, a full cycle for a cyclical business,
  or the available operating life for a young company;
- the normalized earnings, cash flow, asset value, or sector-specific value base
  used by the selected method, including taxes, reinvestment, and working
  capital when applicable;
- current cash, debt and debt-like claims, share classes, actual shares, and
  material dilution, options, warrants, convertibles, minority interests, or
  other claims needed to bridge value to the target security;
- explicit forecast anchors and the few causal drivers of revenue, margin,
  reinvestment, risk, or asset realization that carry the value;
- current method inputs such as risk-free rates, risk premia, borrowing costs,
  commodity or foreign-exchange assumptions, or comparable-market data when
  they are load-bearing; and
- material post-period developments, including guidance or news only to the
  extent that they can change those inputs, the selected method, or confidence.

Load earnings-call transcripts, investor decks, proxies, peer filings,
consensus, and broader news when they contain a load-bearing fact; they are not
universal ceremonial requirements. Record access failures. Do not silently
replace a missing primary source with an aggregator.

The main skill owns gate admission and safe failure. This packet supplies the
evidence for those gates; it does not turn missing evidence into a pass.

## Full Diligence Expansion

For a Full valuation, expand the minimum packet where available with:

- five or more years, a full relevant cycle, and detailed segment history;
- the latest earnings release, call transcript, investor deck, and a
  chronological company-guidance-versus-outcome ledger;
- proxy and compensation disclosures sufficient to reconcile stock-based
  compensation, outstanding awards, buybacks, and governance;
- date-consistent consensus history, dispersion, and revisions;
- fundamentals-controlled peer filings and market data;
- a deduplicated material-news record, unresolved older events, and
  corroborated transcript or sentiment evidence; and
- deeper accounting-quality, country-risk, industry, competitive, regulatory,
  and security-rights evidence where material.

Full means broader challenge and corroboration, not mandatory filler. Omit a
lane that cannot credibly affect value, range, confidence, or a thesis breaker,
and say why only when the omission would otherwise be surprising.

## Evidence Ledger

For every load-bearing item, preserve:

| Field | Requirement |
| --- | --- |
| Claim | Exact fact, estimate, guidance item, assumption, or calculation |
| Class | Reported / estimated / guided / assumed / calculated |
| Period | Fiscal period or forecast horizon |
| Published | Publication or filing date |
| As of | Observation date and time for market data |
| Available by | Confirmation that evidence predates the information cutoff |
| Unit | Currency, scale, per-share basis, nominal or real |
| Definition | GAAP/local GAAP or exact non-GAAP definition |
| Source | Direct URL and filing/section/table where practical |
| Confidence | High / medium / low with reason |

Place citations adjacent to each material current claim. Numerical citations
must support the exact number, period, and definition. If two sources disagree,
prefer the owning primary source or preserve the conflict.

## Structured Filing Data

Use regulator APIs, inline XBRL, and filing data tables to accelerate discovery
and reconstruct history, not as a substitute for reading the filing. Preserve
form, accession, period, context, unit, and tag. Check for custom tags, duplicate
contexts, amendments, restatements, fiscal-calendar mismatches, and facts that
apply to only a segment or class.

For material values, verify the extracted fact against the official HTML or text
filing and cite that filing. The SEC's APIs expose submissions and standardized
XBRL facts, but custom taxonomies and differing reporting dates limit mechanical
comparability; the SEC also directs users to the official filing for decisions:

- [SEC: EDGAR Application Programming Interfaces](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [SEC: Important Information About EDGAR](https://www.sec.gov/edgar/searchedgar/aboutedgar.htm)

## Transformed Issuers

Apply this branch only when owning public evidence shows a transaction or
operating change within the cutoff that makes admitted reported history
non-comparable with the forecast value or cash-flow base, or makes the ordinary
dated event bridge insufficient for the target claim. Do not trigger it from a
transaction label or size alone.

Keep reported actual, transaction-adjusted pro forma, and management guidance
separate by date, entity perimeter, definition, source, and assumptions. For
material applicable effects, build a dated old-to-new bridge covering
consideration and funding, accounting and tax, debt, shares and claims, retained
or divested assets and liabilities, and recurring versus finite synergies,
costs, and stranded obligations.

Use pre-change history only for matched legacy drivers or components; never
present it as combined actual. Admit combined normalization only from filed
actuals or a reproducible applicable identity-and-claim bridge. Pro forma or
guidance alone is not a conservative bound. Apply the main skill's
dependent-method `partial` or `blocked` policy when the new perimeter remains
incomplete.

## Earnings And Guidance

In Compact, inspect current guidance only when it is load-bearing. For Full, or
when guidance revisions or delivery history could materially change the model
or confidence, create a chronological ledger for explicitly guided metrics:

| Guidance date | Metric and definition | Original range | Revision | Outcome | Status | Explanation |
| --- | --- | --- | --- | --- | --- | --- |

Never turn qualitative aspiration into numerical guidance. Distinguish constant
currency, organic, adjusted, and GAAP measures. Reconcile management-defined
metrics to the nearest reported measure when possible. A management-defined
cash-flow measure proposed as a valuation base must meet the admission rule in
[Management-Defined And Analyst-Constructed Cash Flow](valuation-methods.md#management-defined-and-analyst-constructed-cash-flow).
The SEC requires attention to prominence and reconciliation for non-GAAP
measures and explains special limits for forward non-GAAP reconciliation:

- [SEC: Non-GAAP Financial Measures](https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations/non-gaap-financial-measures)

Use consensus to map outside expectations, not as truth. Compare management
guidance, consensus, the analyst's scenario, and market-implied expectations
without merging them. When available, record estimate breadth, dispersion,
revision direction, and the provider's treatment of stale estimates. Historical
surprise or delivery comparisons must use the estimate snapshot that existed
before the result, never a subsequently revised history.

## News And Sentiment

Use a defined window, normally from the latest reported quarter through the
valuation date, extended for unresolved material events. Deduplicate syndication
and trace stories back to filings, court records, regulator releases, or direct
statements.

For each event, ask:

1. What new fact became known?
2. Which forecast driver changes, by how much, and for how long?
3. Is this a cash-flow change, a risk change, a timing catalyst, or only tone?
4. Was the information already in price or prior guidance?
5. What evidence would falsify the interpretation?

When transcript tone is a selected evidence lane, evaluate it longitudinally
and in context. Compare guidance revisions, specificity, qualifiers, Q&A
evasiveness, and subsequent delivery. Generic positive/negative word counts are
fragile in finance; domain-specific language and corroborating quantitative
evidence are stronger. Research shows that text tone can contain information,
but effects and interpretations vary:

- [Tetlock: The Role of Media in the Stock Market](https://doi.org/10.1111/j.1540-6261.2007.01232.x)
- [Federal Reserve: News versus Sentiment](https://www.federalreserve.gov/econres/feds/news-versus-sentiment-predicting-stock-returns-from-news-stories.htm)

Social sentiment may indicate attention, crowding, or volatility. Never use it
as evidence of revenue, earnings, competitive advantage, or intrinsic value.

## Freshness And Stopping

Search until each load-bearing current claim has an owning source, conflicts are
preserved, and another credible source lane is unlikely to change the answer.
Stop earlier when the missing source is observable and blocks safe valuation.

Before returning, re-open citations for the exact identity, period, number, and
claim. Confirm that each item was public by the information cutoff. State the
market-data timestamp and any source that may update after the analysis.

When a publicly scheduled earnings release, filing, financing, vote, or other
load-bearing event is imminent, keep the valuation valid as of its cutoff but
label its shelf life unusually short and name the event and scheduled date.
