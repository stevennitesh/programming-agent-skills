# Programming Agent Skills

A skill pack for programmers who want coding agents to move quickly without losing engineering discipline.

The pack is built around a simple belief: agentic coding gets much better when the agent has strong engineering language, clear repo-local contracts, and hard evidence gates. The agent should explore fast, choose deliberately, prove behavior, keep diffs reviewable, and leave the repo easier to trust.

It encodes this delivery spine:

```text
idea
  -> PRD
  -> tracer-bullet issues
  -> one ready-for-agent slice
  -> proof
  -> fixed-point review
```

In each target repo, setup gives the agent a local operating surface:

```text
AGENTS.md primes
  -> docs/agents/engineering-contract.md teaches the discipline
  -> skills execute the workflow
```

`setup-matt-pocock-skills` writes that surface: issue tracker rules, triage labels, domain-doc routing, and the engineering contract that gives the agent the pack's vocabulary and taste.

## Why This Exists

Coding agents are good at speed. They are less naturally good at judgment, boundaries, and proof.

This pack tries to make the good parts natural:

- turn fuzzy requests into bounded engineering work;
- preserve product intent across long or interrupted sessions;
- split work into tracer-bullet vertical slices instead of layer-by-layer churn;
- push agents toward red-green-refactor when behavior is clear enough to test;
- make semantic correctness harder to fake;
- keep domain language, ADRs, and repo conventions in the loop;
- review against both Standards and Spec before locking work;
- produce commits and notes a human maintainer can inspect with confidence.

The aim is not more ceremony. The aim is better default taste.

## Language Shapes Behavior

This pack treats language as part of the engineering system.

Agents do not only follow steps. They inherit taste from the words around those steps. The pack uses compact attention handles that point the model toward upper-bound engineering priors, then binds those priors to concrete action and proof.

This is not an attempt to put whole books into the context window. A good skill carries the useful force of a source, not its full explanation:

```text
source wisdom
  -> leading word
  -> rule
  -> agent action
  -> evidence gate
  -> forbidden shortcut or stop condition
```

A phrase like `red-green-refactor through the smallest meaningful seam` does more than say "write tests." It points the agent toward TDD, interface choice, behavior preservation, and proof. A phrase like `tracer-bullet vertical slice` points it away from broad layer work and toward one real path through the system.

The vocabulary is intentional. Terms like `product intent`, `shared language`, `tracer bullet`, `vertical slice`, `ready-for-agent`, `red-green-refactor`, `seam`, `deep module`, `acceptance criteria`, `semantic correctness`, `fixed-point review`, and `residual risk` are here because they steer the agent toward specific engineering habits.

The target shape is:

```text
software-engineering taste term
  -> agent execution surface
  -> evidence gate
```

Good skill language should make the agent slower in the right places and faster everywhere else: clarify before building, slice before expanding, test behavior instead of internals, preserve domain language, verify claims, and keep work reviewable.

## What This Makes Easier

| Work | What the pack adds |
| --- | --- |
| Shaping ambiguous ideas | `grill-with-docs`, `grilling`, `decision-mapping`, and `prototype` turn fog into decisions, open questions, or one answering artifact. |
| Capturing product intent | `to-prd` preserves the problem, desired outcome, user stories, accepted decisions, rejected options, edge cases, testing notes, and out-of-scope boundaries. |
| Splitting work | `to-issues` turns a PRD, spec, plan, or issue into dependency-ordered tracer-bullet issues with observable acceptance criteria. |
| Implementing safely | `implement` picks one ready-for-agent issue, captures a fixed point, proves behavior, reviews, commits, and leaves an implementation note. |
| Proving behavior | `tdd` drives red-green-refactor through the highest useful interface or seam when behavior is clear enough to test. |
| Diagnosing bugs | `diagnosing-bugs` builds a tight red-capable feedback loop before hypothesis, instrumentation, fix, and lock-down. |
| Reviewing changes | `review` checks a diff from a fixed point along two separate axes: documented Standards and originating Spec. |
| Improving design | `codebase-design` and `improve-codebase-architecture` give agents deep-module vocabulary: interface, seam, adapter, depth, leverage, and locality. |
| Preserving shared language | `domain-modeling` records glossary terms and ADR-worthy decisions so future agents do not drift. |

