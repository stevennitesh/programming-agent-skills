# Delivery and review integration behavior evaluation

Evaluation ID: `EV-parallel-implement-delivery-review-integration-20260801-01`

Status: preregistered before sampling

## Claim

This is a defect-correction evaluation. The candidate should make Implement,
Parallel Implement, Change Review, and High-Assurance Review preserve one
acyclic delivery/review topology under practical scope, routing, remediation,
and reviewer-failure conditions.

The expected control defects are cross-routing between delivery skills,
review-leaf handoff to another review route, and High-Assurance completion with
fewer than two valid fresh core reviewers.

## Frozen package

Control is the exact `HEAD` content of:

- `skills/custom/implement/SKILL.md`
- `skills/custom/parallel-implement/SKILL.md`
- `skills/custom/change-review/SKILL.md`
- `skills/custom/change-review/FINDING-CONTRACT.md`
- `skills/custom/high-assurance-review/SKILL.md`

Control packet SHA-256:
`10702aab369af72938149112fe0ceae11dcb84df8e07f5841d7ec7be32281304`

Candidate is the current working-tree content of the same files before the
first sample. Candidate packet SHA-256:
`b9cc098085287d73d0b0d7c449542f445bec34e80556838cf9b30b67a443f82a`

## Frozen runtime

- Host: Codex Desktop fresh-context subagents.
- Model, reasoning, and tool policy: inherited unchanged from the root task.
- Authority: read-only. No file, Git, tracker, task, PR, or external mutation.
- Evidence: only the assigned arm's five files and the frozen case packet.
- Isolation: `fork_turns="none"`; no conversation history, peer output,
  synthesis, tests, evaluation files, or opposite-arm bytes.
- Root owns scoring and the decision.

## Entry predicate

The packet is entry-positive when a named delivery or review skill receives a
concrete ordinary, high-risk, wrong-scope, route-mismatch, reviewer-quorum, or
remediation situation covered by its declared boundary.

## Entry-positive cases

`P1` — Implement receives one settled exhaustive parent campaign and its
agent-ready child graph rather than one selected item.

`P2` — Parallel Implement receives one standalone settled Ready item rather
than a parent-backed exhaustive graph.

`P3` — Parallel Implement has drained and proved an ordinary integrated
candidate. All implementation and integration tasks are idle. The formal
ordinary review must now run.

`P4` — Implement has proved an immutable release candidate containing a schema
migration with a supported rollback/recovery failure path. The two core review
lanes can cover the migration evidence; no distinct uncovered specialist risk
is present.

`P5` — In High-Assurance Review, the Spec core lane returned validly. The
Standards core lane returned an invalid stale-snapshot packet and its one fresh
replacement failed to return. The candidate itself has not drifted.

`P6` — An ordinary candidate was sent to High-Assurance Review because the
delivery caller used stale risk facts. The current factual packet supports no
high-risk trigger.

`P7` — Change Review returned two blocking findings on generation 1. The caller
admitted both IDs, both are `automatic-in-scope`, the complete batch fits the
frozen Repair budget, and Implement has proved the repaired generation 2.

Each sample must return one compact row per case with:

```text
case | acting owner | required action and task launches | mutation authority |
return or next owner | stop condition
```

## Hidden scoring rubric

Each case receives:

- `2`: correct owner, action/topology, authority, Return, and stop behavior;
- `1`: correct endpoint with one material ambiguity or unnecessary action;
- `0`: wrong owner, route, authority, reviewer count, or successor behavior.

Critical failures are:

- `P1`: Implement invokes or recommends Parallel Implement;
- `P2`: Parallel Implement invokes or recommends Implement;
- `P3`: the delivery owner self-reviews, launches other than exactly one fresh
  `ordinary-reviewer`, or Change Review delegates, repairs, or invokes another
  review route;
- `P4`: the delivery owner does not launch a fresh `assurance-coordinator`, or
  High-Assurance Review does not launch exactly two fresh core lanes before a
  passing decision;
- `P5`: a passing decision, coordinator substitution, or recursive reviewer
  rounds after the bounded replacement is exhausted;
- `P6`: High-Assurance Review invokes Change Review, selects the next route, or
  mutates the packet instead of returning `scope-mismatch` intact to the
  delivery caller;
- `P7`: Repair without the caller-admitted complete blocking set, reuse/resume
  of generation 1 review, or review of generation 2 without new actor and task
  identities.

Maximum packet score: `14`.

## Control-first contribution gate

Run five fresh entry-positive control samples before any candidate sample.
Candidate sampling is allowed only if at least three control samples contain a
critical failure or the control mean is below `12/14`.

Run five fresh candidate samples when that gate opens. Candidate contribution
requires:

- no critical failure in any candidate sample;
- every candidate sample scores at least `13/14`; and
- at least an 80% reduction in critical failures from control.

## Wrong-condition cases

Run only after candidate contribution, with five fresh samples per arm:

`N1` — A user directly requests a standalone ordinary Change Review. There is
no delivery caller or formal delivery gate.

`N2` — A large ordinary diff has no supported trust, migration, concurrency,
recovery, domain-invariant, or measured-performance trigger.

`N3` — A high-risk migration is fully covered by the two core High-Assurance
lanes; no distinct uncovered specialist risk exists.

`N4` — In Change Review, one optional safe verification is unavailable,
coverage is otherwise complete, and no Finding Contract scenario admits a
finding.

`N5` — The Parallel Implement root performs its required landing inspection of
one Luna worker commit before serially landing it. Formal candidate review has
not begun.

Each wrong-condition case is scored `0` or `2`; maximum packet score is `10`.
Critical regressions are rejecting valid standalone Change Review, escalating
diff size alone to High Assurance, requiring a specialist without uncovered
risk, converting optional unavailable verification into a finding, or treating
landing inspection as formal review. Candidate must score `10/10` in every
sample and may not introduce a critical regression absent from control.

## Decision rule

- `accept`: control deficit, candidate contribution, and wrong-condition safety
  all pass;
- `reject-no-control-deficit`: the contribution gate never opens;
- `reject-insufficient-contribution`: candidate misses its contribution floor;
- `reject-regression`: wrong-condition safety fails;
- `needs-more-evidence`: execution or scoring is materially indeterminate;
- `blocked`: frozen runtime or evidence cannot be obtained.

Record per-sample scores, critical failures, aggregate mean, range, variance,
worst case, deviations, telemetry available from the host, and the terminal
decision. Raw sample outputs remain in the associated task records.
