# JPMorgan Chase residual-income workflow proof

## Snapshot

- Security: JPMorgan Chase & Co. common stock, JPM on the NYSE; issuer CIK 0000019617; USD millions except per-share value.
- Valuation date and information cutoff: 2026-02-13. Latest balance-sheet date: 2025-12-31.
- Supported base value: **$171.85061696 per common share**. No causal fair-value range was established from this one base scenario.
- Market price: not used. Required margin-of-safety hurdle: not supplied; pass/fail: not assessed.
- Confidence: medium-low. Valuation status: **partial** because future income, distributions, repurchases, required return, and continuing ROE are explicit analyst assumptions rather than a causal scenario range.

## Load-bearing valuation

Residual income fits a regulated financial firm whose book value and common earnings are meaningful while industrial FCFF would misclassify financing activity. The admitted Model Lock starts from reported common equity, uses a 10% common-equity required return, forecasts $56.0 billion of FY2026 common income and 15% FY2027 ROE, includes dividends plus net repurchase/direct-equity adjustments in the clean-surplus roll-forward, and fades to 12% continuing ROE with 3% growth.

Receipt status: `pass`; input identity: `sha256:8a15ed39fde124da2c1f67df44101ea8a245642f8b50986bfb95321754f13f04`; calculation path: `residual-income-contract-v2`.

Material arithmetic: receipt only; not manually reproduced.

The authoritative receipt reports beginning common book value `342393`, forecast residual-income present value `34699.21973896`, terminal present value `86251.41371395`, target common equity `463343.63345292`, diluted shares `2696.2`, and per-share value `171.85061696`. Its objective diagnostics report a `0.07` required-return/growth spread and `0.18614999` terminal-value share. Those diagnostics remain evidence for analyst judgment only.

## Material evidence and gates

JPMorgan Chase's 2025 Form 10-K identifies JPM common stock on the NYSE and reports $342.393 billion of common stockholders' equity and 2.6962 billion common shares at year-end. It reports 2025 net income applicable to common equity of $55.949 billion and $5.80 of cash dividends declared per common share. [JPMorgan Chase 2025 Form 10-K](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2025/4th-quarter/corp-10k-2025.pdf)

The filing also reports $31.640 billion of 2025 common-stock repurchases. The Model Lock uses separate assumed net direct-equity adjustments of negative $30.0 billion in FY2026 and negative $25.0 billion in FY2027 so repurchases are not omitted from clean surplus or counted as dividends. [JPMorgan Chase 2025 Form 10-K](https://www.jpmorganchase.com/content/dam/jpmc/jpmorgan-chase-and-co/investor-relations/documents/quarterly-earnings/2025/4th-quarter/corp-10k-2025.pdf)

- Gate 1, As-Of: partial. Security identity and filing cutoff pass; year-end book value and shares are carried to filing date under explicit unchanged-through-cutoff estimates.
- Gate 2, Accounting-Identity: pass. Common equity and common income match the residual-income target claim.
- Gate 3, Security-Claim: pass for the common pool and point-in-time share denominator; preferred stock is excluded by starting from reported common equity.
- Gate 4, Economics-And-Reproduction: partial. Every modeled period rolls beginning book to ending book through income, dividends, and direct-equity adjustments, and all deterministic assertions pass; future ROE and capital return remain assumptions.
- Gate 5, Horizon-And-Decision: partial. Present value is identified, but no authoritative price or causal scenario range was included.

Intervening-event sweep: the 2025 Form 10-K filing and issuer filing notice were checked through the 2026-02-13 cutoff. No separate event was admitted that removed the stated filing-date bridge assumptions. [SEC filing detail](https://www.sec.gov/Archives/edgar/data/19617/0001628280-26-008131-index.htm)

## Thesis breakers

- Credit losses or capital requirements that hold common ROE below the modeled path would reduce residual income.
- Repurchases above the modeled direct-equity adjustment without matching earnings would reduce ending book value.
- A higher common-equity required return or faster fade toward it would reduce value.

This is impersonal research and workflow proof, not personalized investment advice.
