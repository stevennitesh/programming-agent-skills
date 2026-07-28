---
name: high-assurance-review
description: Review one immutable release candidate or concretely high-risk diff or PR read-only through bounded fresh-context reviewers and root-only finding admission, then return one terminal release decision. Root-only. Ordinary diffs and PRs belong to $change-review; immutable repository-baseline audits belong to $audit-codebase.
---

# High-Assurance Review

**Admit -> Pin -> Review -> Converge -> Gate**

## 1. Admit

Accept one release candidate or caller-bounded diff or PR with at least one
supported high-risk trigger:

- security, privacy, or another trust boundary;
- irreversible external effect, data or schema change, migration, or cutover;
- concurrency, state lifecycle, recovery, or failure atomicity;
- high-impact domain, financial, model, or data invariant; or
- a measured performance, resource, or availability obligation.

PR existence, diff size, repository size, severity labels, and hypothetical edge
cases do not establish high risk. Hand an ordinary diff or PR and its packet to
`$change-review`, then stop. Recommend `$audit-codebase` for an immutable
repository-baseline audit, then stop. After this route starts, do not run a
competing ordinary review.

Require the top-level root. A delegated or nested invocation returns
`incomplete` with the root-only blocker before Pin. Direct reviewers never
invoke, orchestrate, or mutate through this skill.

Hold a read-only boundary through Gate. Leave files, worktree, index, Git
objects and administration, dependencies and caches, trackers, PR state,
external systems, Repair state, and successor snapshots unchanged. If required
evidence needs mutation, return `incomplete` with the blocker and verified
partial evidence.

Freeze the caller's Charter, commitment boundary, review mode, fixed point,
target, `Spec required: yes | no`, Source Trace, required proof, skips, accepted
risk, supported route trigger, carried IDs, and later authority.

Use one mode:

- `initial` judges the selected snapshot;
- `remediation` requires the original Charter, prior snapshot identity, stable
  carried IDs, caller-owned Repair delta, remaining acceptance, fixed point,
  and successor target, then judges only those carried outcomes and affected
  surfaces; or
- `assurance` rechecks the same already-reviewed target for one caller-stated
  reason without creating Repair or successor authority.

Return `incomplete` before Pin for a missing, contradictory, or ambiguous
decision-bearing field. A high-risk trigger must identify the changed surface,
one supported scenario, a reachable behavior or failure path, and concrete
impact; otherwise return the routing mismatch to the caller before dispatch.

## 2. Pin

Resolve the supplied fixed point once; otherwise resolve the repository
default-branch merge base. Capture one nonempty immutable target:

- exact commit, tree, and selected diff bytes for a Git-addressed target;
- exact base, head, and diff content for a connected PR; or
- `HEAD`, index tree, staged diff, unstaged diff, normalized status, and every
  in-scope untracked path and its bytes for an explicitly selected live target.

Record the fixed point, target kind, exact identities, selected scope, captured
content, commands, and ref resolutions. Reviewers inspect only captured bytes.
Return `incomplete` when the fixed point or target is unavailable, ambiguous,
empty, partial, or mismatched. Do not infer, switch targets, mutate to obtain
it, or silently narrow scope.

Load the `change-review` skill's `FINDING-CONTRACT.md`. Trace Standards from
repository instructions, `docs/agents/engineering-contract.md`, maintained
configuration, and meaningful nearby conventions. Load
`change-review/SMELL-BASELINE.md` only when Standards are thin. Trace Spec
independently in this precedence:

1. caller-supplied source;
2. captured-commit material;
3. one matching repository source.

A missing, conflicting, unreadable, or unresolved required Spec makes coverage
`incomplete`. An absent optional Spec is skipped, never inferred.

Freeze the same compact coverage rows used by `$change-review`:

```text
change -> governing commitment -> actual behavior path
       -> applicable Finding Contract classes -> proof -> disposition
```

Name one owner for every applicable Spec and Standards class and frozen risk
trigger. Reuse exact-snapshot proof and run only missing, invalidated, or
repository-required safe checks. Mark inapplicable classes `N/A` with a reason;
cover semantic branches and supported interactions, not a blind Cartesian
product. Include displaced paths required by Change Closure. Any required
source, evidence seam, class, or risk trigger left uncovered makes the review
`incomplete`.

