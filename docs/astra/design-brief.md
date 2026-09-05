# Astra skill pack design brief

This is the current design direction for work in `skills/astra/`. It combines
the user's accepted principles in [issue #94: Rebuild the skill pack around lean engineering judgment](https://github.com/stevennitesh/programming-agent-skills/issues/94)
with subsequent decisions from the Astra work on 2026-09-05. The issue supplies
the original brief; this document owns the reconciled direction. It is not a
claim that the final pack or its behavioral evaluation is complete.

## Purpose and philosophy

Improve coding beyond a capable agent's baseline through useful engineering
judgment and necessary project context. Keep ordinary work direct: understand
the request and callers, choose a sound design, implement the outcome, run the
nearest useful check, inspect the result, and remove displaced code.

Explore imaginatively. Converge under proof. Simplify ruthlessly.

Use Matt Pocock's recognizable skill shape, useful engineering principles from
Pstack, and local controls that prevent concrete damage. Upstream packages are
evidence to select from, not bundles to combine or synchronization contracts.
Preserve protections for actual authority, destructive effects, concurrency,
recovery, and evidence risks at the owner that performs the relevant work.

## What earns a place

For a proposed instruction, identify the likely decision it improves or the
credible failure it prevents. Then ask whether this is the right owner, whether
existing code or tooling should enforce it, and whether the common path needs
to see it. Remove instructions with no concrete job.

Give each skill one recognizable outcome, a few natural actions, useful judgment,
and a clear completion condition. Three to six actions is a starting shape,
not a quota. Put substantial conditional detail behind a trigger and a pointer.
Trust ordinary file, code, test, and Git mechanics to the available tools.

Keep shared coding judgment in the engineering contract. Skills should not
repeat it or automatically require tickets, TDD, full suites, reviewers,
subagents, speculative fallbacks, or process artifacts. Use stronger methods
when the user, repository, or accepted task requires them. Word count alone
does not establish better behavior.

## Accepted choices

- Astra source lives in `skills/astra/`, separately from the managed custom pack.
- Astra has no `implement` skill. Implement directly using repository guidance
  and the engineering contract; use specialist skills only when their methods
  are needed. The limited implementation comparisons did not demonstrate a
  benefit from the skill. Preserve their research and test evidence.
- `writing-for-agents` and `repo-bootstrap` are implemented. Installation is a
  separate operation; source presence does not prove a host has installed them.
- Repository instructions supply local facts and conditional pointers. The
  engineering contract is repository-owned after adaptation from a seed.
- New repositories receive familiar tracker, label, and domain defaults. Those
  settings do not force direct coding into a ticket workflow.
- Existing setups receive one optional compatibility proposal covering affected
  docs and enforcement. Preserve local meaning while migrating execution routes
  to the latest Astra version; do not keep legacy compatibility routes.
- Global updates are a separate explicit scope. Keep personal preferences and
  environment guidance; reconcile local and global files by their different jobs.

Issue #94 proposed an `implement` pilot first. The user subsequently chose to
start with instruction authoring and bootstrap. That choice supersedes the
original ordering; it does not demonstrate the pilot's coding-quality claims.
The early research proposal of four default skills is not a settled inventory.

## Validation and migration

Check package structure, links, and affected repository contracts. Exercise a
changed mechanism with evidence that can expose its failure. Use representative
coding tasks when making claims about coding quality or reduced process cost;
structural checks and editorial reviews alone do not establish those effects.

Legacy composition freezes and Deploy Campaigns remain scoped to their selected
legacy work. They are not prerequisites for authoring an Astra skill. Historical
ADRs remain evidence of those decisions, not an implicit instruction to restore
the old composition. Retired source remains historical evidence, not a runtime
compatibility route for projects using this pack.

As Astra replacements are accepted, migrate their consumers, references,
validation and routing together. All projects using this pack target the latest
Astra contracts. Do not retain old execution paths for compatibility. Historical
source and a custom-only installer still exist in this repository; they are not
the current deployment target. Updating external projects or installed copies
remains a separately scoped operation, not an automatic effect of editing a seed.

## Still undecided

The final core and optional inventory, remaining skill boundaries, rewrite order,
and unified installation approach remain open. Choose them from concrete tasks
and evidence, not a target skill count. Limited implementation comparisons have
been run; broader comparative quality claims remain unestablished.

For the supporting source comparison and its limits, consult
[the initial assessment](../research/gpt-6-astra-skill-pack-assessment-2026-09-05.md)
when evaluating retained methods, and
[the contract assessment](../research/astra-engineering-contract-2026-09-05.md)
when revisiting engineering guidance. Their proposals are historical inputs;
the accepted choices above and current source determine this workstream.
