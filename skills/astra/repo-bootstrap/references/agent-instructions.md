# Agent instruction files

## Repository instructions

Inspect the root instruction file and any nested instructions that govern the
affected work. Preserve narrower rules at their own scope. Use the files the
target agent reads; do not create parallel instruction files just to match a seed.

Keep local commands, non-obvious repository constraints, and conditional pointers
in the root file. Verify commands against their scripts or configuration. Point
to the engineering contract for shared judgment and to domain or tracker guidance
when those concerns apply. Keep procedure details at their existing owners.

During a compatibility update, reconcile the root and affected nested instructions
with the other agent docs in the same proposal. Update moved pointers, remove
stale instructions, and consolidate duplication without discarding local rules.
Include engineering guidance copied into these files: reconcile it with the
current contract and retain local exceptions at their appropriate scope. Use
the distinction between inherited defaults and deliberate policy in
[Existing repositories](setup-defaults.md#existing-repositories).
Check that the resulting reading path reaches the right guidance for each scope.

## Global instructions

Global instructions hold durable user preferences across repositories and
environment-specific pitfalls. Keep project commands, repository facts, and
coding procedures with their local owners. Reconcile only when global changes
are explicitly authorized; otherwise report a relevant conflict as a separate
recommendation. A local compatibility approval does not include global edits.

When global setup is requested, use [the Astra global seed](../templates/global-agents.md)
as a starting point, preserving the user's actual preferences. The seed's
delegation policy is a default to reconcile, not authority to replace another
established policy. Retain personal shell guidance only where it fits the host.

The seed links to [delegation guidance](delegation.md) within this package.
Before copying the seed to a global location, resolve that pointer to the actual
installed reference. If the package will not be installed, copy the reference
to a stable user-owned location and link there. Verify the link from the final
global file; source-relative links do not survive relocation automatically.

The managed installer updates its own small bootstrap section using the
repository's `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`; this skill's seed supports
broader, explicitly requested global reconciliation.
An update to the seed does not authorize updating other users' global files.
