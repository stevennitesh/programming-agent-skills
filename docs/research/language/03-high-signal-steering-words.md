# Engineering Steering Vocabulary

The point of this repo's vocabulary is not to create a private dialect. The
point is to use words with strong professional engineering priors, so an agent
reaches for the best practices, books, and review habits that produce
high-quality software.

Average agent behavior is not the target. The vocabulary should shape the LLM
toward upper-bound engineering behavior: sharper taste, stronger discipline,
more exact proof, better boundaries, and less tolerance for plausible-but-weak
work.

Good vocabulary should steer the agent toward:

- product clarity before implementation;
- domain language before generic phrasing;
- thin end-to-end slices before horizontal layer work;
- test-first proof when behavior is clear enough;
- deep interfaces and meaningful seams;
- tight feedback loops;
- semantic correctness, not output existence;
- evidenced review before done.

## Highest-Value Steering Words

Use these terms prominently. They are backed by common professional practice
and widely read software engineering books.

- `tracer bullet` - From The Pragmatic Programmer. Steers toward proving one
  real path through the system and reducing uncertainty with running software.
- `vertical slice` - Common agile and XP delivery language. Steers away from
  layer-by-layer work that cannot be validated end to end.
- `red-green-refactor` - From Kent Beck's TDD practice. Steers toward one
  failing test, the smallest passing change, then simplification while green.
- `acceptance criteria` - Common product and agile delivery language. Steers
  "done" toward observable behavior instead of intention.
- `ubiquitous language` and `domain model` - From Domain-Driven Design. Steer
  the agent to preserve the product's real concepts in code, tests, issues,
  PRDs, and summaries.
- `deep module`, `interface`, and `seam` - From A Philosophy of Software Design
  and testability practice. Steer toward small surfaces with meaningful
  behavior behind them, placed at boundaries that callers and tests can trust.
- `feedback loop` - Common in The Pragmatic Programmer, XP, Lean, debugging,
  and production engineering. Steers toward fast, repeatable evidence.
- `repro`, `hypothesis`, and `probe` - Debugging discipline. Steer toward
  reproducing the symptom, testing falsifiable explanations, and avoiding
  guesswork.
- `evidence` and `proof` - Engineering review culture. Steer away from claims
  and toward tests, fixtures, diffs, logs, screenshots, CI, or user
  confirmation.
- `post-mortem` and `residual risk` - Production and incident practice. Steer
  toward learning from failures and reporting what remains uncertain.

## Useful Repo Terms

These terms are less standard as book vocabulary, but they are valuable because
they compress important engineering judgment for agents.

- `semantic correctness` - Ask whether the result means the right thing, not
  whether some artifact exists.
- `commitment boundary` - Separate what the user committed to from what the
  agent may decide internally.
- `load-bearing internal` - Treat internal behavior as important when it
  determines whether the requested result is correct.
- `bounded slice` - Keep the work small enough to prove, review, and finish.
- `fixed-point review` - Review a diff against a known starting point, not a
  moving memory of what changed.
- `observable validation` - Require proof that can be seen in behavior,
  artifacts, commands, or checks.

These terms should stay, but they should usually support the book-backed words
rather than replace them.

## Operational Terms To De-Emphasize

These terms are useful for running the skill system, but they do not strongly
pull from classic engineering practice. Keep them where they are needed, but do
not make them the main language formula.

- `Codex-ready brief`
- `AFK agent`
- `agent primer`
- `skill pack`
- `context load`
- `model-invoked`
- `user-invoked`
- `no-babysitting implementation plan`
- `grilling session`
- `decision map`

When possible, pair operational terms with stronger engineering vocabulary:

- `Codex-ready brief` -> `independently-grabbable issue` plus `acceptance criteria`
- `grilling session` -> requirements discovery, `ubiquitous language`, and
  `ADR-worthy decision`
- `decision map` -> open decisions, trade-offs, and `ADR-worthy decision`
- `ready-for-agent` -> `bounded vertical slice` with `acceptance criteria`

## Current Ownership

This file preserves candidate vocabulary, not an accepted universal sequence.
`CONTEXT.md`, the engineering contract, and each canonical skill own current
language at their respective boundaries.

## Writing Rule

Prefer the professional steering word when it fits. Use repo-specific language
only when it names an agent workflow concept that the professional term does
not cover.

Choose words for the behavior they recruit. A strong word should make the agent
reach for a known high-quality practice, not merely describe the task. If a word
only produces average coding-agent behavior, replace it with a word that pulls
from stronger engineering taste.

For example, prefer:

- `tracer-bullet vertical slice` over `task`
- `acceptance criteria` over `requirements are clear`
- `red-green-refactor` over `write tests`
- `ubiquitous language` over `project jargon`
- `deep module` or `seam` over `abstraction`
- `evidence` over `looks good`

The best wording makes the agent slower in the right places: before scope
changes, before trusting output, before hiding correctness-critical internals,
and before calling the work done.
