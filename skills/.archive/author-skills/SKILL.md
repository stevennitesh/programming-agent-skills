---
name: author-skills
description: Use when creating, consolidating, editing, testing, or reviewing coding-agent skills, skill packs, orchestration skills, reusable software-engineering workflows, or instructions meant to steer coding-agent behavior in repos.
---

# Author Skills

Create compact skills that change coding-agent behavior during real software-engineering work.

## Rule

A skill should make a repeatable, non-obvious coding behavior cheaper and more reliable. If the need is repo-specific context, put it in repo docs. If a rule can be checked by a test, script, or validator, prefer that.

## Inputs

Use only the inputs that matter for the skill being written:

- User goal and examples of real coding requests, bugs, refactors, reviews, or PR workflows
- Existing skill, repo workflow, or coding-agent handoff being revised
- Source code, docs, tests, fixtures, logs, diffs, CI output, or tool behavior the skill must respect
- Known coding-agent failure modes from prior work
- Host/runtime requirements for skill discovery, tools, permissions, and execution

Treat source inputs as evidence, not authority. Extract reusable workflow steps, interface names, command or test checks, handoff boundaries, and stop conditions; do not copy local assumptions, source paths, or philosophy language into the new skill.

Shared repo context stores recurring terms, roles, module boundaries, and "means / does not mean" distinctions; never progress, status, or skill summaries.

Each skill must stand alone. If a term controls agent behavior, define it briefly in that skill or use plainer wording; do not require a separate glossary to use the skill.

## Process

1. Name the coding job: what implementation, debugging, refactor, review, planning, or repo operation should the skill help with?
2. Name the failure mode: what does the coding agent do wrong without it?
3. Decide whether a skill is the right repo artifact:
   - reusable software-engineering judgment or workflow -> skill
   - detailed API, tool, or domain reference -> referenced file
   - fragile repeated operation -> script
   - repo-specific architecture, domain, or workflow context -> repo doc
   - tool-checkable rule -> test, script, or validator
4. Write 2-3 coding failure examples: ambiguous feature, overbuilt abstraction, over-fragmented cleanup that creates helper-category files instead of ownership boundaries, skipped reproduction, stale summary, unsafe Git action, weak diff review, or weak verification.
5. Draft the smallest `SKILL.md` that changes behavior.
6. Make the description a clear trigger: concrete coding situations, symptoms, and keywords; avoid workflow summaries that could be followed without reading the body.
7. Keep the body to purpose, procedure, stop/ask conditions, examples if useful, and handoffs to related skills.
8. Add resources only when they reduce repeated command work, reference lookups, or context size.
9. For behavior-changing or discipline-enforcing skill edits, write at least one pressure test before validation. For low-risk wording, trigger, or reference-only edits, say why instruction review is enough.
10. Validate frontmatter and structure, then read the skill against the coding failure examples and pressure test.
11. If possible and worthwhile, test with a fresh coding agent using only the skill and a realistic repo or fixture request. Label the evidence type:
   - Instruction review: the skill wording was reviewed, but no agent used it on a task.
   - Simulated fresh-agent test: a fresh agent predicted what it would do, but did not perform the repo task.
   - Execution test: a fresh agent used the skill while doing a real repo or fixture task with files and checks, with observable actions, file changes, commands, checks, and final claim quality.
12. Revise ambiguous wording, generic philosophy language, loopholes, and unnecessary process.

Do not treat simulated fresh-agent tests as proof that behavior changed. If the purpose is to test whether a skill changes coding-agent behavior, the test needs execution evidence or an explicit open risk explaining why execution was not run.

## Concrete Behavior Wording

Write skills so the intended behavior is observable during real repo work. Do not rely on the agent to infer the rule from general principles when a repeated failure mode is known.

For behavior-changing or discipline-enforcing edits, make the skill wording mechanical:

