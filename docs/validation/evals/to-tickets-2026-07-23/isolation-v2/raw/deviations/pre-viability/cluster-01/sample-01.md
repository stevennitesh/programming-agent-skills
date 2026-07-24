# A — Consumer repair packet

- **Evidence:** setup is compatible; settled source `SRC-N01@1`, owned by Cara, names parent `P-N01`, commitments C1/C2, recovery-integration proof, enhancement authority, and exclusion of delivery execution. Candidate publication revision R41 contains coverage C1/C2, bodies B1/B2, edge B1 → B2, roles, and ready states. Cara granted ordinary publication authority but did not review R41's derived bodies or edge.
- **Tracker state:** unchanged: `P-N01` exists, has no children, and no mutation was attempted.
- **Gap:** the exact derived design that would be published has not passed the runtime-specific owner-review gate. Both B1 (issue an expiring token) and B2 (redeem once and consume) are affected; the B1 → B2 dependency is also unapproved. Ordinary publication authority is not approval of those derived semantics.
- **Safe continuation:** present immutable R41—its complete coverage ledger, both ticket bodies, dependency edge, roles, states, profiles, matrices, and intended mutations—to Cara. Continue only if Cara authorizes that exact revision; any change requires a new revision and review.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation spy → zero mutations.

# B — Published graph

## Evidence and publication

- **Source/parent:** `SRC-N01@1`, owner Cara; parent `P-N01`.
- **Authority:** Cara reviewed and authorized exact revision R41 as supplied.
- **Ordered references:** `$I1` = fixture ID returned by the first `create_item`; `$I2` = fixture ID returned by the second.
- **Coverage map:** C1 → `$I1`; C2 and the expired/second-redemption acceptance → `$I2`; delivery execution → explicit source exclusion, no ticket.
- **Dependency graph:** `$I1` → `$I2`; `$I2` consumes the expiring-token outcome produced by `$I1`.
- **Observed ready frontier:** `$I1` only. `$I2` is open and ready-for-agent but remains blocked until `$I1` is satisfied.

## `$I1` — Issue an expiring account-recovery token

- **Bounded slice/work-unit form:** vertical behavior slice implementing C1.
- **Source Trace:** `SRC-N01@1`; outcome; C1; scope “token issue and redemption”; proof “recovery integration fixture”; parent `P-N01`.
- **Desired behavior and acceptance:** issuing recovery produces a token with an expiration boundary that the redemption behavior can enforce. The integration fixture proves a newly issued, unexpired token is redeemable and that the same token at or beyond expiration is rejected. An issuance failure must leave no token that can be redeemed.
- **Seams and durable writes:** account-recovery issue seam; expected production write is only the recovery-token state needed to represent the token and its expiry. Exact storage and implementation technique belong to delivery.
- **Scope fence:** no redemption implementation beyond the contract needed by this slice; no delivery execution; no unrelated account or authentication changes.
- **Dependency state:** true blockers: none. Stable order: 1.
- **Proof lane:** recovery integration fixture. Verification authority is that fixture's pass/fail oracle against the source acceptance. Required evidence is a passing issuance-to-redemption case and a passing expiry-boundary rejection case, including confirmation that failed issuance leaves no redeemable token.
- **Role/state:** `enhancement`; `ready-for-agent`.
- **Parallel safety/execution profile:** Cara owns semantics. Expected production writes are recovery-token creation/expiry state. The scarce proof resource and state seam are shared with `$I2`. Execute serially before `$I2`; the serial tripwire is any change to the token/expiry contract consumed by redemption. No other ordering constraint exists.
- **State-boundary matrix:**

  | Branch | Required behavior |
  |---|---|
  | Absent/initial | No recovery token exists; successful issue creates one expiring token. |
  | Current reusable | A current unexpired, unconsumed token is represented with an enforceable expiry boundary. |
  | Legacy/incompatible | No legacy form is authorized by the source; encountering one is outside this slice and must not be silently treated as current. |
  | Public access path | Account-recovery token-issue path; its concrete interface is left to delivery. |
  | Supported variants | Issuance success and issuance failure; no additional variants are authorized. |
  | Lifecycle | absent → issued/unexpired → expired, with redemption/consumption delegated to `$I2`. |

## `$I2` — Redeem a recovery token once and consume it