## The Convergence Loop

Give the agent room to discover, then force it to converge.

The pack's default coding rhythm is:

```text
Orient -> Explore -> Choose -> Prove -> Expand -> Converge -> Simplify -> Lock
```

Use the loop at the size of the task. Tiny, obvious edits can compress it into a quick source-read, edit, and check. Uncertain, risky, multi-file, user-facing, or architecture-touching work should make the gates explicit.

- **Orient**: name product intent, current behavior, constraints, acceptance criteria, fixed point, and what must be preserved.
- **Explore**: inspect seams, compare local approaches, and use disposable spikes when they reduce uncertainty.
- **Choose**: pick the best local approach inside the bounded slice. Technique belongs to the agent, but load-bearing internal behavior belongs to the result.
- **Prove**: use red-green-refactor when the code slice is suitable for TDD; otherwise use the strongest practical evidence available. Prove semantic correctness, not just that some output exists.
- **Expand**: add the remaining requirements as bounded tracer bullets or focused checks.
- **Converge**: review against Spec and Standards from the fixed point.
- **Simplify**: remove disposable scaffolding, collapse bloated branches, deepen modules where it helps, and preserve behavior.
- **Lock**: rerun the right checks, delete scratch artifacts unless asked to preserve them, record evidence, commit or hand off, and name follow-ups.

This loop is not a permission slip for wandering. Exploration is useful when it finds a better path to the requested result. If the better path changes product intent, acceptance criteria, semantic correctness, user-visible behavior beyond the request, public contracts, dependency or tooling choices, migration/data semantics, security/privacy posture, or the bounded slice itself, stop and ask.

## The Delivery Loop

The delivery loop is the project flow. The convergence loop is the coding rhythm inside an implementation slice.

When route choice is the work, use `ask-matt`, the human-facing router skill. It chooses one next route instead of asking the user to remember the whole pack.

### 1. Shape The Idea

Use `grill-with-docs`, `grilling`, `decision-mapping`, or `prototype` when the work is still foggy.

- `grill-with-docs` sharpens an idea against repo docs and existing code.
- `decision-mapping` turns fog of war into git-tracked decision tickets.
- `prototype` builds throwaway code to answer one design question.
- `handoff` preserves context when a fresh session should continue.

### 2. Capture Product Intent

Use `to-prd` to synthesize the conversation into a PRD.

The PRD preserves the problem, desired outcome, user stories, accepted decisions, rejected options, edge cases, testing notes, open questions, and out-of-scope boundaries. It is intentionally rich enough for a fresh agent session to recover the product shape without rereading the original conversation.

### 3. Split Into Tracer-Bullet Issues

Use `to-issues` to turn the PRD, spec, plan, or issue into dependency-ordered implementation issues.

The pack prefers tracer-bullet vertical slices over horizontal slices. A tracer bullet proves one observable behavior through the real system and reduces uncertainty about behavior, a seam, or a risk.

Support issues are allowed when they clearly unblock or de-risk later tracer bullets and have observable validation.

### 4. Implement One Ready Issue

Use `implement` to pick up one ready-for-agent issue, implement it through existing seams, verify it, review it, commit it, and leave an implementation note.

This is the convergence loop in action: orient around the issue, explore the repo shape, choose the best local approach, prove the slice, expand only to acceptance criteria, converge through review, simplify while behavior is protected, and lock the result with evidence.

### 5. Verify And Review

Use `tdd` when the behavior is clear enough to prove with a red test.

Use `review` to inspect a diff from a fixed point along two separate axes:

- Standards: does the diff follow documented repo conventions?
- Spec: does the diff implement the originating issue, PRD, or spec?

Use `convergent-pr-review` for higher-risk PRs that need independent review passes, a verified finding ledger, and patch-ready triage.

## Methods The Pack Encodes

