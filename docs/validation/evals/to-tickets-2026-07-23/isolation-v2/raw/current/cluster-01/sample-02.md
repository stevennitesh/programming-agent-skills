# A — consumer repair packet

- **Evidence:** settled source `SRC-N01@1`, owned by Cara; candidate design `R41` contains coverage `C1/C2`, bodies `B1/B2`, the `B1 -> B2` blocker edge, `enhancement` roles, and ready-state intent. Setup is compatible. Cara granted ordinary publication authority but did not review or authorize the exact derived bodies and edge.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and no item, relationship, role, or state mutation was attempted.
- **Gap:** the publication gate lacks Cara's review of the exact immutable `R41` design. General publication authority does not authorize unreviewed decomposition, acceptance, or dependency semantics.
- **Safe continuation:** present frozen `R41` (ledger, `B1/B2`, edge, order, profiles, matrices, roles, states, and predicted frontier) to Cara. If she authorizes that exact revision, restart from the clean tracker state and publish it; if she changes it, derive and freeze a new revision and obtain review of that revision before mutation.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists; no children.

# B — published graph

## Evidence and source

- **Source/parent:** `SRC-N01@1`, owner Cara; parent `P-N01`.
- **Publication authority:** Cara reviewed and authorized exact revision `R41`.
- **Proof authority:** the recovery integration fixture is the source-designated verification authority.
- **Read-back:** both created items, both parent links, the blocker edge, both authorized `enhancement` roles, and both `ready-for-agent` states were observed exactly as written; the dependent read reports `I2` as dependent on `I1`.

## Frozen commitment ledger and coverage

| Source commitment or boundary | Disposition |
|---|---|
| `C1` issue an expiring token | `I1` acceptance |
| `C2` redeem the token once and consume it | `I2` acceptance |
| Expired token fails | `I2` acceptance and integration proof |
| Second redemption fails | `I2` acceptance and integration proof |
| Scope: token issue and redemption | Enforced by both scope fences |
| Category: enhancement | Authorized role on `I1` and `I2` |
| Exclusion: delivery execution | No ticket; neither implementation nor worker dispatch was started |

No commitment is undisposed, and no extra product decision is introduced.

## Ordered tickets

### I1 — Issue an expiring account-recovery token

- **Bounded slice / work-unit form:** vertical behavior slice implementing `C1`.
- **Source Trace:** `SRC-N01@1` → `C1`; parent `P-N01`; frozen body `R41/B1`.
- **Desired behavior and acceptance:** issuing account recovery creates a token usable by the recovery flow and carrying an expiry. The recovery integration fixture observes the issued token and its expiry boundary. A token past that boundary is not accepted by redemption; redemption behavior itself remains in `I2`.
- **Edge/error behavior:** invalid issuance inputs follow the existing recovery boundary's rejection behavior and do not create a usable token. This slice must not silently create a non-expiring token.
- **Relevant seams:** account-recovery issuance seam, recovery-token persistence seam, clock/expiry seam, and recovery integration fixture.
- **Expected durable write scope:** only the recovery-token record and expiry metadata created by issuance.
- **Scope fence:** no redemption/consumption implementation, delivery-channel execution, unrelated authentication changes, tracker work, or parent delivery.
- **Dependency state / blockers:** `none`.
- **Stable order:** 1.
- **Proof lane:** recovery integration fixture, using a controlled clock, proves issuance plus an expiry value and proves the issued token becomes unusable after expiry when exercised through the recovery boundary.
- **Verification authority and evidence:** recovery integration fixture; passing observations for token creation, finite expiry, and post-expiry rejection.
- **Parallel safety:** not safe to execute concurrently with `I2`; `I2` consumes this slice's issued-token contract, and both use the recovery-token persistence seam and scarce integration fixture.
- **Execution profile:** semantic owner is the account-recovery token domain represented by Cara's source; production writes are limited to issued-token/expiry persistence; proof seams are issuance, clock, persistence, and the shared recovery fixture; it is first in order; serial tripwires are token schema/contract changes, shared persistence, the controlled clock, and the shared fixture; independence from `I2` is disproved by the blocker edge.
- **Role/state:** `enhancement`; `ready-for-agent`.
- **State-boundary matrix:**

  | Boundary | Supported behavior |
  |---|---|
  | Absent/initial | No issued token is required beforehand; issuance creates an unused token with a finite expiry. |
  | Current reusable | Existing recovery state does not remove the obligation that this issuance returns an expiring token; no reuse/replacement policy beyond the source is added. |
  | Legacy/incompatible | A form that cannot carry/enforce expiry is not a valid output of this slice; no migration or contract removal is authorized. |
  | Public access path | Only the account-recovery issuance path is in scope. |
  | Supported variants | The source-authorized expiring recovery token only. |
  | Lifecycle | Absent → issued/unconsumed; issued/unconsumed → expired by time. Consumption is owned by `I2`. |

