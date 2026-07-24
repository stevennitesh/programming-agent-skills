# A — consumer repair packet

- **Evidence:** `SRC-N01@1`, owned by Cara; settled commitments C1/C2; derived design revision R41 (coverage C1/C2, bodies B1/B2, B1→B2 blocker edge, `enhancement` roles, and `ready-for-agent` states); Cara granted ordinary publication authority but did not review the derived bodies or edge.
- **Observed tracker state:** setup compatible; parent `P-N01` exists; no children; mutation spy observed zero mutations.
- **Gaps:** R41 lacks owner review of the exact ticket bodies and dependency edge. Ordinary publication authority does not approve the derived representation of Cara's source meaning.
- **Safe continuation:** present immutable R41 to Cara for review. If she authorizes that exact revision, rerun publication from a clean read; if anything changes, freeze a new revision and obtain review of that revision.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation-spy observation → no mutation operation was attempted.

# B — published graph

- **Evidence:** `SRC-N01@1`, owned by Cara; Cara reviewed and authorized exact derived revision R41 before mutation. R41 exhaustively covers C1/C2 and was frozen without contradiction.
- **Source/parent:** `SRC-N01@1`; parent `P-N01`.
- **Ordered tickets:**
  1. **`T-N01-1` / B1 — Issue an expiring account-recovery token**
     - **Bounded slice / work-unit form:** vertical behavior slice implementing token issuance.
     - **Source Trace:** `SRC-N01@1` outcome; commitment C1; acceptance “an expired token fails”; scope “token issue and redemption”; proof seam “recovery integration fixture.”
     - **Desired behavior and acceptance:** issue a recovery token with an expiry; a token before expiry is available to the redemption slice; expiry is preserved and an expired token is rejected rather than redeemed. Issuance errors must not leave a usable partial token.
     - **Seams / durable write scope:** recovery-token issuance seam and token persistence; expected production writes are only the recovery-token record and its expiry metadata.
     - **Scope fence:** excludes redemption/consumption behavior, delivery execution, unrelated account or authentication behavior, and implementation technique.
     - **Dependency state:** blockers `none`; stable order 1.
     - **Proof lane:** recovery integration fixture; verification authority is the fixture’s observable issuance/expiry behavior; verification evidence is a passing integration case showing expiry metadata and rejection after expiry, plus an issuance-error case showing no usable token remains.
     - **Parallel safety:** not parallel-safe with B2 because B2 consumes this token contract and both use the recovery integration fixture and token state.
     - **Execution profile:** semantic owner Cara; production writes limited to token plus expiry metadata; scarce proof resource is the shared recovery integration fixture; execute before B2; serial tripwires are token format/expiry semantics, shared state, and shared proof resource.
     - **State-boundary matrix:** absent/initial—no token, issuance creates one expiring token; current reusable—an existing valid token remains governed by the settled token contract and is not silently replaced outside specified issuance behavior; legacy/incompatible—unsupported legacy token forms must not become usable accidentally; public access—only the recovery issuance and downstream redemption seams; supported variants—valid/unexpired and expired; lifecycle—absent → valid/unexpired → expired, with issuance failure returning to absent/no usable token. High-risk interaction: expiry at the redemption boundary.
     - **Role/state:** `enhancement`; `ready-for-agent`.
  2. **`T-N01-2` / B2 — Redeem an account-recovery token exactly once**
     - **Bounded slice / work-unit form:** vertical behavior slice implementing redemption and consumption.
     - **Source Trace:** `SRC-N01@1` outcome; commitment C2; acceptances “an expired token fails” and “a second redemption fails”; scope “token issue and redemption”; proof seam “recovery integration fixture.”
     - **Desired behavior and acceptance:** redeem a valid unexpired token once and atomically consume it; expired, missing, incompatible, already-consumed, or otherwise invalid tokens fail without recovery and without restoring usability. Concurrent or repeated redemption must yield at most one success.
     - **Seams / durable write scope:** recovery-token lookup, redemption, and atomic consume seam; expected production write is only the token’s consumed/invalidated state and the bounded recovery effect required by a successful redemption.
     - **Scope fence:** excludes token issuance, delivery execution, unrelated account/authentication behavior, and implementation technique.
     - **Dependency state:** blocked by `T-N01-1` because redemption consumes its issued-token and expiry contract; stable order 2.
     - **Proof lane:** recovery integration fixture; verification authority is the fixture’s observable redemption and persisted consume state; verification evidence is one successful redemption, rejection of the same token on a second attempt, rejection after expiry, and an at-most-one-success concurrent redemption case.
     - **Parallel safety:** not parallel-safe with B1; it depends on B1’s token contract and shares token state and the recovery integration fixture.
     - **Execution profile:** semantic owner Cara; production writes limited to atomic consumption/invalidating state and bounded recovery effect; scarce proof resource is the shared recovery integration fixture; execute after B1; serial tripwires are the issuance contract, atomic state transition, expiry boundary, and shared proof resource.
     - **State-boundary matrix:** absent/initial—missing token fails with no write; current reusable—valid unexpired unconsumed token may redeem once; legacy/incompatible—incompatible token fails without consumption or recovery; public access—recovery redemption seam only; supported variants—valid/unexpired/unconsumed, expired, consumed, missing, and incompatible; lifecycle—valid/unconsumed → consumed on one atomic success, valid/unconsumed → expired by time, while consumed and expired are terminal rejection branches. High-risk interactions: expiry racing redemption and concurrent double redemption.
     - **Role/state:** `enhancement`; `ready-for-agent`.