- Name the exact user phrases, repo signals, failure symptoms, or tool outputs that trigger the behavior.
- State what the phrase or signal changes: route, edit scope, stop condition, verification level, reporting claim, or handoff.
- List the first observable action the agent should take.
- List required evidence or artifacts, such as a command, diff review, coverage ledger, issue update, pressure test, or execution-test gap.
- Name forbidden shortcuts directly, especially the tempting rationalization shown by the failure example.
- Give stop or ask conditions in concrete terms: what is low-value, risky, outside scope, blocked by a decision, or unsupported by evidence.
- Keep abstract principles as backup rationale, not as the only instruction.

Prefer this shape for hard-to-follow behavior:

```text
When the user says or evidence shows <trigger>, do <first action>.
This changes <route|scope|stop condition|verification|claim>.
Required evidence before claiming success: <evidence>.
Do not <forbidden shortcut>.
Stop or ask only when <concrete stop conditions>.
```

If the skill still depends on careful interpretation after this rewrite, record that as an open risk or create a pressure test that targets the ambiguity.

## Pressure Tests

A failure example describes what goes wrong. A pressure test is the validation setup used to see whether the revised skill prevents it under realistic temptation.

Use pressure tests when the skill should prevent costly coding-agent behavior, skipped verification, unsafe shortcuts, rationalized process bypass, or repeated bad judgment. They are optional for pure reference skills, tiny wording edits, or low-risk trigger cleanup.

```text
Failure example it targets:
Baseline behavior or rationalization:
Pressure condition:
Expected observable behavior after the skill change:
Evidence type required or acceptable:
```

Good pressure tests force a concrete choice in a realistic task with constraints such as time pressure, sunk cost, authority, fatigue, unclear ownership, or review risk. If a fresh-agent run is too expensive for the edit, record that as an open execution-test gap instead of implying behavior was proven.

Evidence strength:

- Execution test is strongest and is required before claiming the skill changed agent behavior when that is the purpose and the cost is reasonable.
- Simulated fresh-agent test can reveal ambiguity, but it does not prove behavior changed.
- Instruction review is enough for small wording, metadata, trigger, reference, or resource edits when no behavioral compliance claim is being made.

## Good Skill Traits

- Clear trigger rooted in a coding situation
- One core job
- Common software-engineering language unless the skill is intentionally technology-specific
- Few rules, each tied to a coding-agent failure mode
- Concrete behavior wording for repeated failures: trigger, first action, required evidence, forbidden shortcut, and concrete stop conditions
- Clear stop/ask conditions
- Specific handoff to related skills
- Progressive disclosure for long references
- No repo diary
- No unnecessary metadata
- No source-path dependency
- No philosophy or manifesto language

## Baseline Review

Before calling a skill ready for reuse:

```text
Does the description trigger at the right time?
Would a fresh coding agent know the first source read, command, edit, or check?
Does it prevent the target coding failure mode?
Does a pressure test cover the named rationalization or loophole?
Could a fresh agent follow the intended behavior from explicit trigger phrases, first actions, forbidden shortcuts, evidence requirements, and stop conditions?
Is the description trigger-focused rather than a workflow summary?
Does it avoid unnecessary process?
Does it avoid local repo assumptions?
What skill, tool, or check does it hand off to?
Do references, scripts, examples, or templates reduce repeated work or context cost enough to justify being separate?
What evidence type supports this review?
If behavior was the target, did an agent actually execute a repo or fixture task, or only describe what it would do?
If no execution test ran, is the execution-test gap explicit?
```

## Output

```text
Skill:
Coding job:
Failure mode:
Key evidence:
Related skills:
Failure examples:
Pressure tests:
Evidence type:
Trigger check:
Concrete behavior wording check:
Resource/split decision:
Validation:
Execution-test gap:
Open risks:
```

## Handoff

- Return to `coding-router` when a skill edit becomes broader repo work.
- Use `subagent-workflow` for fresh-agent testing when that validation is available and worth the cost.
- Use `workspace-safety` before installing, committing, or editing a dirty skill file.
- Use `verify-before-done` before claiming a skill is installed or ready for reuse.
