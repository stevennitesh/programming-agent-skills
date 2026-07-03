# Programming Agent Skills

This context defines the resolved language for maintaining the skill pack. The repo exists to shape agent behavior across target repos through intentional skills, setup docs, validators, and reusable engineering vocabulary.

## Repository Maintenance Invariants

- `AGENTS.md` is the agent primer: short commands, context pointers, and
  non-negotiable local invariants only.
- `docs/plans/README.md` is the active-work router. It links current plans and
  runbooks without copying long plan lists.
- `docs/agents/engineering-contract.md` teaches the local coding discipline;
  skills execute their specific workflows.
- Stable vocabulary belongs in this file. Durable structure or policy decisions
  belong in `docs/adr/`.
- Tracker mechanics and label mappings belong in `docs/agents/issue-tracker.md`
  and `docs/agents/triage-labels.md`.
- Research, synthesis, and validation artifacts live under `docs/research/`,
  `docs/synthesis/`, and `docs/validation/`. Treat historical artifacts,
  transcripts, issue notes, and run logs as evidence unless they explicitly say
  they are current instructions.
- The validator owns mechanical and publishing hygiene. Human review,
  `$writing-great-skills`, and this context own language quality.
- Prefer config, scripts, and skill files over explanatory prose when behavior
  can be enforced directly.

## Workflow Model And Artifact Ownership

- `README.md` is the human-facing product overview and install guide.
- `AGENTS.md` is the boot surface for every agent run.
- `CONTEXT.md` is the stable vocabulary, workflow model, and repo invariants.
- `docs/plans/README.md` routes active work, live runbooks, and current plan
  families.
- `docs/research/` owns source intake, source ranking, search vocabulary, and
  candidate language extraction.
- `docs/synthesis/` owns design judgment between research and final skills:
  methods, prompt templates, facet timelines, skill notes, and family notes.
- `docs/validation/` owns evidence that skill wording changed agent behavior:
  transcript reviews, eval notes, fixtures, and skipped-check records.
- `docs/agents/` owns agent process/config for repos using this skill pack:
  tracker mechanics, triage labels, domain routing, and the engineering
  contract.
- `docs/adr/` owns durable decisions that should not be relitigated during
  routine skill edits.
- `skills/current/` owns active skills. `skills/experimental/` owns workflows
  still being hardened. `skills/extra/` owns optional skills outside the active
  guide.

## Generated And Historical Artifacts

- Prompt outputs under `docs/synthesis/facets/` are synthesis artifacts, not
  boot instructions.
- Research notes, synthesis timelines, validation notes, transcripts, issue
  notes, and run logs stay historical unless an owning README or
  `docs/plans/README.md` marks them current.
- Generated data, caches, downloaded artifacts, bulky outputs, and temporary
  experiments stay out of tracked source unless the repo explicitly needs them.
- Use `.tmp/` for disposable local experiments. Delete scratch before handoff
  unless the user asks to preserve it.

## Stable Defaults

- Python commands should be portable: activate `.venv`, then run
  `python -m ...`.
- Pytest defaults live in `pyproject.toml`; do not repeat addopts, testpaths,
  markers, or ignored directories across docs.
- Focused tests should use `python -m scripts.pytest_focused` so narrow runs do
  not inherit full-suite fanout by accident.
- Skill-pack validation should use `python -m scripts.validate_skills`; the
  POSIX shell script is only a compatibility wrapper.
- Mechanical behavior belongs in config or scripts when possible. Prose should
  explain ownership, routing, and judgment that cannot be enforced directly.

## Skill-Pack Architecture

**Skill pack**:
A coordinated set of skills, setup docs, validators, and reference material that teaches agents a shared engineering discipline across repos.
_Avoid_: prompt collection, script bundle

**Target repo**:
A repo where this skill pack is installed and used to do product, planning, implementation, triage, review, or maintenance work.
_Avoid_: downstream repo, client repo

