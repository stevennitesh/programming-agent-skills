---
name: change-review
description: "Review one branch, WIP, staged, since-X diff, local PR, release candidate, or supported-risk implementation candidate read-only from a fixed snapshot. Judge Spec and Standards separately, with risk-proportional coverage, then return one terminal gate decision."
---

# Change Review

**Pin -> Cover -> Judge -> Gate**

The whole review is read-only. Inspect and safely verify; leave files, Git,
dependencies, trackers, PR state, external systems, and successor snapshots
unchanged.

## Pin

Load [FINDING-CONTRACT.md](FINDING-CONTRACT.md) and the shared
[Runtime Profiles](../parallel-implement/references/RUNTIME-PROFILES.md).
Change Review owns one branch, WIP, staged, since-X diff, local PR, release
candidate, or supported-risk implementation candidate. Release and supported
risk facts expand applicable coverage; they do not select another automatic
review system. Recommend `$audit-codebase`
for an immutable repository-baseline audit, then stop. Return mutation requests
to their caller without beginning review.

Change Review reviews directly and never delegates, invokes another review, or
repairs. Formal delivery requires caller-supplied implementation IDs and any
integration IDs the caller has, plus a fresh reviewer actor and task distinct
from every supplied ID. Use `ordinary-reviewer` for one-item delivery and
`integration-reviewer` for a Parallel Implement final candidate. A missing or
mismatched formal-delivery binding returns
`transport-invalid` before candidate judgment. Standalone review records its current runtime
provenance but needs no binding or separation proof.

Carry every factual caller-supplied Charter field, `Spec required`, invocation
and review modes, implementation and integration IDs, Source Trace, fixed point
and candidate, required proof, skips, risk, contradictory evidence, and carried
finding IDs. Hypotheses, expected conclusions, partial findings, and terminal
cues are not evidence.

Use the supplied fixed point. Otherwise resolve the repository default branch
and its ref, enumerate applicable best merge bases with the candidate, and
require exactly one. Select exactly one candidate in this precedence:

1. supplied review tree;
2. explicitly staged-only;
3. supplied committed candidate or connected local PR head;
4. live WIP.

Capture a nonempty immutable state-location tuple before inspection. For a
connected local PR, record its exact base, head, and diff content. Otherwise
record the candidate kind, fixed point, resolved endpoints, captured diff bytes,
commands and ref resolutions, plus every applicable identity: `HEAD`, index
tree, staged diff, unstaged diff, normalized status and untracked inventory, and
each in-scope untracked path, mode, and content identity. Return `incomplete`
when the fixed point or candidate is missing, ambiguous, partial, empty, or
cannot be identified completely. Judge captured bytes, never later live reads.

Record `Invocation: formal-delivery | standalone` and `Review mode: initial |
remediation`; standalone defaults to `initial`. Apply the Finding Contract's
remediation packet and coverage boundary.

## Cover

Trace the user request, Charter, Source Trace, repository instructions, domain
decisions, captured candidate, tests, required proof, skips, and risk. Narration
is a source pointer, not proof. Supported risk adds the relevant failure,
recovery, security, migration, concurrency, data, or operational scenarios to
coverage; it does not add actors or ceremony by itself.

Trace Spec in this precedence:

1. caller-supplied source;
2. decision-bearing material referenced by captured commits;
3. one matching repository source.

The caller supplies `Spec required: yes | no`; standalone Change Review defaults
to `no`. A missing, unreadable, conflicting, or unresolved required Spec makes
coverage `incomplete`. When optional Spec is absent, record it as skipped; do
not infer intent from tests or implementation.

Trace Standards from repository instructions, the routed
`docs/agents/engineering-contract.md`, maintained test and tool configuration,
and meaningful nearby conventions. Load [SMELL-BASELINE.md](SMELL-BASELINE.md)
only when these Standards are thin. Repository Standards override the fallback.

Freeze one compact in-context row per semantic change unit:

```text
change -> governing commitment -> actual behavior path
       -> applicable Finding Contract classes -> proof -> disposition
```

Trace the real entry, caller, output or effect, and applicable failure or
recovery path. Reuse proof tied to the exact snapshot; run only missing,
invalidated, or repository-required safe checks. Omit inapplicable classes
instead of adding `N/A` bookkeeping. Cover distinct semantic branches and supported risk
interactions, not a blind Cartesian product. Close each row as `inspected`,
`proved`, `skipped-nonmaterial`, or `blocked`; any material skip or block makes
coverage `incomplete`.

When the candidate supersedes or makes behavior redundant, extend coverage to
every displaced implementation, caller, registration, export, flag, test,
configuration, document, and migration required by Change Closure.

## Judge

Judge Spec first: whether the candidate fulfills its commitments with the
intended meaning, scope, contracts, acceptance, and Change Closure. Check for
missing or partial requirements, scope creep, and wrong semantics.

Reset attention to the pinned snapshot and Standards sources; discard Spec
conclusions, severity, counts, and ranking pressure. Judge Standards separately:
whether the candidate is correct, robust, operable, maintainable, well designed,
and adequately proved under the applicable Finding Contract classes. Apply
**Must** rules as floors. Apply **Prefer** rules only when direct evidence shows
violated repository authority or a concrete supported cost.

Behavior is evidence for both axes, not a third axis. Admit finding candidates
only through the Finding Contract. Missing evidence for a required axis makes
coverage `incomplete`; unavailable optional verification is residual risk.

Keep admitted IDs stable. In remediation, dispose each carried ID as `resolved`,
`still admitted`, `disproved`, or `incomplete`.

## Gate

Recompute every applicable snapshot-tuple cell with its recorded command and ref
resolution, including connected PR base, head, and diff content. Any missing or
changed cell makes the decision `incomplete`; name the drift and preserve
findings only as evidence for the original snapshot. Do not recapture.

Derive exactly one decision:

- `blocked` when an admitted finding blocks under the Finding Contract and
  repository policy;
- `incomplete` when required source, coverage, evidence, finding-candidate
  disposition, report state, or drift is unresolved and no admitted blocker
  already establishes `blocked`;
- `pass with residual risk` when coverage is complete and no blocker exists,
  but verified decision-bearing residual risk remains; or
- `pass` when coverage is complete, no blocker remains, and drift is clear.

Return one packet:

```text
Invocation: formal-delivery | standalone
Review mode: initial | remediation
Semantic agent: ordinary-reviewer | integration-reviewer | standalone
Reviewer actor ID:
Reviewer task ID:
Runtime binding: agent type <value or standalone>; requested <model and reasoning or standalone>; observed <values or unavailable>
Fresh-context and separation evidence: <evidence> | standalone
Coverage: complete | incomplete
Decision: pass | pass with residual risk | blocked | incomplete
Fixed point:
Snapshot identity:
Candidate:
Sources: Spec: <source or skipped>. Standards: <sources>.
Covered work:
Spec findings: <admitted findings, none, or skipped>
Standards findings: <admitted findings or none>
Carried dispositions: <when applicable>
Skipped checks:
Residual risk:
Blocker: <when applicable>
Drift: none | detected | not reached
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Completion requires every applicable coverage row and axis to close, the axis
reset to occur, every finding candidate and carried ID to be disposed, drift
read-back to pass, and the packet to be internally consistent. The decision is review
judgment, not mutation, Lock, or Release authority. Return control to the caller
and stop.
