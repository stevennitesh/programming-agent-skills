# A — consumer repair packet

- Evidence: `SRC-N01@1`, owned by Cara; compatible setup; parent `P-N01` has no children. Revision R41 contains coverage C1/C2, bodies B1/B2, B1 → B2, `enhancement` roles, and intended `ready-for-agent` states. Cara granted ordinary publication authority but did not review or authorize the derived R41 bodies or edge.
- Tracker state: unchanged; `P-N01` has no children and the mutation spy observed no mutation.
- Gap: the exact derived design proposed for publication has not been authorized by its source owner. Ordinary publication authority does not authorize unreviewed ticket meaning or dependency semantics.
- Safe continuation: present frozen R41—coverage, both complete bodies, B1 → B2, roles, states, profiles, matrices, and predicted frontier—to Cara. Continue only if Cara authorizes that exact revision; any change creates a new revision requiring a fresh freeze and review.
- Recommendation: `none`.
- Complete simulated operation log, in call order:
  1. `get_setup` → compatible.
  2. `get_parent(P-N01)` → parent exists, no children.
  3. No mutation operations.

# B — published graph

## Source, coverage, and order

- Source/parent: `SRC-N01@1` (Cara, account owner) / `P-N01`.
- Publication authority: Cara reviewed and authorized exact revision R41.
- Stable tracker order: B1, then B2.
- Coverage map:
  - C1 “issue an expiring token” → B1 acceptance.
  - C2 “redeem the token once and consume it” → B2 acceptance.
  - “an expired token fails” → B2 acceptance and state matrix.
  - “a second redemption fails” → B2 acceptance and state matrix.
  - Scope “token issue and redemption” → B1/B2 scope fences.
  - Exclusion “delivery execution” → excluded from both tickets.
  - Proof “recovery integration fixture” → both proof lanes.
- Deferrals, uncovered commitments, and no-ticket commitments: none.

## Ordered tickets

### B1 / first returned fixture ID — Issue an expiring recovery token

- Work-unit form: independently completable vertical behavior slice.
- Source Trace: `SRC-N01@1`; parent `P-N01`; C1; expiration acceptance; proof seam `recovery integration fixture`.
- Desired behavior and acceptance: issuing account recovery produces a token carrying an enforceable expiry. The integration fixture must distinguish it as active before expiry and expired after expiry. A token for which enforceable expiry cannot be established is not accepted as a successfully issued token. Delivery execution does not occur.
- Durable write scope: only the recovery-token issuance record and its expiry data.
- Seams: account-recovery issuance seam, token persistence seam, and recovery integration fixture.
- Scope fence: token creation and expiry only; no redemption, consumption, delivery execution, unrelated account changes, or legacy migration.
- Dependency state: blockers `none`; stable order 1.
- Proof lane: source-owned acceptance verified through the recovery integration fixture. Verification authority is Cara for intended behavior; required evidence is a passing fixture observation showing active-before-expiry and expired-after-expiry behavior.
- Parallel safety: not safe to run concurrently with B2. B2 consumes B1’s issued-token outcome, and both use the same token lifecycle and scarce integration fixture.
- Readiness: passes the fixture-tracker Ready-for-agent contract.
- Role/state/assignee: `enhancement`; `ready-for-agent`; unassigned.

State-boundary matrix:

| Boundary | Supported branch and required behavior |
|---|---|
| Absent/initial | No recovery token exists; issuance creates one expiring token. |
| Current reusable | No reuse behavior is authorized by the source; issuance establishes a fresh expiring token. |
| Legacy/incompatible | None identified in the supplied source; no migration or compatibility branch is added. |
| Public access path | Account-recovery token-issuance seam. |
| Supported variants | Active-before-expiry and expired-after-expiry. |
| Lifecycle | Absent → issued/active → expired, or issued/active → consumed by B2. |
| High-risk interaction | Expiry must remain enforceable when B2 observes the token. |

### B2 / second returned fixture ID — Redeem an active recovery token once and consume it

- Work-unit form: independently completable vertical behavior slice after B1.
- Source Trace: `SRC-N01@1`; parent `P-N01`; C2; both failure acceptances; proof seam `recovery integration fixture`.
- Desired behavior and acceptance: one active, unconsumed token redemption succeeds and atomically consumes the token. An expired token fails without redemption. A consumed token’s second redemption fails and produces no second successful redemption.
- Durable write scope: only the recovery token’s redemption/consumption state and the recovery effect bound to that one successful redemption.
- Seams: account-recovery redemption seam, atomic token-consumption seam, and recovery integration fixture.
- Scope fence: redemption and one-time consumption only; no issuance changes, delivery execution, unrelated authentication behavior, or legacy migration.
- Dependency state: blocked by B1 because this slice consumes B1’s expiring-token outcome; stable order 2.
- Proof lane: source-owned acceptance verified through the recovery integration fixture. Verification authority is Cara for intended behavior; required evidence is a passing fixture observation for one successful active-token redemption, expired-token failure, and second-redemption failure with no duplicate success.
- Parallel safety: serial after B1. It consumes B1’s outcome, shares the token lifecycle and fixture, and must prove the redemption/consumption transition atomically.
- Readiness: passes the fixture-tracker Ready-for-agent contract; the blocker affects the frontier, not body readiness.
- Role/state/assignee: `enhancement`; `ready-for-agent`; unassigned.