## 3. Review

Dispatch exactly two direct reviewers with `fork_turns="none"`:

1. **Spec and commitments** — Commitment Fidelity, Scope and Contracts, and
   Acceptance and Change Closure.
2. **Standards and behavior** — Semantic Correctness, Robustness and
   Operability, Code Quality and Design, Proof Discipline, and Stewardship.

Add at most one specialist when a frozen supported risk requires a distinct
security, migration, concurrency, model, data, or performance evidence lane that
the two core assignments cannot responsibly cover. The specialist covers
assigned classes and risk only; Risk never becomes a third axis.

Give each reviewer only the immutable snapshot and factual sources, assigned
classes and proof seams, read-only boundary, and this return contract:

```text
status: complete | blocked
reviewer: spec | standards | specialist
axis: Spec | Standards
classes:
coverage:
candidates:
skipped checks:
blockers:
```

Withhold parent hypotheses, peer output, the partial ledger, and terminal cues.
Reviewers return candidates only; they do not spawn, admit findings, assign the
terminal decision, or authorize Repair. No review result grants Repair
authority.

Verify each return's freshness, snapshot, lane, axis, classes, read-only
boundary, coverage, and fields. A contaminated, mutating, out-of-lane, or
incomplete return receives no credit. Permit at most one unbiased replacement
for an invalid lane when the same snapshot and factual brief remain valid. An
evidence blocker or second invalid return closes that coverage `incomplete`; do
not create new hypotheses or recursive rounds.

Apply this completed-core-reviewer fallback:

| Valid fresh core reviewers | Required root action | Maximum clean decision |
| --- | --- | --- |
| Two | Verify complete assigned coverage. | `pass` |
| One | Run a separated root pass for the missing core lane and disclose reduced confidence. | `pass with residual risk` |
| Zero | Run separated root Spec and Standards passes with an explicit reset and disclose missing independent coverage. | `pass with residual risk` |
| Any required class, evidence seam, or specialist lane remains uncovered | Stop with the exact gap. | `incomplete` |

An independently verified blocking finding may still produce `blocked`.

## 4. Converge

Normalize reviewer and separated-root observations into one root-owned ledger.
Give each item a stable ID, factual origin, axis, primary class, and one state:
`candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Preserve
carried IDs through remediation.

The root verifies every candidate against the immutable snapshot and shared
Finding Contract. Reject speculative, preference-only, unsupported-environment,
adjacent-cleanup, missing-evidence, and optional-hardening claims. Required
unavailable evidence makes coverage `incomplete`, not a finding.

Resolve duplicates and disagreements from anchors, supported scenarios, behavior
paths, direct evidence, and contrary evidence. Reviewer count, agreement,
majority, and debate do not establish truth. An unresolved material dispute is
`incomplete`; only a separately verified and admitted blocker supports
`blocked`. Close every observation and carried ID before Gate.

## 5. Gate

Re-read the originally captured target and compare it with the pinned
identities: Git object and content; connected PR base, head, and content; or
live `HEAD`, index tree, staged diff, unstaged diff, status, and every captured
in-scope untracked path and its bytes. Target drift returns `incomplete` with
verified partial evidence. Do not recapture; symbolic baseline movement does not
replace the pinned fixed point.

Derive exactly one decision:

- `blocked` when a directly verified admitted finding blocks release;
- `incomplete` when required source, coverage, candidate, dispute, protocol,
  report, specialist, or drift state remains unresolved and no admitted
  blocker already establishes `blocked`;
- `pass with residual risk` when coverage is complete and no blocker exists,
  but reviewer capacity was reduced or decision-bearing residual risk remains;
  or
- `pass` when coverage is complete, both core fresh reviewers and any required
  specialist completed, no blocker or decision-bearing residual risk remains,
  and drift is clear.

Return one caller-bound packet with mode, fixed point, snapshot, target,
sources, reviewer capacity, coverage by axis and class, admitted findings,
carried dispositions, closed candidate states, skipped checks, residual risk,
drift, decision, and blockers. End with:

```text
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires every applicable axis, class, and risk trigger to close;
every candidate and carried ID to be disposed; drift to pass; and one internally
consistent decision to return. Return control to the caller and stop.
