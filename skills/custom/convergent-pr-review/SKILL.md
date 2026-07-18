---
name: convergent-pr-review
description: "Review one immutable local PR or high-risk diff read-only through independent fresh-context reviewers and a root-verified evidence ledger, then return one terminal decision. Use for release gates, shared plumbing, migrations, security or permission changes, CI/workflow/config, public interfaces, and data contracts."
---

# Convergent PR Review

**Pin. Trace. Isolate. Challenge. Verify. Return.**

Own one read-only convergence gate over one immutable review snapshot. The review root owns reviewer dispatch, the evidence ledger, verification, drift detection, and the final decision. The implementation caller owns any authorized repair, tracked mutation, and closeout.

**Terminal boundary:** Return one decision and stop. This invocation performs no remediation, fix-worker dispatch, worktree creation, tracker mutation, successor review, or snapshot recapture. A `blocked` decision supplies evidence; it grants no mutation or rereview authority.

**Read-only boundary:** Inspect only. Disposable evidence may live under `.tmp/`. A required pre-capture ref fetch may update Git metadata with normal approval and must be recorded. Keep the working tree, index, commits, tracked `.scratch/`, tracker, PR reviews or comments, and external messages unchanged.

**Defaults:** two reviewers, two rounds maximum, and `P0/P1/P2/P3` severity. Use three to five reviewers only when distinct Charter surfaces need their own high-risk lenses; more than five requires an explicit user request.

## 1. Pin

Resolve and record the caller-supplied base ref to a commit SHA; otherwise discover the default branch and merge base, then record the resolved commit.

Capture one complete target:

- supplied review tree: verify `<tree>^{tree}` and inspect with `git show`;
- branch or PR: record base, head, merge base, status, commit range, stat, and full diff;
- worktree: record `HEAD`, status, staged and unstaged diffs, and every in-scope untracked file.

A supplied review tree wins over live targets. Resolve a PR before any fetch needed to capture its head.

Give reviewers the captured snapshot, never a live diff command. A Git commit or tree SHA is already immutable and needs no second hash; hash only captured live content not already addressed by Git.

Record `Review mode: initial | remediation`; default to `initial`. Remediation mode requires the original Charter, prior snapshot, carried finding IDs, and repair delta.

Return `incomplete` before dispatch when the fixed point or review tree does not resolve, the target is empty, or the complete snapshot cannot be captured.

## 2. Trace

Build one Source Trace from the request or caller packet, PR body and decision-bearing comments, linked issues or specs, captured commits, repo instructions, `docs/agents/engineering-contract.md`, and validation configuration. Follow `docs/agents/issue-tracker.md` for PR and issue transport and mutation rules when it exists. Record unavailable or conflicting sources, their affected axis, and precedence.

Resolve Spec in this order:

1. Caller-supplied item, slice, criteria, path, issue, or spec.
2. PR body, decision-bearing comments, and directly linked sources.
3. References in captured commit messages.
4. Matching sources under repository conventions.

The caller supplies `Spec required: yes | no`. Default to `no` for standalone review.

When `Spec required: yes`, a missing, conflicting, or unresolved authoritative source makes the review `incomplete`; return `incomplete` before reviewer dispatch and never skip or replace the Spec axis. When `no` and no Spec resolves, record `Spec: skipped - no source available` and replace that reviewer with the highest-risk uncovered lens.

For Standards, use repository rules and meaningful nearby conventions. Load [SMELL-BASELINE.md](../review/SMELL-BASELINE.md) only when documented repository standards and meaningful nearby conventions are thin. Label any resulting finding a `baseline judgement call`.

Read [FINDING-CONTRACT.md](../review/FINDING-CONTRACT.md). Build one reviewer brief containing the captured snapshot, Charter, review mode, Source Trace, repo contract, Standards and Spec sources, acceptance criteria, touched seams and contracts, validation commands, and relevant migration, permission, generated-artifact, network, or external-service constraints. In remediation mode, include only carried findings, the repair delta, and remaining original acceptance.

Inline it when compact. Put only large captured artifacts under `.tmp/convergent-pr-review/<run-id>/` and pass exact paths; the review root may finish that reading while reviewers run, but must finish before ledger verification.

