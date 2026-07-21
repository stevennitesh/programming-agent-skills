---
name: skill-router
description: Route only an explicit next-skill selection request or a terminal out-of-scope residual packet delegated by another skill. Return one next skill or none without executing it. Do not replace an active skill's in-scope work or owned handoffs.
---

# Skill Router

Own one decision: select one next skill or `none` for an explicit route-selection request or a terminal residual packet outside its caller's scope. Never interrupt an active owner's in-scope work, replace a known contractual handoff, or start downstream execution.

## Spine

1. **Admit.** Accept only an explicit route-selection request or a caller-delegated terminal residual. Return to the caller when work remains in its scope or an owned handoff applies.
2. **Inspect.** Use the packet and visible repository state. Inspect only facts that can change ownership.
3. **Exclude.** Remove the current owner, Skill Router, exhausted owners, and routes whose admission predicates fail.
4. **Prefer.** Choose the narrowest owner that can close the residual: one leaf before an orchestrator, an owned deterministic handoff before routing, and settled delivery before renewed discovery. When the chosen engineering route requires a missing or outdated setup surface, select `$repo-bootstrap` instead.
5. **Clarify.** Ask one highest-leverage question only when two routes remain materially plausible and the packet cannot decide.
6. **Return.** Recommend exactly one skill or `none`, name its precondition, and stop without executing it.

## Residual Packet

A caller supplies as much as it knows:

```text
Current owner:
Owner result: complete | blocked | rejected as out of scope
Original outcome:
Residual work:
Available evidence and source pointers:
Attempted or exhausted owners:
Rejected or excluded routes:
Known decisions and prerequisites:
Constraints and authority:
Caller return boundary:
```

A caller may not label expected, difficult, or merely unfinished in-scope work as residual.

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

### Build

| Situation | Route |
| --- | --- |
| Settled source needs a durable parent spec | `$to-spec` |
| Settled source needs dependency-ordered ready-for-agent tickets | `$to-tickets` |
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
| An ordinary branch, WIP, staged, or since-X diff needs fixed-point review | `$review` |
| A local PR or high-risk local diff needs independent passes and a finding ledger | `$convergent-pr-review` |
| An immutable repository baseline needs a bounded domain robustness, correctness, methodology, model-risk, leakage, validation, analytics, or performance audit without a release decision | `$audit-codebase` |
| Existing behavior in one bounded region should be simplified under proof | `$simplify-code` |

**Existing-code tie-breaker:** route a caller-bounded repository correctness, domain-robustness, or performance baseline to `$audit-codebase`, one bounded behavior-preserving reduction to `$simplify-code`, one already-framed interface or seam to `$codebase-design`, and broad uncertainty about what to eliminate, concentrate, retain, or investigate to `$improve-codebase`. A selected ready item belongs to `$implement`, new behavior to `$tdd`, and an existing diff needing judgment rather than edits to `$review` or `$convergent-pr-review`.

**Triage / Review:** route incoming work to `$triage`; route an existing diff to `$review` or `$convergent-pr-review`.

### Design And Pack Maintenance

| Situation | Route |
| --- | --- |
| Find and rank the strongest evidence-backed codebase improvements | `$improve-codebase` |
| Design one bounded module, interface, seam, or adapter | `$codebase-design` |
| Resolve domain terms, context boundaries, or ADR-worthy decisions | `$domain-modeling` |
| Create, edit, or review Codex skills | `$writing-great-skills` |

`$domain-modeling` and `$codebase-design` are shared disciplines. Route to them when language or interface shape is the work; otherwise let the owning workflow load them.

**Handoff / compact:** `$handoff` carries context to a fresh session or agent thread; `/compact` continues the current conversation.

## Wayfinder Pre-Screen

Select `$wayfinder` only when one bounded destination remains foggy, at least two interdependent material decisions remain, at least one needs non-conversational work, and the set needs durable tracker-backed sequencing. Question count, size, severity, session count, or generic fog alone does not qualify.

Prefer `$grill-with-docs` for question- or domain-only work; `$domain-modeling` for settled domain persistence; the direct leaf for one evidence gap; `$to-spec` for settled source needing a parent artifact; `$to-tickets` for several settled slices; `$implement` for one ready slice; and `none` when no skill owns the residual.

A Wayfinder rejection excludes Wayfinder until material evidence changes its Admission state.

## Loop Guards

- Never select Skill Router.
- Never immediately return unchanged residual work to the caller that rejected it.
- A leaf invoked by an orchestrator returns to that orchestrator; it does not route the next step.
- An open Wayfinder campaign keeps in-scope consequences inside its map.
- Grill With Docs invoked by Wayfinder returns residuals to that map.
- Repeated routing with an unchanged packet returns the same route or `none`.
- A recommendation never starts the selected skill.

## Return

```text
Skill: <skill-name> | none
Reason:
Precondition:
Return boundary:
Downstream execution: none
```

Complete when Admission holds, exclusions and the narrowest-owner preference leave one justified route or `none`, Return is complete, and downstream execution remains unstarted.
