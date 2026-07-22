---
name: prototype
description: Prototype one bounded design question with a disposable runnable probe; exclude production proof, uncertain defects, and multi-decision design.
---

# Prototype

**Outcome:** one design question answered by a judgeable disposable probe. The verdict is durable; the probe is not.

**Boundary.** Prototype owns one question from admission through terminal packet. The caller owns adoption, later routing, durable truth, production implementation, and production proof.

**Authority.** Default to one invocation-owned `.tmp/prototype/<question-slug>/` root; use a unique sibling when ownership is uncertain. Use `.scratch/<feature>/prototype/` only for authorized durable evidence. Touch exact application-tree paths only when real context requires it and the caller authorizes paths and disposition behind a repository-proved development-only or build-excluded boundary.

Inventory dirty work and every file or non-file side effect before mutation. Confine disposable assertions, fixtures, and launch configuration to authorized prototype paths; preserve production behavior, tests, dependencies, configuration, external data, trackers, specs, domain records, ADRs, Git state, and releases.

```text
Admit -> Freeze -> Load -> Probe -> Smoke -> Judge -> Reconcile -> Return
```

## 1. Admit

Admit without mutation only when all are true:

1. exactly one material design decision lacks runnable evidence;
2. one falsifiable or discriminating question expresses the uncertainty;
3. runnable evidence can compare directions, explore one bounded variation frame, or test one explicit threshold; and
4. a disposable probe can be built and reconciled inside the authorized repository and side-effect boundary.

Failed fit returns `not-admitted` with the original `request_subject`, failed fit, and actual need shape. Missing Freeze authority or evidence is instead a readiness failure; return `blocked` when it cannot be resolved safely.

## 2. Freeze

Before mutation, read back five locks; every applicable fact is required.

1. **Ownership:** invoker, `return_owner`, named `decision_owner`, named human judge when human, and proposed custodian for `preserve-for-verdict`. The decision owner and human judge are independent roles; never infer either from the other. Missing ownership blocks Freeze.
2. **Question and evidence:** one question and informed decision; alternatives, threshold, or variation frame; one branch; `claim level: shape/feel | design evidence`; `judgment mode: human | rule-based`; a predeclared rule when rule-based; and representative cases, variants, workload, or interactions.
3. **Mutation:** disposable root; exact application or durable-evidence paths; permitted and prohibited effects; and artifact dispositions.
4. **Execution:** one entry point or smallest ordered recipe and a finite iteration, variant, case, time, or effort bound.
5. **Limits:** known evidence limits and unsupported extrapolations.

Supply proportional representatives, variation, and bounds when immaterial choices are omitted. Ask when choices materially change cost, effects, coverage, or authority. Caller bounds and material thresholds win; never invent a business threshold or tune a rule after decisive evidence.

A change to the question, decision, claim level, judgment mode, representative set, verdict rule, or mutation boundary requires a fresh Admit and Freeze.

## 3. Load

Freeze selects the decision-bearing branch. Load exactly one branch reference:

| Evidence need | Load |
| --- | --- |
| State, rules, data, API shape, or interface behavior | [LOGIC.md](LOGIC.md) |
| Visual hierarchy, density, navigation, flow, or interaction structure | [UI.md](UI.md) |
| Comparative latency, throughput, resources, variability, or scaling shape | [MEASURE.md](MEASURE.md) |

Authorized tools do not add branch contracts. If two branches must independently establish the answer, return fresh questions to the caller.

## 4. Probe

Build the smallest artifact that exercises the frozen representatives and can change the verdict. Prefer repository-native tools, in-memory state, and only enough structure and error handling for judgeable evidence; persist only when persistence is the question.

## 5. Smoke

Run the frozen entry point or recipe and pass branch Smoke. Record the command, path or URL, reachable representative surface, material process state, and judgment-affecting assumptions.

Smoke proves only that the probe runs and is judgeable. It does not answer the question or prove production behavior.

## 6. Judge

Collect discriminating evidence over the frozen representative set.

| Claim level | Judgment mode | Rule |
| --- | --- | --- |
| `shape/feel` | `human` | Capture the named human's explicit verdict. |
| `shape/feel` | `rule-based` | Invalid; restate the claim as `design evidence`. |
| `design evidence` | `rule-based` | Apply the predeclared reproducible rule. |
| `design evidence` | `human` | Capture the named human's verdict when judgment is reserved. |

Never replace an unavailable human with a proxy rule: after green Smoke, prepare `awaiting-verdict`. Prepare `blocked` when the frozen rule and representatives cannot discriminate inside the bound. Record evidence, invariants, cases, feedback, limits, unsupported claims, and one `verdict` when answered. It may be an alternative, `none`, a threshold result, or another answer defined by the frozen rule.

Verdict evidence answers only the frozen design question. Production correctness remains with the real coding workflow and its caller-facing proof seam.

## 7. Reconcile

Account for every changed file, directory, process, port, cache, database, datum, route, overlay, and credential. Give each artifact one disposition:

- `delete`: remove created disposable content and verify absence;
- `restore`: remove only Prototype changes and preserve other work;
- `preserve-for-verdict`: keep the restartable minimum only after the named `return_owner` accepts custody and cleanup;
- `authorized-durable-evidence`: retain only at the authorized path and verify by read-back.

Stop processes, release resources, remove ephemeral credentials and stale pointers, and verify repository status and authorized paths. Answered work deletes or restores the probe unless durable evidence was authorized. No terminal return leaves a live resource. Ambiguous cleanup preserves the conflict and returns `blocked` without overwriting, resetting, or forcing cleanup.

## 8. Return

Before writing the packet, read back the current invocation identity. Populate `invoker`, `return_owner`, and `request_subject` only from the current invocation; never carry them from a preceding request or supplied packet.

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

- **`not-admitted`:** failed fit, actual need shape, and no-mutation confirmation; no fabricated question or informed decision.
- **`blocked`:** question and decision; Freeze fields reached; failed operation and exhausted or unsafe boundary; evidence; reconciliation; and smallest resumption requirement. Its artifact can inform a fresh invocation but cannot enter Resume.
- **`awaiting-verdict`:** question and decision; complete Freeze; human judge; restart recipe and expected URL; Smoke; preserved minimum; accepting custodian and cleanup duty; judging action; and explicit unresolved/no-live-resource state.
- **`answered`:** question and decision; complete Freeze; Smoke; verdict evidence or feedback; one `verdict`; supported and unsupported claims; limits and production-proof non-claim; reconciliation and repository read-back; and any domain or ADR candidate.

Each delta is its completion predicate; only `answered` resolves the question. Do not add universal `last_operation` or `next_required_action` fields, a second result field, or meaningless `inapplicable` values.

Caller-invoked work always returns to its caller. Direct work returns every terminal status, including `not-admitted`, to the user. Return and stop without selecting or invoking a downstream route.

## Resume

For any Resume request, load [RESUME.md](RESUME.md). It owns Resume admission and restart checks, then returns an admitted invocation to Judge; this file retains Reconcile and Return.

## Completion

Complete when admission is resolved and every started operation either meets its criterion or returns `blocked` at the exact failed boundary. Judgment requires five locks, one branch contract, green Smoke, and an authorized verdict or truthful residual. Every path accounts for artifacts, leaves no live resource, and returns one consistent packet to the invoker or user without downstream execution.
