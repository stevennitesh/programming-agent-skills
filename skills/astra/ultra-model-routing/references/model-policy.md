# Model policy

Use when an assignment's route is unclear or a stronger effort is being
considered. Keep the exact model and effort pairs in the
[main skill](../SKILL.md) as the routing source of truth.

## Classify the scoped assignment

Choose a route after identifying the work, decisions still open, and observable
completion. Do not inherit the apparent difficulty of the whole project.

- **Routine execution:** the rule is settled, the relevant inputs are available,
  and acceptance can distinguish a correct result without substantial new design.
  Use Terra for an approved repetitive transformation, specified extraction,
  mechanical update, or execution of a defined check. Volume alone does not
  require Sol.
- **Substantive work:** the worker must investigate causes, resolve interacting
  behavior, make implementation decisions, or reason through uncertain cases.
  Use Sol High. An unknown test failure can require this route even if running
  the test was routine.
- **Review:** the assignment is to assess a candidate independently against its
  obligations. Use Sol Extra High. Finding locations or collecting fixed test
  evidence can be routine support; judging whether the candidate is correct
  remains review.

A broad instruction such as "clean up these files" does not become a Terra
assignment merely because the edits look repetitive. Settle the transformation
and preservation requirements first, or route the unresolved work to Sol.

Examples are classification aids, not mandatory task decomposition. Let the
native lead choose whether a separate assignment is useful.

## Escalate for a concrete reason

Route a routine assignment to Sol High when it reveals substantive ambiguity
or debugging work. Preserve the useful evidence and accepted decisions in the
handoff rather than restarting the investigation.

Choose Sol Max for a bounded problem when the evidence or known difficulty
justifies more reasoning: for example, an unresolved ordering invariant across
interacting execution paths, or a consequential compatibility question that
existing review has not resolved. The lead may select Max at the outset when
that need is already clear; do not require a sequence of failed cheaper runs.

State the question that warrants Max and the result needed to settle it.
Neither the label "final review" nor elapsed time, repository size, or output
volume is sufficient by itself. A Max reviewer can perform a required review
round; escalation does not create an extra round automatically.

Missing requirements, access, data, dependencies, or functioning tools need the
missing prerequisite. Address those causes within authority, continue useful
independent work, and report a consequential block. Do not use model escalation
as a substitute for missing evidence or authorization.

Keep a suitable worker's context for ordinary corrections. Reassign when the
work or required capability changes, not simply to reduce its remaining token
use. Do not restart a coherent assignment solely to change effort.

## Preserve the user's choices

Keep the selected lead unchanged, including Ultra. Explicit later user choices
override this default routing policy for their stated scope. Do not infer a
permanent policy change from a one-assignment override.

Use the routes on the available host; do not silently substitute older models,
Astra, or Luna. Read [Native spawning](native-spawning.md) when a requested pair
is unavailable or the effective configuration conflicts.

Treat this allocation as a task policy, not a benchmark result. When measurement
is requested, compare complete accepted outcomes with equivalent scope and
review obligations. Include lead work, handoffs, cached and uncached input,
output, review, and repair where the host exposes them. Do not equate fewer
worker tokens with lower total cost or infer account billing from incomplete
traces.
