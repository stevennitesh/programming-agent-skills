---
name: prototype
description: Prototype one design question with a throwaway runnable probe. Use when the user asks to drive state, domain logic, or a data shape through cases in a tiny terminal app; compare structurally different UI bets on one real route; or another skill delegates a runnable evidence gap.
---

# Prototype

A prototype is a **throwaway probe for one design question**. The question decides the shape. The **verdict**, not the code, is durable.

Question -> branch -> smallest probe -> smoke gate -> verdict -> cleanup or handoff.

## Ownership

- **Prototype:** Own the locked question, authorized `.tmp/` and app-tree paths, one repo-native command, branch smoke proof, verdict packet, and cleanup.
- **Caller:** Own the decision, durable publication, tracker, spec, ADR, domain, and commit mutations, and promotion into production behavior.
- **Judge:** The user owns shape/feel verdicts. Named examples, invariants, fixtures, and edge cases support design evidence. The real coding workflow owns production proof.
- **Write boundary:** Use `.tmp/` for disposable work. Route explicitly authorized version-controlled evidence to caller-owned `.scratch/<feature-slug>/prototype/`. Use app-tree paths only when real constraints require them and the request or caller authorizes them.

## 1. Lock The Prototype Contract

Trace one question to the user prompt or caller packet and the relevant code constraints.

Name:

- the decision it unlocks;
- the judge;
- the claim level: shape/feel verdict or design evidence;
- the authorized paths;
- the cleanup plan.

Hold one question. Iterate within it until the judge can decide. A disproved premise may replace it; adjacent questions wait.

**Production-proof gate:** When the requested result must establish production behavior or semantic correctness, return the contract to the real coding workflow. Read `docs/agents/engineering-contract.md` before changing production behavior.

## 2. Pick The Branch

- **Logic, state, or data shape:** Read [LOGIC.md](LOGIC.md). Build a tiny terminal app that lets the judge drive the decision surface through cases.
- **UI direction:** Read [UI.md](UI.md). Build structurally different UI bets on one route, switchable through URL state and visible prototype chrome.

When the branch is ambiguous, infer it from the decision surface and record the assumption.

## 3. Build The Smallest Probe

Build only what can change the verdict.

- **Disposable first:** Put shells, copied references, experiments, and notes under `.tmp/`. Call real seams from there when possible.
- **Real constraints:** Use an authorized app-tree path only when routing, layout, auth, data, density, or component behavior is part of the question.
- **Repo-native:** Use the existing language, runtime, tooling, and one run command.
- **Fidelity budget:** Add only the structure and error handling needed to make the question judgeable.
- **In-memory default:** Persist only when persistence is the question; use clearly marked `.tmp/` storage.
- **Disposable diff:** Mark prototype code clearly and keep every `.tmp/` or authorized prototype path easy to delete.

## 4. Pass The Smoke Gate

Run the prototype through its one command and complete the branch-specific smoke check.

The smoke gate proves the probe is judgeable. The verdict gate answers the question.

Report the command, artifact path or URL, and every assumption that affects judgment.

## 5. Capture The Verdict

Hand the probe to its judge and iterate within the locked question.

- **Shape/feel:** Capture the user's verdict and decisive feedback. When the user is unavailable, set status to `awaiting-verdict`, preserve the named artifacts intentionally, and report the exact command or URL.
- **Design evidence:** Record the examples, invariants, fixtures, edge cases, and observed limits. Label the result design evidence; production proof remains with the real coding workflow.
- **Blocked:** Record the blocker, attempted path, and evidence still needed.

Return a **verdict packet** containing:

- status: `answered`, `awaiting-verdict`, or `blocked`;
- Source Trace: originating prompt or caller artifact, plus relevant code constraints;
- question and decision it unlocks;
- branch and claim level;
- artifact paths, command, URL, and variant keys;
- smoke proof;
- verdict, feedback or evidence, and limits;
- chosen direction and residual uncertainty;
- cleanup or preservation state;
- next route and any domain or ADR candidate.

Return the packet directly to the invoking caller. Recommend `$handoff` only when the verdict must cross sessions. Flag domain or ADR candidates for the caller to route through `$domain-modeling`.

## 6. Reconcile The Artifacts

- **Answered:** Capture the verdict packet, then delete prototype artifacts by default. Preserve only artifacts the request or caller explicitly keeps.
- **Awaiting verdict:** Preserve the named runnable artifacts and report the single next judging action.
- **Blocked:** Reconcile every prototype path as deleted or intentionally preserved.
- **Promotion:** Send the validated shape into the real coding workflow. Prototype code remains disposable.

## Completion Criteria

Complete only when the prototype contract is locked, the correct branch file was followed, the probe runs through one repo-native command, the branch smoke gate passed, the verdict packet was returned, and every prototype path is deleted or intentionally preserved.

`awaiting-verdict` completes the build-and-handoff session; the design question remains open.
