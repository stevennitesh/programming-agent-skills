---
name: prototype
description: Prototype one design question with a throwaway runnable probe. Use for a terminal decision surface over logic, state, or data; structurally different UI bets on one real route; or a caller's runnable evidence gap.
---

# Prototype

**Outcome:** one design question answered by a judgeable, disposable probe. The verdict is durable; the code is not.

**Ownership.** Prototype owns the locked question, authorized artifacts, one repo-native command, branch smoke proof, verdict packet, and reconciliation. The user judges shape and feel. The caller owns the resulting decision, durable publication, tracker, spec, domain, ADR, commit, and production mutations. The real coding workflow owns production proof.

**Write boundary.** Use `.tmp/` for disposable work. Use an app-tree path only when real constraints require it and the request or caller authorizes it. Put explicitly authorized version-controlled evidence in caller-owned `.scratch/<feature-slug>/prototype/`.

## 1. Lock

Trace exactly one question to the prompt or caller packet and relevant code constraints.

Lock:

- the decision it unlocks;
- the judge;
- the claim level: `shape/feel` or `design evidence`;
- authorized paths;
- cleanup or preservation intent.

Iterate within that question. A disproved premise may replace it; adjacent questions wait.

When the answer must establish production behavior or semantic correctness, return it to the real coding workflow under `docs/agents/engineering-contract.md`.

## 2. Branch

- **Logic, state, or data:** Read [LOGIC.md](LOGIC.md) and build a terminal decision surface.
- **UI direction:** Read [UI.md](UI.md) and compare structural bets in real app context.

When ambiguous, infer the branch from the decision surface and record the assumption.

## 3. Probe

Build the smallest artifact that can change the verdict.

Use the repo's language, runtime, tooling, and one run command. Keep state in memory unless persistence is the question. Add only enough structure and error handling to make the probe judgeable.

## 4. Smoke

Run the command and pass the branch-specific smoke gate.

Smoke proves the probe is judgeable, not production-correct. Report the command, artifact path or URL, and assumptions that affect judgment.

## 5. Judge

Hand the probe to its judge and iterate within the locked question.

- **Shape/feel:** Capture the user's verdict and decisive feedback. If unavailable, return `awaiting-verdict`, preserve the named runnable artifacts, and report the exact command or URL.
- **Design evidence:** Record the examples, invariants, fixtures, edge cases, observed limits, and chosen direction.
- **Blocked:** Record the blocker, attempted path, and evidence still needed.

Return a verdict packet with:

- status: `answered`, `awaiting-verdict`, or `blocked`;
- Source Trace, question, decision, branch, and claim level;
- artifact paths, command, URL, and variant keys;
- smoke proof and judgment-affecting assumptions;
- verdict or evidence, limits, chosen direction, and residual uncertainty;
- cleanup or preservation state;
- next route and any domain or ADR candidate.

Return the packet directly to the invoking caller. Recommend `$handoff` only when the verdict must cross sessions. Recommend `$domain-modeling` when the caller should resolve durable language or an ADR candidate.

## 6. Reconcile

- **Answered:** Return the packet, then delete prototype artifacts unless the request or caller explicitly preserves them.
- **Awaiting verdict:** Preserve the named runnable artifacts and report one next judging action.
- **Blocked:** Account for every prototype path as deleted or intentionally preserved.

Return the validated direction, not prototype code, to the real coding workflow.

## Completion

Complete when the question is locked, the selected branch file was followed, one repo-native command runs, the branch smoke gate passes, the verdict packet is returned, and every prototype path is deleted or intentionally preserved.

`awaiting-verdict` completes only the build-and-handoff session. `blocked` returns evidence without claiming completion.
