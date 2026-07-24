# A — Consumer repair packet

- **Evidence:** `SRC-N01@1`, owned by Cara, is settled and supports the frozen two-ticket design in revision R41. Setup and parent reads report a compatible `fixture-tracker` and existing parent `P-N01`. Cara granted ordinary publication authority but did not review or authorize R41's derived bodies or blocker edge.
- **Tracker state:** Unchanged: `P-N01` has no children, roles, states, or dependency relationships.
- **Gap:** Publication authority is not approval of the exact derived design. R41 lacks revision-bound source-owner authorization for B1, B2, and the B1-to-B2 edge, so the runtime-specific publication gate is not satisfied. Both slices are affected.
- **Safe continuation:** Preserve R41 and tracker state. Present the complete frozen R41 ledger, bodies, graph, profiles, and matrices to Cara for explicit review and authorization. If anything changes, assign a new revision and repeat the freeze audit before any mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:** `[]`.

# B — Published graph

- **Evidence:** Setup is compatible; `get_parent(P-N01)` confirms the source parent. Cara reviewed and authorized the exact frozen revision R41, including coverage C1/C2, bodies B1/B2, the B1-to-B2 blocker edge, both `enhancement` roles, and both `ready-for-agent` states. Every simulated mutation succeeded. `get_item(I1)` and `get_item(I2)` returned the exact bodies, parent, role, state, assignee, and dependency data below; `get_dependents(I1)` returned I2 as its dependent.
- **Source/parent:** `SRC-N01@1` / `P-N01`.
- **Gaps:** None.

## Ordered tickets

1. **I1 / B1 — Issue an expiring account-recovery token**
   - **Work-unit form:** Independently completable vertical behavior slice.
   - **Source Trace:** `SRC-N01@1`; commitment C1; outcome “Issue an expiring account-recovery token and redeem it once”; scope “token issue and redemption”; proof seam “recovery integration fixture”; owner Cara; parent `P-N01`; frozen design R41.
   - **Desired behavior and acceptance:** A valid recovery request issues a token with an expiry. The token is usable before expiry. Missing or invalid recovery-request input fails without issuing a token. An expired issued token is rejected rather than treated as usable.
   - **Expected durable write scope:** Create only the recovery-token record and its expiry metadata required by C1.
   - **Scope fence:** No redemption/consumption behavior, delivery execution, unrelated account changes, or implementation beyond token issue.
   - **Dependency state:** True blockers: `none`. Stable tracker order: 1.
   - **Proof lane:** Recovery integration fixture.
   - **Verification authority:** The source-designated recovery integration fixture, evaluated against Cara-approved R41 acceptance.
   - **Verification evidence:** Fixture evidence must show issuance with expiry, no write for invalid input, usability before expiry, and rejection after expiry.
   - **Parallel safety:** Not safe to run concurrently with I2. I2 consumes I1's token contract and lifecycle outcome, and both use the same scarce recovery integration fixture and token state.
   - **State-boundary matrix:**

     | Branch | Required behavior |
     |---|---|
     | Absent/initial | A valid recovery request with no issued token creates one expiring token; invalid or missing input creates none. |
     | Current reusable | A currently issued, unexpired token remains governed by its recorded expiry; issuance must not make it non-expiring. |
     | Legacy/incompatible | Any token lacking the supported expiry contract is not silently treated as a valid non-expiring token. |
     | Public access path | Account-recovery token-issue path only. |
     | Supported variants | Valid request, invalid/missing request, issued-before-expiry, issued-after-expiry. |
     | Lifecycle transitions | `absent → issued/unexpired → expired`; high-risk interaction is the expiry boundary. |

2. **I2 / B2 — Redeem the token once and consume it**
   - **Work-unit form:** Independently completable vertical behavior slice once I1 is complete.
   - **Source Trace:** `SRC-N01@1`; commitment C2; acceptance “an expired token fails” and “a second redemption fails”; outcome and scope as above; proof seam “recovery integration fixture”; owner Cara; parent `P-N01`; frozen design R41.
   - **Desired behavior and acceptance:** The first redemption of a valid, unexpired issued token succeeds and atomically consumes it. A missing, invalid, expired, or already-consumed token fails without a second successful recovery or a second consumption transition.
   - **Expected durable write scope:** Record only the token's successful redemption/consumption transition and the recovery state directly required by that successful redemption.
   - **Scope fence:** No token issuance, delivery execution, unrelated authentication/account behavior, token reuse, or broader recovery redesign.
   - **Dependency state:** Blocked by I1 because redemption consumes I1's issued-token and expiry contract. Stable tracker order: 2.
   - **Proof lane:** Recovery integration fixture.
   - **Verification authority:** The source-designated recovery integration fixture, evaluated against Cara-approved R41 acceptance.
   - **Verification evidence:** Fixture evidence must show one successful redemption, durable consumption, failure for a second redemption, failure for expired/missing/invalid tokens, and no duplicate recovery side effect on failures.
   - **Parallel safety:** Not safe to run concurrently with I1 or another writer to the same token lifecycle. The true dependency, shared token state, atomic one-time transition, and shared fixture require serialization.
   - **State-boundary matrix:**

     | Branch | Required behavior |
     |---|---|
     | Absent/initial | Missing or unknown token fails with no durable redemption write. |
     | Current reusable | Issued and unexpired token redeems exactly once and becomes consumed. |
     | Legacy/incompatible | Unsupported or malformed token fails closed and is not migrated by redemption. |
     | Public access path | Account-recovery token-redemption path only. |
     | Supported variants | Valid/unexpired first use, expired use, invalid/missing use, consumed second use. |
     | Lifecycle transitions | `issued/unexpired → redeemed/consumed`; `expired → rejected`; `consumed → rejected`. High-risk interaction is concurrent or repeated redemption. |

