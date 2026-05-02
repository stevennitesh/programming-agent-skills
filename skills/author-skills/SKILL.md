---
name: author-skills
description: Use when creating, consolidating, editing, testing, or reviewing agent skills, skill packs, orchestration skills, reusable workflows, or instructions meant to steer agent behavior.
---

# Author Skills

Create compact skills that change agent behavior under pressure.

## Rule

A skill should make a repeatable, non-obvious behavior cheaper and more reliable. If the need is one-off project context, put it in project docs. If a rule can be enforced mechanically, prefer a validator or script.

## Inputs

Use only the inputs that matter for the skill being written:

- User goal and examples of real requests
- Existing skill or workflow being revised
- Source evidence, docs, code, logs, or tool behavior the skill must respect
- Known failure modes from prior agent behavior
- Platform requirements for skill discovery and execution

Treat source material as evidence, not authority. Extract portable mechanisms, names, checks, and stop conditions; do not copy local assumptions, source paths, or philosophy language into the new skill.

Shared glossary docs, when present, store recurring terms, roles, boundaries, and "means / does not mean" distinctions. Do not use them for progress, status, or skill summaries.

## Process

1. Name the job: what task should the skill help with?
2. Name the failure mode: what does the agent do wrong without it?
3. Decide whether a skill is the right vehicle:
   - reusable judgment or workflow -> skill
   - detailed reference -> referenced file
   - fragile repeated operation -> script
   - one-off context -> project doc
   - mechanical rule -> validator
4. Write 2-3 pressure scenarios: ambiguity, overbuild, shortcut, stale context, or weak verification.
5. Draft the smallest `SKILL.md` that changes behavior.
6. Make the description trigger-focused: concrete situations, symptoms, and keywords; avoid workflow summaries that could be followed without reading the body.
7. Keep the body to purpose, procedure, stop conditions, examples if useful, and related handoff.
8. Add resources only when they reduce repeated work or context load.
9. Validate structure, then read the skill against the pressure scenarios.
10. If possible and worthwhile, forward-test with a fresh agent using only the skill and a realistic request.
11. Revise loopholes, vague language, and unnecessary process.

## Good Skill Traits

- Clear trigger
- One core job
- Universal language unless the skill is intentionally technology-specific
- Few rules, each tied to a failure mode
- Clear stop conditions
- Specific handoff to related skills
- Progressive disclosure for long references
- No project diary
- No unnecessary metadata
- No source-path dependency
- No self-important process language

## Baseline Review

Before calling a skill durable:

```text
Does the description trigger at the right time?
Would a fresh agent know the next action?
Does it prevent the target failure mode?
Does it avoid unnecessary process?
Does it avoid local assumptions?
What does it hand off to?
```

## Handoff

Return to `coding-router` when a skill edit becomes broader coding work. Use `manage-subagents` for forward-testing only when fresh-agent validation is available and worth the cost. Use `workspace-safety` before installing, committing, or editing a dirty skill file. Use `verify-before-done` before claiming a skill is durable, deployed, or ready.

## Output

```text
Skill:
Job:
Prevents:
Key inputs:
Related skills:
Pressure scenarios:
Validation:
Open risks:
```
