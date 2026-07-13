---
name: convergent-pr-review
description: "Review local PRs and high-risk local diffs with fresh-context independent reviewer subagents and a root-verified evidence ledger. Trigger for release gates, shared plumbing, migrations, security or permission changes, CI/workflow/config, public interfaces, and data contracts. Hand off ordinary fixed-point Standards/Spec review to $review."
---

# Convergent PR Review

Run a read-only **convergence gate** over one pinned **review snapshot**:

**review snapshot -> fresh-context reviewers -> evidence ledger -> targeted challenge -> verified survivors -> drift check -> patch-ready handoff**

The main agent is the **review root**. It pins the target, dispatches direct reviewer children, waits for every requested lens, builds and verifies the ledger, and owns the final report. Reviewers inspect only. Reviewers never spawn subagents, edit files, mutate external state, or claim completion for the gate. Consensus is signal, not truth.

**Fresh-context independence:** start every round-one reviewer without forked parent conversation history. Use `fork_turns="none"` when the active collaboration tool exposes it. Each reviewer receives one complete shared reviewer brief containing the immutable review snapshot and Source Trace, plus its assigned axis, lens, and output contract. Keep parent hypotheses, preliminary findings, peer output, and a partially built ledger out of round-one reviewer context.

**Read-only boundary:** Inspect only. Validation may create disposable artifacts under `.tmp/`. A required pre-capture ref fetch may update Git metadata; record it and follow normal tool approval. After capture, keep the review snapshot fixed. Leave the working tree, index, commits, tracked `.scratch/` state, tracker, PR reviews or comments, and external messages unchanged. Downstream implementation owns patches and closeout mutations. Report sandbox-crossing, network, or external validation and its approval state.

**Spec requirement:** The caller supplies `Spec required: yes | no`. Default to `no` for standalone review. When `yes`, a missing, conflicting, or unresolved Spec source makes the review `incomplete`; never skip or replace the Spec axis.

Hand off to `$review` and stop for ordinary branch, WIP, or `review since X` fixed-point review where Standards and Spec are the main axes. Carry the caller-supplied Spec requirement, Source Trace and Spec sources, fixed point, and captured target into the handoff.

## Defaults

- Base ref: caller-supplied; otherwise discover the repository default branch and merge base
- Reviewers: `2`
- Max rounds: `2`
- Severity: `P0/P1/P2/P3`
- Optional Spec fallback: highest-risk uncovered lens

Scale reviewers by coverage:

- `2`: Standards and Spec.
- `3`: Standards, Spec, and the highest-risk changed surface.
- `4-5`: Standards, Spec, plus distinct security, migration, public-contract, CI/release, performance, caching, or data-contract lenses.
- `>5`: explicit user request only.

## 1. Pin The Review Snapshot

Resolve the fixed point and capture the complete review target once.

- **Supplied review tree:** verify it with `git cat-file -e <review-tree>^{tree}` and inspect snapshot content with `git show <review-tree>:<path>`.
- **Branch or PR:** capture status, branch, base SHA, head SHA, merge base, diff stat, full diff, and commit range.
- **Worktree:** capture `HEAD`, status, staged diff, unstaged diff, and every in-scope untracked file.

For a PR number, resolve and read the PR before fetching its head when needed.

Give every reviewer the captured snapshot, not a live diff command.

**Target gate:** stop before dispatch when the fixed point or review tree does not resolve, the target is empty, or the complete snapshot cannot be captured.

Done means the fixed point and non-empty review snapshot are recorded with the applicable target metadata: snapshot identifier or capture hash, selected diff command, captured content, status for live targets, and commit range when relevant.

## 2. Trace Sources And Build The Reviewer Brief

Trace the current request or caller packet, PR body and decision-bearing comments, linked issue or spec, repo `AGENTS.md`, `docs/agents/engineering-contract.md`, and validation configuration. Resolve each named source before dispatch. Readable sources enter `Source Trace`; unavailable sources enter it with the affected axis and reason. Read every decision-bearing source in full before verifying the ledger; the review root may finish that reading while reviewers run.

Resolve Spec in this order:

1. Caller-supplied selected item, bounded slice, acceptance criteria, path, issue, or spec.
2. PR body, decision-bearing comments, and directly linked issue or spec.
3. Issue or PR references in the captured commit messages.
4. A matching spec, legacy PRD, or issue packet under the repo's documented conventions.