## Coverage, graph, and frontier

| Source commitment or boundary | Disposition |
|---|---|
| C1 issue an expiring token | I1 acceptance and proof |
| C2 redeem once and consume | I2 acceptance and proof |
| Expired token fails | I1 expiry contract plus I2 rejection proof |
| Second redemption fails | I2 acceptance and proof |
| Scope: token issue and redemption | Split exhaustively across I1 and I2 |
| Exclusion: delivery execution | Explicit scope fence in both tickets |
| Category: enhancement | Authorized role applied to I1 and I2 |

- **Dependency graph:** `I1 → I2`, where I2 consumes I1's issued-token and expiry outcome. No cycle, missing edge, or contradictory order is observed.
- **Ready frontier:** `[I1]`. I1 is open, ready-for-agent, unclaimed, and unblocked; I2 is ready-for-agent but not on the frontier until I1 completes.
- **Publication/read-back:** Both items exist under `P-N01`; I2 is blocked by I1; both have role `enhancement`, state `ready-for-agent`, and no assignee. Item and dependent read-back match R41 exactly.
- **Safe continuation:** Begin with I1; after its verified outcome satisfies I2's blocker, refetch the dependent and proceed serially.
- **Recommendation:** `$implement`.
- **Complete simulated operation log:**

  1. `create_item(B1@R41) -> I1`
  2. `create_item(B2@R41) -> I2`
  3. `set_parent(I1, P-N01) -> success`
  4. `set_parent(I2, P-N01) -> success`
  5. `set_blocker(I2, I1) -> success`
  6. `set_role(I1, enhancement) -> success`
  7. `set_role(I2, enhancement) -> success`
  8. `set_state(I1, ready-for-agent) -> success`
  9. `set_state(I2, ready-for-agent) -> success`

# C — Consumer repair packet

- **Evidence:** Setup and parent reads are compatible and unchanged. Cara reviewed R40, while the intended complete publication design is R41.
- **Tracker state:** Unchanged: `P-N01` has no children, roles, states, or dependency relationships.
- **Gap:** Approval of R40 does not authorize R41. The exact R41 bodies, edge, roles, and ready states lack revision-bound approval; both slices are affected.
- **Safe continuation:** Preserve source and tracker state. Supply a complete R40-to-R41 delta and the frozen R41 design to Cara. Publish only after Cara explicitly authorizes R41 without further changes; otherwise freeze a new revision and repeat review.
- **Recommendation:** `none`.
- **Complete simulated operation log:** `[]`.

# D — Source-gap packet

- **Evidence:** Cara authorized R41, but the second acceptance changed before mutation. That change invalidated the frozen ledger and B2 acceptance and produced a different design revision, R42. The packet does not state the exact replacement acceptance or bind Cara's authorization to R42.
- **Tracker state:** Unchanged: `P-N01` has no children, roles, states, or dependency relationships.
- **Gap:** The changed second acceptance can alter B2, its proof evidence, its state matrix, and possibly the dependency graph. R41 authorization is stale, while the exact changed acceptance and R42 authorization are missing. B2 is directly affected; B1 and the B1-to-B2 edge require re-audit because the graph must be frozen as one complete design.
- **Safe continuation:** Cara must settle the exact replacement acceptance. Rebuild and freeze the complete ledger, bodies, graph, profiles, matrices, and intended mutations as R42 (or a later revision), then obtain authorization for that exact revision before mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:** `[]`.

# E — No-ticket coverage result

- **Evidence:** Compatible setup and unchanged parent read. Verification through the source-designated recovery integration fixture shows that the requested behavior already exists: an expiring recovery token is issued, an expired token fails, the first valid redemption consumes the token, and a second redemption fails.
- **Tracker state:** Unchanged: `P-N01` has no children, roles, states, or dependency relationships.
- **Complete coverage:**

  | Source commitment or boundary | Disposition |
  |---|---|
  | C1 issue an expiring token | Existing verified behavior; no implementation ticket justified |
  | C2 redeem once and consume | Existing verified behavior; no implementation ticket justified |
  | Expired token fails | Existing recovery integration fixture passes |
  | Second redemption fails | Existing recovery integration fixture passes |
  | Scope: token issue and redemption | Fully covered by verified current behavior |
  | Exclusion: delivery execution | Preserved; no delivery work started |
  | Category: enhancement | No item exists, so no role is applied |

- **Gaps:** None.
- **Safe continuation:** Preserve source and tracker state; no implementation or publication action is warranted.
- **Recommendation:** `none`.
- **Complete simulated operation log:** `[]`.
