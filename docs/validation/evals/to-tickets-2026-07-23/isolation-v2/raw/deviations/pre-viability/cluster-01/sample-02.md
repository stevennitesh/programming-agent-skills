# A

**Typed result: source-gap packet**

- **Evidence:** settled source `SRC-N01@1`, owned by Cara, names parent `P-N01`, commitments C1/C2, the recovery integration proof seam, and the `enhancement` category. The proposed publication artifact is revision R41, containing bodies B1/B2 and the B1→B2 blocker edge. Cara granted only ordinary publication authority and has not reviewed the derived bodies or edge.
- **Gap and affected slices:** frozen-revision authorization is missing for all of R41: C1/B1, C2/B2, and the B1→B2 edge. Because review could change acceptance, scope, or the edge, neither item can pass the publication gate.
- **Tracker state:** unchanged: `P-N01` exists with no children; no item, relationship, role, or state mutation was attempted.
- **Safe continuation:** present the complete frozen R41 ledger, bodies, graph, profiles, matrices, roles, states, and predicted frontier to Cara. Continue only if Cara authorizes that exact revision; any change requires a new frozen revision and review.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; children `[]`.

# B

**Typed result: published graph**

## Evidence and source

- Source/parent: `SRC-N01@1` / `P-N01`; source owner: Cara.
- Publication authority: Cara reviewed and authorized frozen revision R41 exactly as supplied.
- Source Trace: C1 “issue an expiring token”; C2 “redeem the token once and consume it”; acceptance requires expired-token failure and second-redemption failure; scope is token issue and redemption; delivery execution is excluded; proof authority is the recovery integration fixture; authorized role is `enhancement`.

## Ordered tickets

### `FT-N01-1` — Issue an expiring account-recovery token

- **Bounded slice / work-unit form:** vertical behavior slice implementing C1.
- **Source Trace:** `SRC-N01@1` C1; outcome and scope; proof seam “recovery integration fixture”; parent `P-N01`; frozen body B1 in R41.
- **Desired behavior and acceptance:** issuing account recovery creates a redeemable token with an expiry. The recovery integration fixture observes successful issuance and proves that the issued token is rejected after expiry. Expiry is the source-defined edge/error branch; no delivery behavior is included.
- **Relevant seams and expected durable write scope:** account-recovery issuance path, token representation, expiry handling, and only the recovery-token state needed to support later one-time consumption.
- **Scope fence:** no redemption implementation, delivery execution, unrelated authentication behavior, or recovery-channel work.
- **Dependencies:** true blockers `none`; stable order 1.
- **Proof lane / verification authority / evidence:** recovery integration fixture; that fixture is authoritative; retained evidence is a passing issue-and-expire scenario showing issuance and expired-token rejection.
- **Parallel safety:** not safe to run concurrently with `FT-N01-2`. The tickets share recovery-token semantics, expected production write scope, and the scarce integration fixture; `FT-N01-2` also consumes this ticket's token outcome.
- **Execution profile:** semantic owner is the account-recovery token domain under Cara's source meaning; production writes are limited to issuance/expiry and token state; proof seam is the recovery integration fixture; execute first; serial tripwires are token representation, lifecycle semantics, and shared fixture state.
- **State-boundary matrix:**

  | Boundary | Supported branch |
  |---|---|
  | Absent/initial | No recovery token exists; issuance creates an expiring, unconsumed token. |
  | Current reusable | A valid, unconsumed issued token remains redeemable until expiry. |
  | Legacy/incompatible | No legacy form is authorized by the source; do not add compatibility or migration work. |
  | Public access path | Account-recovery token issuance path. |
  | Supported variants | Newly issued valid token; issued token after its expiry. |
  | Lifecycle transition | absent → valid/unconsumed → expired if not redeemed. |
  | High-risk interaction | Expiry must be carried consistently into the redemption seam; proof stays serial with the shared fixture. |

### `FT-N01-2` — Redeem an account-recovery token exactly once

- **Bounded slice / work-unit form:** dependent vertical behavior slice implementing C2.
- **Source Trace:** `SRC-N01@1` C2 and both acceptance statements; outcome and scope; proof seam “recovery integration fixture”; parent `P-N01`; frozen body B2 in R41.
- **Desired behavior and acceptance:** the first redemption of a valid, unconsumed token succeeds and consumes it. An expired token fails without redemption. A second redemption of the same consumed token fails. Concurrent redemption attempts preserve the source's “once” invariant: at most one can complete successfully.
- **Relevant seams and expected durable write scope:** recovery-token lookup/validation, expiry check, redemption path, and atomic consumed-state transition.
- **Scope fence:** no token issuance changes beyond consuming the established predecessor contract; no delivery execution, unrelated account recovery, or authentication changes.
- **Dependencies:** blocked by `FT-N01-1`, because redemption consumes the predecessor's issued-token representation, expiry, and lifecycle outcome; stable order 2.
- **Proof lane / verification authority / evidence:** recovery integration fixture; that fixture is authoritative; retained evidence is a passing first-redemption case plus expired, repeat, and concurrent-redemption failure cases.
- **Parallel safety:** not parallel-safe with `FT-N01-1` or another writer to recovery-token state. It must follow `FT-N01-1` and use the shared fixture serially.
- **Execution profile:** semantic owner is the one-time recovery-token lifecycle under Cara's source meaning; production writes are limited to validation and atomic consumption; proof seam is the recovery integration fixture; execute after `FT-N01-1`; serial tripwires are atomic consumption, shared token state, and the shared fixture.
- **State-boundary matrix:**

  | Boundary | Supported branch |
  |---|---|
  | Absent/initial | Missing token is not redeemable and creates no consumed state. |
  | Current reusable | Valid, unconsumed token can be redeemed once. |
  | Legacy/incompatible | Expired or already-consumed token is non-redeemable; no legacy migration is authorized. |
  | Public access path | Account-recovery token redemption path. |
  | Supported variants | Valid/unconsumed, expired, consumed, and simultaneous attempts against one valid token. |
  | Lifecycle transition | valid/unconsumed → consumed on the sole successful redemption; expired and consumed states remain non-redeemable. |
  | High-risk interaction | Consumption must be atomic so competing attempts cannot both succeed. |

