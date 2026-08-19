# Skill mechanics

Read this reference only when creating, editing, or auditing a skill.

## Invocation

Automatic selection is the default. A model-invokable skill has a description
that acts as its context pointer. Name the observable requests that should load
the skill and the closest likely misroute. Keep runtime procedure in the body.

Make a skill explicit-only only when the user asks for that behavior. An
explicit-only skill spends no automatic context load, but the user must
remember to invoke it. A router may help a person choose among several
explicit-only skills, but it recommends a route rather than silently running
one. Keep shared reference outside an explicit-only skill when another skill
must reach it. Only the user can expose an explicit-only skill by invoking it
with its `$`-prefixed name.

## Package

Keep the folder name, frontmatter `name`, metadata, and every current pointer
consistent. Put the shared method in `SKILL.md`. Put substantial branch-only
rules in `references/` and link each reference at the point where its condition
becomes active.

Use the bundled `skill-creator` for a new package or metadata mechanics. When
editing an existing skill, preserve unrelated metadata and installation state.
The canonical package is the edit source; an installed copy is not.

## Check

Verify the skill name and folder, parse the frontmatter, inspect reference
links, and check model invocation metadata when it changed. Use repository
validation when available. These structural checks prove package integrity,
not that wording changes agent behavior.