- **Coverage map:** C1 → B1 acceptance and proof; C2 → B2 acceptance and proof; expired-token acceptance → B1 expiry contract plus B2 rejection proof; second-redemption acceptance → B2 atomic consumption and repeat/concurrency proof; delivery execution → explicit exclusion in both scope fences. No source-visible commitment is undisposed.
- **Dependency graph / frontier:** `T-N01-1` → `T-N01-2` (B2 consumes B1’s issued-token and expiry contract). No cycles, missing edges, or contradictory order. Observed frontier: [`T-N01-1`].
- **Mutation read-back:** both ticket bodies, parent links, the B2 blocker, `enhancement` roles, unassigned status, and `ready-for-agent` states matched R41; dependent read showed B2 depends on B1; resulting frontier matched the prediction.
- **Gaps:** none.
- **Safe continuation:** implement `T-N01-1`; do not dispatch B2 until its true blocker is satisfied and the shared proof/state tripwires are clear.
- **Recommendation:** `$implement`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. `create_item(B1@R41)` → `T-N01-1`.
  4. `create_item(B2@R41)` → `T-N01-2`.
  5. `set_parent("T-N01-1", "P-N01")` → success.
  6. `set_parent("T-N01-2", "P-N01")` → success.
  7. `set_blocker("T-N01-2", "T-N01-1")` → success.
  8. `set_role("T-N01-1", "enhancement")` → success.
  9. `set_role("T-N01-2", "enhancement")` → success.
  10. `set_state("T-N01-1", "ready-for-agent")` → success.
  11. `set_state("T-N01-2", "ready-for-agent")` → success.
  12. `get_item("T-N01-1")` → exact B1@R41 body, parent `P-N01`, role `enhancement`, state `ready-for-agent`, assignee none, blockers none.
  13. `get_item("T-N01-2")` → exact B2@R41 body, parent `P-N01`, role `enhancement`, state `ready-for-agent`, assignee none, blocker `T-N01-1`.
  14. `get_dependents("T-N01-1")` → [`T-N01-2`].
  15. `get_dependents("T-N01-2")` → [].

# C — consumer repair packet

- **Evidence:** `SRC-N01@1`; the mutation candidate is R41, but Cara reviewed R40 only.
- **Observed tracker state:** setup compatible; parent `P-N01` exists; no children; mutation spy observed zero mutations.
- **Gaps:** review of R40 is stale and does not authorize R41’s exact coverage, bodies, edge, roles, and states.
- **Safe continuation:** provide the immutable R41 package and its delta from R40 to Cara. Publish only after she authorizes R41 exactly, or freeze and review a later revision if changes are required.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation-spy observation → no mutation operation was attempted.

# D — consumer repair packet

- **Evidence:** `SRC-N01@1`; Cara reviewed R41, but B2 acceptance changed before mutation, making the current derived design R42.
- **Observed tracker state:** setup compatible; parent `P-N01` exists; no children; mutation spy observed zero mutations.
- **Gaps:** the approved R41 is no longer the publication candidate. R42’s changed B2 acceptance can affect its body, coverage, proof, state matrix, readiness, and possibly graph, but R42 has not been frozen, audited, and authorized.
- **Safe continuation:** rebuild and exhaustively audit the complete R42 ledger, bodies, graph, profiles, matrices, roles, readiness, and intended mutations; obtain Cara’s review of exact R42; then restart publication against unchanged tracker state.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation-spy observation → no mutation operation was attempted.

# E — no-ticket coverage result

- **Evidence:** `SRC-N01@1`; verification through the recovery integration fixture shows the requested issuance, expiry rejection, one-time redemption/consumption, and second-redemption rejection already exist.
- **Coverage result:** C1 is covered by existing expiring-token issuance; C2 is covered by existing atomic one-time redemption and consumption; expired-token failure and second-redemption failure are both verified. Scope and delivery-execution exclusion remain preserved. Therefore no implementation commitment remains that justifies an item.
- **Observed tracker state:** setup compatible; parent `P-N01` exists; no children; tracker unchanged.
- **Gaps:** none.
- **Safe continuation:** preserve the verification evidence with the source owner’s material; create no implementation item and make no tracker mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists with no children.
