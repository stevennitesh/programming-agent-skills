# A — source-gap packet

**Evidence**

- Settled source: `SRC-N01@1`, owned by Cara, with parent `P-N01`.
- Frozen derived revision: R41, containing coverage C1/C2, bodies B1/B2, the B1 → B2 blocker edge, `enhancement` roles, and intended `ready-for-agent` states.
- Authority observation: Cara granted ordinary publication authority but did not review or authorize the derived R41 bodies or edge.
- Setup read: compatible.

**Unchanged tracker state**

`P-N01` exists with no children. No item, relationship, role, or state mutation was attempted; the mutation spy remained empty.

**Gaps**

The exact derived publication unit is not authorized. Ordinary publication authority does not establish Cara's approval of R41's ticket bodies or dependency claim. Both slices and the complete graph remain unpublished.

**Safe continuation**

Present the frozen R41 coverage ledger, B1/B2 bodies, blocker edge, roles, states, profiles, and state matrices to Cara. Continue only after she explicitly authorizes that exact revision; if any element changes, freeze and review a new revision before mutation.

**Recommendation:** `none`

**Complete simulated operation log**

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; children `[]`.
3. `get_parent("P-N01")` → unchanged; children `[]`.

# B — published graph

**Evidence**

- Settled source: `SRC-N01@1`, owner Cara, parent `P-N01`.
- Cara reviewed and authorized frozen revision R41 exactly as supplied.
- R41 is internally consistent and exhaustively disposes C1 and C2.
- Setup read: compatible. All listed fixture mutations and read-backs succeeded.

## Ordered tickets

### `FT-N01-1` — Issue an expiring account-recovery token

- **Bounded slice / work-unit form:** independently provable vertical behavior slice implementing C1.
- **Parent and Source Trace:** `P-N01`; `SRC-N01@1` → C1, outcome, expiry acceptance, scope, proof seam, and delivery-execution exclusion.
- **Desired behavior and acceptance:** the recovery issue path produces an account-recovery token with a finite expiry. The recovery integration fixture observes the issued token and proves that it is accepted only within its validity period and rejected after expiry. Expiry-boundary behavior is part of acceptance; no non-expiring variant is allowed. No additional issuance policy is introduced.
- **Seams:** recovery token issuance and the token contract consumed by redemption. Storage, cryptography, and interface technique remain delivery-owner choices.
- **Expected durable write scope:** only recovery-token issuance state and its expiry metadata; no redemption consumption write and no unrelated account or delivery-system write.
- **Scope fence:** includes issuing an expiring token; excludes redemption/consumption, message delivery, unrelated authentication, and delivery execution.
- **Dependency state:** true blockers `none`; stable order 1.
- **Proof lane:** recovery integration fixture, with controlled expiry-boundary observation.
- **Verification authority and evidence:** the recovery integration fixture is authoritative; required evidence is a passing issuance assertion plus passing before-expiry and after-expiry observations against the issued token.
- **Parallel safety:** not safe to run concurrently with B2. B2 consumes this slice's token contract, and both use the same recovery fixture and token state.
- **Role / state / assignee:** `enhancement`; `ready-for-agent`; unassigned.
- **Execution profile:** Cara owns source meaning; this ticket owns only C1's production behavior. Expected writes are limited to issuance state. The token contract and recovery integration fixture are shared proof resources. Run first. Serial tripwires are token-format or expiry-semantics changes, shared-fixture contention, trust-boundary changes, and any write outside the declared scope.
- **State-boundary matrix:**
  - Absent/initial: no recovery token; issuance creates one unexpired, expiring token.
  - Current reusable: no token-reuse behavior is authorized; an already issued valid token is merely a redemption input.
  - Legacy/incompatible: none identified by the source; do not add compatibility behavior.
  - Public access paths: only the configured account-recovery issue path.
  - Supported variants: the expiring recovery-token form only.
  - Lifecycle: absent → issued/unexpired → expired by time. Redemption-driven consumption belongs to B2.

### `FT-N01-2` — Redeem an account-recovery token exactly once

