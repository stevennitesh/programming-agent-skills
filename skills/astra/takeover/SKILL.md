---
name: takeover
description: Take responsibility for unfinished work from another PR, branch, or agent conversation. Exclude routine continuation, preparing handoffs, and PR refresh alone.
---

# Takeover

Finish the inherited goal while preserving accepted decisions, useful work,
contributor credit, and authority. Use only when explicitly requested; inherited
implementation and handoff claims remain evidence to assess.

## Recover the goal and actual state

Read the source PR, branch, conversation, or handoff and later user corrections.
Recover the accepted outcome, unfinished obligations, known findings, authority,
and endpoint. Distinguish user decisions from suggestions or instructions quoted
by another agent. Resolve consequential gaps before dependent work while continuing
independent authorized work.

Reconcile the actual repository, worktree, base, current and published heads, and
dirty/untracked work with the reported state. Old checks or claimed completion do
not establish the current result. Identify writers, subprocesses, and resource
owners. Before taking write custody, confirm the earlier writer and its mutating
processes stopped and released it; idle, interrupted, or unavailable is not proof.
Follow the active execution workflow's custody and recovery rules.

A takeover request authorizes continuing the accepted goal within its stated
scope. It does not independently authorize publication, history rewriting,
merge, closure of the original PR, messaging another conversation, or discarding
unrelated work. Preserve existing user authority without asking for it again.

## Continue the useful work and preserve credit

Assess whether the inherited approach still satisfies current requirements and
architecture. For an old PR that needs refreshing, read
[Refresh an existing PR](../pr-delivery/references/refresh-existing-pr.md).
Use [codebase-design](../codebase-design/SKILL.md) when reuse, ownership, or
replacement remains unresolved. Retain useful behavior while correcting the
implementation within scope; sunk effort is not a reason to preserve it.

Honor the requested in-place, stacked, or replacement continuation. Reuse a
suitable existing branch or PR when no replacement is needed. Before replacing
or rewriting work, preserve recoverable source identities and account for local
changes. Recheck a source that can still receive contributions before integrating
or superseding it; a moved head requires assessing the new work.

Preserve original Git authors and existing co-author trailers. Keep continuation
fixes distinguishable from inherited commits when importing them. A replacement
PR should link its source and identify the original contributors and retained
work. If an authorized squash would lose human credit, carry verified author or
co-author identities into the merge commit using the forge's supported controls.
Do not guess email addresses or use model attribution as contributor credit.

## Verify and reach the requested endpoint

Reproduce the inherited failure or inspect the intended workflow independently,
using evidence suited to the affected behavior. Reuse prior evidence only while
its inputs and candidate remain applicable. Distinguish reported, locally
verified, published, and deployed results; state material gaps in real interface
or runtime verification.

Complete supported corrections and authorized work. Use
[change-review](../change-review/SKILL.md) when candidate assessment is needed and
[pr-delivery](../pr-delivery/SKILL.md) for a requested PR endpoint; their contracts
apply without a mandatory reviewer, model allocation, or delivery pipeline.
Branch/worktree cleanup retains its lifecycle owner and existing authorization.

Return what was inherited, the relevant source and resulting candidate, material
changes, verification, how contributor credit was preserved, the endpoint
reached, and any remaining blocker. If work must transfer again, preserve a usable
[continuation handoff](../writing-for-agents/references/continuation-handoffs.md)
without treating the packet as a custody transfer.
