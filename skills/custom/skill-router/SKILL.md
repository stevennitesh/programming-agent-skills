---
name: skill-router
description: Choose one next engineering skill when the user explicitly asks which skill to use or invokes $skill-router. Return that skill or none, then stop without starting it.
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
3. **Route.** Choose one exact route below. After a candidate wins, inspect only
   its applicable installed `docs/agents/*` contract when compatibility could
   change the route; never load Repo Bootstrap guidance. If that contract is
   missing, incompatible, or outdated, route to `$repo-bootstrap` instead. If no
   available skill satisfies its entry contract, select `none`; never
   substitute the nearest or weakest route.
4. **Stop.** Return `Skill: <skill-name | none>` and
   `Reason: <winning contract | exact unmet routing predicates>`. Add
   `Precondition: <setup, fact, authority, or handoff need>` only when the user
   must satisfy one before starting the route. The user starts any selected
   skill; downstream work remains unstarted.

`none` is a terminal abstention, not a recommendation. Use it only when current
facts make every available route ineligible, not instead of one allowed
clarification or a required `$repo-bootstrap` route.

## Route Map

### Shape

| Situation | Route |
| --- | --- |
| One current-user-owned repo-backed decision needs live grilling and domain reconciliation as answers settle | `$grill-with-docs` |
| The current user owns one bounded decision needing conversation-only stress-testing | `$grilling` |
| A bounded destination has interdependent decisions, a non-conversational resolver, and needs multi-session tracker sequencing | `$wayfinder` |
| One external stakeholder holds missing knowledge and needs an async discovery questionnaire | `$to-questionnaire` |
| One bounded source-answerable question needs cited evidence | `$research` |
| One design question needs disposable runnable evidence | `$prototype` |
| A fresh context that can read the same work root needs a verified local pickup | `$handoff` |

**Unknown-owner tie-breaker:** route a source-answerable fact to `$research`, a
runnable design choice to `$prototype`, an external-stakeholder gap to
`$to-questionnaire`, and a current-user decision to `$grilling` or
`$grill-with-docs` when domain meaning may change during the conversation.
Route to `$wayfinder` only after the destination is bounded and several
interdependent decisions or prerequisites, including at least one
non-conversational resolver, need a tracker-backed multi-session route.

### Build

| Situation | Route |
| --- | --- |
| Settled source needs a durable parent decision contract before ticket slicing | `$to-spec` |
| A verified parent specification or equivalent settled bounded source needs a dependency-ordered implementation ticket graph and actionable frontier | `$to-tickets` |
| One bounded settled implementation is selected directly or as a Ready-for-agent item | `$implement` |
| One explicitly requested bounded campaign must repeatedly improve one frozen measurable runtime, resource, cost, capacity, or product outcome against a settled target | `$hillclimb` |
| One explicitly requested bounded procedure has several settled steps only the current human can perform and needs a guided repository-native script | `$wizard` |
| One explicit fixed delivery set has at least two accepted implementation items and a non-empty ready frontier | `$parallel-implement` |

Route one selected item to `$implement`; route an explicitly requested fixed
set of at least two accepted items with a non-empty ready frontier to
`$parallel-implement`. Parallel Implement checks dependencies, ownership, and
write effects before concurrent dispatch.
Route one settled optimization to `$implement`, a sustained runtime, resource,
cost, capacity, or product target to `$hillclimb`, measured code-shape or
maintainability reduction to `$simplify-code`, and unexplained slowness or
regression to `$diagnosing-bugs`.

Route agent-executable setup or maintained automation to `$implement`, one
manual action to no skill, and several settled human-only stages that need an
interactive script to `$wizard`. An unresolved decision, source fact, or
stakeholder answer remains with its shaping or evidence owner.

### Incoming Work And Quality

| Situation | Route |
| --- | --- |
| Raw tracker issues or configured external PR/MR requests need sorting and readiness verification | `$triage` |
| A hard, intermittent, performance, environment-only, production-only, or causally ambiguous failure needs dedicated investigation | `$diagnosing-bugs` |
| The user explicitly requests TDD, test-first work, or RED-GREEN-REFACTOR, or applicable repository policy requires TDD, and one bounded behavior and independent oracle are settled | `$tdd` |
| An active merge, rebase, cherry-pick, or revert is conflicted, or an index is unmerged | `$resolving-merge-conflicts` |
| A branch, WIP, staged, since-X diff, PR, release candidate, or supported-risk candidate needs read-only judgment | `$change-review` |
| The user explicitly requests high-assurance, heavy, or final review of one fixed complete code candidate | `$high-assurance-review` |
| A repository needs a whole-system HTML map, one user-selected subsystem audit, or one user-selected audit-candidate analysis | `$audit-codebase` |
| One user-selected existing-code target has accepted behavior and needs behavior-preserving simplification | `$simplify-code` |

**Existing-code tie-breaker:** route repository-wide discovery or baseline
judgment to `$audit-codebase`; one user-selected target with accepted behavior to
`$simplify-code`; and one module, interface, or seam decision to
`$codebase-design`. Route a selected ready item to `$implement`, which invokes
TDD only under an explicit user or repository-policy requirement. Route one
standalone explicitly test-first behavior to `$tdd`, ordinary test,
integration-test, regression-test, or coverage work to `$implement`, uncertain
broken behavior that needs dedicated investigation to `$diagnosing-bugs`, and
an ordinary existing diff needing judgment to `$change-review`. Route to
`$high-assurance-review` only for an explicit heavy-review request; candidate
size, PR presence, release status, novelty, or risk does not qualify.

**Conflict tie-breaker:** route an active unresolved operation or unmerged index
to `$resolving-merge-conflicts`; an already-resolved candidate to review; a
routine post-operation repair to `$implement`; and a hard post-operation failure
that needs dedicated investigation to `$diagnosing-bugs`.

### Design And Pack Maintenance

| Situation | Route |
| --- | --- |
| Decide the architecture of one bounded module or interface | `$codebase-design` |
| Resolve or capture domain terms, invariants, context boundaries, or relationships; assess or record an already-settled ADR candidate | `$domain-modeling` |
| Create, edit, or audit instructions agents consume | `$writing-for-agents` |

`$domain-modeling` and `$codebase-design` are shared disciplines. Route
unresolved code shape, interfaces, or module ownership to Codebase Design;
route project-specific semantic truth or an already-settled ADR candidate to
Domain Modeling. Otherwise let the owning workflow proceed directly.

**Handoff / compact:** `$handoff` starts a fresh same-root context; `/compact`
continues the current conversation.
