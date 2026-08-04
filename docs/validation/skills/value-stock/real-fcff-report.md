# Alphabet FCFF workflow proof

## Snapshot

- Security: Alphabet Inc. common economic pool, represented by Class A GOOGL on Nasdaq; issuer CIK 0001652044; USD millions except per-share value.
- Valuation date and information cutoff: 2026-02-05. Latest balance-sheet date: 2025-12-31.
- Supported base value: **$77.53553524 per common share**. No causal fair-value range was established from this one base scenario.
- Market price: not used. Required margin-of-safety hurdle: not supplied; pass/fail: not assessed.
- Confidence: low. Valuation status: **partial** because the short forecast, excess-cash estimate, filing-date bridge, and unvalued existing-award claim can materially move value.

## Load-bearing valuation

FCFF fits Alphabet's non-financial operating business and values the common economic pool shared by its three economically equivalent common classes. The admitted Model Lock uses two derived forecast periods, a 9% USD WACC, 17% normalized operating tax rate, 3% terminal growth, and an $80.0 billion excess-cash estimate. These are analyst assumptions, not facts selected by the calculator.

Receipt status: `pass`; input identity: `sha256:9936733095cb3e8d2cde8bf452edf0f9d54b15234b8904752f2cf1164c016d43`; calculation path: `fcff-contract-v1`.

Material arithmetic: receipt only; not manually reproduced.

The authoritative receipt reports enterprise value `906334.5500365`, target common equity `937249.5500365`, diluted shares `12088`, and per-share value `77.53553524`. Its objective diagnostics report a `0.06` discount-rate/growth spread and `0.92690481` terminal-value share. The high terminal share lowers confidence; it did not alter any input or status mechanically.

## Material evidence and gates

Alphabet's 2025 Form 10-K identifies the issuer and GOOGL/GOOG listings, reports 2025 operating income of $129.039 billion, and reports 12.088 billion issued and outstanding Class A, B, and C shares. It also reports $126.843 billion of cash, cash equivalents, and marketable securities and $49.085 billion face value of long-term debt. [Alphabet 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm)

The filing reports $91.447 billion of 2025 capital expenditures and $21.1 billion of depreciation; management also stated that 2026 technical-infrastructure investment was expected to increase significantly. That evidence anchors the deliberately heavy 2026 reinvestment assumption rather than supplying a forecast chosen by code. [Alphabet 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm)

- Gate 1, As-Of: partial. Security identity and filing cutoff pass; balance-sheet claims are carried to filing date under explicit unchanged-through-cutoff estimates.
- Gate 2, Accounting-Identity: pass for an EBIT-derived FCFF base. The calculator derives both forecast FCFF values from EBIT, tax, depreciation, capex, and working-capital inputs.
- Gate 3, Security-Claim: partial. Actual year-end shares and debt are identified, but existing awards are not separately valued.
- Gate 4, Economics-And-Reproduction: partial. The receipt reproduces and all deterministic assertions pass, while the short forecast and infrastructure reinvestment path remain economically uncertain.
- Gate 5, Horizon-And-Decision: partial. Present value is identified, but no authoritative price or causal scenario range was included.

Intervening-event sweep: the filing and same-day fiscal-year release were checked from the 2025-12-31 balance sheet through the 2026-02-05 cutoff. No separate event was admitted that removed the stated bridge assumptions. [Alphabet fiscal 2025 results](https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Fourth-Quarter-2025-and-Fiscal-Year-Results-2026-KEvZIMKBLS/default.aspx)

## Thesis breakers

- Capital expenditures staying near or above the modeled level without the modeled EBIT conversion would reduce FCFF.
- A higher required return or shorter excess-return duration would reduce terminal value, which carries most of this base result.
- A lower excess-cash amount or material award claim would reduce common value per share.

This is impersonal research and workflow proof, not personalized investment advice.
