---
name: simplify-code
description: Simplify one user-selected existing-code target without changing accepted behavior. Use only when explicitly selected; exclude new behavior, bug fixes, broad discovery, and unsettled interface or ownership decisions.
---

# Simplify Code

Remove concrete complexity from one named target without changing
accepted behavior. If no worthwhile safe reduction exists, leave the code
unchanged and say why.

Apply the repository instructions and engineering contract. The invocation
authorizes local source changes inside the target and the code they directly
displace. It does not authorize staging, commit, external mutation, or unrelated
cleanup.

## 1. Understand

Accept a target named by the user or selected in an Audit Codebase pickup. If
the target is missing, too broad, requires new behavior or bug repair, or
depends on an unsettled interface or ownership decision, return the mismatch
without changing code.

Read the target and its real callers. Name the accepted behavior and the
concrete complexity to remove. Reuse an Audit pickup's current evidence and
refresh only facts that may have changed.

## 2. Choose

Choose one coherent reduction. Prefer deletion, reuse of an existing owner or
native capability, collapsing an unearned layer, then simpler control flow or
state. Pick the clearest total design, not the fewest lines.

A reduction must remove maintenance work rather than move it into callers,
configuration, tests, or another wrapper.

Return unchanged only when the current owner and callers expose no credible cut
that preserves behavior, removes rather than moves complexity, and can be
proved with available evidence.

## 3. Simplify

Apply the reduction completely. Migrate affected callers and remove displaced
code, configuration, tests, or documentation.

## 4. Prove and return

Run the nearest useful check through the real caller or artifact. Use a
before-and-after comparison only when the behavior-preservation claim needs it.
Broaden proof only for shared impact, repository policy, or a concrete risk.

Inspect the reduction's diff. Confirm that accepted behavior remains and the
named complexity is gone rather than relocated.

For an explicitly requested repeated pass, run Choose, Simplify, and Prove
serially inside the same target. Continue only after the current reduction
passes both checks. Stop when no worthwhile cut remains, the user's stated
limit is reached, or proof or scope fails.

Before returning, inspect the complete invocation diff and confirm unrelated
work is untouched. If proof fails, remove only the current reduction's changes
when they can be isolated safely. If they cannot, preserve the exact state and
report it.

Return the reductions and proof, the concrete reason the code stayed unchanged,
or a failed check with the exact current state and recovery needed. A failed
check is not completion. Start no successor.

Complete when every applied reduction removes rather than moves complexity,
accepted behavior remains, and relevant proof passes, or when current evidence
supports no worthwhile safe reduction in the selected target.
