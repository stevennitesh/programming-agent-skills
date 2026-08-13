# Finance and Market Backtesting

Read this file only when model output is evaluated through a historical
securities or portfolio simulation, or is intended to influence a security or
portfolio market action. This branch extends the common data, evaluation,
testing, promotion, operation, and risk contracts in `SKILL.md`. Execute every
matching section here and in `EVALUATION-BRANCHES.md`; recurring-origin and
other universal time-series controls remain there. Do not require execution or
portfolio machinery for a prediction-only claim that does not simulate or imply
tradability, returns, allocation, or market action.

## Freeze the point-in-time market population

For every decision time, recover the matching facts:

- the historically eligible universe under the declared selection rules;
- when the claim depends on investability or tradability, the historically
  investable subset after instrument status, venue, session, price, liquidity,
  borrow, funding, and portfolio constraints;
- stable security and listing identities plus effective-dated mappings across
  symbols, listings, share classes, exchanges, mergers, acquisitions, and
  spin-offs; and
- the decision calendar, timezone, source vintage, retrieval or as-of time, and
  availability time observed by the historical decision process.

Do not construct the universe from current constituents or surviving vendor
records. Preserve delisted, acquired, bankrupt, renamed, and otherwise
terminated instruments when they were eligible at the decision time.

Define terminal treatment from governing instrument and event evidence.
Include applicable delisting returns, cash or stock consideration,
distributions, and final position or cash settlement. Do not silently drop a
terminal instrument, carry its last quote indefinitely, or assign zero merely
because terminal evidence is missing.

Represent corporate actions consistently across prices, quantities, positions,
cash flows, features, and outcomes. State whether each series is raw or adjusted
and prevent double counting of splits, dividends, distributions, rights,
spin-offs, mergers, and other consideration. Respect announcement, effective,
ex-, record, payment, and system-availability times as applicable.

For vendor and fundamental data, bind every value to its provider, dataset
version or snapshot, filing or release identity, publication time, observed
availability time, and applicable revision or restatement vintage. Do not use a
latest revised value as though it were historically available.

If point-in-time eligibility, identity, terminal treatment, corporate-action
treatment, or a load-bearing vintage cannot be reconstructed, report the
affected investability, survivorship, or economic claim as `unknown`. Preserve
descriptive results with the limitation, but block the dependent unbiased,
point-in-time, executable, or comparable claim.

## Separate opportunity, execution, and outcome state

Execute this section when a simulation or claim depends on whether a prediction
or intended market action becomes an order, fill, or realized outcome.

Use project-native records with stable identities and these meanings:

- **Opportunity:** a rule-admitted prediction or decision candidate at its
  decision time, before execution is known.
- **Order:** an authorized instruction derived from an opportunity, including
  instrument, side, quantity or target, order type, limit, submission time,
  expiry, and policy identity.
- **Fill:** executed quantity with execution time, price, venue or price source,
  and applicable costs. A partial fill records its executed quantity and leaves
  the residual explicitly unfilled.
- **Mature outcome:** an outcome whose declared horizon, terminal events,
  attribution rule, and required source arrivals or revisions have completed.

Keep opportunity availability, fill availability, and outcome availability as
separate facts. A no-fill remains in opportunity identity, the prediction
denominator, and fill or coverage denominators. It is not a loss or a win. When
the target is realized trade outcome, exclude the no-fill from outcome fitting
and realized-trade metrics rather than inventing an outcome. A separately
defined hypothetical market outcome is a different label and requires its own
point-in-time and execution assumptions.

Retain filled but immature observations with outcome availability false until
maturity. Exclude unavailable outcomes from fitting and outcome metrics without
removing their opportunity or execution identity.

## Reconcile signal to portfolio economics

Execute this section when a simulation or claim depends on executable trading,
positions, cash, portfolio returns, or capacity.

Trace the complete economic chain:

```text
signal or prediction -> decision or target -> order -> fill
-> position and cash state -> portfolio net outcome
```

Bind every transition to its policy, instrument, timestamp, quantity and unit
or notional, price and quote convention, currency, and portfolio identity.
Where applicable, bind the effective-dated multiplier or conversion and
exercise, expiry, and settlement terms. Do not translate a prediction metric
directly into a tradable-return claim.