Follow `docs/agents/issue-tracker.md` for PR and issue transport and mutation rules when it exists. When sources disagree, record their precedence and the conflict in `Source Trace`. When `Spec required: yes` and no authoritative Spec source resolves, return `incomplete` before reviewer dispatch. Never replace the required Spec reviewer with a risk lens. When `Spec required: no` and no Spec source exists, record `Spec: skipped - no source available` and replace that reviewer with the highest-risk uncovered lens.

For Standards, include repo rules and [SMELL-BASELINE.md](../review/SMELL-BASELINE.md) when repo standards are thin.

Record missing Standards sources and the affected axis.

The reviewer brief contains:

- captured review snapshot;
- Source Trace;
- repo instructions and engineering contract;
- Standards and Spec sources;
- acceptance criteria or bounded slice;
- touched seams, public interfaces, and data contracts;
- validation commands;
- migration, generated-artifact, permission, network, and external-service constraints.

Build one complete reviewer brief. Inline it when compact. Put only large captured artifacts under `.tmp/convergent-pr-review/<run-id>/` and pass their exact paths.

A Git commit or tree SHA is already immutable and needs no duplicate content hash. Hash a captured artifact only when it represents live staged, unstaged, or untracked work that Git does not already address.

The reviewer brief owns repeated review context. Reviewer prompts carry only the brief or artifact pointer, assigned axis, assigned lens, and output contract.

Done means every reviewer receives the same snapshot, source trace, repo contract, risk surfaces, and validation context.

## 3. Dispatch Fresh-Context Reviewers

The review root is the only dispatcher.

Assign one reviewer the Standards axis and one the Spec axis. Assign additional reviewers distinct risk lenses from the changed surface.

Spawn every round-one reviewer as a direct child with `fork_turns="none"` when supported. Give each reviewer the same reviewer brief and only its assigned axis and lens. Keep every result private until all requested round-one reviewers have returned.

Reviewer prompt:

```text
You are one fresh-context, read-only reviewer. Do not spawn subagents, edit files, or inspect other reviewer output.

Reviewer brief: <inline complete brief or exact artifact path>
Axis: <Standards / Spec / Risk>
Lens: <primary lens>

Read the complete reviewer brief and every source it assigns to your axis. Review only its captured snapshot.

Return only high-confidence actionable findings. Each finding must include severity, axis and lens, file:line evidence, the violated behavior or contract, concrete impact, remediation direction, and confidence.

Prioritize correctness, behavioral regressions, broken contracts, workflow failures, missing validation, CI blockers, security or permission risk, and operator risk. Exclude style-only feedback, broad refactors, and speculation.

Return:
status: <complete / blocked>
axis:
lens:
coverage:
findings: <list or "none">
skipped checks:
blockers:
```

Wait for every requested reviewer. Replace failed or timed-out reviewers when another slot is available.

**Independence gate:** require at least two fresh-context reviewers over the same immutable snapshot. Parent-context forks do not satisfy independence. When fresh-context reviewers are unavailable, run two separated manual lens passes, mark them distinct but non-independent, and report reduced confidence.

Done means every requested lens returned a complete result, was replaced, or is named as an unresolved blocker; and at least two independent passes completed, or the reduced-confidence fallback is explicit.

## 4. Build The Evidence Ledger

Normalize reviewer output into one evidence ledger.

Each ledger item includes ID, severity, axis, title, evidence, impact, remediation direction, reviewer lens, confidence, status, verification state, and blocking decision.

Axis is `Standards`, `Spec`, or `Risk`; lens is the reviewer's assigned focus. Cross-axis overlap may be linked but remains separate.

Status is `candidate`, `accepted`, `rejected`, `duplicate`, or `disputed`. Verification is `unverified`, `verified`, `disproved`, or `not checked`.

During convergence, `candidate` is interim and normally `unverified`. At final report, keep status and verification consistent:

- `accepted` is `verified`.
- `rejected` is `disproved`, or is `not checked` with an explicit non-evidentiary rejection reason.
- `duplicate` points to its canonical ledger ID; its verification and blocking decision follow that item.
- `disputed` is `verified` or `not checked` and records the unresolved question and provisional blocking decision.
- every `not checked` item records the reason and confidence impact.

No `candidate` or `unverified` item survives the final report.

Evidence decides: consensus is signal, not truth; one-reviewer findings can survive; agreed findings can fail.

Done means every reviewer finding is represented, and every surviving candidate has an ID.

## 5. Run Targeted Convergence

Round one establishes independent findings. Keep peer findings private until every round-one reviewer returns.

