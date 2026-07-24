---
name: convergent-pr-review
description: Review one immutable local PR, release candidate, or bounded high-risk diff read-only through direct fresh-context reviewers, root-only finding admission, and exact degraded-capacity fallbacks, then return one terminal release decision. Root-only. Ordinary branch, WIP, staged, or since-X review belongs to $review; recommend $audit-codebase and stop for an immutable repository-baseline audit.
---

# Convergent PR Review

Apply these gates in order.

## 1. Route, Guard, And Freeze The Caller Packet

Accept one local pull request, release candidate, or caller-bounded high-risk
diff selected for independent review. An ordinary branch, WIP, staged, or
since-X diff is outside this skill: return `incomplete` with the routing
mismatch without starting an ordinary review. For an immutable
repository-baseline correctness, domain-robustness, methodology, model-risk,
leakage, validation, analytics, or performance audit, recommend
`audit-codebase` and stop before Pin. After the high-risk route starts, never
hand control back to `review`.

Require the top-level root. If this skill is invoked from a delegated or nested
task, return `incomplete` with the root-only blocker before Pin. Direct
reviewers apply their factual briefs; they do not invoke or orchestrate this
skill.

Hold a read-only boundary through Return. Inspection and safe verification
leave repository files, the worktree, index, Git objects and administration,
dependencies and caches, trackers, PR state, reviews and comments, external
systems and messages, Repair state, and successor snapshots unchanged. Keep
snapshot material and ledgers in root context or another already-authorized
non-mutating surface; create no review artifact. When required evidence would
need a fetch, checkout, helper side effect, file write, dependency change, or
other mutation, return `incomplete` with the exact blocker and verified partial
evidence.

Read the complete caller packet before Pin and freeze it without rewriting it:

- Charter and commitment boundary;
- review mode, fixed point when supplied, and exact target;
- `Spec required: yes | no`, Source Trace, required proof, allowed skips, and
  accepted risk;
- required Standards, Spec, and risk lenses; and
- advisories setting and caller-owned later authority.

Use one mode:

- `initial` judges the complete selected snapshot.
- `remediation` requires the original Charter, prior snapshot identity, stable
  carried finding IDs, caller-owned Repair delta, remaining acceptance, fixed
  point, and successor target. Judge only carried outcomes, the delta,
  affected seams, and exercised remaining acceptance.
- `assurance` requires the same already-reviewed target and a caller-stated
  reason. Recheck that immutable target without creating Repair or successor
  authority.

Return `incomplete` before reviewer dispatch for a missing, contradictory, or
ambiguous decision-bearing field or identity.

## 2. Pin One Complete Snapshot

Resolve the caller-supplied fixed point once. Otherwise resolve the repository
default-branch merge base. Retain the exact object; later movement of a
symbolic baseline does not replace it.

Capture exactly one nonempty target before source tracing or dispatch:

- for a Git-addressed target, resolve the exact commit or tree and capture all
  selected diff bytes;
- for a connected PR, read without changing PR state and pin the exact base,
  head, and diff content; or
- for an explicitly selected live local target, capture `HEAD`, the index
  tree, staged diff, unstaged diff, status, and every in-scope untracked path
  and its bytes.

Record the fixed point, target kind, exact identities, selected scope, and
captured content. Reviewers inspect only the captured content. If the fixed
point or target is unavailable, ambiguous, empty, partial, or identity
mismatched, return `incomplete`; do not infer, switch targets, mutate to obtain
it, or silently narrow scope.

## 3. Trace Sources And Freeze Coverage

Freeze a finite coverage plan before dispatch. For every required Standards,
Spec, or risk lens, name its sources, snapshot surfaces, proof seams, and one
review owner. A required lens without an evidence seam is uncovered and makes
the review `incomplete`.

Trace Standards independently from repository instructions, routed guidance,
maintained configuration, test and tool documentation, and meaningful nearby
conventions. Load the `review` skill's `SMELL-BASELINE.md` only when local
Standards are thin. Local Standards govern over fallback preferences.

Trace Spec independently under the frozen `Spec required` value, in this
order:

1. caller-supplied source;
2. captured-commit material; and
3. one matching repository source.

A missing, conflicting, unreadable, or unresolved required Spec makes coverage
`incomplete`; do not infer intent from implementation or tests. When Spec is
optional and absent, record it as skipped and continue Standards and risk
coverage.

Load the `review` skill's `FINDING-CONTRACT.md` for root admission. Load its
`ADVISORY-CONTRACT.md` only when the caller enabled advisories. Record exact
sources, conflicts, and optional unavailable checks.

## 4. Isolate Candidate Generation

After Pin and coverage freeze, assign required axes and lenses to direct
fresh-context reviewers. Spawn each reviewer with `fork_turns="none"` and give
it only:

- the immutable snapshot and factual source material;
- its assigned axis and lens;
- the read-only inspection boundary; and
- the typed return contract below.

