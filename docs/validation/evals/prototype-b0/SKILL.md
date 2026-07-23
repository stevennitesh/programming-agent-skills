---
name: prototype
description: Prototype one design question with a throwaway runnable probe. Use for a terminal decision surface over logic, state, data, or API/interface shape; structurally different UI bets on one real route; or a caller's runnable evidence gap.
---

# Prototype

**Outcome:** one bounded design question answered by a judgeable disposable probe. The verdict is durable; the probe is not.

**Ownership.** Prototype owns the frozen question, authorized artifacts, one entry point or smallest run recipe, branch Smoke, supported result, and reconciliation. The caller owns adoption, later routing, durable truth, production implementation, and production proof. Direct use returns to the user.

**Write boundary.** Use one invocation-owned `.tmp/prototype/<question-slug>/` root for disposable work. Use `.scratch/<feature-slug>/prototype/` only for explicitly authorized durable evidence. Touch exact application-tree paths only when real context requires it and the caller authorizes them behind a repository-proved development-only or build-excluded boundary. Preserve unrelated work and external state.

## Fit

Before mutation, decide whether one material design decision can be answered by one bounded runnable-evidence question. When it cannot, state the mismatch and actual need without mutating.

## Freeze

Before mutation, read back:

- the question and informed decision;
- the selected Logic or UI evidence surface;
- who decides and who receives the result;
- the verdict basis and representative cases, variants, or interactions;
- authorized paths and effects;
- one entry point or smallest ordered recipe and a finite bound; and
- known evidence limits.

Ask only when a missing fact materially changes cost, effects, coverage, or authority. Do not mutate until the applicable facts are known.

## Branch

- **Logic, state, data, API shape, or interface behavior:** read [LOGIC.md](LOGIC.md).
- **Visual hierarchy, density, navigation, flow, or interaction structure:** read [UI.md](UI.md).

Use one evidence surface for the question. Return independent evidence needs as separate questions.

## Probe

Build the smallest artifact that can change the decision. Use repository-native tools, in-memory state by default, and only enough structure and error handling to make the probe judgeable.

## Smoke And Judge

Run the frozen entry point or recipe and pass the selected branch's Smoke gate. Record the command, path or URL, representative surface, and judgment-affecting assumptions.

Smoke proves only that the probe runs and is judgeable. Apply the frozen verdict basis to the representative evidence. Preserve human-reserved judgment; when that human is unavailable, keep only the restartable minimum under a named owner and state that the verdict remains pending. State the supported direction, evidence, limits, and unsupported production claims. If the probe cannot discriminate inside the bound, return the exact residual without claiming an answer.

## Reconcile

Stop Prototype-created processes and release their resources. Delete or restore Prototype-owned disposable changes while preserving unrelated work. Preserve only the minimum restartable artifact required for a pending human verdict under a named owner, or retain explicitly authorized durable evidence at its authorized path. Verify resulting paths and resource state. When cleanup ownership is ambiguous, preserve the conflict and state the blocker without overwriting or forcing cleanup.

## Return

Return directly to the current caller, or to the user for direct work, and stop. State truthfully whether the question was answered, awaits human judgment, could not proceed, or did not fit. Include only applicable question, evidence, residual, artifact, limitation, and decision-candidate facts. Do not select, recommend, or invoke a downstream route.

## Completion

Complete when fit is resolved; every mutation followed Freeze; the selected Logic or UI surface ran when admitted; evidence or a truthful residual is returned; Prototype-owned artifacts and live resources are safely reconciled; and the current caller or user receives the result without downstream execution.
