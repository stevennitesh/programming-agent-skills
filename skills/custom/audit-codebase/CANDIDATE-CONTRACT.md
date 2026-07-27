# Improvement Candidate Contract

An improvement candidate is one user-selectable improvement boundary inside
one audited subsystem. It contains at least one verified defect or admitted
opportunity. Group multiple items only when every member shares one change
direction and proof seam plus either one causal owner or one unresolved
decision. Gap-only hypotheses and retained complexity are not candidates.

## Present

Keep every member item visible:

```text
Candidate ID:
Subsystem:
Title:
Primary class: reliability | domain | design | simplification | coding practice | performance | declared:<lens-id> | mixed
Concepts:
Member defect, opportunity, and gap IDs:
Files and Modules:
Supported behavior:
Problem:
Snapshot evidence:
Improvement direction:
Expected benefit:
Behavior and safety floors:
Required proof:
Decision questions:
Recommendation strength: Strong | Worth exploring | Speculative
Strength reason:
State: presented
```

- **Strong:** direct evidence, concrete cost or impact, a plausible bounded
  alternative, and a meaningful proof seam.
- **Worth exploring:** real friction is evidenced, but a material choice,
  experiment, compatibility fact, or Interface question remains.
- **Speculative:** at least one member is admitted, but one exact gap weakens
  the direction, expected benefit, or proof plan. If the gap prevents every
  defect or opportunity from admission, keep only the gap.

Rank only candidates inside their audited subsystem. Never rank or select
subsystems.

## Analyze

One Analyze invocation changes one user-selected candidate:

```text
Current shape and cost:
Keep:
Smallest sufficient change:
Structural change:
Replacement:
Recommended direction:
Rejected alternatives and why:
Affected contracts and decisions:
Migration, compatibility, cutover, and rollback:
Proof plan:
Residual risk:
Suggested next step:
Suggestion reason:
Pickup prerequisite:
Result recipient:
Audit re-entry: <exact invocation> | none
Suggested invocation:
Decision status: none | pending | settled | evidence gap | blocked
State: analyzed | decision pending | disproved | blocked
```

Do not force every alternative to exist. Mark one `not applicable` with
evidence when appropriate. Replacement needs explicit parity, migration,
cutover, rollback, and proof.

Compare Keep as the present shape and continuing cost; Smallest sufficient
change as the first valid reduction rung; Structural change as deepening,
merging, inlining, Seam movement, or an earned Adapter only when Leverage,
Locality, and testability improve; and Replacement only when incremental
evolution is worse.

Use **Goal-Driven Execution** to name the observable success criterion and
proof. Use **Surgical Change** to bound change-created fallout and leave
unrelated cleanup separate.

## Suggest One Next Step

After analysis or returned evidence, suggest exactly zero or one:

| Remaining work | Suggested next step |
| --- | --- |
| One non-diagnostic source-answerable authoritative fact is missing | `$research` |
| One settled design question needs a disposable runnable probe or performance experiment | `$prototype` |
| Broken or slow behavior still has uncertain expected behavior, symptom, cause, or trusted reproduction | `$diagnosing-bugs` |
| One current-user decision also requires current domain language, Invariants, relationships, or ADR handling | `$grill-with-docs` |
| One current-user decision needs conversation but no domain-record maintenance | `$grilling` |
| One identifiable external stakeholder holds required knowledge unavailable from sources or the user | `$to-questionnaire` |
| One bounded code Module, Interface, Seam, Adapter, or caller-facing test-surface design remains unresolved after user decisions settle | `$codebase-design` |
| Multiple interdependent unresolved decisions or prerequisites need a configured tracker-backed route | `$wayfinder` |
| Direction and commitments are settled, but a durable parent specification is needed | `$to-spec` |
| Direction, authority, commitments, acceptance, dependency meaning, and supported states are settled; no parent specification is needed or one exists; and implementation requires multiple slices | `$to-tickets` |
| One analyzed candidate has a bounded behavior-preserving reduction, current report identity, supported behavior, Source Trace, and proof seam | `$simplify-code` |
| One non-reduction direct item has settled outcome, observable acceptance, commitment boundary, scope and write authority, Source Trace, proof, and a finite Repair budget | `$implement` |
| The candidate is disproved or no route is justified | `none` |

