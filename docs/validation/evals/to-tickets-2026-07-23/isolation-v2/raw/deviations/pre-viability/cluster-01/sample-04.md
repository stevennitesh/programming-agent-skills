# A — source-gap packet

- Evidence: settled source `SRC-N01@1`, parent `P-N01`, compatible setup, and frozen derived revision R41. Cara granted ordinary publication authority but did not review or authorize R41's derived ticket bodies or blocker edge.
- Tracker state: unchanged; `P-N01` has no children.
- Gap: current-revision authorization for bodies B1/B2, the B1 → B2 blocker edge, enhancement roles, ready states, execution profiles, state matrices, and intended mutations.
- Safe continuation: Cara reviews and explicitly authorizes the complete frozen R41 publication design. If anything changes, refreeze the resulting revision and obtain authorization for that exact revision before mutation.
- Recommendation: `none`.
- Simulated operation log:
  1. `get_setup` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists; no children.

# B — published graph

- Evidence: settled source `SRC-N01@1`; Cara reviewed and authorized frozen revision R41 as supplied; compatible setup; all simulated mutations and read-backs succeeded.
- Source/parent: `SRC-N01@1` / `P-N01`.
- Stable order: `I-N01-1` (B1), then `I-N01-2` (B2).
- Coverage map: C1 → B1; C2 → B2; expired-token failure → B1 acceptance and B2 boundary verification; second-redemption failure → B2 acceptance; delivery execution → explicit exclusion. No source-visible commitment is undisposed.
- Dependency graph: `I-N01-1` → `I-N01-2`; B2 consumes B1's issued-token outcome. Verified ready frontier: [`I-N01-1`].

## `I-N01-1` — Issue an expiring account-recovery token

- Work-unit form: bounded vertical behavior slice.
- Source Trace: `SRC-N01@1`, C1, expired-token acceptance, scope “token issue and redemption,” proof seam “recovery integration fixture,” parent `P-N01`.
- Desired behavior and acceptance: issuing account recovery creates a token with an expiry; the recovery integration fixture observes the token as redeemable before expiry and rejected after expiry. Expired-token redemption fails without granting recovery.
- Dependency state: true blockers `none`; tracker order 1.
- Proof lane: recovery integration fixture. Verification authority is Cara-owned source acceptance as exercised by that fixture. Required evidence is a passing issue/expiry integration case, including rejection after expiry and no recovery side effect.
- Expected durable write scope: only the account-recovery token record/state and its expiry metadata.
- Scope fence: excludes redemption consumption behavior, delivery execution, unrelated account/authentication state, and policy for multiple concurrent tokens because it is not settled by the source.
- Role/state: `enhancement`; `ready-for-agent`.
- Execution profile: semantic owner is account-recovery token issuance; production writes are limited to token and expiry state; scarce proof resource is the recovery integration fixture. It is ordered before B2 and is not parallel-safe with B2 because B2 consumes its outcome and both use the same token state and proof seam. Serial tripwires are token-state format, expiry semantics, or fixture-contract changes.
- State-boundary matrix:
  - Absent/initial: no recovery token; successful issue transitions to an active expiring token.
  - Current reusable: an active token is the output consumed by B2; behavior for issuing while one already exists is not source-settled and is fenced out.
  - Legacy/incompatible: none identified; no migration is authorized.
  - Public access path: the account-recovery issue path.
  - Supported variants: newly issued active token and its expired state only.
  - Lifecycle: absent → active; active → expired by time. No expand-migrate-contract sequence is required by the evidence.

## `I-N01-2` — Redeem an account-recovery token once and consume it

