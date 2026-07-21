---
name: prototype
description: Answer one bounded design question with a disposable runnable probe. Use for logic, state, data, API or interface shape, structurally different UI bets, or predeclared comparative measurement. Not for production proof, uncertain defect diagnosis, or multi-decision design.
---

# Prototype

**Outcome:** one design question answered by a judgeable disposable probe. The verdict is durable; the probe is not.

**Boundary.** Prototype owns admission, one frozen question, authorized artifacts, branch Smoke and verdict evidence, reconciliation, and one terminal packet. The caller owns adoption, later routing, durable domain or specification truth, production implementation, and production proof.

**Authority.** Default disposable work to one invocation-owned `.tmp/prototype/<question-slug>/` root. Use a unique sibling when an existing root's ownership is uncertain. Use `.scratch/<feature>/prototype/` only for explicitly authorized durable evidence. Touch exact application-tree paths only when real context is necessary, the paths and disposition are authorized, a pre-existing development-only or build-excluded boundary positively isolates them from production, and repository proof can verify that isolation.

Keep production behavior, production tests, dependencies, package and environment configuration, external data, trackers, specs, domain records, ADRs, Git state, and releases unchanged. Use disposable assertions, fixtures, and local launch configuration only inside authorized prototype paths. Inventory pre-existing dirty work and every file or non-file side effect before mutation.

```text
Admit -> Freeze -> Load -> Probe -> Smoke -> Judge -> Reconcile -> Return
```

## 1. Admit

Admit without mutation only when:

1. exactly one material design decision lacks runnable evidence;
2. one falsifiable or discriminating question expresses the uncertainty;
3. runnable evidence can compare directions, explore one bounded variation frame, or test one explicit threshold; and
4. a disposable probe can be built and reconciled inside the authorized repository and side-effect boundary.

If any condition fails, return `not-admitted` with the original `request_subject`, failed fit, and actual need shape. Missing Freeze authority or evidence fields are readiness failures, not non-admission; return `blocked` if they cannot be resolved safely.

## 2. Freeze

Before mutation, read back five locks. Every fact remains required when applicable.

1. **Ownership:** invoker, `return_owner`, `decision_owner`, named human judge when human, and the proposed custody owner for any `preserve-for-verdict` artifact.
2. **Question and evidence:** one question and informed decision; alternatives, threshold, or bounded variation frame; one branch; `claim_kind: shape/feel | design-evidence`; `judgment_mode: human | rule-based`; predeclared rule when rule-based; and representative cases, variants, workload, or interactions.
3. **Mutation authority:** disposable root, exact application-tree or durable-evidence paths, permitted and prohibited effects, and each artifact's intended disposition.
4. **Execution and finite bound:** one primary entry point or smallest ordered run recipe, plus the iteration, variant, case, time, or effort bound.
5. **Known limitations:** evidence limits and unsupported extrapolations known before execution.

Propose a proportional representative set, variation frame, and finite bound when omitted. Ask only when materially different choices change cost, effects, coverage, or decision authority. Caller-supplied bounds and material success thresholds win. Do not invent a business threshold or tune a rule after seeing decisive evidence.

A change to the question, decision, claim kind, judgment mode, representative set, verdict rule, or mutation boundary requires a fresh Admit and Freeze.

## 3. Load

Freeze selects one decision-bearing branch. Load exactly one branch reference:

| Evidence need | Load |
| --- | --- |
| State, rules, data, API shape, or interface behavior | [LOGIC.md](LOGIC.md) |
| Visual hierarchy, density, navigation, flow, or interaction structure | [UI.md](UI.md) |
| Comparative latency, throughput, resources, variability, or scaling shape | [MEASURE.md](MEASURE.md) |

The probe may use any authorized host, renderer, driver, collector, language, or tool without loading a second branch contract. If two branch contracts must independently establish the answer, return coordination to the caller as fresh questions.

## 4. Probe

Build the smallest artifact that can exercise the frozen representative set and change the verdict. Use repository-native language, runtime, and tooling. Keep state in memory unless persistence is the question. Add only enough structure and error handling to make the evidence judgeable.

## 5. Smoke

Run the frozen entry point or ordered recipe and pass the selected branch's Smoke gate. Record the command or recipe, artifact path or URL, reachable representative surface, material process state, and judgment-affecting assumptions.

Smoke proves only that the probe runs and is judgeable. It does not answer the question or prove production behavior.

## 6. Judge