## Coverage, graph, and frontier

- C1 → `FT-N01-1`.
- C2 → `FT-N01-2`.
- Expired-token failure → acceptance and proof in both the issued-token lifecycle and `FT-N01-2`.
- Second-redemption failure and one-time consumption → acceptance and proof in `FT-N01-2`.
- Scope “token issue and redemption” → the two vertical slices.
- Exclusion “delivery execution” → both scope fences; no ticket.
- Category `enhancement` → authorized role on both tickets.
- Graph: `FT-N01-1` → `FT-N01-2`.
- Ready frontier after publication: [`FT-N01-1`]. `FT-N01-2` is open and ready-for-agent in content/state but is not on the frontier until its blocker is satisfied.
- No cycle, missing edge, contradictory order, unresolved blocker, migration stage, or expand-migrate-contract sequence is present.

## Mutation read-back and tracker state

Both items read back with the exact R41 bodies above, parent `P-N01`, role `enhancement`, no assignee, and state `ready-for-agent`. `FT-N01-1` has no blocker and reports dependent `FT-N01-2`; `FT-N01-2` is blocked by `FT-N01-1` and reports no dependents. The observed frontier is [`FT-N01-1`].

- **Gaps:** none.
- **Safe continuation:** `$implement` may take `FT-N01-1`; do not start `FT-N01-2` until `FT-N01-1` is satisfied and its serial proof resource is released.
- **Recommendation:** `$implement`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; children `[]`.
  3. `create_item(B1@R41)` → created `FT-N01-1`.
  4. `create_item(B2@R41)` → created `FT-N01-2`.
  5. `set_parent("FT-N01-1", "P-N01")` → success.
  6. `set_parent("FT-N01-2", "P-N01")` → success.
  7. `set_blocker("FT-N01-2", "FT-N01-1")` → success.
  8. `set_role("FT-N01-1", "enhancement")` → success.
  9. `set_role("FT-N01-2", "enhancement")` → success.
  10. `set_state("FT-N01-1", "ready-for-agent")` → success.
  11. `set_state("FT-N01-2", "ready-for-agent")` → success.
  12. `get_item("FT-N01-1")` → exact B1@R41 body; parent `P-N01`; blockers `[]`; role `enhancement`; assignee none; state `ready-for-agent`.
  13. `get_item("FT-N01-2")` → exact B2@R41 body; parent `P-N01`; blockers [`FT-N01-1`]; role `enhancement`; assignee none; state `ready-for-agent`.
  14. `get_dependents("FT-N01-1")` → [`FT-N01-2`].
  15. `get_dependents("FT-N01-2")` → `[]`.

# C

**Typed result: source-gap packet**

- **Evidence:** `SRC-N01@1` is settled, and the proposed two-item design is R41. Cara reviewed R40 only; that review does not authorize R41's bodies or blocker edge.
- **Gap and affected slices:** exact-revision authorization for R41 is missing for C1/B1, C2/B2, and B1→B2. Treating the R40 review as transferable would publish unaudited source interpretation and could falsely mark either item ready.
- **Tracker state:** unchanged: `P-N01` exists with no children; no mutation was attempted.
- **Safe continuation:** provide Cara with the complete frozen R41 design and obtain authorization for that exact revision. If she changes it, freeze and audit the resulting revision before any mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; children `[]`.

# D

**Typed result: source-gap packet**

- **Evidence:** Cara authorized R41, but the second ticket's acceptance changed before mutation. That change creates R42 and invalidates R41's frozen-ledger and exact-revision authorization for publication.
- **Gap and affected slices:** R42's changed C2/B2 acceptance is not owner-authorized. The change also requires re-auditing B1→B2, the proof plan, state matrix, parallel-safety judgment, coverage, and frontier; therefore both slices and their relationship remain unpublished.
- **Tracker state:** unchanged: `P-N01` exists with no children; no mutation was attempted.
- **Safe continuation:** freeze the complete R42 design, re-run coverage/readiness/graph auditing, and obtain Cara's authorization for R42 exactly before creating either item.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; children `[]`.

# E

**Typed result: no-ticket coverage result**

- **Evidence:** `SRC-N01@1` requests C1/C2 with expired-token and second-redemption failure proof at the recovery integration fixture. Verification establishes that the requested issue, expiry, first-redemption consumption, and repeat-redemption behavior already exists.
- **Coverage:** C1 is dispositioned as existing verified behavior; C2 is dispositioned as existing verified behavior; expired-token failure and second-redemption failure are covered by the verification; the scope and delivery-execution exclusion require no additional work. No implementation ticket, support slice, migration, or contract stage is justified.
- **Tracker state:** unchanged: `P-N01` has no children; no mutation was attempted.
- **Gaps:** none.
- **Safe continuation:** preserve the verification evidence with the source/parent record if the tracker owner has a non-ticket evidence mechanism; otherwise stop without fabricating work.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; children `[]`.
