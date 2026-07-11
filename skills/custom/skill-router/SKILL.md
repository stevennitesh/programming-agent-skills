---
name: skill-router
description: Route the current situation to exactly one next skill or flow in this engineering pack.
---

# Skill Router

Use this **router** when route choice is the work.

## Router Contract

The router owns the recommendation. Downstream skills own their Source Trace, procedure, artifacts, mutations, and completion.

Route from the user's stated situation and visible repo state. Inspect only the fact that would change the route.

- **Clear:** Recommend exactly one skill or flow and explain why it fits.
- **Unclear:** Ask one highest-leverage question, then route.
- **Return:** Give one route, one reason, and one setup or handoff precondition when needed.

Return the route and stop. The user starts it.

## Setup Gate

Route first to `$repo-bootstrap` when the chosen engineering flow depends on a missing or outdated setup contract:

- current setup-schema marker and installed-pack primer in `AGENTS.md`;
- `docs/agents/issue-tracker.md`;
- `docs/agents/triage-labels.md`;
- `docs/agents/domain.md`;
- `docs/agents/engineering-contract.md`.

Let `$repo-bootstrap` own inventory, choices, writes, tracker mutations, and verification.

## Route Map

### Shape

| Situation | Route |
| --- | --- |
| Product or design intent needs a repo-backed interview and durable domain capture | `$grill-with-docs` |
| A plan or design needs a conversation-only interview | `$grilling` |
| A large, foggy effort needs a tracker-backed decision map | `$wayfinder` |
| One source question needs a cited repo-local note | `$research` |
| One design question needs runnable evidence | `$prototype` |
| Context must cross into a fresh session or agent thread | `$handoff` |

### Build

| Situation | Route |
| --- | --- |
| A multi-session idea lacks a durable parent spec | `$to-spec` then `$to-tickets` |
| Settled source needs dependency-ordered ready-for-agent tickets | `$to-tickets` |
| One bounded ready-for-agent item is selected | `$implement` |
| A ready frontier has non-overlapping write scopes and proof lanes | `$parallel-implement` |

`$to-tickets` output is already ready-for-agent. Route its ready frontier directly to `$implement` or `$parallel-implement`.

### Incoming Work And Quality

| Situation | Route |
| --- | --- |
| Raw issues, requests, or external PRs need sorting | `$triage` |
| A symptom, cause, or reproduction is uncertain | `$diagnosing-bugs` |
| Expected behavior and a red-capable proof seam are known | `$tdd` |
| A merge, rebase, cherry-pick, or revert is conflicted | `$resolving-merge-conflicts` |
| An ordinary branch, WIP, staged, or since-X diff needs fixed-point review | `$review` |
| A local PR or high-risk local diff needs independent passes and a finding ledger | `$convergent-pr-review` |

### Design And Pack Maintenance

| Situation | Route |
| --- | --- |
| Find codebase-wide architecture deepening candidates | `$improve-codebase-architecture` |
| Design one bounded module, interface, seam, or adapter | `$codebase-design` |
| Resolve domain terms, context boundaries, or ADR-worthy decisions | `$domain-modeling` |
| Create, edit, or review Codex skills | `$writing-great-skills` |

`$domain-modeling` and `$codebase-design` are **shared disciplines**. Route to them when language or interface shape is the work; otherwise let the owning workflow load them.

## Tie-Breakers

- **Grill / Wayfind:** Use `$grill-with-docs` for a decision tree that fits one session; use `$wayfinder` when fog of war requires a multi-session tracker map.
- **Research / Prototype:** Use `$research` for a source fact; use `$prototype` for a runnable design verdict.
- **Diagnose / TDD:** Use `$diagnosing-bugs` when the symptom, cause, or repro is uncertain; use `$tdd` when behavior and a red-capable seam are known.
- **Review / Convergent:** Use `$review` for ordinary fixed-point review; use `$convergent-pr-review` for local PRs or high-risk local diffs.
- **Implement / Parallel:** Use `$implement` for one ready item; use `$parallel-implement` for a parallel-safe ready frontier.
- **Triage / Architecture:** Use `$triage` for incoming tracker work; use `$improve-codebase-architecture` for codebase health.
- **Handoff / compact:** `$handoff` carries context to a fresh session or agent thread; `/compact` continues the current conversation.

## Completion Criteria

Complete only when the user has exactly one recommended next skill or flow, the reason it wins, and any setup or handoff precondition. When a routing question was required, completion waits for the answer and final route. Downstream work remains unstarted.