| Method | Why it matters |
| --- | --- |
| Engineering contract | Gives each target repo a local operating contract for agentic coding. |
| Convergence loop | Gives the agent room to discover, then forces proof, review, simplification, and evidence. |
| Commitment boundary | Separates agent-owned technique from user-owned commitments. |
| Load-bearing internals | Prevents correctness-critical logic from hiding behind "implementation detail." |
| Semantic correctness | Proves the output is correct, not merely present. |
| PRD | Keeps product intent, decisions, edge cases, and boundaries durable. |
| User stories | Connects actors, capabilities, and benefits in product language. |
| Acceptance criteria | Turns "done" into observable proof. |
| Issue triage | Keeps incoming issues and external PRs moving through clear state roles. |
| Ready-for-agent | Marks work that an unattended coding session can safely pick up. |
| Vertical slices | Avoids layer-by-layer work that cannot be validated end to end. |
| Tracer bullets | Proves one real path through the system to reduce uncertainty. |
| TDD | Uses red-green-refactor when behavior is clear enough to test. |
| Seams and interfaces | Put tests and adapters at meaningful design boundaries. |
| Deep modules | Improve leverage for callers and locality for maintainers. |
| Domain modeling | Keeps product language, code language, and ADR-worthy decisions aligned. |
| Fixed-point review | Makes review stable by comparing the diff to a known base ref. |
| Git hygiene | Preserves unrelated work, scopes commits, and records evidence. |

## Skills

### Core Skills

| Skill | Use it when |
| --- | --- |
| `ask-matt` | You want the right next skill or flow. |
| `to-prd` | A product idea needs a durable PRD. |
| `to-issues` | A PRD, spec, plan, or issue needs bounded implementation issues. |
| `triage` | Incoming issues or external PRs need sorting into state roles. |
| `implement` | One ready-for-agent issue should be implemented, verified, reviewed, committed, and noted. |
| `tdd` | A behavior is clear enough to prove with a red test. |
| `diagnosing-bugs` | A bug, failure, or regression lacks a trusted repro or cause. |
| `review` | A diff needs fixed-point Standards and Spec review. |

### Supporting Skills

| Skill | Use it when |
| --- | --- |
| `grill-with-docs` | A loose idea needs codebase-aware questioning before product or implementation work. |
| `grilling` | A plan or idea needs direct questioning without codebase docs. |
| `decision-mapping` | Fog of war blocks a PRD or implementation plan. |
| `prototype` | A throwaway runnable artifact is needed to answer a design question. |
| `handoff` | A fresh session or agent thread needs to continue from a compact brief. |
| `domain-modeling` | Domain language, glossary terms, or ADR-worthy decisions need recording. |
| `codebase-design` | Module, interface, seam, adapter, depth, leverage, or locality vocabulary is needed. |
| `improve-codebase-architecture` | A repo needs architecture review and deepening candidates. |
| `writing-great-skills` | Skills need to be written or edited for predictable behavior. |
| `setup-matt-pocock-skills` | A repo needs the issue tracker, triage labels, domain docs, or engineering contract expected by these skills. |

### Experimental Skills

| Skill | Use it when |
| --- | --- |
| `to-slice-plan` | A no-babysitting implementation plan needs strict slice contracts and validation. |
| `next-slice` | One pending slice from a validated slice plan should be executed. |
| `slice-plan-runner` | An approved validated plan can run bounded slices unattended. |
| `convergent-pr-review` | A risky PR needs independent review passes, a verified finding ledger, and patch-ready triage. |

## Git Discipline

Implementation skills treat Git as part of the engineering contract.

- Inspect `git status` before editing.
- Preserve unrelated dirty work.
- Capture a starting ref before implementation so review has a fixed point.
- Keep each issue or slice narrow enough to validate, review, and commit alone.
- Stage only files touched for the selected issue unless the user explicitly asks for a broader commit.
- Write implementation notes with commit SHA, summary, validation, skipped checks, and residual risk.

This is not ceremony. It is how the next human or agent can tell what changed, why it changed, and what evidence supports it.

## Quick Start

Set `AGENT_SKILLS_DIR` to the skills directory your agent runtime reads. Common locations:

- Codex: `~/.codex/skills`
- Claude Code: `~/.claude/skills`
- Shared local setup: `~/.agents/skills`

Install the current active skills:

