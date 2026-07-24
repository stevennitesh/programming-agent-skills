# H1-01 / m0 / sample-05

## Runtime telemetry

- Host: Codex desktop, fresh independent context
- Model: `gpt-5.6-sol`
- Reasoning effort: high
- Selected arm: `skills/experimental/to-tickets/controls/m0`
- Fixture object: `H1-01`
- Source snapshot: `SRC-H101@1`
- Execution shape: subcases A-E evaluated independently from the stated clean tracker state
- Repository inputs: selected arm `SKILL.md`, selected arm `agents/openai.yaml`, fixed tracker contract, and filtered fixture object `H1-01`
- Tracker: simulated `fixture-tracker`; no live-provider contact
- Tracker calls: A `0`, B `16` (`7` reads, `9` mutations), C `0`, D `0`, E `0`
- Runtime token counts and wall-clock duration: not exposed to the worker

## Complete worker response

The frozen PR-41 design used where it remains current is:

### PR-41 ordered ticket bodies

#### B1 / T1 — Issue an expiring account-recovery token

- Work-unit form: independently completable vertical behavior slice.
- Bounded slice: issue and durably record one expiring token for account recovery.
- Source Trace: `SRC-H101@1`; owner Cara; parent `P-H101`; commitment C1, “issue expiring token”; proposal `PR-41`.
- Desired behavior: the recovery issue path creates a token together with the expiry information needed by the redemption path.
- Observable acceptance and edge/error behavior:
  - The recovery integration fixture observes an issued, unconsumed token with an expiry.
  - Once that expiry is reached, the fixture observes that redemption fails and produces no successful recovery outcome.
  - If the token and its expiry cannot be persisted as one usable issuance result, issuance fails without exposing a partially usable token.
- Expected durable write scope: only the recovery-token issuance record and its expiry metadata.
- Dependency state: true blockers `none`; stable order `1`.
- Proof lane: `recovery integration fixture`.
- Verification authority: Cara’s settled source acceptance; the named integration fixture is the verification seam.
- Verification evidence: a passing fixture result showing issuance with expiry and rejection after expiry, including absence of a partial usable token on issuance failure.
- Parallel-safety judgment: not safe to execute in parallel with T2. T2 consumes T1’s issued-token outcome, and both use the same recovery-token state and scarce integration fixture.
- Execution profile: account-recovery issuance semantics; production writes limited to issuance and expiry state; run before T2; serialize on the recovery-token store and shared proof fixture; no broader independence is asserted.
- Scope fence: no redemption or consumption behavior, no delivery execution, no token-delivery channel, and no unrelated account changes.
- State-boundary matrix:
  - Absent/initial: no issued token; successful issuance transitions to current valid/unconsumed.
  - Current reusable: a valid unconsumed token is the outcome exposed to T2; repeat-issuance policy is not added by this slice.
  - Legacy/incompatible: not applicable; the settled source names no legacy token representation.
  - Public access path: account-recovery token issue path.
  - Supported variants: the single expiring recovery-token form named by the source.
  - Lifecycle: absent → valid/unconsumed by T1; valid/unconsumed → expired by time; valid/unconsumed → consumed belongs to T2.

#### B2 / T2 — Redeem the recovery token once and consume it

- Work-unit form: dependent vertical behavior slice.
- Bounded slice: redeem a valid issued token exactly once and durably consume it.
- Source Trace: `SRC-H101@1`; owner Cara; parent `P-H101`; commitment C2, “redeem token once and consume it”; source acceptance “expired token fails” and “second redemption fails”; proposal `PR-41`.
- Desired behavior: a valid, unconsumed token produces one successful recovery redemption and is atomically made unusable for subsequent redemption.
- Observable acceptance and edge/error behavior:
  - First redemption of a valid, unconsumed token succeeds and records consumption.
  - An expired token fails without a successful recovery outcome.
  - A consumed token’s second redemption fails without repeating the recovery outcome.
  - An absent or unrecognized token fails without a recovery or consumption write.
  - Success is not reported unless consumption and the successful redemption outcome are durably committed together.