- **Bounded slice / work-unit form:** independently provable vertical behavior slice implementing C2 after B1 supplies the required token contract.
- **Parent and Source Trace:** `P-N01`; `SRC-N01@1` → C2, outcome, expired-token and second-redemption acceptance, scope, proof seam, and delivery-execution exclusion.
- **Desired behavior and acceptance:** the recovery redemption path accepts a valid, unexpired, unconsumed token once and consumes it. An expired token fails without recovery completion. Every later or competing redemption of the same token fails; at most one redemption succeeds.
- **Seams:** the B1 token contract, recovery redemption, and atomic consumption boundary. Persistence and concurrency-control technique remain delivery-owner choices.
- **Expected durable write scope:** only the consumed state for the redeemed recovery token and the recovery state directly required by that successful redemption; no issuance, delivery, or unrelated account write.
- **Scope fence:** includes one-time redemption and consumption; excludes token issuance, message delivery, unrelated authentication, and delivery execution.
- **Dependency state:** blocked by `FT-N01-1` because this slice consumes its issued-token contract; stable order 2.
- **Proof lane:** recovery integration fixture, including valid, expired, sequential repeat, and competing-redemption scenarios.
- **Verification authority and evidence:** the recovery integration fixture is authoritative; required evidence is one successful valid redemption, expired-token rejection, repeat rejection after success, and at-most-one success under competing redemption.
- **Parallel safety:** not safe with B1 or another writer to the same token. Its blocker must clear, and shared token state plus the scarce integration fixture require serialization.
- **Role / state / assignee:** `enhancement`; `ready-for-agent`; unassigned.
- **Execution profile:** Cara owns source meaning; this ticket owns only C2's production behavior. It writes the token consumption boundary and uses the recovery integration fixture. Run after B1. Serial tripwires are non-atomic consumption, token-contract drift, shared-fixture contention, trust-boundary changes, and writes outside the declared scope.
- **State-boundary matrix:**
  - Absent/initial: absent or unknown tokens are not valid redemption inputs.
  - Current reusable: an issued, unexpired, unconsumed token is accepted once.
  - Legacy/incompatible: none identified by the source; no legacy token support is added.
  - Public access paths: only the configured account-recovery redemption path.
  - Supported variants: unexpired/unconsumed, expired, and consumed.
  - Lifecycle: issued/unexpired/unconsumed → consumed on the sole success; issued/unexpired/unconsumed → expired by time; expired and consumed remain rejected. Competing attempts yield at most one transition to consumed.

## Coverage, graph, and frontier

| Source commitment or boundary | Disposition |
|---|---|
| C1 issue an expiring token | `FT-N01-1` |
| C2 redeem once and consume | `FT-N01-2` |
| Expired token fails | Cross-slice contract established by `FT-N01-1`, rejection proved by `FT-N01-2` |
| Second redemption fails | `FT-N01-2` |
| Scope: token issue and redemption | Exactly B1 and B2 |
| Exclusion: delivery execution | Explicitly fenced from both tickets; no ticket |
| Proof: recovery integration fixture | Named in both proof lanes; serialized as a shared scarce resource |
| Category: enhancement | Applied to both tickets under source authority |

Dependency graph: `FT-N01-1` → `FT-N01-2`. The edge is a true blocker because B2 consumes B1's token contract. There are no cycles, missing edges, or contradictory order constraints.

Observed ready frontier: [`FT-N01-1`]. `FT-N01-2` is open and ready-for-agent but is not on the frontier until its true blocker is satisfied.

## Mutation read-back

- Parent `P-N01` lists `FT-N01-1` and `FT-N01-2` in stable order.
- Both items read back with the exact bodies above, parent `P-N01`, role `enhancement`, state `ready-for-agent`, and assignee unassigned.
- `FT-N01-1` reads back with no blockers.
- `FT-N01-2` reads back blocked by `FT-N01-1`.
- The dependent read for `FT-N01-1` returns `FT-N01-2`.
- The read-back frontier is [`FT-N01-1`], matching the prediction.

**Gaps:** none.

**Safe continuation**

The graph is completely published and verified. Preserve tracker order and clear the B2 blocker only when B1's required outcome is actually available. The source excludes delivery execution, so no delivery owner is invoked here.

**Recommendation:** `none`

