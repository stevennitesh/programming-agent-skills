# A — Consumer repair packet

- **Evidence:** `SRC-N01@1`, owned by Cara; parent `P-N01`; setup is compatible. The frozen derived design is revision `R41`, containing coverage `C1/C2`, bodies `B1/B2`, the `B1 -> B2` blocker edge, `enhancement` roles, and intended `ready-for-agent` states. Cara granted ordinary publication authority but did not review or authorize those exact derived bodies and edge.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and the mutation spy observed zero mutation attempts.
- **Gap:** runtime-specific publication approval is missing for the exact frozen ticket bodies, coverage, edge, roles, and states in `R41`. Ordinary publication authority does not establish approval of derived meaning or dependency structure.
- **Safe continuation:** present exact revision `R41` to Cara for review. If she authorizes it without change, rerun publication against a fresh unchanged state; if she changes it, freeze and obtain approval for the resulting new revision before any mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; no children.
  3. Mutation spy → no calls to `create_item`, `set_parent`, `set_blocker`, `set_role`, or `set_state`.

# B — Published graph

- **Evidence:** `SRC-N01@1`, owned by Cara; parent `P-N01`; compatible setup; exact derived revision `R41` was reviewed and authorized by Cara before mutation.
- **Observed tracker state:** parent `P-N01` has ordered children `FT-N01-1`, `FT-N01-2`. Both are unassigned, open, and `ready-for-agent`, both have role `enhancement`, and `FT-N01-2` is blocked by `FT-N01-1`. Read-back matches the frozen design.
- **Gaps:** none.
- **Safe continuation:** implement the first ready item; do not start the dependent item until the predecessor outcome and its proof are complete.
- **Recommendation:** `$implement`.

## Ordered tickets

### 1. `FT-N01-1` — Issue an expiring account-recovery token

- **Bounded slice / work-unit form:** vertical behavior slice implementing `C1`.
- **Source Trace:** `SRC-N01@1`; parent `P-N01`; outcome “Issue an expiring account-recovery token and redeem it once”; commitment `C1`; proof seam “recovery integration fixture”; frozen body `B1` in authorized revision `R41`.
- **Desired behavior and acceptance:** an account-recovery request issues a token with an expiry. A token is usable before expiry by the redemption behavior. Missing or invalid issue inputs fail without issuing a usable token. The integration fixture demonstrates issuance and expiration metadata; expiry behavior is completed end-to-end by ticket 2.
- **Relevant seams / expected durable writes:** recovery-token creation and persistent token record containing expiry and initial unconsumed state.
- **Scope fence:** only token issuance and the minimal persisted state consumed by redemption; no redemption behavior, delivery execution, unrelated account recovery, or transport changes.
- **Dependency state:** true blockers: `none`; stable tracker order: 1.
- **Proof lane:** recovery integration fixture.
- **Verification authority and evidence:** the recovery integration fixture is the authority; passing evidence must show a newly issued token, a future expiry, initial unconsumed state, and no usable token on invalid input.
- **Parallel safety:** serial with ticket 2 because ticket 2 consumes the token representation and lifecycle established here; safe from unrelated work only when production writes and the fixture are not shared.
- **Execution profile:** semantic owner: account-recovery token issuance; production writes: token creation/persistence; proof seam and scarce resource: recovery integration fixture and its token store; ordering: first; serial tripwires: token representation, expiry semantics, shared store, shared fixture; independence: not evidenced relative to ticket 2.
- **State-boundary matrix:**

  | Branch | Required behavior |
  |---|---|
  | Absent/initial | Valid request creates one expiring, unconsumed token. |
  | Current reusable | Existing unrelated current tokens are not silently overwritten or consumed by issuance. |
  | Legacy/incompatible | Not authorized by source; fail safely rather than migrate or reinterpret legacy records. |
  | Public access paths | Account-recovery issue path only. |
  | Supported variants | Valid issue input and invalid/missing issue input. |
  | Lifecycle transition | absent → issued/unconsumed with expiry. |

### 2. `FT-N01-2` — Redeem an account-recovery token once and consume it

- **Bounded slice / work-unit form:** dependent vertical behavior slice implementing `C2` and completing the end-to-end expiry and one-use acceptance.
- **Source Trace:** `SRC-N01@1`; parent `P-N01`; outcome “Issue an expiring account-recovery token and redeem it once”; commitment `C2`; acceptance “an expired token fails” and “a second redemption fails”; proof seam “recovery integration fixture”; frozen body `B2` in authorized revision `R41`.
- **Desired behavior and acceptance:** the first redemption of a valid, unexpired, unconsumed issued token succeeds and atomically consumes it. An expired, missing, invalid, or already consumed token fails without granting recovery or restoring usability. Concurrent or repeated redemption produces at most one success; a second redemption fails.
- **Relevant seams / expected durable writes:** token lookup, expiry validation, atomic consume transition, and the recovery action authorized by successful redemption.
- **Scope fence:** redemption and consumption of the ticket-1 token only; no issuance changes, token delivery execution, unrelated authentication, or broader account-recovery redesign.
- **Dependency state:** blocked by `FT-N01-1`, whose required outcome is the issued-token representation and persisted lifecycle consumed here; stable tracker order: 2.
- **Proof lane:** recovery integration fixture, including expiry, repeat-redemption, and concurrent-redemption branches.
- **Verification authority and evidence:** the recovery integration fixture is the authority; passing evidence must show one successful valid redemption, persisted consumption, expired-token failure, missing/invalid-token failure, second-redemption failure, and at most one success under competing redemptions.
- **Parallel safety:** not parallel-safe with ticket 1 and not ready until its blocker completes; the two tickets share token state and the integration fixture.
- **Execution profile:** semantic owner: redemption and one-use token lifecycle; production writes: atomic unconsumed → consumed transition plus the authorized recovery effect; proof seam and scarce resource: recovery integration fixture and shared token store; ordering: second; serial tripwires: shared schema/interface, atomicity, expiry clock, shared fixture; independence: explicitly false relative to ticket 1.
- **State-boundary matrix:**

  | Branch | Required behavior |
  |---|---|
  | Absent/initial | Missing or invalid token fails with no recovery effect. |
  | Current reusable | Issued, unexpired, unconsumed token redeems once and is atomically consumed. |
  | Legacy/incompatible | Unrecognized or incompatible token state fails safely; no migration is authorized. |
  | Public access paths | Account-recovery redemption path only. |
  | Supported variants | Valid current, expired, consumed, missing/invalid, and competing-redemption interactions. |
  | Lifecycle transitions | issued/unconsumed → consumed on first valid redemption; expired stays unusable; consumed stays unusable. |