Keep Standards and Spec assignments and judgment separate. Conclusions from
one axis do not seed the other, and an optional Spec never becomes required
coverage.

Withhold parent hypotheses, preliminary findings, peer output, the partial
ledger, and terminal cues. A reviewer returns candidates only; spawning,
finding admission, and the release decision remain root-owned.

Require:

```text
status: complete | blocked
axis: Standards | Spec | Risk
lens:
coverage:
findings:
advisories: <only when enabled>
skipped checks:
blockers:
```

Verify each return's lane, freshness, snapshot identity, assigned axis and
lens, read-only boundary, coverage, and required fields. A contaminated,
mutating, out-of-lens, or incomplete return receives zero credit. Rerun only
when the same snapshot and an unbiased factual brief remain valid; otherwise
mark the affected coverage incomplete.

Apply this skill's exact completed-reviewer capacity contract:

| Valid fresh completed reviewers | Required root action | Maximum clean decision |
| --- | --- | --- |
| At least two | Cover every required axis and lens across direct fresh reviewers. | `pass` |
| Exactly one | Add a separated root pass or passes for every missing lens and disclose reduced confidence. | `pass with residual risk` |
| Zero | Run separated root passes with an explicit lens reset, collectively cover every required lens, and disclose missing independent coverage and reduced confidence. | `pass with residual risk` |
| Any required lens or evidence axis remains uncovered | Stop with the exact coverage gap. | `incomplete` |

Count completed valid fresh returns, not dispatches, failed lanes, duplicates,
inherited contexts, or resumed tasks. A separately admitted blocking finding
may still produce `blocked`.

## 5. Converge And Admit

Normalize every reviewer and separated-root observation into one root-owned
candidate ledger. Give each item a stable ID, factual origin, assigned axis and
lens, and exactly one state: `candidate`, `accepted`, `rejected`, `duplicate`,
or `disputed`. Preserve stable carried IDs through remediation.

The root directly verifies each candidate against the immutable snapshot and
the shared Finding Contract. Admit a finding only after verifying its Anchor,
Reach, Evidence, Impact, and Proportion; assign severity only after admission.
Reject speculative, preference-only, unsupported-environment,
adjacent-cleanup, missing-evidence, and optional-hardening claims. When required
evidence is unavailable, record incomplete coverage rather than inventing a
finding.

Resolve duplicates and disagreements from claims, anchors, scenarios, direct
evidence, and contrary evidence. Consolidate true duplicates without losing
provenance. Agreement, reviewer count, majority, or debate does not establish
truth. An unresolved material dispute remains `incomplete`; only a separately
verified and admitted blocking finding supports `blocked`.

Close every observation and carried ID as accepted, rejected, duplicate, or an
evidence-resolved dispute. No untracked observation or unresolved candidate
may reach decision.

When enabled, verify advisories under the shared Advisory Contract in a
separate ledger; omit unsupported ones or record skipped optional verification.
They have no severity or effect on confidence, decision, or Repair authority;
violated contracts remain findings.

## 6. Read Back Drift

Before decision, re-read the originally captured target surfaces and compare
them with the pinned identities:

- re-resolve a Git-addressed object and its captured content identity;
- for a connected PR, re-read only the fields needed to detect target-content
  or head drift; or
- for a live local target, recompute `HEAD`, index tree, staged diff, unstaged
  diff, status, and every captured in-scope untracked path and its bytes.

Any target-surface change returns `incomplete` with verified partial evidence.
Do not recapture. Movement of a symbolic baseline alone does not change the
already pinned fixed-point object.

## 7. Decide, Return, And Stop

Derive exactly one decision from admitted findings, required coverage,
completed-reviewer capacity, residual risk, protocol state, and drift:

- `blocked` when a directly verified and admitted finding blocks release;
- `incomplete` for unresolved required coverage, source, candidate, dispute,
  protocol, report, or drift state when no admitted blocker already establishes
  `blocked`;
- `pass with residual risk` when coverage is complete and no blocker exists,
  but capacity was reduced or decision-bearing residual risk remains; or
- `pass` only when coverage is complete, at least two valid fresh reviewers
  completed, no blocker or decision-bearing residual risk remains, and drift
  is clear.

Never let an advisory alter the decision, soften an admitted blocker into
residual risk, or infer a clean result from partial evidence.

Return one internally consistent caller-bound packet containing:

- review mode, fixed point, snapshot identity, target, and exact sources;
- reviewer capacity and confidence;
- coverage for every applicable axis and lens;
- admitted findings, stable carried-ID dispositions, and rejected, duplicate,
  or resolved candidates;
- advisories only when enabled, skipped checks, residual risk, and drift;
- the terminal decision and exact blockers; and
- `Return boundary: caller`, `Mutation authority: none`, and
  `Successor snapshot authority: none`.

Every applicable axis and lens must be covered or explicitly block; every
candidate and carried ID must be disposed; drift must pass; and the packet
must be complete. Return control to the caller and stop.