The review root normalizes round-one output into the evidence ledger, merges same-axis duplicates, links cross-axis overlap, and performs the first evidence check.

Use round two only for a named candidate that remains disputed, ambiguous, materially under-evidenced, or inconsistent across lenses. Send a targeted follow-up to the original reviewer or one opposing reviewer containing only the ledger ID, original claim and evidence, contrary evidence or unresolved question, and the exact confirm, reject, revise, merge, split, or severity decision required.

Do not resend the whole ledger or ask every reviewer to reread the snapshot. New findings in round two require direct file, diff, or command evidence and must be marked `new in round 2`.

Stop when no candidate requires a targeted challenge, or after the configured maximum round. Remaining disagreement stays `disputed`.

Done means every candidate is accepted, rejected, duplicate, or disputed with its evidence state recorded.

## 6. Verify Survivors

The review root verifies accepted and disputed findings.

Use the cheapest meaningful evidence: inspect cited lines, inspect nearby tests, run `git diff --check`, run targeted validation, or inspect affected config, migrations, permissions, or operator workflows.

Keep generated verification artifacts local and disposable under `.tmp/`; delete them or name each intentionally preserved path in the report. Hand off any evidence that must become tracked `.scratch/` state to downstream implementation. Use installs, network or external services, destructive commands, or large generated artifacts only when explicitly requested and permitted by the repo contract and tool policy.

Done means every accepted or disputed finding has a consistent status and verification state; disproved findings were rejected; and every `not checked` item records the blocker, confidence impact, and provisional blocking decision.

## 7. Triage And Report

Severity:

- `P0`: data loss, security exposure, or catastrophic production break.
- `P1`: merge-blocking correctness, contract, or workflow failure on an important path.
- `P2`: required validation or CI failure, important missing validation, optional-tooling blocker, or significant edge-case bug.
- `P3`: lower-risk correctness or maintainability issue with concrete impact.

P0/P1 block merge. P2 blocks when required validation or CI is affected. P3 does not block unless the user says otherwise.

**Review decision:** return exactly one:

- `pass`: the snapshot is current, confidence is full, no accepted or disputed item blocks, and no required check was skipped.
- `pass with residual risk`: the snapshot is current and no item blocks, but confidence is reduced or non-blocking `not checked` evidence remains.
- `blocked`: an accepted item blocks, or a disputed or `not checked` item has a provisional blocking decision.
- `incomplete`: the target, required-lens, verification, or drift gate was not satisfied and no permitted fallback closed it.

The review root owns this decision. The caller owns whether `pass with residual risk` is acceptable for Lock.

**Drift check:** A supplied review tree is immutable. For a branch or PR, compare the current target head with the captured head. For a live worktree, compare the current `HEAD`, index, status, and in-scope untracked content with the captured snapshot. Any difference makes the review stale; rerun before reporting a current result.

Begin with:

```text
Review snapshot: <fixed point and captured target>
Source Trace: <sources and skipped axes>
Reviewers: <completed lenses / requested lenses>
Rounds: <completed / maximum>
Confidence: <full / reduced with reason>
Review decision: <pass / pass with residual risk / blocked / incomplete>
```

Report the final ledger under:

```md
## Standards
## Spec
## Risk
## Rejected Or Duplicate
```

Keep findings in their axis. Sort within each axis by severity. Include ID, location, evidence, impact, remediation direction, verification state, confidence, and blocking decision.

When an axis has no accepted or disputed item, report `No accepted findings.` When disputed items exist without accepted findings, report `No accepted findings; disputed: <IDs>.`

End accepted findings with a patch-ready handoff: finding ID, likely files, required change, and validation expected after the fix.

Done means the report returns the complete ledger, preserves axis separation, records drift and confidence, and provides a patch-ready handoff for every accepted finding.

## Completion Criteria

Complete only when the fixed point and non-empty review snapshot are pinned; Source Trace is recorded; required Spec resolved; round-one reviewers were fresh-context direct children when the runtime supported context control; reviewers never fanned out; at least two independent reviewers inspected the same captured target, or the result is explicitly reduced-confidence and non-independent; Standards and Spec ran, or optional Spec was explicitly skipped and replaced; every reviewer finding is represented in the ledger; any second round was limited to targeted ledger challenges; no candidate or unverified item remains; final status and verification agree; survivors are verified or explicitly not checked; drift and the read-only boundary were checked; severity and blocking decisions are clear; and one review decision plus the complete ledger and any patch-ready handoffs were returned.
