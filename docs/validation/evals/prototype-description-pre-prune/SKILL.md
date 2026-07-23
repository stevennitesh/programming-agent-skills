---
name: prototype
description: Answer one bounded design question with a disposable runnable probe. Use for logic, state, data, API or interface shape, structurally different UI bets, or predeclared comparative measurement. Not for production proof, uncertain defect diagnosis, or multi-decision design.
---

# Prototype

**Outcome:** one bounded design question answered by a judgeable disposable probe. The verdict is durable; the probe is not.

**Ownership.** Prototype owns the frozen question, authorized artifacts, one entry point or smallest run recipe, branch Smoke, supported result, and reconciliation. The caller owns adoption, later routing, durable truth, production implementation, and production proof. Direct use returns to the user.

**Write boundary.** Use one invocation-owned `.tmp/prototype/<question-slug>/` root for disposable work, choosing a unique sibling when ownership is uncertain. Use `.scratch/<feature>/prototype/` only for explicitly authorized durable evidence. Touch exact application-tree paths only when real context requires it and the caller authorizes them behind a repository-proved development-only or build-excluded boundary. Preserve unrelated work and external state.

## Fit

Before mutation, decide whether one material design decision can be answered by one bounded runnable-evidence question. When it cannot, state the mismatch and actual need without mutating.

## Freeze

Before mutation, read back:

- the question and informed decision;
- the selected evidence surface;
- the invoker, result recipient, named decision owner, and named human judge when human;
- `claim level: shape/feel | design evidence` and `judgment mode: human | rule-based`;
- the predeclared verdict basis and representative cases, variants, workload, or interactions;
- authorized paths, effects, and artifact disposition;
- one entry point or smallest ordered recipe and a finite bound; and
- known evidence limits.

Decision owner and human judge are independent authorities; never infer either from the other. A `shape/feel` claim requires human judgment. Never invent a material threshold or tune a rule after decisive evidence. Ask only when a missing fact materially changes cost, effects, coverage, or authority, and do not mutate until applicable facts are known.

## Branch

Read only the decision-bearing branch:

| Evidence need | Load |
| --- | --- |
| State, rules, data, API shape, or interface behavior | [LOGIC.md](LOGIC.md) |
| Visual hierarchy, density, navigation, flow, or interaction structure | [UI.md](UI.md) |
| Comparative latency, throughput, resources, variability, or scaling shape | [MEASURE.md](MEASURE.md) |

Return independent evidence needs as separate questions.

## Probe

Build the smallest artifact that exercises the frozen representatives and can change the verdict. Prefer repository-native tools, in-memory state, and only enough structure and error handling for judgeable evidence; persist only when persistence is the question.

## Smoke And Judge

Run the frozen entry point or recipe and pass branch Smoke. Record the command, path or URL, representative surface, material process state, and judgment-affecting assumptions.

Smoke proves only that the probe runs and is judgeable. Apply the frozen verdict basis to the representative evidence. Preserve human-reserved judgment; never replace an unavailable human with a proxy rule. State the supported result or truthful residual, evidence, limits, and unsupported production claims.

Prototype evidence answers only the frozen design question. Production correctness remains with the real coding workflow and its caller-facing proof seam.

## Reconcile

Account for every changed file, directory, process, port, cache, database, datum, route, overlay, and credential. Give each artifact one disposition:

- `delete`: remove created disposable content and verify absence;
- `restore`: remove only Prototype changes and preserve other work;
- `preserve-for-verdict`: keep the restartable minimum only after the result recipient accepts custody and cleanup;
- `authorized-durable-evidence`: retain only at the authorized path and verify by read-back.

Stop processes, release resources, remove ephemeral credentials and stale pointers, and verify repository status and authorized paths. No terminal return leaves a live resource. When cleanup ownership is ambiguous, preserve the conflict and state the blocker without overwriting, resetting, or forcing cleanup.

## Return

Return directly to the current caller, or to the user for direct work, and stop. State truthfully whether the question was answered, awaits human judgment, could not proceed, or did not fit. Include only applicable identity, question, evidence, residual, artifact, limitation, and decision-candidate facts.

Never carry caller identity from a preceding request or supplied result. Do not select, recommend, or invoke a downstream route.

## Completion

Complete when fit is resolved; every mutation followed Freeze; the selected branch ran when admitted; evidence or a truthful residual is returned; Prototype-owned artifacts and live resources are safely reconciled; and the current caller or user receives the result without downstream execution.
