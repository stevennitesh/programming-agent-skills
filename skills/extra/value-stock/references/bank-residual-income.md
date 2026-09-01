# Bank residual-income route

Read this reference after selecting residual income for a bank or another
regulated financial firm whose common-equity book value and earnings basis are
meaningful. The active repository's valuation methodology and residual-income
contract own field shapes, formulas, versions, and supported operations. This
reference orders the analyst work; it does not create a second calculation path.

## Close the opening state

Use one matched basis throughout: reported common equity with ROE, or tangible
common equity with ROTCE. Reconcile multiple historical periods on that basis
and preserve reported and normalized earnings separately. Each normalization
needs exact semantic support for its amount, tax, common attribution, accounting
location, recurrence, and intended use.

Bridge selected equity from the latest admitted balance-sheet date to the
valuation date. Disposition interim common earnings, owner distributions,
issuance, employee equity, AOCI, other direct effects, and basis changes. Keep
exact, finite-bound, directional-bound, and unresolved outcomes distinct.

Map every stub and forecast period with explicit start, end, economic duration,
earnings convention, and realization timing. State whether a partial-period ROE
or ROTCE is period-specific or explicitly annualized. Never apply a full-year
return or equity charge to an irregular period by omission.

## Build the forecast foundation

Obtain a typed foundation disposition for every forecast period before freezing
the Model Lock. For a bank, bridge the material company-specific drivers such as
net interest income, noninterest revenue and expense, credit costs, taxes,
preferred distributions, owner distributions, direct-equity movements, and
capital constraints into common earnings, selected equity, and implied ROE or
ROTCE. Evidence, an explicit company-specific assumption, a finite bound, or an
exact gap must support each material driver. Code reproduces the bridge; the
analyst selects and calibrates it.

A passed foundation supports its declared point path. A finite bound remains a
bound, and a gap prevents that period from supporting a complete forecast. A
sealed Evidence Pack, accepted lock, generic bank narrative, or mechanically
passed base calculation does not promote the foundation.

## Reconcile claims and required return

Reconcile actual common shares through the information cutoff. A pre-cutoff
observation needs affirmative event coverage, including evidenced no-event
coverage when applicable. Preserve exact, interval, directional, and unresolved
share-event outcomes; do not collapse a bound into a point denominator.

Build common cost of equity through the public equity-rate path. Match each
component to its concept, value, unit, date, evidence class, and intended use.
Use the selected receipt in forecast and terminal periods. Do not substitute
WACC, an unrelated admission, or the model rate as a decision hurdle.

## Run the public calculation path

Use the repository's current public sequence:

1. call `seal_evidence_pack()` for intrinsic evidence;
2. run `reconcile_common_equity_claims()`,
   `reconcile_residual_income_history()`, and
   `reconcile_residual_income_opening_bridge()`;
3. run `build_common_equity_cost_of_equity()` and
   `build_residual_income_forecast_foundation()`;
4. call `freeze_residual_income_model_lock()` and shared `calculate()`;
5. use `author_residual_income_scenario()` for causal cases, then run only the
   requested or conclusion-changing scenario, sensitivity, composition, and
   price-implied public operations;
6. calculate the typed `as_of_ptbv` market-context lanes when price or relative
   valuation is in scope; and
7. call `assemble_valuation_report()` with every requested branch disposition.

Use P/TBV only with synchronized common market capitalization and normalized
TCE. Preserve role-specific evidence for whole-firm competitors, segment
competitors, and economic peers. Enforce cohort adequacy, honest industry-
universe completeness, and cutoff-valid price, TCE, and ROTCE timing.
Broad-market P/E may correctly be nonblocking `not_comparable`; it supplies no
bank P/TBV ratio or fabricated membership evidence.

## Keep ranges and reverse results honest

Only a passed causal scenario receipt can support a causal fair-value range. A
favorable or adverse parameter bundle is a sensitivity or analytically partial
case unless named bank causes, calibrations, transmissions, and held-fixed
conventions support every material changed driver.

Treat reverse ROTCE or another price-implied solve as conditional on its fixed
inputs, bounds, and declared transform. Report solution-set completeness and do
not call one solved path the market's unique belief.

When material, retain separate sensitivity receipts for common cost of equity,
terminal ROTCE or ROE, terminal growth, one explicit forecast-period return,
and an alternative passed share case. Sensitivity endpoints do not define a
causal range.

## Close the request

Before a supported verdict, assemble the active report and disposition every
requested or conclusion-bearing foundation and branch. Base, scenario,
sensitivity, price-implied, and market-context receipts are intermediate. The
pinned false-complete JPM pattern remains `partial` or `blocked` when timing,
normalization, share coverage, cost of equity, forecast foundation, preserved
market artifacts, peer roles, adequacy, or industry-universe support is missing,
even if its calculators pass.

Allow correct `not_applicable` and nonblocking `not_comparable` lanes without
forcing `partial`. Do not use that exception for missing evidence or unsupported
comparison claims. A supported verdict requires passed report assembly under the
repository's method-specific completion disposition. Persistence and audit
follow only when separately requested.