### I2 — Redeem an account-recovery token once and consume it

- **Bounded slice / work-unit form:** vertical behavior slice implementing `C2`.
- **Source Trace:** `SRC-N01@1` → `C2` and both source acceptance statements; parent `P-N01`; frozen body `R41/B2`.
- **Desired behavior and acceptance:** one redemption of an unexpired, unconsumed token succeeds and durably consumes it. An expired token fails. Any second redemption of the consumed token fails.
- **Edge/error behavior:** a missing, unknown, expired, or already-consumed token produces no successful recovery and does not restore usability. Failure must not perform the successful recovery transition.
- **Relevant seams:** account-recovery redemption seam, recovery-token persistence/consumption seam, clock/expiry seam, and recovery integration fixture.
- **Expected durable write scope:** the matching recovery token's consumption state and only the account-recovery state transition already required by successful redemption.
- **Scope fence:** no token issuance, delivery-channel execution, unrelated credential/authentication behavior, generalized token framework, tracker work, or parent delivery.
- **Dependency state / blockers:** blocked by `I1`; this slice consumes the issued expiring-token contract produced by `I1`.
- **Stable order:** 2.
- **Proof lane:** recovery integration fixture issues a token through `I1`, redeems it once, observes durable consumption, retries it and observes failure, and advances the controlled clock to observe expired-token failure.
- **Verification authority and evidence:** recovery integration fixture; passing observations for first-use success, durable consumption, second-use failure, and expired-token failure.
- **Parallel safety:** not safe to execute concurrently with `I1`; it consumes `I1`'s outcome and shares recovery-token persistence, clock control, and the integration fixture.
- **Execution profile:** semantic owner is account-recovery redemption represented by Cara's source; production writes are limited to token consumption and the required successful recovery transition; proof seams are redemption, persistence, clock, and the shared fixture; it follows `I1`; serial tripwires are any token-interface/schema change, atomic consumption behavior, shared persistence, clock control, and the shared fixture; serialization is evidenced by the true blocker.
- **Role/state:** `enhancement`; `ready-for-agent`.
- **State-boundary matrix:**

  | Boundary | Supported behavior |
  |---|---|
  | Absent/initial | Missing or unknown token fails without a successful recovery transition. |
  | Current reusable | Issued, unexpired, unconsumed token redeems once and transitions durably to consumed. |
  | Legacy/incompatible | Any token form that cannot prove expiry and one-time consumption is rejected; no migration or contract removal is authorized. |
  | Public access path | Only the account-recovery redemption path is in scope. |
  | Supported variants | Unexpired/unconsumed, expired, consumed, and missing/unknown branches required to distinguish the source behavior. |
  | Lifecycle | Issued/unconsumed → consumed on first valid redemption; issued/unconsumed → expired by time; consumed and expired remain non-redeemable. |

## Dependency graph and frontier

`I1 -> I2`, where `I2` consumes `I1`'s issued expiring-token contract. The graph is acyclic, order is `I1`, then `I2`, and no serial constraint was misrepresented as a blocker. The observed ready frontier is **`I1` only**: it is ready, unclaimed, open, and unblocked; `I2` is not on the frontier until `I1` is satisfied.

## Mutation read-back