```bash
: "${AGENT_SKILLS_DIR:?Set AGENT_SKILLS_DIR to your agent's skills directory}"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R skills/current/* "$AGENT_SKILLS_DIR/"
```

Then run `setup-matt-pocock-skills` inside each target repo before first use. Setup writes or updates:

- `AGENTS.md`: the short primer and local pointers.
- `docs/agents/engineering-contract.md`: the full vocabulary and discipline.
- `docs/agents/issue-tracker.md`: how skills use the repo's tracker.
- `docs/agents/triage-labels.md`: label vocabulary for triage roles.
- `docs/agents/domain.md`: domain glossary and ADR routing.

Install selected experimental skills only when you want them:

```bash
cp -R skills/experimental/convergent-pr-review "$AGENT_SKILLS_DIR/"
cp -R skills/experimental/to-slice-plan "$AGENT_SKILLS_DIR/"
cp -R skills/experimental/next-slice "$AGENT_SKILLS_DIR/"
cp -R skills/experimental/slice-plan-runner "$AGENT_SKILLS_DIR/"
```

For a smaller starter setup with `ask-matt` and core local skills:

```bash
cp -R skills/current/ask-matt "$AGENT_SKILLS_DIR/"
cp -R skills/current/to-prd "$AGENT_SKILLS_DIR/"
cp -R skills/current/to-issues "$AGENT_SKILLS_DIR/"
cp -R skills/current/implement "$AGENT_SKILLS_DIR/"
cp -R skills/current/tdd "$AGENT_SKILLS_DIR/"
cp -R skills/current/review "$AGENT_SKILLS_DIR/"
```

Use `AGENTS_PORTABLE_FALLBACK.md` as a repo-level `AGENTS.md` when a repo cannot use the skill pack, or as global guidance only in an environment where the skill pack is not installed. Use `AGENTS_SKILL_PACK_GUIDE.md` when skills are installed and you want a thin global suggestion index that preserves the pack's vocabulary without duplicating every skill's instructions. Do not use both in the same Codex profile.

If a skill is unavailable, do not simulate it. Use the closest installed route only when it prevents the same failure mode.

## What This Is Not

- Not a package manager or runtime framework.
- Not a replacement for repo docs, source code, tests, review, CI, or user instruction.
- Not a requirement that every task needs process. Tiny safe edits can use a tiny source-read, edit, check loop.
- Not a promise that process creates correctness. Evidence still has to come from the repo and the checks that matter.

## Repository Layout

- `skills/current/`: active coding-agent skills.
- `skills/experimental/`: experimental workflows under active hardening.
- `skills/extra/`: optional skills outside the active guide.
- `skills/.archive/`: retired skill versions kept for reference.
- `AGENTS.md`: this repo's local primer generated by setup.
- `AGENTS_PORTABLE_FALLBACK.md`: portable fallback coding-agent instructions for repos or environments that do not install the skill pack.
- `AGENTS_SKILL_PACK_GUIDE.md`: a suggestion index for environments where skills are installed.
- `docs/agents/`: this repo's local setup output, including the engineering contract.
- `docs/adr/`: durable architecture decisions for the skill pack.
- `scripts/validate-skills.sh`: local validation for skill layout, skill resource references, guide skill references, installed-copy drift, secret/local-identifier hygiene, trailing whitespace, and `git diff --check`.
- `ACKNOWLEDGMENTS.md`: inspiration and no-affiliation notes.
- `LICENSE`: MIT license.

## Maintainer Notes

For maintainers, the source of truth for this repo's vocabulary is `CONTEXT.md`. Durable structure decisions live in `docs/adr/`, and `writing-great-skills` is the standard for editing skill wording: preserve predictability, choose strong leading words, keep each meaning in one place, and prune no-ops, sediment, and sprawl.

For routine local skill edits:

```bash
./scripts/validate-skills.sh
git diff --check
```

To catch installed-copy drift, set `AGENT_SKILLS_DIR` to the directory your agent runtime reads:

```bash
AGENT_SKILLS_DIR=~/.codex/skills ./scripts/validate-skills.sh
```

Before publishing or cutting a release, run the repo's release validation path.

## License

MIT. See [LICENSE](LICENSE).