Choose the first unresolved work, not the eventual workflow. Diagnosis wins
over Prototype for an observed uncertain symptom. A current-user decision
precedes design. To Spec wins when a parent specification is required;
otherwise a settled multi-slice candidate may go directly to To Tickets.
Simplify Code owns a behavior-preserving reduction; Implement owns a settled
non-reduction correction or addition.

`$to-questionnaire` applies only to one external stakeholder. Use Research for
source-answerable facts, Grilling for a conversation-only current-user
decision, and Grill With Docs only when its Domain Delta is required.
Label every suggestion `user selection required`, invoke nothing, and encode
no workflow chain. For a non-`none` suggestion, write one complete
`Suggested invocation` that names the skill, candidate ID, absolute report
path, and pickup prerequisite. Copy the callee's admission facts into the
candidate packet without copying its procedure.

Research, Prototype, Diagnosis, Grilling, Grill With Docs, and Codebase Design
return evidence through the user to the exact Audit re-entry. Questionnaire
returns only an unsent artifact; keep the candidate blocked until the user
returns attributable stakeholder answers. Planning and execution routes use
`Audit re-entry: none`. Cross-session transport is not a semantic route: the
report and exact invocation are the pickup; the user may invoke `$handoff`
independently when needed.

## Decision Brief And Returned Evidence

When one material current-user-owned repo-backed decision blocks analysis:

```text
Run ID:
Snapshot:
Subsystem ID:
Candidate ID:
Decision:
Why it is material:
Governing domain terms, Invariants, relationships, and ADRs:
Constraints:
Viable options:
Consequences:
Evidence already settled:
Exact unresolved question:
Decision owner: current user
Documentation effect: none | Domain Delta required
Context action: render only unless separately authorized
ADR action: offer only unless separately approved
Re-entry owner: $audit-codebase Analyze
Re-entry invocation:
```

For `$grilling`, set domain-only fields to `not applicable`. For
`$grill-with-docs`, populate the Domain Delta and ADR fields.

Publish the brief before recommending:

- `$grilling` when `Documentation effect: none`; its return must include the
  intact Grilling exit packet.
- `$grill-with-docs` when a Domain Delta is required; its return must include
  the intact Grilling exit packet and current Domain Delta.

On every Analyze re-entry, verify the original report, run, snapshot,
subsystem, candidate, question or claim, result owner, authority, status,
freshness, and intact payload or pointer. A mismatched or stale packet changes
no judgment.

Normalize qualifying returned evidence:

- evidence that answers the pickup reruns only affected judgments;
- evidence that disproves the candidate marks it `disproved`;
- unresolved required evidence marks it `blocked` with its exact re-entry;
- a foreign route recommendation is evidence only; Audit chooses any next
  owner; and
- an unchanged exhausted or blocked return keeps the candidate `blocked` with
  suggestion `none` until its named unblock condition changes.

`Questionnaire ready` is not answer evidence. Re-enter only with stakeholder
answers attributed to the named recipient and original question set.

For a returned decision packet:

- `Confirmed`: record the decision, rerun only affected judgments, mark
  `analyzed`, and suggest its next step.
- `Evidence gap`: preserve the uninvoked evidence owner and exact re-entry
  requirement, mark `blocked`, and suggest that owner only when one route row
  matches.
- `Blocked`: preserve the blocker and re-entry condition and mark `blocked`.

If a returned Domain Delta changed an in-scope live-baseline path, the old
report becomes stale. Preserve the packet only as foreign post-snapshot
evidence and require Map Refresh; do not change old-snapshot judgments.

## Bound

Candidate analysis confirms, disproves, or frames an improvement. It does not
implement, approve a public contract, mutate domain records, invoke a
suggested next step, or grant that suggestion authority.
