# Writing Great Skills Glossary

Load this file only when invocation, behavior shape, information hierarchy,
pruning, or completion vocabulary affects the work.

## Behavior shape

**Predictable behavior** means Codex follows the intended decision process
under applicable variation; it does not require identical output.

**Leading word** is a compact pretrained concept that recruits one intended
behavior. Define it once and reuse the term only where that behavior must stay
salient. It earns its place only when it changes behavior relative to the
tested default and never replaces an exact contract.

**Gate** is a boundary check with an applicability condition, passing evidence,
and safe failure action. Use gates for cross-cutting constraints instead of
turning each constraint into a workflow step.

## Invocation

**Implicitly invocable** means Codex may discover the skill from its
description and a human may still name it explicitly.

**Explicit-only** means the package disables semantic auto-invocation. The
human must name the skill or explicitly approve one exact caller-owned
invocation packet that names it; otherwise callers recommend it and stop.

**Description** is the machine-readable routing predicate for an implicitly
invocable skill. It names observable entry triggers and the closest exclusions
without copying runtime procedure or summarizing the body.

## Information hierarchy

**Common behavior** is needed on every applicable run and stays inline.

**Branch-only reference** is needed only under a named condition. A context
pointer names both the reference target and that loading condition.
When required branch material is observably missed, sharpen the pointer's
target and loading condition first; inline the material only if the sharpened
pointer still fails.

**Co-location** keeps one concept's rule, conditions, and caveats together.

## Completion

**Completion criterion** is the condition that closes a unit of work. Make it
clear enough to distinguish pass from fail and demanding enough to force the
required legwork. Sharpen it before adding a step or considering a context
split for early stopping.

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
