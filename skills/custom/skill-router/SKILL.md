---
name: skill-router
description: Route the current situation to exactly one next skill in this engineering pack.
---

# Skill Router

**Route:** recommend exactly one next skill and stop. Downstream skills own their procedures, artifacts, mutations, proof, and completion.

## Spine

1. **Inspect.** Use the user's stated situation and visible repo state. Inspect only a fact that could change the route.
2. **Clarify.** If two routes remain plausible, ask one highest-leverage question and wait.
3. **Route.** Choose one route below. If the chosen engineering route depends on a missing or outdated setup surface, route to `$repo-bootstrap` instead.
4. **Stop.** Return `Skill: <skill-name>`, `Reason: <why it wins>`, and `Precondition: <setup or handoff need | none>`. The user starts it; downstream work remains unstarted.

## Route Map

### Shape

| Situation | Route |
| --- | --- |
| A repo-backed plan or design needs an interview and durable domain capture | `$grill-with-docs` |
| A plan or design needs a conversation-only interview | `$grilling` |
| A large, foggy effort needs a tracker-backed decision map | `$wayfinder` |
| One external stakeholder holds missing knowledge and needs an async discovery questionnaire | `$to-questionnaire` |
| One source question needs a cited repo-local note | `$research` |
| One design question needs runnable evidence | `$prototype` |
| Context must cross into a fresh session or agent thread | `$handoff` |

**Destination-before-scale tie-breaker:** when the destination or scope is
still user-owned and unclear, route one conversation to `$grilling`, or to
`$grill-with-docs` when the decision may change durable domain terms,
Invariants, Context Relationships, or an ADR. Route to `$wayfinder` only after
the destination is bounded and several interdependent decisions or
prerequisites need a tracker-backed, multi-session route.

### Build

| Situation | Route |
| --- | --- |
| Settled source needs a durable parent decision contract before ticket slicing | `$to-spec` |
| A `ready-spec` or equivalent settled bounded source needs a dependency-ordered Ready-for-agent ticket graph | `$to-tickets` |
| One bounded ready-for-agent item is selected | `$implement` |
| One parent spec or PRD has an associated ready ticket graph to finish | `$parallel-implement` |

`$to-tickets` output is already ready-for-agent. Route one selected item to `$implement`; route an explicitly requested parent-delivery run to `$parallel-implement`, which serializes or parallelizes each frontier until the parent graph closes.

### Incoming Work And Quality

| Situation | Route |
| --- | --- |
| Raw issues, requests, or configured external PR/MR intake need sorting | `$triage` |
| A bug's expected behavior, exact symptom, cause, or trusted red-capable reproduction is uncertain | `$diagnosing-bugs` |
| Settled new behavior has a red-capable proof seam, or for a bug expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known | `$tdd` |
| A merge, rebase, cherry-pick, or revert is conflicted, or files contain conflict markers | `$resolving-merge-conflicts` |
| An ordinary branch, WIP, staged, since-X diff, or ordinary PR needs fixed-point review | `$change-review` |
| A release candidate or supported high-risk diff or PR needs independent passes and a finding ledger | `$high-assurance-review` |
| A repository needs an exhaustive system map, serial subsystem audit, or user-selected improvement-candidate analysis for correctness, robustness, code quality, architecture, methodology, data, analytics, or performance | `$audit-codebase` |
| Existing behavior in one bounded region should be simplified under proof | `$simplify-code` |

**Existing-code tie-breaker:** route a whole-repository map, baseline audit, or wide uncertainty about correctness, robustness, stale code, complexity, or architecture to `$audit-codebase`; one bounded behavior-preserving reduction to `$simplify-code`; and one already-framed interface or seam to `$codebase-design`. A selected ready item belongs to `$implement`, new behavior to `$tdd`, and an existing diff needing judgment rather than edits to `$change-review` or `$high-assurance-review`.

**Triage / Review:** route incoming work to `$triage`; route an existing diff to `$change-review` or `$high-assurance-review`.

### Design And Pack Maintenance

| Situation | Route |
| --- | --- |
| Design one bounded module, interface, seam, or adapter | `$codebase-design` |
| Resolve domain terms, context boundaries, or ADR-worthy decisions | `$domain-modeling` |
| Create, edit, or review Codex skills | `$writing-great-skills` |

`$domain-modeling` and `$codebase-design` are shared disciplines. Route to them when language or interface shape is the work; otherwise let the owning workflow load them.

**Handoff / compact:** `$handoff` carries context to a fresh session or agent thread; `/compact` continues the current conversation.