## 3. Isolate

**Fresh-context independence:** The review root is the only dispatcher. Reviewers never spawn subagents, edit files, mutate external state, or own the final decision.

Assign Standards and Spec first, then distinct risk lenses when justified. Spawn every round-one reviewer as a direct child with `fork_turns="none"` when supported. Give each reviewer only the shared brief, assigned axis, assigned lens, and this output contract:

```text
status: complete | blocked
axis: Standards | Spec | Risk
lens:
coverage:
findings:
skipped checks:
blockers:
```

Each finding applies the shared admission gates and returns its fields plus lens and confidence.

Keep parent hypotheses, preliminary findings, peer output, and the partial ledger out of round-one context. Wait for every requested lens; replace failed or timed-out reviewers when capacity permits.

Require at least two fresh-context reviewers over the same snapshot. Parent-context forks do not satisfy independence. When fresh-context reviewers are unavailable, run two separated manual lens passes, label them distinct but non-independent, and report reduced-confidence.

## 4. Challenge

Normalize every reviewer finding into one evidence ledger using the shared finding fields plus `title | lens | confidence | status | verification | blocking decision`.

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

Evidence decides; consensus is signal, not truth. Merge same-axis duplicates, link cross-axis overlap without collapsing the axes, and preserve one-reviewer findings when the evidence survives.

Use round two only to challenge a named candidate that remains disputed, ambiguous, under-evidenced, or inconsistent across lenses. Send only its ledger ID, claim, evidence, contrary evidence or open question, and the exact decision needed. Keep the same snapshot and lenses; round two is not a new audit. Label a round-two repair regression `new in round 2`.

Stop after no candidate needs challenge or after round two. Finalize every item:

- `accepted` is `verified`;
- `rejected` is `disproved`, or `not checked` with a non-evidentiary reason;
- `duplicate` points to its canonical item and follows its verification and blocking decision;
- `disputed` is `verified` or `not checked`, with the unresolved question and provisional blocking decision;
- every `not checked` item records its reason and confidence impact.

No `candidate` or `unverified` item survives the final report.

## 5. Verify

The review root verifies every accepted and disputed item under the shared Bound rules. Reject disproved claims; preserve `not checked` only with its reason, Charter relevance, confidence impact, and provisional blocking decision.

Delete disposable verification artifacts or name each intentionally preserved `.tmp/` path in the report.

Run the drift check before reporting:

- A supplied review tree is immutable.
- For a branch or PR, compare the current target head with the captured head.
- For a live worktree, compare the current `HEAD`, index tree, staged diff, unstaged diff, status, and all in-scope untracked paths and content with the captured snapshot.

Any difference makes the review stale. Return `incomplete`; the caller alone decides whether another snapshot is authorized.

## 6. Return

**Review decision:** return exactly one:

- `pass`: current snapshot, full confidence, no blocker, and no required check skipped;
- `pass with residual risk`: current snapshot and no blocker, but reduced confidence or non-blocking `not checked` evidence remains;
- `blocked`: an accepted item blocks, or a disputed or `not checked` item has a provisional blocking decision;
- `incomplete`: the target, required Spec or lens, verification, or drift gate did not close, and no permitted fallback closed it.

The review root owns this decision. The caller owns whether `pass with residual risk` is acceptable for Lock.

Begin with:

```text
Review snapshot:
Source Trace:
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

Sort each axis by severity and render the shared finding fields plus the ledger fields. Use `No accepted findings.` for a clean axis and `No accepted findings; disputed: <IDs>.` when disputes remain.

End each accepted finding with an advisory patch-ready handoff naming the finding ID, likely files, required change, and expected validation.

End the report with:

```text
Return boundary: caller
Mutation authority: none
Successor snapshot authority: none
```

Complete only when the snapshot, Charter boundary, review mode, and Source Trace are recorded; the required Spec gate closed; at least two independent reviewers completed or reduced confidence is explicit; every finding reached a terminal ledger state and passed the admission contract; survivors were verified or explicitly not checked; drift and the read-only boundary were checked; and one decision plus the complete ledger and advisory handoffs returned control to the caller.
