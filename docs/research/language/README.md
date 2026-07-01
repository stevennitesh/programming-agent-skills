# Language Research

Language docs are exploratory research for the skill pack.

They record the language we currently have, language borrowed or compared from
other skill packs, and candidate terms that may later become synthesis or
runtime wording. They are not the committed source of truth for operational
instructions.

Use this folder to answer:

- What words are already present?
- Which words recruit upper-bound engineering priors?
- Which words bridge those priors into agent behavior?
- Which words should be avoided because they are vague, decorative, or stale?
- Which words deserve promotion into synthesis, `CONTEXT.md`, `docs/agents/`,
  or runtime skills?

## Workflow

| Step | File | Role |
| --- | --- | --- |
| 1 | [`01-current-vocabulary-inventory.md`](01-current-vocabulary-inventory.md) | Inventory the language already present in this repo and comparison surfaces. |
| 2 | [`02-upstream-skill-pack-audit.md`](02-upstream-skill-pack-audit.md) | Compare the upstream/Matt-style skill pack vocabulary with this repo's active language. |
| 3 | [`03-high-signal-steering-words.md`](03-high-signal-steering-words.md) | Extract candidate professional software-engineering terms that may steer high-quality behavior. |
| 4 | [`04-agentic-bridge-vocabulary.md`](04-agentic-bridge-vocabulary.md) | Bridge engineering taste into LLM execution language and completion criteria. |

## Promoted Synthesis

These language findings have been promoted into synthesis:

- [`../../synthesis/target-spine.md`](../../synthesis/target-spine.md)
- [`../../synthesis/language-direction.md`](../../synthesis/language-direction.md)

## Rule

Research vocabulary should act as an attention handle. Promote words that
change behavior; cut words that only decorate the prose.
