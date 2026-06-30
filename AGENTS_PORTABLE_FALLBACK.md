# Portable Fallback AGENTS.md For Programming Work

Copy this into a repo-level `AGENTS.md` when the skill pack is unavailable for
that repo. Use it as global guidance only in a Codex profile or environment
where the skill pack is not installed.

Keep repo-specific commands, release rules, architecture notes, tracker policy,
and source-of-truth docs in each target repo. This file is a portable fallback:
it should steer taste and gates, not replace repo docs, source code, tests,
review, CI, or direct user instruction.

Do not keep this fallback active after `setup-matt-pocock-skills` installs
repo-local `docs/agents/*`. Setup should replace this fallback contract with
the thin installed-pack `AGENTS.md` block and move coding discipline to
`docs/agents/engineering-contract.md`.

## North Star

Build faster without making the repo harder to trust.

Good agentic coding is fast discovery plus disciplined convergence. Give the
agent room to discover, then force it to converge.

Use strong leading words:

- **product intent**: the outcome the work exists to create.
- **shared language**: the repo's domain vocabulary, not throwaway wording.
- **decision map**: unresolved choices made visible instead of guessed.
- **tracer bullet**: one narrow behavior through the real system.
- **vertical slice**: work split by observable behavior, not technical layer.
- **ready-for-agent**: specific enough for a fresh session without hidden context.
- **acceptance criteria**: observable proof that the slice is done.
- **red-green-refactor**: test-first change when behavior is clear enough to prove.
- **seam/interface**: the surface where meaningful behavior is exercised.
- **deep module**: a lot of behavior behind a small interface.
- **fixed-point review**: compare the diff against a known starting point.
- **commitment boundary**: product intent, acceptance criteria, semantic
  correctness, user-visible behavior, public contracts, data semantics,
  security/privacy posture, and bounded slice belong to the user.
- **load-bearing internal**: internal behavior that determines whether the
  requested result is correct; it needs a contract and proof through a seam.
- **evidence**: source, tests, fixtures, logs, diffs, command output, CI, or
  explicit user confirmation.

## Working Loop

Use this rhythm, scaled to task size:

```text
Orient -> Explore -> Choose -> Prove -> Converge -> Lock
```

- **Orient**: name product intent, current behavior, constraints, acceptance
  criteria, fixed point, and what must be preserved.
- **Explore**: read the real repo surface before guessing. Use `.tmp/` for
  disposable spikes and notes when it reduces uncertainty.
- **Choose**: pick one local approach before production work grows.
- **Prove**: prove semantic correctness through the smallest meaningful seam.
- **Converge**: simplify, remove scaffolding, and review from the fixed point.
- **Lock**: rerun the right checks, record evidence, and report residual risk.

Compress the loop for tiny edits. Make every gate explicit for uncertain,
risky, multi-file, user-facing, data, security, or architecture-touching work.

## Hard Gates

- Current user instruction wins.
- Source code, tests, fixtures, logs, diffs, command output, and CI show repo
  reality. Generated summaries, memory, plans, and notes are maps, not proof.
- Do not widen the bounded slice while exploring. Record follow-ups instead.
- Ask before changing product intent, acceptance criteria, semantic correctness,
  user-visible behavior beyond the request, public contracts, dependencies,
  data semantics, security/privacy posture, or the bounded slice itself.
- Preserve unrelated user work. Do not revert changes you did not make unless
  explicitly asked.
- Inspect `git status --short --branch` and the relevant diff before risky
  edits, staging, commits, branch changes, generated output, cleanup, or
  dependency installs.
- No evidence, no done.

## Shape Before Build

If the work is foggy, reduce ambiguity before building. Ask only questions that
change product intent, acceptance criteria, public behavior, interface shape,
risk, reversibility, data integrity, cost, or validation.

If a question cannot be settled quickly, name it as a decision map. Do not hide
fog of war inside implementation.

If the work will outlive the current thread, capture durable intent: problem,
desired outcome, accepted decisions, rejected options, edge cases, validation
notes, open questions, and out-of-scope boundaries.

Preserve shared language from the repo's glossary, domain model, ADRs,
architecture notes, issue text, and code. If a new term or ADR-worthy decision
appears, call it out as durable knowledge.

## Implementation Taste

Prefer tracer-bullet vertical slices. A good slice proves one observable
behavior through the real system, has checkable acceptance criteria, is narrow
enough to review, names blockers, and leaves enough context for a fresh agent or
human to continue.

Use existing seams, repo patterns, and domain vocabulary before inventing new
structure. Add abstraction only when it improves correctness, locality,
testability, ownership, or future change.

Use red-green-refactor when behavior is clear enough to test. Test observable
behavior through the highest useful seam. Avoid tests that only assert
implementation shape.

Load-bearing internals need semantic proof: fixtures, known input/output
examples, invariants, row-level expectations, checksums, thresholds, or other
evidence that proves the result is correct, not merely present.

For bugs, reproduce or observe the symptom before fixing, prove the cause, fix
the cause, and keep a regression check.

For refactors, preserve behavior unless the user explicitly approves behavior
change. If behavior is hard to prove through the public interface, treat that as
design feedback.

## Review And Report

Review nontrivial diffs from a fixed point on two axes:

- **Standards**: repo conventions, maintainability, locality, naming, and
  operability.
- **Spec**: user request, issue, PRD, acceptance criteria, semantic correctness,
  and residual risk.

Use the smallest check that proves the slice: focused tests, typechecks, lint on
touched paths, smoke commands, fixture checks, rendered output, diff inspection,
or CI. Use broader checks at commit, PR, release, shared-infrastructure, or
high-risk boundaries.

Every changed line should trace to the request, the chosen slice, an acceptance
criterion, or necessary cleanup caused by the change.

If verification fails or cannot run, say so directly and name the next useful
action.

Report briefly:

- what changed;
- what evidence supports it;
- what remains uncertain;
- the next useful action.

Do not bury the result in process narration. The point is trusted work, not the
performance of process.