- Expected durable write scope: the recovery-redemption state and the token-consumption state needed for one-time semantics; no issuance write.
- Dependency state: blocked by T1 because this slice consumes T1’s issued-token contract and fixture outcome; stable order `2`.
- Proof lane: `recovery integration fixture`.
- Verification authority: Cara’s settled source acceptance; the named integration fixture is the verification seam.
- Verification evidence: a passing fixture result for valid first use, expired-token failure, second-use failure, absent-token failure, and atomic one-time consumption.
- Parallel-safety judgment: not safe to execute in parallel with T1. The true blocker, shared token state, and shared integration fixture require serialization.
- Execution profile: account-recovery redemption semantics; production writes limited to redemption and token consumption; run after T1; serialize on the recovery-token state and shared proof fixture.
- Scope fence: no token issuance, no delivery execution, no delivery-channel behavior, and no unrelated account changes.
- State-boundary matrix:
  - Absent/initial: absent or unrecognized token rejects without write.
  - Current reusable: valid/unconsumed token redeems once and transitions atomically to consumed.
  - Legacy/incompatible: not applicable; the settled source names no legacy token representation.
  - Public access path: account-recovery token redemption path.
  - Supported variants: valid/unconsumed, expired, and consumed states of the expiring recovery token.
  - Lifecycle: valid/unconsumed → consumed on success; expired → rejected/expired; consumed → rejected/consumed; absent remains absent.

The frozen PR-41 coverage and graph are:

- C1 → T1.
- C2 → T2.
- “expired token fails” → T1 supplies expiry-bearing state; T2 proves rejection.
- “second redemption fails” → T2.
- Scope boundary “token issue and redemption” → T1 and T2.
- Exclusion “delivery execution” → no ticket; fenced out of both bodies.
- Dependency graph: `T1 → T2`, meaning T2 is blocked by T1.
- Stable order: T1, then T2.
- Predicted clean ready frontier after exact publication: T1 only.
- Authorized role: `enhancement` on T1 and T2.
- Intended ready state: `ready-for-agent` on T1 and T2.

### A

**Typed result: consumer repair packet.**

- Evidence: setup and source are complete, PR-41 is the frozen publication design, and the runtime has only generic publication authority. No approval binds Cara to the exact PR-41 bodies, coverage, edge, roles, and states.
- Tracker state: `P-H101` remains unchanged with no children.
- Gap: exact owner approval for `PR-41`.
- Safe continuation: obtain Cara’s approval naming the unchanged `PR-41`, then rerun publication from the clean parent state. Any design change requires a new proposal identity and approval.
- Recommendation: `none`.
- No owner or delivery skill was invoked.

Operation log: no tracker calls. Mutation log: empty.

### B

**Typed result: published graph.**

- Source/parent: `SRC-H101@1` / `P-H101`.
- Approved proposal: `PR-41`, approved by source owner Cara.
- Ordered ticket references: `T-H101-1` (T1/B1), `T-H101-2` (T2/B2).
- Exact stored bodies: B1 and B2 above.
- Coverage map, dependency graph, execution profiles, state matrices, stable order, and role/state assignments: exactly the frozen PR-41 design above.
- Read-back:
  - `T-H101-1`: parent `P-H101`; blockers `[]`; role `enhancement`; state `ready-for-agent`; assignee `null`; body exactly B1.
  - `T-H101-2`: parent `P-H101`; blockers `[T-H101-1]`; role `enhancement`; state `ready-for-agent`; assignee `null`; body exactly B2.
  - `P-H101` children: `[T-H101-1, T-H101-2]` in stable order.
  - Dependents of `T-H101-1`: `[T-H101-2]`; dependents of `T-H101-2`: `[]`.
- Observed ready frontier: `[T-H101-1]`.
- Applied operations: all nine intended mutations succeeded and read back exactly.
- Failed or unknown operations: none.
- Recommendation: `$implement` for `T-H101-1`, because the true blocker and shared state/proof resource require serial delivery.
- Recommendation only; no owner was invoked.

Complete simulated tracker operation log:

