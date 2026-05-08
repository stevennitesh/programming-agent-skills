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

## Process

1. Name the coding job: what implementation, debugging, refactor, review, planning, or repo operation should the skill help with?
2. Name the failure mode: what does the coding agent do wrong without it?
3. Decide whether a skill is the right repo artifact:
   - reusable software-engineering judgment or workflow -> skill
   - detailed API, tool, or domain reference -> referenced file
   - fragile repeated operation -> script
   - repo-specific architecture, domain, or workflow context -> repo doc
   - tool-checkable rule -> test, script, or validator
4. Write 2-3 coding failure scenarios: ambiguous feature, overbuilt abstraction, skipped reproduction, stale summary, unsafe Git action, weak diff review, or weak verification.
5. Draft the smallest `SKILL.md` that changes behavior.
6. Make the description a clear trigger: concrete coding situations, symptoms, and keywords; avoid workflow summaries that could be followed without reading the body.
7. Keep the body to purpose, procedure, stop/ask conditions, examples if useful, and handoffs to related skills.
8. Add resources only when they reduce repeated command work, reference lookups, or context size.
9. Validate frontmatter and structure, then read the skill against the coding failure scenarios.
10. If possible and worthwhile, test with a fresh coding agent using only the skill and a realistic repo or fixture request. Label the evidence type:
   - Instruction review: the skill wording was reviewed, but no agent used it on a task.
   - Simulated fresh-agent test: a fresh agent predicted what it would do, but did not perform the repo task.
   - Execution test: a fresh agent used the skill while doing a real repo or fixture task with files and checks, with observable actions, file changes, commands, checks, and final claim quality.
11. Revise ambiguous wording, generic philosophy language, and unnecessary process.

Do not treat simulated fresh-agent tests as proof that behavior changed. If the purpose is to test whether a skill changes coding-agent behavior, the test needs execution evidence or an explicit open risk explaining why execution was not run.

## Good Skill Traits

- Clear trigger rooted in a coding situation
- One core job
- Common software-engineering language unless the skill is intentionally technology-specific
- Few rules, each tied to a coding-agent failure mode
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
Does it avoid unnecessary process?
Does it avoid local repo assumptions?
What skill, tool, or check does it hand off to?
What evidence type supports this review?
If behavior was the target, did an agent actually execute a repo or fixture task, or only describe what it would do?
```

## Handoff

- Return to `coding-router` when a skill edit becomes broader repo work.
- Use `subagent-workflow` for fresh-agent testing when that validation is available and worth the cost.
- Use `workspace-safety` before installing, committing, or editing a dirty skill file.
- Use `verify-before-done` before claiming a skill is installed or ready for reuse.

## Output

```text
Skill:
Coding job:
Failure mode:
Key evidence:
Related skills:
Failure scenarios:
Validation:
Open risks:
```