For each order and fill, define the decision timestamp, information cutoff,
latency, market session, order type and lifetime, and executable-price rule. Do
not fill at a bar or quote that helped establish the signal unless availability,
latency, and order assumptions make that execution possible. Handle closed
markets, halts, limits, missing quotes, and stale prices explicitly.

Apply, as material:

- commissions, exchange, regulatory, clearing, and other fees;
- bid-ask spread, slippage, market impact, and price improvement;
- borrow availability, borrow fees, recalls, buy-ins, and short constraints;
- cash interest, margin, financing, and funding costs;
- partial fills, rejected orders, cancellations, and residual quantities; and
- currency conversion and cash-flow timing.

Reconcile fills into positions, realized and unrealized value, income and
corporate-action cash flows, financing, and portfolio cash. Reject or mark
invalid any result whose positions and cash do not reconcile under the declared
accounting rules.

Apply portfolio rules at the time they would bind: turnover, gross and net
exposure, concentration, leverage and margin, liquidity, volume participation,
borrow, cash, and capacity. A ranking or desired target is not an executable
portfolio when these rules reject or resize it.

## Report economic evidence at its actual level

Execute this section when reporting realized-trade, return, portfolio,
liquidity, or capacity evidence.

Keep opportunity-level prediction evidence, filled-trade evidence, and
portfolio-policy evidence distinct. Report fill and maturity coverage beside
dependent results.

Report gross results before trading and financing costs and net results after
all included fees, spread, slippage, impact, borrow, funding, and other declared
cash effects. Name every omitted material cost. Gross-only evidence cannot
support a net-economic claim.

Report applicable turnover, gross and net exposure, concentration, leverage,
liquidity, capacity, and drawdown alongside return. Do not extrapolate capacity
beyond the tested capital, participation, borrow, or market-depth conditions.

Stress assumptions capable of reversing the decision, including execution
timing, price, spread, slippage, impact, liquidity, partial fills, borrow,
funding, terminal events, and relevant portfolio limits. Bind each stress
result to its parameter set and candidate identity. Do not call a strategy
robust from an unstressed or gross-only result.

If executable prices, material costs, borrow or funding, position/cash
reconciliation, or binding portfolio constraints are unavailable, preserve
valid prediction or gross-hypothetical evidence but block the dependent net,
executable, portfolio, liquidity, or capacity claim.

## Escalate regulated decisions and market actions

Activate this gate when output will recommend, allocate, route, submit, cancel,
execute, finance, borrow for, or automatically control a security or portfolio
market action, or when an owner-provided policy classifies the decision as
regulated.

Recover rather than infer the jurisdiction, instrument and venue, operator and
account roles, proprietary or client context, discretion and automation,
affected parties, governing sources, organizational policy, accountable owner,
approval path, and specialist escalation route.

Do not make a legal or regulatory applicability conclusion. When applicability,
permission, controls, or owner acceptance is unresolved, block only the
dependent recommendation, market action, promotion, automation, or compliance
claim. Continue valid read-only, offline, or descriptive work.

Return one bounded handoff to the applicable legal, compliance,
market-structure, execution, or financial-risk specialist. Name the exact
question, decision context, applicable date and owner-supplied jurisdiction,
governing sources already inspected, supported evidence, blocked action or
claim, and MLE as return owner. Source research may supply evidence; it does not
decide applicability or authorize an action.

## Complete this branch

Complete each activated section only when its listed evidence reads back
consistently. For the matching sections:

- point-in-time universe, security identity, corporate actions, terminal
  treatment, load-bearing data vintages, and—when claimed—investability are
  bound to the result;
- opportunity, order, fill, position, cash, and mature-outcome identities and
  availability states read back consistently;
- timing, executable-price, partial-fill, cost, borrow, funding, and portfolio
  rules are explicit and the accounting reconciles;
- opportunity, filled-trade, gross, net, portfolio, and stress claims are
  separated and calibrated to their evidence;
- turnover, exposure, concentration, leverage, liquidity, and capacity claims
  are supported at their declared conditions; and
- every triggered market-action or regulated-decision gate has an accountable
  owner and either supported authority or an exact specialist handoff.

Otherwise report the branch disposition, preserve independent supported MLE
results, and name each blocked economic claim or transition to the root Return
owner. A prediction-only finance Review can complete without order, fill,
position, cash, investability, or portfolio evidence when it makes no dependent
economic or market-action claim.
