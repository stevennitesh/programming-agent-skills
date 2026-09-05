# Skill authoring

## Make discovery precise

Describe the task the skill serves and the observable requests that should
activate it. Add an exclusion only for a likely competing interpretation.
Keep detailed procedure in the body so the description remains a useful
selection cue.

Keep the folder name, frontmatter name, and any invocation metadata consistent.
Preserve the intended invocation policy. For a new skill, use the target host's
default unless the user requests another policy.

Discovery and context loading depend on the host. Do not assume that making
a skill explicit-only removes all metadata from context or prevents other
instructions from referencing its files. Check current host documentation when
changing that behavior.

## Keep the package small

Put the shared method and completion condition in `SKILL.md`. Add supporting
references only for detail a particular branch needs, with a conditional link
at the point of use. Add scripts or templates when they remove repeated work
or protect a concrete contract.

For host-specific schema, metadata, or installation mechanics, use the current
bundled `skill-creator` guidance when available; otherwise consult the target
host's official documentation. Keep those changing mechanics out of this method.
Edit the source package and preserve unrelated metadata and installation state.

## Check the package

Use the available package validator to check frontmatter and naming. Resolve
local links from their containing files and inspect changed discovery metadata.
Confirm that required tools and references exist in the intended environment.
Report package checks separately from any evidence about agent behavior.
