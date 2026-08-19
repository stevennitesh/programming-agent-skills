---
name: skill-router
description: Route the current situation to exactly one next skill in this engineering pack, or abstain when no available skill satisfies the exact contract.
---

# Skill Router

**Route:** return exactly one next skill or a truthful `none`, then stop.
Downstream skills own their procedures, artifacts, mutations, proof, and
completion.

## Spine

1. **Inspect.** Use the user's stated situation and visible repo state. Inspect
   only a fact that could change the route.
2. **Clarify.** If two routes remain plausible, ask one highest-leverage
   question and wait.
3. **Route.** Choose one exact route below. If it needs a missing, incompatible,
   or outdated setup surface, route to `$repo-bootstrap` instead. If no
   available skill satisfies its entry contract, select `none`; never
   substitute the nearest or weakest route.
4. **Stop.** Return `Skill: <skill-name | none>`,
   `Reason: <winning contract | exact unmet routing predicates>`, and
   `Precondition: <setup, fact, authority, or handoff need | none>`. The user
   starts any selected skill; downstream work remains unstarted.

`none` is a terminal abstention, not a recommendation. Use it only when current
facts make every available route ineligible, not instead of one allowed
clarification or a required `$repo-bootstrap` route.

## Route Map

### Shape

| Situation | Route |
| --- | --- |
| One repo-backed decision needs direct grilling and durable domain capture | `$grill-with-docs` |
| The current user owns one bounded decision needing conversation-only stress-testing | `$grilling` |
| A bounded destination has interdependent decisions, a non-conversational resolver, and needs multi-session tracker sequencing | `$wayfinder` |
| One external stakeholder holds missing knowledge and needs an async discovery questionnaire | `$to-questionnaire` |
| One bounded source-answerable question needs cited evidence | `$research` |
| One design question needs disposable runnable evidence | `$prototype` |
| A fresh context that can read the same work root needs a verified local pickup | `$handoff` |

**Unknown-owner tie-breaker:** route a source-answerable fact to `$research`, a
runnable design choice to `$prototype`, an external-stakeholder gap to
`$to-questionnaire`, and a current-user decision to `$grilling` or
`$grill-with-docs` when durable domain capture may change. Route to `$wayfinder`
only after the destination is bounded and several interdependent decisions or
prerequisites, including at least one non-conversational resolver, need a
tracker-backed multi-session route.

### Build

| Situation | Route |
| --- | --- |
| Settled source needs a durable parent decision contract before ticket slicing | `$to-spec` |
| A `ready-spec` or equivalent settled bounded source needs a dependency-ordered implementation ticket graph and actionable frontier | `$to-tickets` |
| One bounded settled implementation is selected directly or as a Ready-for-agent item | `$implement` |
| One explicitly requested parent has an exhaustive non-empty Ready-for-agent graph | `$parallel-implement` |

Route one selected item to `$implement`; route an explicitly requested parent
delivery through its complete ready graph to `$parallel-implement`. Parallel
Implement decides whether each frontier runs serially or concurrently.

### Incoming Work And Quality

| Situation | Route |
| --- | --- |
| Raw tracker issues or configured external PR/MR requests need sorting and readiness verification | `$triage` |
| Expected behavior, symptom, cause, reproduction, environment, or performance mechanism is uncertain | `$diagnosing-bugs` |
| The user explicitly requests TDD, test-first work, or RED-GREEN-REFACTOR, or applicable repository policy requires TDD, and one bounded behavior and independent oracle are settled | `$tdd` |
| An active merge, rebase, cherry-pick, or revert is conflicted, an index is unmerged, or plausible markers need inspection | `$resolving-merge-conflicts` |
| A branch, WIP, staged, since-X diff, PR, release candidate, or supported-risk candidate needs read-only judgment | `$change-review` |
| A repository needs a whole-system map, one selected subsystem audit, one selected audit-candidate analysis, or one selected analyzed-candidate closeout | `$audit-codebase` |
| Existing behavior in one bounded region should be simplified under proof | `$simplify-code` |

**Existing-code tie-breaker:** route repository-wide discovery or baseline
judgment to `$audit-codebase`; one bounded behavior-preserving reduction to
`$simplify-code`; and one module, interface, or seam decision to
`$codebase-design`. Route a selected ready item to `$implement`, which invokes
TDD only under an explicit user or repository-policy requirement. Route one
standalone explicitly test-first behavior to `$tdd`, ordinary test,
integration-test, regression-test, or coverage work to `$implement`, uncertain
broken behavior to `$diagnosing-bugs`, and an existing diff needing judgment to
`$change-review`.
High Assurance Review is an explicit user-selected alternative, never an
automatic route.

**Conflict tie-breaker:** route an active unresolved operation or unmerged index
to `$resolving-merge-conflicts`; an already-resolved candidate to review; and a
post-operation behavioral failure to `$diagnosing-bugs`.

### Design And Pack Maintenance

| Situation | Route |
| --- | --- |
| Design one bounded module, interface, seam, or adapter | `$codebase-design` |
| Resolve domain terms, context boundaries, or ADR-worthy decisions | `$domain-modeling` |
| Create, edit, audit, or behaviorally test canonical Codex skill semantics | `$writing-great-skills` |

`$domain-modeling` and `$codebase-design` are shared disciplines. Route to them
when language or interface shape is the work; otherwise let the owning workflow
load them.

**Handoff / compact:** `$handoff` starts a fresh same-root context; `/compact`
continues the current conversation.
