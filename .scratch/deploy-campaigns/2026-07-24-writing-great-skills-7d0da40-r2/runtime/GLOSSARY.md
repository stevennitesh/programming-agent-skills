# Writing Great Skills Glossary

Load this file only when invocation, information hierarchy, pruning, or
completion vocabulary affects the work.

## Invocation

**Implicitly invocable** means Codex may discover the skill from its
description and a human may still name it explicitly.

**Explicit-only** means the package disables implicit invocation and requires
the human to name the skill.

**Description** is the machine-readable routing predicate for an implicitly
invocable skill. It names observable entry triggers and the closest exclusions
without copying runtime procedure or summarizing the body.

## Information hierarchy

**Common behavior** is needed on every applicable run and stays inline.

**Branch-only reference** is needed only under a named condition. A context
pointer names both the reference target and that loading condition.

**Co-location** keeps one concept's rule, conditions, and caveats together.

## Completion

**Completion criterion** is the checkable condition that closes a unit of
work. Sharpen it before considering a context split for early stopping.

**Persistent early-stop defect** is observed completion before that criterion
is met after the criterion has been sharpened. Only such an observed defect
can justify a split intended to hide later work.

## Pruning

**Single owner** means one authoritative location owns a semantic rule.

**Duplication** repeats one meaning in more than one authoritative location.

**No-op** is an instruction that changes no observable behavior relative to
the tested default.

**Stale exposition** describes history or theory that no longer changes the
skill's current behavior.