## Coverage, graph, and frontier

- `C1 issue an expiring token` → `FT-N01-1`.
- `C2 redeem the token once and consume it` → `FT-N01-2`.
- Expired-token failure → `FT-N01-2`, consuming ticket 1's expiry-bearing token.
- Second-redemption failure → `FT-N01-2`.
- Scope “token issue and redemption” → fully covered by the two tickets.
- Exclusion “delivery execution” → explicit scope fence on both tickets; no ticket.
- Dependency graph: `FT-N01-1 -> FT-N01-2`.
- Predicted and observed ready frontier: [`FT-N01-1`].
- Category authorization: source category `enhancement` authorizes the role on both implementation tickets.

## Mutation read-back and complete simulated operation log

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; no children.
3. `create_item(B1)` → success, `FT-N01-1`.
4. `create_item(B2)` → success, `FT-N01-2`.
5. `set_parent("FT-N01-1", "P-N01")` → success.
6. `set_parent("FT-N01-2", "P-N01")` → success.
7. `set_blocker("FT-N01-2", "FT-N01-1")` → success.
8. `set_role("FT-N01-1", "enhancement")` → success.
9. `set_role("FT-N01-2", "enhancement")` → success.
10. `set_state("FT-N01-1", "ready-for-agent")` → success.
11. `set_state("FT-N01-2", "ready-for-agent")` → success.
12. `get_item("FT-N01-1")` → exact `B1`; parent `P-N01`; role `enhancement`; unassigned; state `ready-for-agent`; blockers `none`.
13. `get_item("FT-N01-2")` → exact `B2`; parent `P-N01`; role `enhancement`; unassigned; state `ready-for-agent`; blocker `FT-N01-1`.
14. `get_dependents("FT-N01-1")` → [`FT-N01-2`].
15. `get_dependents("FT-N01-2")` → [].

# C — Consumer repair packet

- **Evidence:** `SRC-N01@1`, owned by Cara; parent `P-N01`; compatible setup. The candidate publication design is `R41`, but Cara reviewed only `R40`.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and the mutation spy observed zero mutation attempts.
- **Gap:** the available review is stale and does not authorize the exact `R41` coverage, bodies, edge, roles, and states. No equivalence between `R40` and `R41` is established.
- **Safe continuation:** provide an exact `R40`→`R41` change account and obtain Cara's explicit review of `R41`; freeze any resulting revision and rerun only after that exact revision is authorized.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; no children.
  3. Mutation spy → no calls to `create_item`, `set_parent`, `set_blocker`, `set_role`, or `set_state`.

# D — Consumer repair packet

- **Evidence:** `SRC-N01@1`, owned by Cara; parent `P-N01`; compatible setup. Cara reviewed `R41`, but the second ticket's acceptance changed before mutation, producing derived revision `R42`.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and the mutation spy observed zero mutation attempts.
- **Gap:** the authorized revision is no longer the revision proposed for mutation. The changed acceptance can alter `B2`, coverage, proof, readiness, and possibly the edge; `R42` has not been reviewed or authorized.
- **Safe continuation:** freeze the complete `R42` ledger, bodies, graph, profiles, state matrices, roles, states, and intended mutations; obtain Cara's explicit review of exact `R42`; then rerun publication from an unchanged tracker state.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; no children.
  3. Mutation spy → no calls to `create_item`, `set_parent`, `set_blocker`, `set_role`, or `set_state`.

# E — No-ticket coverage result

- **Evidence:** `SRC-N01@1`, owned by Cara; parent `P-N01`; compatible setup; verification through the recovery integration fixture demonstrates that issuance already creates an expiring token, valid redemption consumes it once, expired redemption fails, and second redemption fails.
- **Coverage result:** `C1` is satisfied by verified existing issuance behavior; `C2` is satisfied by verified existing atomic one-use redemption; both acceptance boundaries are covered by the fixture. The source scope is already implemented, and delivery execution remains excluded. Therefore neither an implementation slice nor a support/migration slice is justified.
- **Tracker state:** unchanged: parent `P-N01` has no children; no tracker mutation occurred.
- **Gaps:** none.
- **Safe continuation:** preserve the verification evidence with the parent/source record; create no implementation items. Re-slice only if the settled commitments or verified behavior change.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible setup.
  2. `get_parent("P-N01")` → parent exists; no children.
  3. No mutation operations called.