- Work-unit form: bounded vertical behavior slice.
- Source Trace: `SRC-N01@1`, C2, expired-token and second-redemption acceptance, scope “token issue and redemption,” proof seam “recovery integration fixture,” parent `P-N01`.
- Desired behavior and acceptance: a valid active token grants recovery once and is consumed atomically; a second redemption fails and grants no recovery; an expired token fails and remains unusable.
- Dependency state: blocked by `I-N01-1`; tracker order 2. The edge is true because this slice consumes B1's issued active-token outcome.
- Proof lane: recovery integration fixture. Verification authority is Cara-owned source acceptance as exercised by that fixture. Required evidence is one successful redemption followed by a rejected second redemption, plus rejected expired-token redemption, with no recovery side effect on either rejection.
- Expected durable write scope: only consumption state for the recovery token and the recovery state change directly authorized by successful redemption.
- Scope fence: excludes token issuance, delivery execution, unrelated authentication behavior, token migration, and unspecified malformed/absent-token policy.
- Role/state: `enhancement`; `ready-for-agent`.
- Execution profile: semantic owner is single-use redemption/consumption; production writes are token-consumption state and the directly authorized recovery transition; scarce proof resource is the recovery integration fixture. It follows B1 and is not parallel-safe with B1 because of the true dependency, shared token state, atomic single-use boundary, and shared fixture. Serial tripwires are any non-atomic recovery/consume sequence, token-state compatibility change, or fixture contention.
- State-boundary matrix:
  - Absent/initial: no issued token is outside the settled successful path and no behavior is invented.
  - Current reusable: an active, unexpired token redeems once and transitions atomically to consumed.
  - Legacy/incompatible: none identified; no migration is authorized.
  - Public access path: the account-recovery redemption path.
  - Supported variants: active/unexpired, expired, and consumed.
  - Lifecycle: active → consumed on first successful redemption; active → expired by time; consumed → rejected on later redemption; expired → rejected. The high-risk interaction is concurrent or repeated redemption, which must yield at most one success.

- Mutation read-back: both items have the exact R41 bodies above, parent `P-N01`, role `enhancement`, state `ready-for-agent`, and no assignee; `I-N01-2` is blocked by `I-N01-1`; `get_dependents(I-N01-1)` returns `I-N01-2`. The observed frontier is exactly [`I-N01-1`].
- Gaps: none.
- Safe continuation: implement `I-N01-1`; do not start B2 until B1's required outcome satisfies the blocker.
- Recommendation: `$implement`.
- Simulated operation log:
  1. `get_setup` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists; no children.
  3. `create_item(B1 R41 body)` → `I-N01-1`.
  4. `create_item(B2 R41 body)` → `I-N01-2`.
  5. `set_parent("I-N01-1", "P-N01")` → success.
  6. `set_parent("I-N01-2", "P-N01")` → success.
  7. `set_blocker("I-N01-2", "I-N01-1")` → success.
  8. `set_role("I-N01-1", "enhancement")` → success.
  9. `set_role("I-N01-2", "enhancement")` → success.
  10. `set_state("I-N01-1", "ready-for-agent")` → success.
  11. `set_state("I-N01-2", "ready-for-agent")` → success.
  12. `get_item("I-N01-1")` → exact B1 body, parent `P-N01`, role `enhancement`, state `ready-for-agent`, assignee none, blockers none.
  13. `get_item("I-N01-2")` → exact B2 body, parent `P-N01`, role `enhancement`, state `ready-for-agent`, assignee none, blocker `I-N01-1`.
  14. `get_dependents("I-N01-1")` → [`I-N01-2`].

# C — source-gap packet

- Evidence: settled source `SRC-N01@1`, compatible setup, current frozen derived revision R41, and Cara's authorization of R40 only.
- Tracker state: unchanged; `P-N01` has no children.
- Gap: authorization does not cover current bodies, graph, roles, states, profiles, matrices, or intended mutations in R41.
- Safe continuation: present the complete frozen R41 design to Cara. Publish only if she authorizes R41 exactly; refreeze and reauthorize if it changes.
- Recommendation: `none`.
- Simulated operation log:
  1. `get_setup` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists; no children.

# D — source-gap packet

- Evidence: Cara authorized R41, but the second acceptance changed before mutation; the derived design is now R42. R41 is not the current source-derived design.
- Tracker state: unchanged; `P-N01` has no children.
- Gap: the changed acceptance must be captured in the commitment ledger and B2, followed by complete graph/readiness/profile/matrix audit and authorization of the resulting frozen R42 design. R41 authorization cannot authorize R42.
- Safe continuation: freeze the complete R42 design after incorporating the new acceptance, have Cara review and authorize that exact revision, then begin publication from the still-clean tracker.
- Recommendation: `none`.
- Simulated operation log:
  1. `get_setup` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists; no children.

# E — no-ticket coverage result

- Evidence: `SRC-N01@1` commitments C1/C2, both acceptance cases, the stated scope and exclusion, and verification showing that the requested issue/expiry and redeem-once/consume behavior already exists.
- Coverage result: C1, C2, expired-token rejection, and second-redemption rejection are covered by the verified existing behavior; delivery execution remains an explicit exclusion. Therefore no implementation commitment remains and no implementation item is justified.
- Tracker state: unchanged; `P-N01` has no children.
- Gaps: none.
- Safe continuation: preserve the verification evidence with the source record; create no implementation tickets.
- Recommendation: `none`.
- Simulated operation log:
  1. `get_setup` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists; no children.
