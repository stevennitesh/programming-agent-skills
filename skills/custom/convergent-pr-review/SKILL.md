---
name: convergent-pr-review
description: "Review local PRs and high-risk local diffs through independent fresh-context reviewers and a root-verified evidence ledger. Use for release gates, shared plumbing, migrations, security or permission changes, CI/workflow/config, public interfaces, and data contracts. Hand off ordinary fixed-point Standards/Spec review to $review."
---

# Convergent PR Review

**Pin. Trace. Isolate. Converge. Verify. Report.**

Own one read-only convergence gate over one immutable review snapshot. The review root owns reviewer dispatch, the evidence ledger, verification, drift detection, and the final decision. Downstream implementation owns fixes, tracked mutations, and closeout.

**Route:** Hand off to `$review` and stop for an ordinary branch, WIP, staged, or `review since X` fixed-point review. Carry the caller-supplied Spec requirement, Source Trace and Spec sources, fixed point, and captured target into the handoff.

**Read-only boundary:** Inspect only. Disposable evidence may live under `.tmp/`. A required pre-capture ref fetch may update Git metadata with normal approval and must be recorded. Keep the working tree, index, commits, tracked `.scratch/`, tracker, PR reviews or comments, and external messages unchanged.

**Defaults:** two reviewers, two rounds maximum, and `P0/P1/P2/P3` severity. Use three to five reviewers only when distinct high-risk surfaces need their own lenses; more than five requires an explicit user request.

## 1. Pin

Use the caller-supplied base ref; otherwise discover the repository default branch and merge base.

Capture one complete target:

- supplied review tree: verify `<tree>^{tree}` and inspect with `git show`;
- branch or PR: record base, head, merge base, status, commit range, stat, and full diff;
- worktree: record `HEAD`, status, staged and unstaged diffs, and every in-scope untracked file.

A supplied review tree wins over live targets. Resolve a PR before any fetch needed to capture its head.

Give reviewers the captured snapshot, never a live diff command. A Git commit or tree SHA is already immutable and needs no second hash; hash only captured live content not already addressed by Git.

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

For Standards, use repository rules and meaningful nearby conventions. Load [SMELL-BASELINE.md](../review/SMELL-BASELINE.md) only when repository standards are thin.

Build one reviewer brief containing the captured snapshot, Source Trace, repo contract, Standards and Spec sources, acceptance criteria, touched seams and contracts, validation commands, and relevant migration, permission, generated-artifact, network, or external-service constraints.

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

Each finding includes severity, axis, lens, file:line evidence, violated behavior or contract, impact, remediation direction, and confidence.

Keep parent hypotheses, preliminary findings, peer output, and the partial ledger out of round-one context. Wait for every requested lens; replace failed or timed-out reviewers when capacity permits.

Require at least two fresh-context reviewers over the same snapshot. Parent-context forks do not satisfy independence. When fresh-context reviewers are unavailable, run two separated manual lens passes, label them distinct but non-independent, and report reduced-confidence.

## 4. Converge

Normalize every reviewer finding into one evidence ledger with:

`ID | severity | axis | title | evidence | impact | remediation | lens | confidence | status | verification | blocking decision`

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

Evidence decides; consensus is signal, not truth. Merge same-axis duplicates, link cross-axis overlap without collapsing the axes, and preserve one-reviewer findings when the evidence survives.

Use round two only for a named candidate that remains disputed, ambiguous, under-evidenced, or inconsistent across lenses. Send only its ledger ID, claim, evidence, contrary evidence or open question, and the exact decision needed. Do not resend the whole ledger. Mark any directly evidenced new finding as `new in round 2`.

Stop after no candidate needs challenge or after round two. Finalize every item:

- `accepted` is `verified`;
- `rejected` is `disproved`, or `not checked` with a non-evidentiary reason;
- `duplicate` points to its canonical item and follows its verification and blocking decision;
- `disputed` is `verified` or `not checked`, with the unresolved question and provisional blocking decision;
- every `not checked` item records its reason and confidence impact.

No `candidate` or `unverified` item survives the final report.

## 5. Verify

The review root verifies every accepted and disputed item with the cheapest meaningful direct evidence. Reject disproved claims. Preserve `not checked` only when its blocker, confidence impact, and provisional blocking decision are explicit.

Delete disposable verification artifacts or name each intentionally preserved `.tmp/` path in the report.

Run the drift check before reporting:

- A supplied review tree is immutable.
- For a branch or PR, compare the current target head with the captured head.
- For a live worktree, compare the current `HEAD`, index, status, and in-scope untracked content with the captured snapshot.

Any difference makes the review stale. Rerun against a new snapshot or return `incomplete`.

## 6. Report

Severity and blocking:

- `P0/P1` block.
- `P2` blocks when required validation or CI is affected.
- `P3` is non-blocking unless the caller says otherwise.

**Review decision:** return exactly one:

- `pass`: current snapshot, full confidence, no blocker, and no required check skipped;
- `pass with residual risk`: current snapshot and no blocker, but reduced confidence or non-blocking `not checked` evidence remains;
- `blocked`: an accepted item blocks, or a disputed or `not checked` item has a provisional blocking decision;
- `incomplete`: the target, required Spec or lens, verification, independence, or drift gate did not close.

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

Sort each axis by severity. Include location, evidence, impact, remediation, verification, confidence, and blocking decision. Use `No accepted findings.` for a clean axis and `No accepted findings; disputed: <IDs>.` when disputes remain.

End each accepted finding with a patch-ready handoff naming the finding ID, likely files, required change, and expected validation.

Complete only when the snapshot and Source Trace are recorded; the required Spec gate closed; at least two independent reviewers completed or reduced confidence is explicit; every finding reached a terminal ledger state; survivors were verified or explicitly not checked; drift and the read-only boundary were checked; and one decision plus the complete ledger and patch-ready handoffs were returned.
