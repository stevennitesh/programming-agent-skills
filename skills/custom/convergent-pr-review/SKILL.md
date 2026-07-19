---
name: convergent-pr-review
description: Review one immutable local PR, release candidate, or bounded high-risk diff read-only through direct fresh-context reviewers, root-verified finding admission, exact degraded-capacity fallbacks, and optional nonblocking advisories, then return one terminal release decision. Root-only. Route open-ended repository correctness, methodology, model-risk, leakage, validation, calibration, analytics, or performance baselines to $audit-codebase.
---

# Convergent PR Review

**Pin. Trace. Isolate. Challenge. Verify. Return.**

Own one read-only convergence gate over one immutable review snapshot.

**Root-only guard:** the top-level root owns review dispatch, the evidence ledger, verification, drift checks, and the decision. If invoked inside a delegated task, stop before Pin and return `incomplete` with a routing blocker. Reviewers apply supplied contracts; they never invoke or orchestrate this skill.

**Terminal:** return one decision and stop. Start no remediation, fix dispatch, worktree creation, tracker mutation, successor review, or snapshot recapture. A `blocked` decision supplies evidence only.

**Read-only:** inspect only. Store disposable evidence under `.tmp/` and record any required pre-capture ref fetch. Keep the worktree, index, commits, tracked `.scratch/`, tracker, PR reviews or comments, and external messages unchanged.

**Defaults:** two reviewers, two rounds maximum, `P0/P1/P2/P3` severity, and `Advisories: no`. Use three to five reviewers only for distinct high-risk Charter lenses; more than five requires an explicit user request.

## 1. Pin

Resolve and record the caller-supplied base ref to a commit SHA; otherwise discover the default branch and merge base.

Capture one complete target:

- supplied review tree: verify `<tree>^{tree}` and inspect with `git show`;
- branch or PR: record base, head, merge base, status, commit range, stat, and full diff;
- worktree: record `HEAD`, status, staged and unstaged diffs, and every in-scope untracked file.

**Snapshot precedence:** a supplied review tree wins over live targets. Resolve a PR before any fetch needed to capture its head. Give reviewers the captured snapshot, never live diff commands. Git-addressed content needs no second hash; hash only captured live content.

Record a new run ID and `Review mode: initial | remediation | assurance`.

- `initial`: first full-Charter review of the candidate.
- `remediation`: new invocation over a successor snapshot; require the original Charter, prior snapshot, carried finding IDs, Repair delta, and remaining acceptance.
- `assurance`: new full-Charter invocation over the same accepted snapshot because the caller requested more confidence.

**Fresh invocation:** every mode gets a new brief and ledger. A prior-invocation reviewer is not independent. Assurance is neither remediation, a same-invocation retry, nor round two.

Return `incomplete` before dispatch when the fixed point or target does not resolve, the target is empty, or the complete snapshot cannot be captured.

## 2. Trace

Build one Source Trace from the request or caller packet, PR body and decision-bearing comments, linked issues or specs, captured commits, repo instructions, `docs/agents/engineering-contract.md`, and validation configuration. Follow `docs/agents/issue-tracker.md` when present. Record unavailable or conflicting sources, their axis, and precedence.

Resolve Spec in this order:

1. Caller-supplied item, slice, criteria, path, issue, or spec.
2. PR body, decision-bearing comments, and directly linked sources.
3. References in captured commit messages.
4. Matching sources under repository conventions.

The caller supplies `Spec required: yes | no`; default to `no` for standalone review. A required missing, conflicting, or unresolved source makes the review `incomplete` before dispatch. Never skip or replace a required Spec axis. When optional and absent, record `Spec: skipped - no source available` and replace that reviewer with the highest-risk uncovered lens.

For Standards, use repository rules and meaningful nearby conventions. Load [SMELL-BASELINE.md](../review/SMELL-BASELINE.md) only when those are thin and label resulting findings `baseline judgement call`.

Read [FINDING-CONTRACT.md](../review/FINDING-CONTRACT.md). When the Charter says `Advisories: yes`, also read [ADVISORY-CONTRACT.md](../review/ADVISORY-CONTRACT.md). Build one brief containing the snapshot, Charter, mode, Source Trace, Standards and Spec sources, acceptance, touched seams, validation, and relevant migration, permission, generated-artifact, network, or service constraints. In remediation mode, limit the brief to carried findings, the Repair delta, and remaining original acceptance.

**Inline:** keep the brief in context. Store only large captured artifacts under `.tmp/convergent-pr-review/<run-id>/` and pass exact paths. Finish decision-bearing reading before ledger verification.

## 3. Isolate