- `I1`: body `R41/B1`, parent `P-N01`, role `enhancement`, state `ready-for-agent`, blockers `none`, assignee unclaimed.
- `I2`: body `R41/B2`, parent `P-N01`, role `enhancement`, state `ready-for-agent`, blocker `I1`, assignee unclaimed.
- Affected-dependent read: `get_dependents(I1)` returned `I2` with the same blocker relationship.

## Safe continuation and recommendation

Tracker publication is complete and consistent. Continue with the first ready item, **`I1`**. **Recommendation:** `$implement`.

## Complete simulated operation log

1. `get_setup` → compatible `fixture-tracker` setup and Ready-for-agent contract.
2. `get_parent("P-N01")` → parent exists; no children.
3. `create_item(R41/B1)` → `I1`.
4. `create_item(R41/B2)` → `I2`.
5. `set_parent("I1", "P-N01")` → success.
6. `set_parent("I2", "P-N01")` → success.
7. `set_blocker("I2", "I1")` → success.
8. `set_role("I1", "enhancement")` → success.
9. `set_role("I2", "enhancement")` → success.
10. `set_state("I1", "ready-for-agent")` → success.
11. `set_state("I2", "ready-for-agent")` → success.
12. `get_item("I1")` → exact `R41/B1` body, parent `P-N01`, no blockers, `enhancement`, `ready-for-agent`, unclaimed.
13. `get_item("I2")` → exact `R41/B2` body, parent `P-N01`, blocker `I1`, `enhancement`, `ready-for-agent`, unclaimed.
14. `get_dependents("I1")` → `I2`, with the expected blocker edge.

# C — consumer repair packet

- **Evidence:** settled source `SRC-N01@1`; compatible setup; current candidate is `R41`, but Cara reviewed only `R40`. `R41` is the revision containing the proposed coverage, bodies, edge, roles, and ready states.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and no mutation was attempted.
- **Gap:** no source-owner authorization applies to exact revision `R41`. Approval of `R40` cannot be carried across an unreviewed revision.
- **Safe continuation:** provide Cara an exact diff from `R40` to frozen `R41` and the complete `R41` publication design. Publish only after she authorizes exact `R41`; otherwise incorporate her decision into a newly identified revision and obtain review of that exact revision.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists; no children.

# D — consumer repair packet

- **Evidence:** settled source began at `SRC-N01@1`; setup is compatible; Cara reviewed `R41`; before mutation the second ticket's acceptance changed, invalidating frozen `R41` and producing a different derived design, `R42`.
- **Tracker state:** unchanged: parent `P-N01` exists, has no children, and no mutation was attempted.
- **Gap:** Cara's authorization covers `R41`, not `R42`. The changed second acceptance also requires re-auditing coverage, `B2`, the edge, profiles, state matrices, readiness, order, and predicted frontier before any write.
- **Safe continuation:** capture the changed acceptance as owner-confirmed source, rebuild and freeze the complete design as `R42`, audit it for exhaustive non-contradictory coverage, and obtain Cara's review of exact `R42`. Restart publication only from a clean tracker state after that authorization.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists; no children.

# E — no-ticket coverage result

- **Evidence:** `SRC-N01@1` requested token issuance and one-time redemption, with expired-token and second-redemption failures proven through the recovery integration fixture. Verification shows that the complete requested behavior already exists.
- **Coverage:** `C1` is covered by the existing verified issuance behavior; `C2`, expired-token rejection, and second-redemption rejection are covered by the existing verified redemption behavior. The token issue/redemption scope is therefore exhausted without a new implementation commitment. Delivery execution remains explicitly excluded. `enhancement` is not applied because there is no item.
- **Tracker state:** unchanged: parent `P-N01` has no children; no item, relationship, role, or state mutation occurred.
- **Gaps:** none. No implementation ticket is justified.
- **Safe continuation:** preserve the verification evidence with the source/parent according to the source owner's normal records; do not create an implementation item unless later evidence identifies a concrete uncovered behavior.
- **Recommendation:** `none`.
- **Complete simulated operation log:**
  1. `get_setup` → compatible `fixture-tracker` setup and Ready-for-agent contract.
  2. `get_parent("P-N01")` → parent exists; no children.