Collect discriminating evidence over the frozen representative set.

| Claim kind | Judgment mode | Rule |
| --- | --- | --- |
| `shape/feel` | `human` | Capture the named human's explicit verdict. |
| `shape/feel` | `rule-based` | Invalid; restate the claim as `design-evidence`. |
| `design-evidence` | `rule-based` | Apply the predeclared reproducible rule. |
| `design-evidence` | `human` | Capture the named human's verdict when judgment is reserved. |

Never replace an unavailable human with a proxy rule. If human judgment is unavailable after green Smoke, prepare `awaiting-verdict`. If the rule or representative set cannot discriminate inside the finite bound, prepare `blocked`. Record evidence, invariants, cases, feedback, limits, unsupported claims, and the one `verdict` when answered. A `verdict` may be an alternative, `none`, a threshold result, or another answer defined by the frozen rule.

Verdict evidence answers only the frozen design question. Production correctness remains with the real coding workflow and its caller-facing proof seam.

## 7. Reconcile

Account for every file, directory, process, port, cache, database, generated datum, route, overlay, and credential created or changed by the invocation. Give each artifact one final disposition:

- `delete`: remove invocation-created disposable content and verify absence;
- `restore`: remove only Prototype-owned changes while preserving pre-existing and concurrent work;
- `preserve-for-verdict`: keep the minimum restartable judgeable surface only after the named `return_owner` explicitly accepts custody and cleanup responsibility;
- `authorized-durable-evidence`: retain only at the caller-authorized evidence path and verify it by read-back.

Stop processes, release resources, remove ephemeral credentials, verify repository status and authorized paths, and remove stale packet pointers. Answered work deletes or restores the runnable probe unless durable evidence was authorized. No terminal return leaves a live resource. When cleanup ownership is ambiguous, preserve the conflicting artifact and return `blocked` rather than overwriting, resetting, or forcing cleanup.

## 8. Return

Return one labeled Markdown packet with this shared envelope:

```text
invoker:
return_owner:
decision_owner: <when known>
status: answered | awaiting-verdict | blocked | not-admitted
source_trace:
request_subject:
```

Add exactly one status-owned delta:

- **`not-admitted`:** failed fit, actual need shape, and confirmation that no prototype mutation occurred. Do not fabricate a question or informed decision.
- **`blocked`:** question and informed decision; Freeze fields reached; failed operation; exhausted or unsafe boundary; evidence; artifact reconciliation; and smallest resumption requirement. A blocked artifact may inform a later fresh invocation but cannot enter Resume.
- **`awaiting-verdict`:** question and informed decision; complete Freeze; human judge; entry point or restart recipe and expected URL; Smoke; minimum preserved inventory; accepting custody owner and cleanup obligation; exact judging action; and an explicit unresolved/no-live-resource statement.
- **`answered`:** question and informed decision; complete Freeze; Smoke; verdict evidence or human feedback; one `verdict`; supported and unsupported claims; limits and production-proof non-claim; artifact reconciliation and repository read-back; and any domain or ADR candidate.

Each delta is also its completion predicate. `answered` alone resolves the question. Do not add universal `last_operation` or `next_required_action` fields, a second result field, or meaningless `inapplicable` values.

Caller-invoked work always returns to its caller. After completing a direct `not-admitted` packet, invoke `$skill-router` only when the active Router policy admits terminal residuals, no caller-owned return or handoff applies, the residual packet is complete, and no unchanged Router cycle exists. Surface its intact recommendation or `none`; do not start or promise the destination. Otherwise return the non-admission directly to the user.

## Resume

Resume is permitted only from an `awaiting-verdict` packet. Start a fresh invocation, then verify the same question, decision, owners, claim kind, judgment mode, verdict rule, representative set, mutation boundary, and bounds; verify artifact path and accepted custody; inspect repository drift; restart from the recorded recipe; and rerun Smoke.

When those checks pass, re-assume execution and reconciliation ownership, Judge, Reconcile, and return a superseding terminal packet. A changed Freeze fact or blocked packet requires a fresh Admit and Freeze.

## Completion

Complete when admission is resolved and every started operation either meets its criterion or returns `blocked` at the exact failed boundary. A run that reaches judgment has five frozen locks, exactly one loaded branch contract, green branch Smoke, and an authorized verdict or truthful awaiting/blocked residual. Every path has complete artifact accounting with no live resource, one internally consistent packet, and return to the invoker or user without downstream execution.
