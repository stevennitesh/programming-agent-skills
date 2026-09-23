# Plans And Runbooks

This file routes current work. Keep it short; put long procedures in the
owning runbook or method doc, and leave historical run logs where they were
created.

## Current Runbooks

| Work | Route |
| --- | --- |
| Astra skill design and migration | [Astra design brief](../astra/design-brief.md), based on [issue #94](https://github.com/stevennitesh/programming-agent-skills/issues/94) and subsequent decisions |
| Optional source distillation | [`docs/synthesis/methods/source-distillation-flow.md`](../synthesis/methods/source-distillation-flow.md) |
| Optional source-distillation prompts | [`docs/synthesis/methods/prompts/`](../synthesis/methods/prompts/) |

Source distillation is optional evidence work for primary and outside sources,
upstream skills, books, and engineering practice; it stops at important
concepts and usable techniques rather than drafting or deploying a skill.

## Legacy methods and historical plans

The [Deploy Campaign method](../synthesis/methods/deploy-prompts.md) is retained
for explicitly requested legacy custom-pack synthesis work. It is not a current
Astra runbook or prerequisite.

[Engineering vocabulary reconciliation](../../.archive/docs/plans/engineering-vocabulary-reconciliation.md)
is archived completed legacy work. Its old baseline and delivery deferrals are
historical, not pending Astra tasks. Current direction comes from the brief above.

## Rules

- Update this router when a plan becomes active or stops being active.
- Do not copy full plan text, prompt text, run logs, or historical issue notes
  into this file.
- If a procedure becomes long, keep it in a focused runbook and link it here.
- Treat facet artifacts as historical evidence unless their owning README or
  this router marks them current.
