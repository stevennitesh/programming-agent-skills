# Source Protocol

Use this protocol for a live public-stock valuation. Adapt filing names and
regulators to the issuer's jurisdiction.

## Contents

- [Source Hierarchy](#source-hierarchy)
- [Minimum Evidence Packet](#minimum-evidence-packet)
- [Evidence Ledger](#evidence-ledger)
- [Structured Filing Data](#structured-filing-data)
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

For U.S. issuers, start with the latest 10-K, subsequent 10-Q, every material
later 8-K, the latest proxy, and filed earnings exhibits. The SEC explains that
a 10-K covers the business, risks, and annual operating and financial results;
10-Q statements are quarterly and unaudited; and 8-Ks disclose major current
events. Read MD&A and footnotes, not just headline statements:

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

## Minimum Evidence Packet

Collect and date:

- latest annual and interim filings plus material later event filings;
- at least three to five years of statements and segment history when available;
- the latest earnings release, call transcript, guidance, and investor deck;
- proxy data relevant to dilution, compensation, ownership, and governance;
- current price, share classes, ADR ratio, actual and diluted shares, security
  rights, debt, cash, options, warrants, convertibles, and other equity claims;
- relevant rates, commodity prices, foreign exchange, or industry drivers;
- peer filings and date-consistent market data;
- consensus estimates with provider, as-of date, period, and definition; and
- material news since the latest reported period plus older unresolved events.

Record access failures. Do not silently replace a missing primary source with an
aggregator.

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

Numerical citations must support the exact number, period, and definition. If
two sources disagree, prefer the owning primary source or preserve the conflict.

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

## Earnings And Guidance

Create a chronological ledger for explicitly guided metrics:

| Guidance date | Metric and definition | Original range | Revision | Outcome | Status | Explanation |
| --- | --- | --- | --- | --- | --- | --- |

Never turn qualitative aspiration into numerical guidance. Distinguish constant
currency, organic, adjusted, and GAAP measures. Reconcile management-defined
metrics to the nearest reported measure when possible. The SEC requires
attention to prominence and reconciliation for non-GAAP measures and explains
special limits for forward non-GAAP reconciliation:

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

Use transcript tone longitudinally and in context. Compare guidance revisions,
specificity, qualifiers, Q&A evasiveness, and subsequent delivery. Generic
positive/negative word counts are fragile in finance; domain-specific language
and corroborating quantitative evidence are stronger. Research shows that text
tone can contain information, but effects and interpretations vary:

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