Assign Standards and Spec first, then distinct risk lenses. Spawn every round-one reviewer as a direct child with `fork_turns="none"`. Reviewers never spawn, edit, mutate external state, or own the final decision.

Give each reviewer only the shared brief, assigned axis, lens, and output contract:

```text
status: complete | blocked
axis: Standards | Spec | Risk
lens:
coverage:
findings:
advisories: <when enabled>
skipped checks:
blockers:
```

**Blind round one:** withhold parent hypotheses, preliminary findings, peer output, and the partial ledger. Wait for every requested lens; replace failed reviewers when capacity permits. Reconcile active capacity and retry dispatch once before degrading.

| Available independent review | Required coverage | Maximum no-blocker decision |
| --- | --- | --- |
| At least two fresh completed reviewers | All required Standards, Spec, and risk lenses across fresh direct reviewers | `pass` |
| Exactly one fresh completed reviewer | Fresh reviewer plus separated root pass or passes covering every missing lens | `pass with residual risk` |
| Zero fresh completed reviewers | Two separated root passes with an explicit lens reset, collectively covering every required lens | `pass with residual risk` |
| Any required lens or evidence axis remains uncovered | Stop | `incomplete` |

A blocker may still produce `blocked` in any row. Reused, inherited-context, campaign-participating, or resumed tasks never count as independent. Reduced-capacity execution never produces plain `pass`.

## 4. Challenge

Normalize reviewer findings into one evidence ledger using the shared finding fields plus `title | lens | confidence | status | verification | blocking decision`.

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

**Evidence over consensus:** merge same-axis duplicates, link cross-axis overlap without collapsing axes, and preserve one-reviewer findings whose evidence survives.

Use round two only for a named candidate that remains disputed, ambiguous, under-evidenced, or inconsistent. Prefer a new direct `fork_turns="none"` challenger and send only the ledger ID, claim, evidence, contrary evidence or question, and exact decision needed. Use `followup_task` on the originating reviewer only to obtain an omitted contract field, locate evidence it already claimed, or answer a narrow question about its own output. Such continuation adds no independence and receives no peer findings or shared provisional ledger.

**Same snapshot:** round two keeps the original snapshot and lenses; it is not a new audit. Label a remediation regression `new in round 2`. Stop when no candidate needs challenge or after round two.

Finalize every item: accepted is verified; rejected is disproved or `not checked` with a non-evidentiary reason; duplicate points to its canonical item; disputed records the unresolved question and provisional blocking decision; every `not checked` item records its reason and confidence impact. No `candidate` or `unverified` item survives.

When enabled, verify advisories separately under the advisory contract. They never enter the finding ledger.

## 5. Verify

**Root verification:** verify every accepted and disputed finding under the shared Bound rules. Reject disproved claims. Preserve `not checked` only with its reason, Charter relevance, confidence impact, and provisional blocking decision.

Delete disposable evidence or name each preserved `.tmp/` path.

**Drift gate:** before reporting, compare:

- supplied review tree: immutable;
- branch or PR: compare current target head with captured head;
- live worktree: compare current `HEAD`, index tree, staged diff, unstaged diff, status, and all in-scope untracked paths and content with the captured snapshot.

Any difference makes the review stale. Return `incomplete`; only the caller may authorize another snapshot.

## 6. Return

**Review decision:** return exactly one:

- `pass`: current snapshot, full confidence, no blocker, every required check covered, and at least two independent reviewers completed;
- `pass with residual risk`: current snapshot and no blocker, but capacity was degraded or non-blocking `not checked` evidence remains;
- `blocked`: an accepted item blocks, or a disputed or `not checked` item has a provisional blocking decision;
- `incomplete`: the target, required Spec or lens, verification, or drift gate did not close.

The caller alone decides whether `pass with residual risk` is acceptable for Lock.

Begin with:

```text
Review snapshot:
Source Trace:
Review mode:
Run ID:
Reviewers:
Rounds:
Confidence:
Review decision:
```

Return the complete ledger under:

```md
## Standards
## Spec
## Risk
## Rejected Or Duplicate
```

Sort each axis by severity and render the shared fields plus ledger fields. Use `No accepted findings.` for a clean axis and `No accepted findings; disputed: <IDs>.` when disputes remain. End each accepted finding with a repair-ready handoff naming its ID, likely files, required change, and expected validation.

When enabled, append a separate `## Advisories` annex. Advisories have no severity, never affect confidence or decision, and grant no mutation authority. Omit the annex when disabled.

End with:

```text
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

**Complete:** record the snapshot, Charter, mode, run ID, and Source Trace; close the Spec, capacity, terminal-ledger, admission, verification, advisory, drift, and read-only gates; return one decision and the complete ledger to the caller.
