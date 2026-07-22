# Agentic Bridge Vocabulary

Professional software engineering vocabulary is necessary, but not sufficient.

Book-backed engineering terms give the agent the taste target:

- `tracer bullet`
- `red-green-refactor`
- `ubiquitous language`
- `domain model`
- `deep module`
- `seam`
- `evidence`
- `residual risk`

Agentic vocabulary gives the execution control surface:

- when to read;
- when to stop;
- how much evidence to gather;
- what counts as done;
- when to ask;
- how to avoid premature completion;
- how to preserve context;
- how to recover from uncertainty.

The skill pack should bridge both.

```text
professional engineering term
  + agent execution instruction
  + completion criterion
```

For example:

```text
Use a tracer-bullet vertical slice.
It must cross the real system boundary, prove one observable behavior,
and end with evidence from a test, command, fixture, or rendered artifact.
```

`tracer bullet` pulls the agent toward the right professional prior. The next
sentence makes it operational for an LLM.

Without the LLM-facing layer, the agent may recognize the word but still behave
averagely. With the execution layer, the word becomes a behavioral constraint.

## Agentic Language That Matters

These terms matter because they shape how the agent executes professional
engineering taste.

- `agent-computer interface` - the tool, shell, editor, test, and repo surface
  the model acts through.
- `workflow` - a predictable sequence where code paths and tools are mostly
  predefined.
- `agent` - a system where the model dynamically chooses actions and control
  flow to pursue a goal.
- `augmented LLM` - an LLM equipped with retrieval, tools, memory, or other
  external capabilities.
- `tool use` - deliberate use of shell, tests, search, browser, editor, or APIs
  to observe or change reality.
- `guardrail` - a constraint that prevents unsafe, out-of-scope, or invalid
  behavior.
- `context engineering` - selecting, ordering, compressing, and refreshing the
  information the model needs to act well.
- `context budget` - the limited attention and token budget available for
  instructions, repo state, evidence, and task details.
- `retrieval` - bringing source material into context when latent memory is not
  enough.
- `trajectory` - the sequence of observations, actions, tool results, edits,
  checks, and revisions an agent takes.
- `reason-act loop` - alternating reasoning, action, and observation instead of
  guessing from static context.
- `feedback signal` - the observable result that tells the agent whether a step
  improved or failed.
- `evaluation harness` - a repeatable system for measuring behavior against
  criteria.
- `LLM-as-judge` - using a model to evaluate output only when criteria and
  evidence constrain the judgment.
- `observability` - logs, traces, command outputs, screenshots, metrics, and
  diffs that make agent behavior inspectable.
- `structured output` - constrained output that downstream tools or humans can
  parse reliably.
- `completion criterion` - prevents premature "done."
- `evidence` - forces verification instead of confident prose.
- `read before editing` - prevents shallow guessing.
- `fixed point` - stabilizes review.
- `bounded slice` - limits scope creep.
- `load-bearing internal` - tells the agent when internals are not "just
  implementation."
- `semantic correctness` - prevents output-exists fallacies.
- `context pointer` - controls when supporting material is loaded.
- `progressive disclosure` - keeps skills readable without hiding required
  rules.
- `single source of truth` - prevents drift and duplicated instructions.
- `no-op` - prunes words that do not change model behavior.
- `leading word` - chooses terms that activate useful priors.
- `legwork` - makes the model dig instead of asking the user too soon.
- `premature completion` - names a real LLM failure mode.
- `post-completion steps` - explains why agents rush.

## Terms To Use Sparingly

Some terms are useful in research but weak as skill-pack steering words unless
paired with a concrete completion criterion.

- `chain of thought`: can invite verbosity; prefer observable reasoning
  artifacts, plans, decisions, and evidence.
- `self-refine`: useful only when the critique changes the next revision.
- `reflection`: useful only when it records a lesson or redirects the next
  attempt.
- `agent`: too broad by itself; specify the tool surface, control flow, and
  completion criteria.
- `memory`: dangerous if it means stale facts; use source-backed memory and
  verify drift-prone claims.
- `LLM-as-judge`: helpful for triage and review only when criteria-bound and
  evidence-grounded.

## Bridge Patterns

Use these pairings when writing or editing skills.

- `tracer bullet` + `completion criterion`
- `red-green-refactor` + "watch it fail before implementation"
- `ubiquitous language` + "use CONTEXT.md terms in issue titles, tests, and commits"
- `deep module` + "test through the public interface"
- `seam` + "prove through the smallest meaningful boundary"
- `feedback loop` + "one command that can go red and green"
- `evidence` + "source, tests, fixtures, logs, diffs, commands, CI, screenshots"
- `fixed-point review` + "compare HEAD against the starting ref"

## Current Ownership

This file preserves candidate agentic terms, weak terms, and bridge patterns.
It defines no universal sequence or skill-writing formula. Current synthesis
and canonical skill owners decide whether any term or pattern applies.
