# Wayfinder Critical-Boundary Behavioral Evaluation

Date: 2026-08-01

Registration: defect-correction

Decision: accept

## Scope

Evaluate Wayfinder's finite tracker-backed fog route at its easiest-to-break boundaries: waiting, closure and successor admission, allowance-bounded growth, effectful resolver drift, nested Grilling returns, explicit-only invocation, and direct-work wrong conditions.

This evaluation applies only when the work needs a bounded multi-session route with durable tracker custody. It does not make Wayfinder the default for one bounded question, one conversational decision, settled specification work, or implementation delivery.

## Frozen candidates

Control: repository `HEAD` at `217b531520e14221e837eb8ea24aedc86a2a2029`.

Pre-prune candidate Git blob identities:

- Wayfinder `SKILL.md`: `465056f713d3adefe938df301e90f55713796e61`
- Wayfinder `MAP-FORMAT.md`: `149240e29938026ca3e5db259fdc9e1237244be1`
- Grilling `SKILL.md`: `d8f4f5ca998b3f5c3e3ad8db6d412c8b8ae80bce`
- Grill With Docs `SKILL.md`: `3f02afc5860067b6a9e78fdf5dd01ebdce1e0bf8`

Post-prune replay identities:

- Wayfinder `SKILL.md`: `643a46d3add9ceed30a0f3643f86c96e6e0bd277`
- Wayfinder `MAP-FORMAT.md`: `149240e29938026ca3e5db259fdc9e1237244be1`
- Grilling `SKILL.md`: `da7dea573f6ab78dcc8f1828f7d4eeb607db1dfa`
- Grill With Docs `SKILL.md`: `06f7c9ddebff4253492939837136ade3a43d914d`

Final challenged candidate identities:

- Wayfinder `SKILL.md`: `de2bbffa45f0d34f426004240879d6fa467a9c8e`
- Wayfinder `MAP-FORMAT.md`: `149240e29938026ca3e5db259fdc9e1237244be1`
- Grilling `SKILL.md`: `da7dea573f6ab78dcc8f1828f7d4eeb607db1dfa`
- Grill With Docs `SKILL.md`: `06f7c9ddebff4253492939837136ade3a43d914d`

## Cohorts

Each cohort used five fresh-context Codex desktop subagents with read-only filesystem and shell access. The host did not expose exact backend model or reasoning telemetry; agents inherited the active runtime. No evaluator mutated the repository.

Every scored prompt fixed the named cases and instructed the evaluator to read only the frozen arm, return the operation or terminal result, allowed mutation, next admission, stop point, and undefined fields, and avoid repository edits. Candidate replays additionally required matching `git hash-object` identities before and after sampling. Sample identifiers below are the durable decision record; the host did not expose standalone raw task transcript artifacts.

The first control pilot disclosed expected conclusions in its prompts and was discarded before scoring. Two wrong-condition candidate samples used raw SHA-1 instead of `git hash-object`, falsely reported drift, and were replaced with fresh valid samples.

## Entry-positive cases

1. An unanswered `Waiting` ticket returns waiting without resolver invocation or mutation.
2. A fresh invocation independently selects `Closure`; the close is claim-free until `Seal` owns the closing claim.
3. A fired fog trigger with one approved growth slot lets `Maintain` create and wire one ticket without fresh approval or resolver judgment; a later `Orient` may select `Advance`.
4. Research writes its authorized note, then dependency drift appears at the commit point; Wayfinder preserves the external effect and evidence but records no tracker outcome or map mutation.
5. A nested Grilling Route gap returns through Grill With Docs to the active Wayfinder, which admits at most one bounded replacement graph and never recommends itself.

Score: one point per required behavior, five points per sample.

| Cohort | Sample scores | Aggregate |
| --- | --- | --- |
| Control | 2, 2, 3, 2, 3 | 12/25 |
| Candidate | 5, 5, 5, 5, 5 | 25/25 |

Per-sample rubric (`P` pass, `F` fail):

| Arm/sample | E1 | E2 | E3 | E4 | E5 | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Control 1 | P | F | F | P | F | 2/5 |
| Control 2 | P | F | F | P | F | 2/5 |
| Control 3 | P | F | F | P | P | 3/5 |
| Control 4 | P | F | F | P | F | 2/5 |
| Control 5 | P | F | F | P | P | 3/5 |
| Candidate 1 | P | P | P | P | P | 5/5 |
| Candidate 2 | P | P | P | P | P | 5/5 |
| Candidate 3 | P | P | P | P | P | 5/5 |
| Candidate 4 | P | P | P | P | P | 5/5 |
| Candidate 5 | P | P | P | P | P | 5/5 |