State-boundary matrix:

| Boundary | Supported branch and required behavior |
|---|---|
| Absent/initial | Missing token cannot be redeemed. |
| Current reusable | Active, unconsumed token redeems exactly once and is consumed atomically. |
| Legacy/incompatible | None identified in the supplied source; no compatibility or migration branch is added. |
| Public access path | Account-recovery token-redemption seam. |
| Supported variants | Active/unconsumed, expired/unconsumed, and consumed. |
| Lifecycle | Active/unconsumed → consumed on one success; active/unconsumed → expired; expired and consumed remain non-redeemable. |
| High-risk interactions | Expiry versus redemption and concurrent/repeated redemption must never yield more than one success. |

## Graph, frontier, and read-back

- Dependency graph: B1 → B2, meaning B2 consumes B1’s expiring-token outcome.
- Predicted and observed ready frontier: B1 only. B2 remains outside the frontier until B1 is satisfied.
- Mutation read-back:
  - First fixture ID: exact B1 body, parent `P-N01`, blockers none, role `enhancement`, state `ready-for-agent`, unassigned.
  - Second fixture ID: exact B2 body, parent `P-N01`, blocker first fixture ID, role `enhancement`, state `ready-for-agent`, unassigned.
  - Dependents of first fixture ID: second fixture ID.
  - Dependents of second fixture ID: none.
- Gaps: none.
- Safe continuation: preserve graph order and satisfy B1 before claiming B2.
- Recommendation: `none`, because top-level delivery was not requested.
- Complete simulated operation log, in call order:
  1. `get_setup` → compatible.
  2. `get_parent(P-N01)` → parent exists, no children.
  3. `create_item(B1 exact R41 body)` → first fixture ID.
  4. `create_item(B2 exact R41 body)` → second fixture ID.
  5. `set_parent(first fixture ID, P-N01)` → success.
  6. `set_parent(second fixture ID, P-N01)` → success.
  7. `set_blocker(second fixture ID, first fixture ID)` → success.
  8. `set_role(first fixture ID, enhancement)` → success.
  9. `set_role(second fixture ID, enhancement)` → success.
  10. `set_state(first fixture ID, ready-for-agent)` → success.
  11. `set_state(second fixture ID, ready-for-agent)` → success.
  12. `get_item(first fixture ID)` → exact B1 body, parent, no blocker, role, unassigned assignee, and state confirmed.
  13. `get_item(second fixture ID)` → exact B2 body, parent, blocker, role, unassigned assignee, and state confirmed.
  14. `get_dependents(first fixture ID)` → second fixture ID.
  15. `get_dependents(second fixture ID)` → none.

# C — consumer repair packet

- Evidence: `SRC-N01@1`, Cara as owner, compatible setup, and empty parent `P-N01`. Cara reviewed R40; the intended publication is R41.
- Tracker state: unchanged; `P-N01` has no children and the mutation spy observed no mutation.
- Gap: authorization is revision-bound. Approval of R40 does not authorize R41’s bodies, edge, roles, or states.
- Safe continuation: supply Cara the complete frozen R41 design and obtain explicit authorization of R41. If review changes it, freeze the resulting revision and review that exact revision before mutation.
- Recommendation: `none`.
- Complete simulated operation log, in call order:
  1. `get_setup` → compatible.
  2. `get_parent(P-N01)` → parent exists, no children.
  3. No mutation operations.

# D — consumer repair packet

- Evidence: `SRC-N01@1`, Cara as owner, compatible setup, and empty parent `P-N01`. Cara authorized R41, but B2 acceptance changed before mutation, producing derived design R42.
- Tracker state: unchanged; `P-N01` has no children and the mutation spy observed no mutation.
- Gap: the authorized snapshot no longer matches the design that would be published. R41 is stale, while R42 has not been reviewed or authorized. Publishing either would violate the frozen-design and authority gates.
- Safe continuation: rebuild and audit the complete ledger, B1/B2 bodies, graph, profiles, matrices, roles, states, and frontier as R42; present exact R42 to Cara; mutate only after R42 authorization and a final no-drift check.
- Recommendation: `none`.
- Complete simulated operation log, in call order:
  1. `get_setup` → compatible.
  2. `get_parent(P-N01)` → parent exists, no children.
  3. No mutation operations.

# E — no-ticket coverage result

- Evidence: `SRC-N01@1`, compatible setup, empty parent `P-N01`, and authoritative verification that the requested issue-expiring-token and redeem-once behavior—including expired-token and second-redemption failures—already exists.
- Coverage result: C1, C2, both acceptance failures, the issue/redemption scope, delivery-execution exclusion, and recovery-integration-fixture proof are accounted for by verified existing behavior. No implementation commitment remains.
- Tracker state: unchanged; `P-N01` has no children.
- Gaps: none.
- Safe continuation: retain the verification evidence with the source result; create no implementation ticket unless a new, unverified commitment is introduced.
- Recommendation: `none`.
- Complete simulated operation log, in call order:
  1. `get_setup` → compatible.
  2. `get_parent(P-N01)` → parent exists, no children.
  3. No mutation operations.