**Setup surface**:
The repo-local files installed by `setup-matt-pocock-skills` so the skills can work from local truth: `AGENTS.md`, `docs/agents/engineering-contract.md`, issue-tracker rules, triage labels, and domain-doc routing.
_Avoid_: bootstrap output, generated docs

**Agent primer**:
The short `AGENTS.md` block that primes an agent with local pointers and compact vocabulary before it chooses a skill or edits code.
_Avoid_: router, full contract, manual

**Engineering contract**:
The target repo's local statement of agentic coding discipline: convergence loop, commitment boundary, semantic proof, slicing, `.tmp` exploration cleanup, review, and lock.
_Avoid_: style guide, process doc

**Local contract slice**:
The part of the engineering contract that a single skill must enforce because it is directly relevant to that skill's job.
_Avoid_: duplicated contract, copied philosophy

**Router skill**:
An explicit-only skill whose job is to point the user at the right next skill, reducing cognitive load without performing the downstream skill itself.
_Avoid_: dispatcher, index, automatic router

**Suggestion index**:
A repo-local guide that suggests relevant explicit skills and files but does not invoke skills or teach their full procedures.
_Avoid_: router skill, command menu

## Skill-Authoring Discipline

**Predictability**:
The degree to which a skill makes the agent behave the same way on every run: the same process, not the same output.
_Avoid_: output determinism, generic reliability

**Leading word**:
A compact concept already living in the model's priors that anchors a region of behavior, invocation, or review in fewer tokens than repeated explanation.
_Avoid_: keyword, slogan

**Context pointer**:
A loaded reference that tells the agent when to read some out-of-context material. The wording of the pointer determines whether the agent reaches the material reliably.
_Avoid_: link, import

**Information hierarchy**:
The ranking of skill content by how immediately the agent needs it: in-skill steps first, in-skill reference second, disclosed reference behind context pointers third.
_Avoid_: layout, organization

**Completion criterion**:
The checkable condition that tells the agent a unit of work is genuinely done and sets how much legwork the step demands.
_Avoid_: vague done condition

**Single source of truth**:
The state where each meaning lives in one authoritative place, so changing behavior is a one-place edit.
_Avoid_: repeated explanation, parallel definitions

**Relevance**:
Whether a line still bears on what the skill does now. Relevant lines can still be no-ops, but irrelevant lines should be removed or moved.
_Avoid_: keeping prose because it once helped

**Sediment**:
Stale or outdated layers that accumulate because adding feels safer than deleting.
_Avoid_: cruft, historical leftovers

**Sprawl**:
Skill length that hurts readability and maintainability even when the lines are not stale or duplicated.
_Avoid_: bloat, verbosity

**No-op**:
An instruction that does not change agent behavior because the model already does it by default.
_Avoid_: restating the obvious

**Context load**:
The token and attention cost paid when an implicitly invocable skill keeps its description loaded for discovery.
_Avoid_: token cost only

**Cognitive load**:
The cost paid by the human when explicit-only skills require them to remember which skill to invoke.
_Avoid_: human burden as a defect

**Progressive disclosure**:
Moving reference behind a context pointer so the top-level skill stays legible while branch-specific material remains reachable.
_Avoid_: lazy loading, hiding required steps

## Skill Encoding

**Skill-writing formula**:
The default vocabulary shape for this skill pack: software-engineering taste term -> agent execution surface -> evidence gate. The software-engineering term recruits high-quality professional priors; the agent execution surface tells the LLM how to operate inside repo context and tools; the evidence gate prevents good language from becoming confident but unproven output.
_Avoid_: taxonomy for its own sake, sophisticated phrasing without proof

**Attention handle**:
A compact word or phrase that points the agent toward a useful pretrained cluster of knowledge and behavior. The goal is not to teach the whole source in context; it is to focus the model on upper-bound engineering priors already associated with terms like `red-green-refactor`, `tracer bullet`, `deep module`, or `ubiquitous language`.
_Avoid_: generic reminder, decorative keyword, book summary

