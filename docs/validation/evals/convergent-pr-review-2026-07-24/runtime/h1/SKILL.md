---
name: convergent-pr-review
description: Review one immutable local PR, release candidate, or bounded high-risk diff read-only through direct fresh-context reviewers, root-only finding admission, and exact degraded-capacity fallbacks, then return one terminal release decision. Root-only. Ordinary branch, WIP, staged, or since-X review belongs to $review; recommend $audit-codebase and stop for an immutable repository-baseline audit.
---

# Convergent PR Review

Own one read-only terminal release gate over one immutable review snapshot.
Apply the gates below in order. The top-level root owns Pin, reviewer dispatch,
the candidate ledger, direct verification, finding admission, the decision,
and Return.

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

For each committed object identity, record the object format and full object
ID. For a live target, declare one manifest covering `HEAD`, every index entry
including stages and object IDs, tracked path bytes, in-scope untracked paths
and bytes, the ignored-path policy, and relevant nested repository or submodule
state. Use only acquisition operations whose non-writing behavior is
established for the recorded Git, host, and provider conditions; suppress
optional locks and helpers, and create no object, ref, worktree, index, stash,
or branch.

Record whether the declared live surfaces were observed as one temporal unit
and name external state outside the manifest. A hash, object ID, clean status,
or integrity check establishes content identity only within its declared
scope; it does not establish authenticity, semantic completeness, external
state, or temporal atomicity. When required completeness or non-writing
behavior cannot be established, return `incomplete` rather than claiming a
complete snapshot.

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

Close every required lens as `covered`, `blocked with reason`, or `uncovered`.
For each lens record the deciding source owner, reviewer or separated root
pass, checks performed, verified partial evidence, and exact blocker. Apply the
unchanged terminal decision rules only after every required lens has one
determination. An admitted blocker may establish `blocked` while another lens
remains explicitly uncovered; reviewer count, an optional absent source, or an
advisory never substitutes for required-lens coverage. Equivalent complete
fields are sufficient; no particular table rendering is required.

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

Request the smallest number of fresh lanes that coherently covers the frozen
finite plan, normally two through five under this local allocation policy.
More than five requires explicit caller authority. Combine only compatible
lenses whose distinct failure questions and evidence seams remain visible;
otherwise return the exact uncovered lens or authority gap. File count does
not determine lane count, and neither two nor five is a professional optimum.

For each lane record its assignment, whether the reviewer authored or
participated in the target, the fresh-context mechanism, completed coverage,
and material shared dependencies such as model, training, source packet, or
prompt family. Seal the first report before any recovery. Fresh context
supports factual isolation but is not statistical independence; a separated
root fallback is non-independent. Shared dependencies limit the confidence
claim without automatically erasing useful direct evidence.

Withhold parent hypotheses, preliminary findings, peer output, the partial
ledger, and terminal cues. A reviewer inspects only its assignment, performs
safe read-only verification, does not mutate or spawn, and returns candidates
rather than admitting findings or deciding release.

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

After all blind first reports close, permit at most one bounded evidence
recovery attempt under the same snapshot, caller packet, mode, assignment, and
read-only boundary:

- replace one failed lane once with a new blind same-assignment reviewer when
  the original unbiased brief remains valid;
- send one named ambiguity or contradiction to a new fresh reviewer using
  only the claim, evidence, contrary evidence, factual sources, and exact
  question; or
- ask the originating reviewer only for one omitted return field or evidence
  it already claimed.

Choose one of those recovery forms. Do not start a third wave, expose peer
results or the whole ledger, search for new findings or a new general lens,
recapture the target, substitute recovery for required capacity, or consume a
new caller invocation. A resumed participant gains no independence credit.

Apply this skill's exact completed-reviewer capacity contract:

| Valid fresh completed reviewers | Required root action | Maximum clean decision |
| --- | --- | --- |
| At least two | Cover every required axis and lens across direct fresh reviewers. | `pass` |
| Exactly one | Add a separated root pass or passes for every missing lens and disclose reduced confidence. | `pass with residual risk` |
| Zero | Run separated root passes with an explicit lens reset, collectively cover every required lens, and disclose missing independent coverage and reduced confidence. | `pass with residual risk` |
| Any required lens or evidence axis remains uncovered | Stop with the exact coverage gap. | `incomplete` |

Count completed valid fresh returns, not dispatches, failed lanes, duplicates,
inherited contexts, or resumed tasks. Reduced-capacity execution never returns
plain `pass`. A separately admitted blocking finding may still produce
`blocked`.

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

When advisories are enabled, verify them under the shared Advisory Contract
and keep them in a separate ledger. Advisories have no severity, do not affect
confidence or decision, and grant no Repair authority. Omit or mark skipped an
unsupported optional advisory; a violated contract remains a finding.

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
must be complete. Return control to the caller and stop. Start no Repair,
tracker or PR mutation, merge, publication, delivery, or successor snapshot.