- **Bounded slice/work-unit form:** vertical behavior slice implementing C2 after `$I1`.
- **Source Trace:** `SRC-N01@1`; outcome; C2; acceptance “an expired token fails” and “a second redemption fails”; scope and proof; parent `P-N01`.
- **Desired behavior and acceptance:** the first redemption of an unexpired, unconsumed issued token succeeds and atomically consumes it. An expired token fails without a successful recovery effect. A consumed token's second redemption fails without repeating the successful effect.
- **Seams and durable writes:** account-recovery redemption seam; expected production write is only the token-consumption/invalidation state and the bounded successful recovery effect. Exact storage, transaction mechanism, and interface belong to delivery.
- **Scope fence:** no token delivery execution; no token issuance changes except consumption of `$I1`'s contract; no unrelated authentication or account behavior.
- **Dependency state:** blocked by `$I1`. Stable order: 2.
- **Proof lane:** recovery integration fixture. Verification authority is that fixture's pass/fail oracle against source acceptance. Required evidence is one successful first redemption, rejection at/after expiry with no successful effect, and rejection of a second redemption with no repeated effect.
- **Role/state:** `enhancement`; `ready-for-agent` with a true blocker.
- **Parallel safety/execution profile:** Cara owns semantics. Expected production writes are token consumption/invalidation and the bounded recovery effect. It shares token state and the recovery fixture with `$I1`; execute serially after `$I1`. Tripwires are non-atomic consume/success behavior, any altered expiry contract, or any broadened recovery effect.
- **State-boundary matrix:**

  | Branch | Required behavior |
  |---|---|
  | Absent/initial | A token not produced by the supported issue lifecycle is not redeemable. |
  | Current reusable | An issued, unexpired, unconsumed token succeeds once. |
  | Legacy/incompatible | No legacy token form is authorized; it must not be silently accepted. |
  | Public access path | Account-recovery redemption path; its concrete interface is left to delivery. |
  | Supported variants | Unexpired/unconsumed, expired, and consumed. |
  | Lifecycle | issued/unexpired → consumed on one successful redemption; issued/unexpired → expired by time; consumed and expired states never return to redeemable. |

## Mutation read-back

Both item reads matched R41 exactly: bounded bodies, Source Trace, acceptance, blocker state, proof, write scope, scope fence, work-unit form, verification facts, execution profiles, matrices, parent, enhancement role, ready state, and no assignee. The dependent read returned `$I2` as the dependent of `$I1`; no relationship mismatch was observed.

- **Gaps:** none.
- **Observed tracker state:** `P-N01` has children `$I1`, `$I2`; `$I2` is blocked by `$I1`; both have role `enhancement` and state `ready-for-agent`; frontier is `$I1`.
- **Safe continuation:** deliver `$I1` first; after its blocker outcome is satisfied and read back, `$I2` may proceed.
- **Recommendation:** `$implement`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. `create_item(B1@R41)` → success, returns `$I1`.
  4. `create_item(B2@R41)` → success, returns `$I2`.
  5. `set_parent($I1, "P-N01")` → success.
  6. `set_parent($I2, "P-N01")` → success.
  7. `set_blocker($I2, $I1)` → success.
  8. `set_role($I1, "enhancement")` → success.
  9. `set_role($I2, "enhancement")` → success.
  10. `set_state($I1, "ready-for-agent")` → success.
  11. `set_state($I2, "ready-for-agent")` → success.
  12. `get_item($I1)` → exact R41 body, parent, role, state, no assignee, and no blockers.
  13. `get_item($I2)` → exact R41 body, parent, role, state, no assignee, and blocker `$I1`.
  14. `get_dependents($I1)` → `$I2`.

# C — Consumer repair packet

- **Evidence:** setup and settled source are the same as A/B. The intended publication is R41, but Cara reviewed only R40.
- **Tracker state:** unchanged: `P-N01` exists, has no children, and no mutation was attempted.
- **Gap:** R40 approval cannot authorize R41. The complete diff is not supplied, so approval cannot be inferred for B1, B2, their acceptance, the B1 → B2 edge, roles, states, profiles, matrices, or intended mutations.
- **Safe continuation:** give Cara immutable R41 for review and obtain explicit authorization of that exact revision. If it changes, version the result again and review the new exact revision before any mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation spy → zero mutations.

# D — Consumer repair packet

- **Evidence:** setup and source are compatible and Cara reviewed R41. Before mutation, the second ticket's acceptance changed, producing derived design R42.
- **Tracker state:** unchanged: `P-N01` exists, has no children, and no mutation was attempted.
- **Gap:** the changed B2 acceptance invalidates R41's frozen audit and Cara's revision-specific approval. B2 must be revalidated for readiness; B1 coverage and the B1 → B2 edge must be re-audited for effects from the change. R42 is not authorized.
- **Safe continuation:** freeze the complete R42 ledger, bodies, graph, order, frontier, roles, profiles, matrices, and mutations; audit it; then obtain Cara's authorization of exact R42 before publication.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation spy → zero mutations.

# E — No-ticket coverage result

- **Evidence:** settled source `SRC-N01@1` requests C1/C2 and the two failure behaviors; verification establishes that issuance, expiration rejection, one-time redemption, and consumption already exist. Thus C1, C2, both acceptance clauses, scope, and the recovery-integration proof seam are covered by existing behavior. Delivery execution remains explicitly excluded.
- **Tracker state:** unchanged: `P-N01` exists, has no children, and no mutation was attempted.
- **Coverage disposition:** C1 → existing verified behavior, no implementation ticket; C2 → existing verified behavior, no implementation ticket; expired-token failure → existing verified behavior; second-redemption failure → existing verified behavior; delivery execution → exclusion. No uncovered implementation commitment remains.
- **Gaps:** none.
- **Safe continuation:** preserve the verification evidence with the source owner's records; create no implementation item unless a later verified regression or new commitment changes the settled source.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup()` → compatible `fixture-tracker` setup.
  2. `get_parent("P-N01")` → parent exists with no children.
  3. Mutation spy → zero mutations.