**Source compression formula**:
The act of converting source wisdom into the smallest skill text that changes agent behavior: leading word -> rule -> agent action -> evidence gate -> forbidden shortcut or stop condition. A skill should carry the source's useful force, not the source's full explanation.
_Avoid_: bibliography as instruction, long explanation, compressed trivia

**Upper-bound prior**:
A high-quality professional or book-backed model prior that the skill pack intentionally recruits. The target is not average coding-agent behavior; it is sharper taste, smaller slices, stronger proof, better boundaries, and more honest residual risk.
_Avoid_: average best-practice slogan, broad software advice

**Software-engineering taste term**:
A book-backed or professional term that pulls the agent toward strong engineering judgment, such as `tracer bullet`, `red-green-refactor`, `semantic correctness`, `seam`, `deep module`, `fixed-point review`, or `residual risk`.
_Avoid_: average best-practice slogan, vague quality word

**Agent execution surface**:
The concrete model-operational surface through which a taste term becomes action: context engineering, agent-computer interface, trajectory, feedback signal, evaluation harness, guardrail, observability, tool use, or structured output.
_Avoid_: AI research term used as decoration

**Evidence gate**:
The checkable proof condition a slice must pass before the agent can call it done. This is the hard behavioral version of a completion criterion: no pass through the gate without source, tests, fixtures, logs, diffs, command output, CI, screenshots, rendered output, or user confirmation.
_Avoid_: vibe check, plausible completion, longer final answer as proof

## Agentic Delivery

**Convergence loop**:
The default coding rhythm for this skill pack, scaled to task size: orient, explore, choose, prove, expand, converge, simplify, and lock. It gives the agent room to discover a better local approach, then forces proof, review, simplification, cleanup, and evidence before done.
_Avoid_: rigid pipeline, unchecked exploration

**Commitment boundary**:
The line between what the user has committed to and what the agent may decide. Requirements, acceptance criteria, semantic correctness, user-visible behavior, public contracts, data semantics, security/privacy posture, and the bounded slice are commitments; internal technique belongs to the agent unless internal behavior is load-bearing for the requested result.
_Avoid_: permission for every internal choice, silent renegotiation

**Load-bearing internal**:
Internal behavior that determines whether the requested result is correct, even when the user does not care about the implementation shape. Load-bearing internals need a contract and proof through the smallest meaningful seam.
_Avoid_: unproven helper logic, hidden semantics

**Semantic correctness**:
Correctness of the actual meaning of the result, not just the existence of an output, passing command, or rendered artifact.
_Avoid_: output exists, smoke test only

**Proof**:
The strongest practical evidence that a slice works, without weakening TDD discipline when a code slice is suitable for it. Behavior changes should use red-green-refactor through a useful test seam when appropriate.
_Avoid_: plausibility, vibe check, replacing TDD with after-the-fact checks

**Bounded slice**:
The smallest useful scope that can move the repo toward the requested outcome while preserving the commitment boundary and producing evidence.
_Avoid_: broad mission, open-ended cleanup

**Tracer bullet**:
A narrow end-to-end slice that proves one observable behavior through the real system and reduces uncertainty about behavior, a seam, or a risk.
_Avoid_: horizontal layer, isolated plumbing

**Vertical slice**:
Work split by observable behavior across the system rather than by technical layer.
_Avoid_: frontend-only/backend-only as the default

**Fixed-point review**:
Review of a diff against a known starting ref, checking both documented Standards and the originating Spec.
_Avoid_: floating review, vibe review

**Evidence**:
The source, tests, fixtures, logs, diffs, commands, CI, screenshots, rendered output, or user confirmation that supports a claim of done.
_Avoid_: unverified claim

**Red-green-refactor**:
The TDD rhythm for behavior that is clear enough to test: write a failing test, make it pass, then simplify while preserving behavior.
_Avoid_: after-the-fact testing