**Complete simulated operation log**

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; children `[]`.
3. `create_item(B1 exact body above)` → `FT-N01-1`.
4. `create_item(B2 exact body above)` → `FT-N01-2`.
5. `set_parent("FT-N01-1", "P-N01")` → success.
6. `set_parent("FT-N01-2", "P-N01")` → success.
7. `set_blocker("FT-N01-2", "FT-N01-1")` → success.
8. `set_role("FT-N01-1", "enhancement")` → success.
9. `set_role("FT-N01-2", "enhancement")` → success.
10. `set_state("FT-N01-1", "ready-for-agent")` → success.
11. `set_state("FT-N01-2", "ready-for-agent")` → success.
12. `get_item("FT-N01-1")` → exact B1 body; parent `P-N01`; blockers `[]`; role `enhancement`; state `ready-for-agent`; assignee unassigned.
13. `get_item("FT-N01-2")` → exact B2 body; parent `P-N01`; blockers [`FT-N01-1`]; role `enhancement`; state `ready-for-agent`; assignee unassigned.
14. `get_dependents("FT-N01-1")` → [`FT-N01-2`].
15. `get_parent("P-N01")` → children [`FT-N01-1`, `FT-N01-2`] in stable order.

# C — source-gap packet

**Evidence**

- Settled source: `SRC-N01@1`, owned by Cara, with parent `P-N01`.
- Intended publication revision is R41.
- Cara reviewed R40 only. No evidence authorizes R41's coverage, B1/B2 bodies, blocker edge, roles, states, profiles, matrices, or intended mutations.
- Setup read: compatible.

**Unchanged tracker state**

`P-N01` exists with no children. No mutation was attempted; the mutation spy remained empty.

**Gaps**

Approval of R40 cannot authorize the materially distinct frozen publication unit R41. Both slices and the graph are affected because publication must use one complete, non-contradictory frozen revision.

**Safe continuation**

Provide Cara the exact R41 ledger, bodies, graph, profiles, matrices, and mutation plan. Publish only if she authorizes R41 without change. Any change requires another freeze and revision-specific review.

**Recommendation:** `none`

**Complete simulated operation log**

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; children `[]`.
3. `get_parent("P-N01")` → unchanged; children `[]`.

# D — source-gap packet

**Evidence**

- Settled source identity supplied for slicing: `SRC-N01@1`, owned by Cara, parent `P-N01`.
- Cara reviewed R41.
- Before mutation, the second acceptance changed and the complete derived design became R42.
- Cara has not reviewed or authorized R42.
- Setup read: compatible.

**Unchanged tracker state**

`P-N01` exists with no children. No mutation was attempted; the mutation spy remained empty.

**Gaps**

R41 approval became stale when B2's acceptance changed. The exact new acceptance and R42's corresponding B2 body, proof, state interactions, and any graph consequences require revision-specific owner review. Because publication is atomic at the design level, neither R41 ticket may be published under the stale approval.

**Safe continuation**

Freeze R42 with the changed acceptance fully stated, rebuild and audit the affected coverage and slice graph, and obtain Cara's explicit authorization of that exact complete revision. Then restart publication from the clean tracker state.

**Recommendation:** `none`

**Complete simulated operation log**

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; children `[]`.
3. `get_parent("P-N01")` → unchanged; children `[]`.

# E — no-ticket coverage result

**Evidence**

- Source examined: `SRC-N01@1`, owned by Cara, parent `P-N01`.
- Verification establishes that the requested account-recovery behavior already exists: an expiring token is issued, it can be redeemed once and consumed, an expired token fails, and a second redemption fails.
- The recovery integration fixture is the verification authority.
- Setup read: compatible.

**Coverage result**

| Source commitment or boundary | Disposition |
|---|---|
| C1 issue an expiring token | Already satisfied and verified; no implementation ticket |
| C2 redeem once and consume | Already satisfied and verified; no implementation ticket |
| Expired token fails | Already satisfied and verified; no implementation ticket |
| Second redemption fails | Already satisfied and verified; no implementation ticket |
| Scope: token issue and redemption | Fully covered by existing verified behavior |
| Exclusion: delivery execution | Preserved; no ticket |
| Proof: recovery integration fixture | Supplies the no-ticket evidence |

An implementation graph would duplicate verified behavior and is therefore unjustified. There are no ticket bodies, edges, roles, states, execution profiles, or state matrices to publish.

**Unchanged tracker state**

`P-N01` exists with no children. No mutation was attempted.

**Gaps:** none.

**Safe continuation**

Preserve the verification evidence with the source owner's records. Re-slice only if the desired behavior or the verified implementation changes.

**Recommendation:** `none`

**Complete simulated operation log**

1. `get_setup()` → compatible setup.
2. `get_parent("P-N01")` → parent exists; children `[]`.
3. `get_parent("P-N01")` → unchanged; children `[]`.