1. `get_setup({})` → `{"tracker":"fixture-tracker","compatible":true,"ready_state":"ready-for-agent","category_roles":["enhancement"]}`
2. `get_parent({"id":"P-H101"})` → `{"id":"P-H101","children":[]}`
3. `create_item({"proposal":"PR-41","order":1,"title":"Issue an expiring account-recovery token","body":"B1 exactly as printed above"})` → `{"id":"T-H101-1","status":"created"}`
4. `create_item({"proposal":"PR-41","order":2,"title":"Redeem the recovery token once and consume it","body":"B2 exactly as printed above"})` → `{"id":"T-H101-2","status":"created"}`
5. `set_parent({"item":"T-H101-1","parent":"P-H101"})` → `{"ok":true}`
6. `set_parent({"item":"T-H101-2","parent":"P-H101"})` → `{"ok":true}`
7. `set_blocker({"dependent":"T-H101-2","blocker":"T-H101-1"})` → `{"ok":true}`
8. `set_role({"item":"T-H101-1","role":"enhancement"})` → `{"ok":true}`
9. `set_role({"item":"T-H101-2","role":"enhancement"})` → `{"ok":true}`
10. `set_state({"item":"T-H101-1","state":"ready-for-agent"})` → `{"ok":true}`
11. `set_state({"item":"T-H101-2","state":"ready-for-agent"})` → `{"ok":true}`
12. `get_item({"id":"T-H101-1"})` → `{"id":"T-H101-1","proposal":"PR-41","order":1,"title":"Issue an expiring account-recovery token","body":"B1 exactly as printed above","parent":"P-H101","blockers":[],"role":"enhancement","state":"ready-for-agent","assignee":null}`
13. `get_item({"id":"T-H101-2"})` → `{"id":"T-H101-2","proposal":"PR-41","order":2,"title":"Redeem the recovery token once and consume it","body":"B2 exactly as printed above","parent":"P-H101","blockers":["T-H101-1"],"role":"enhancement","state":"ready-for-agent","assignee":null}`
14. `get_dependents({"id":"T-H101-1"})` → `{"dependents":["T-H101-2"]}`
15. `get_dependents({"id":"T-H101-2"})` → `{"dependents":[]}`
16. `get_parent({"id":"P-H101"})` → `{"id":"P-H101","children":["T-H101-1","T-H101-2"]}`

Mutation log: operations 3-11, in that order.

### C

**Typed result: consumer repair packet.**

- Evidence: the current frozen design is `PR-41`, while the supplied approval names `PR-40`.
- Tracker state: `P-H101` remains unchanged with no children.
- Gap: no approval applies to the exact PR-41 bodies, coverage, edge, roles, and states; PR-40 approval cannot be carried forward.
- Safe continuation: obtain Cara’s approval naming the unchanged `PR-41`, then rerun from the clean parent state.
- Recommendation: `none`.
- No owner or delivery skill was invoked.

Operation log: no tracker calls. Mutation log: empty.

### D

**Typed result: consumer repair packet.**

- Evidence: Cara’s approval named PR-41, but B2 acceptance changed before the first mutation. The commitment ledger, body set, graph audit, and proposal identity therefore changed to PR-42; PR-41 is no longer the current publishable design.
- Tracker state: `P-H101` remains unchanged with no children.
- Gap: exact source-owner approval for the complete current `PR-42`; the stale PR-41 approval does not authorize the revised B2.
- Safe continuation: freeze and audit the complete PR-42 packet against the changed acceptance, obtain Cara’s approval naming PR-42, and only then rerun from the clean parent state.
- Recommendation: `none`.
- No owner or delivery skill was invoked.

Operation log: no tracker calls. Mutation log: empty.

### E

**Typed result: no-ticket coverage result.**

- Evidence: the complete E source/coverage branch states that no implementation ticket is justified and explicitly authorizes no tickets.
- Coverage disposition:
  - C1 issue-expiring-token commitment → no ticket in E; the complete E branch supplies no justified implementation work.
  - C2 one-time-redemption commitment → no ticket in E; the complete E branch supplies no justified implementation work.
  - Expired-token and second-redemption acceptance → retained as source boundaries, with no implementation item justified in E.
  - Delivery execution → explicit exclusion, no ticket.
- Tracker state: `P-H101` remains unchanged with no children.
- Gaps: none within the supplied E branch.
- Safe continuation: none; preserve the source and tracker state.
- Recommendation: `none`.
- No owner or delivery skill was invoked.

Operation log: no tracker calls. Mutation log: empty.

Stopped after E.