Control already preserved cases 1 and 4 in all samples. The candidate retained both while repairing closure, allowance ownership, and nested-return behavior. Candidate variance was zero; its worst sample was 5/5.

## Wrong-condition cases

1. One source-answerable question.
2. One conversational decision resolvable now.
3. Settled source ready for specification.
4. An agent-ready implementation graph asking Wayfinder to deliver.
5. A closed map with no material new gap asking to continue.

Both control and candidate rejected all five wrong conditions across all five valid samples: 25/25 each. The candidate did not increase false-positive admission.

| Arm/sample | W1 | W2 | W3 | W4 | W5 | Score |
| --- | --- | --- | --- | --- | --- | --- |
| Control 1-5, each | P | P | P | P | P | 5/5 |
| Candidate 1-5, each | P | P | P | P | P | 5/5 |

## Post-prune replay

Five fresh-context samples replayed eight practical boundaries against the final simplified text:

1. Closed map without a new material gap returns its immutable closing packet.
2. A predecessor-bound material gap may select `Chart`, but creation still requires the exact destination packet approval.
3. A nested Route gap returns intact to the active Wayfinder and admits at most one allowance-bounded replacement graph.
4. A direct Grilling Evidence gap returns to the one uninvoked Research owner.
5. An unapproved Questionnaire packet invokes nothing, mutates nothing, and returns the exact approval re-entry point.
6. A complete Prototype packet admits exactly one resolver invocation and returns to Wayfinder.
7. An effectful Research result followed by dependency drift preserves the effect while preventing tracker reconciliation.
8. One source-answerable question stays outside Wayfinder and goes directly to Research.

All five samples preserved all eight core decisions: 40/40, zero variance. Scenario fields not supplied by the fixtures remained explicitly undefined rather than invented.

| Sample | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Prune replay 1 | P | P | P | P | P | P | P | P | 8/8 |
| Prune replay 2 | P | P | P | P | P | P | P | P | 8/8 |
| Prune replay 3 | P | P | P | P | P | P | P | P | 8/8 |
| Prune replay 4 | P | P | P | P | P | P | P | P | 8/8 |
| Prune replay 5 | P | P | P | P | P | P | P | P | 8/8 |

## Final adversarial repair replay

Two fresh challenges found four reachable defects: successor-versus-closed ambiguity, map-claim retention on commit drift, same-invocation Advance-to-Closure, and Chart-bound Route-gap normalization without a ticket. The repair also restored Task's no-durable-mutation rule and made Research's complete invocation packet local to its resolver row.

The final frozen candidate was replayed by five new fresh-context samples:

1. A valid successor identity selects Chart rather than returning the predecessor.
2. A selected closed exact-destination map without a new gap returns immutably.
3. Effectful Research drift releases both claims while preserving the authorized note.
4. Advance that makes the map closeable returns; a later invocation independently selects Closure.
5. A Chart-bound Route gap remains claim-free proposed input requiring exact packet approval.
6. A Task contract proposing durable mutation is incompatible before claim or execution.
7. An eligible Research ticket invokes with its complete caller packet.

| Sample | F1 | F2 | F3 | F4 | F5 | F6 | F7 | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Final replay 1 | P | P | P | P | P | P | P | 7/7 |
| Final replay 2 | P | P | P | P | P | P | P | 7/7 |
| Final replay 3 | P | P | P | P | P | P | P | 7/7 |
| Final replay 4 | P | P | P | P | P | P | P | 7/7 |
| Final replay 5 | P | P | P | P | P | P | P | 7/7 |

Final replay result: 35/35, zero variance, no candidate drift, no critical failure.

## Simplification findings

The accepted behavior survived these consolidations:

- Successor admission owns predecessor selection, new-gap identity, and explicit imports in one local predicate.
- Grilling owns the active-Wayfinder return exception; Grill With Docs preserves the returned packet instead of restating its routing logic.
- Relationship prose and machine packets retain authority-bearing fields but drop repeated narrative.
- Setup validation parses each Markdown section once.
- Contract tests use semantic relationship identities and avoid duplicate persisted-field checks.
- One current Wayfinder behavioral fixture replaces two overlapping fixtures.
- The retired experimental Wayfinder exists only under `skills/.archive/wayfinder`; it is not runtime compatibility.

The remaining repetitions are gate-local safety controls: waiting, drift, growth allowance, closure, and nested-return boundaries. Removing them would separate an action from the condition that authorizes or stops it.

## Residual transfer gap

These simulations did not perform live tracker mutations or supply every ticket field, so exact tracker-adapter behavior remains structural rather than behavioral proof. Exact backend model and reasoning telemetry were unavailable. Those limits do not affect the tested routing, authority, mutation, and stop decisions.
