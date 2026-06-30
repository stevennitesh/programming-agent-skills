---
name: prototype
description: "Build a throwaway prototype to answer a design question: a runnable terminal app for state/business-logic questions, or radically different UI variations toggleable from one route. Use when conversation cannot settle a design without trying it."
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

This is a detour, not implementation. The only durable output is the answer.

## Pick A Branch

Identify the question being answered from the user's prompt, surrounding code, or by asking if the user is around.

- **"Does this logic, state model, or data shape feel right?"** -> Read [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that lets the user press buttons and watch state change.
- **"What should this look like?"** -> Read [UI.md](UI.md). Build several radically different UI variations on one route, switchable by URL param and a floating bottom bar.

The branches produce different artifacts. If the question is ambiguous and the user is not reachable, choose the branch that best matches the surrounding code: backend module means logic; page or component means UI. State the assumption at the top of the prototype.

## Rules

- **Keep the contract boundary.** If prototype output is promoted into repo behavior or used as semantic proof, switch to the repo's real coding workflow and read `docs/agents/engineering-contract.md` first.
- **State the question first.** Write the question in the prototype location so the artifact can be judged later.
- **Build the smallest answering artifact.** Do not expand to adjacent questions unless the prototype disproves the original one.
- **Keep it throwaway.** Prefer `.tmp/` for prototype shells, scratch artifacts, copied references, and rough notes. When possible, call real module seams, methods, adapters, or page-level surfaces from `.tmp/` instead of placing throwaway code in the production tree.
- **Use production placement only when the question needs it.** Put prototype code near a module or page only when that is required to answer the question against real app constraints. Mark it clearly as prototype code and keep the diff easy to delete.
- **Use one command.** Add or report the repo-native command that runs it.
- **Run it once.** Run the prototype with its one command and complete the branch-specific smoke check.
- **Skip production polish.** No tests, broad error handling, generic abstractions, or unrelated cleanup. Make it runnable enough to learn.
- **Avoid persistence by default.** Keep state in memory unless persistence is the question. If storage is needed, use scratch storage clearly marked as prototype-only.
- **Surface the state.** Logic prototypes print the relevant state after each action. UI prototypes make the active variant obvious and reload-stable.
- **Do not quietly ship prototype code.** After the answer is known, delete prototype artifacts by default unless the user asks to preserve them. Move code near the module only when the validated shape is ready for a real implementation pass.

## Capture The Answer

When the prototype has answered its question, capture:

- the original question
- what the prototype proved or disproved
- whether the answer is a shape/feel verdict or semantic proof
- if semantic proof is claimed, what fixtures, examples, invariants, or edge cases support it
- the chosen direction, if any
- what should happen next
- whether the prototype should be deleted, used as input, or revisited

Use the smallest durable place that fits: issue comment, PRD note, ADR, commit message, `NOTES.md`, or `$handoff`.

If the prototype was a detour from a larger `$grilling`, `$to-prd`, or design thread, use `$handoff` to carry the answer back into that thread.

If the answer resolves domain language, update it with `$domain-modeling`. If it creates an ADR-worthy decision, offer or record the ADR there.

## Completion Criteria

Done means the question is written down, the correct branch doc was followed, the prototype runs in one command, the branch-specific smoke check passed, the answer or pending verdict is captured durably, and the cleanup or next-step path is clear.
