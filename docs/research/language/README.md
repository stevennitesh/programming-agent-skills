# Language Research

Language docs are exploratory research for the skill pack.

They preserve candidate professional and agentic terms that may later inform
synthesis. They are not the committed source of truth for operational
instructions.

Use this folder to answer:

- What words are already present?
- Which words recruit upper-bound engineering priors?
- Which words bridge those priors into agent behavior?
- Which words should be avoided because they are vague, decorative, or stale?
- Which words deserve promotion into synthesis, `CONTEXT.md`, `docs/agents/`,
  or runtime skills?

## Files

| File | Role |
| --- | --- |
| [`03-high-signal-steering-words.md`](03-high-signal-steering-words.md) | Candidate professional software-engineering terms that may steer high-quality behavior. |
| [`04-agentic-bridge-vocabulary.md`](04-agentic-bridge-vocabulary.md) | Candidate bridges from engineering concepts into agent execution and completion criteria. |

## Current Owners

`CONTEXT.md` owns active pack vocabulary. The engineering contract owns shared
runtime engineering language, and each canonical skill owns its behavior.
Future outside-source refreshes use the source-distillation method rather than
reusing earlier language synthesis as current guidance. Use the generic
[skill-pack vocabulary profile](../../synthesis/methods/prompts/extract-skill-pack-vocabulary.md)
when extracting language from an upstream or local skill pack.

## Rule

Research vocabulary should act as an attention handle. Promote words that
change behavior; cut words that only decorate the prose.
