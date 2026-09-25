---
name: triage
description: Classify raw tracker intake into a supported next state or bounded handoff. Exclude project-created ready work, implementation, deep diagnosis, and code review.
---

# Triage

Turn raw tracker intake into an evidence-supported next state without implementing
the request.

## 1. Read the intake and tracker contract

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If the
required tracker or role mapping is missing or incompatible, recommend
[repo-bootstrap](../repo-bootstrap/SKILL.md) and stop. Before recommending a
mutation, confirm the configured roles can represent the item truthfully: a
mutated item must be able to end with exactly one configured category role and
one configured state role. If a current blocker or role conflict cannot be
represented without misusing a state, treat that as a setup gap rather than
inventing a disposition. Include external PR or MR intake only when the tracker
configuration permits it.

For a queue overview, read
[Attention scan](references/attention-scan.md) and remain read-only. Otherwise
read the selected item's body, decision-bearing discussion, current roles,
relevant relationships, and useful attachments.

When the maintainer names an exact state, skip discovery that cannot change that
instruction, but inspect enough current state to avoid fabricating verification,
an invalid role combination, a blocked ready state, or a stale handoff. An
exact-state instruction changes the requested disposition; it does not turn an
unverified claim into evidence or waive tracker invariants.

## 2. Establish the honest disposition

Choose the configured category and next state from current evidence. Inspect
repository behavior, tracker history, duplicates, prior fixes, or settled
rejections only as far as they can change that disposition.

Use `bug` for a defect in intended existing behavior and `enhancement` for new
or changed behavior. Use:

- `needs-info` when missing reporter facts can change the disposition;
- `ready-for-agent` for one bounded implementation-ready outcome;
- `ready-for-human` for one named human-owned action;
- `implemented` when current evidence establishes the requested outcome already
  exists; and
- `wontfix` only for an authorized rejection, duplicate, supersession, or
  out-of-scope disposition.

`needs-triage` marks unprocessed intake; it is not the completed result of
triaging a selected item.

Before recommending `ready-for-agent` or `ready-for-human`, verify that the
recipient has one bounded actionable outcome, no unresolved consequential
decision they would have to invent, and no active configured blocker that makes
the item non-actionable. If a blocker exists and the configured state model has
no honest non-ready representation for it, report the mapping gap and recommend
[repo-bootstrap](../repo-bootstrap/SKILL.md) instead of advertising false
readiness.

Separate observations from hypotheses. Use the cheapest safe check that can
support the disposition. A failed reproduction does not prove a report false.
Likewise, a claim that is not confirmed or is supported by insufficient evidence
is an evidence limit, not by itself a reason to use `wontfix` or `implemented`.
When readiness depends on dedicated causal investigation, recommend
[diagnosing-bugs](../diagnosing-bugs/SKILL.md) and stop with the intake evidence
intact. When an attached diff needs fixed-candidate judgment, recommend
[change-review](../change-review/SKILL.md) instead.

If a user-owned product decision remains open, name that decision and owner
rather than inventing an answer to make the item ready.

## 3. Return a bounded handoff

State the recommended category and state, decisive evidence, and material
uncertainty. For `needs-info`, preserve what is already established and ask only
questions whose answers can change the disposition. For a duplicate or rejection,
name the existing item or governing decision when one exists.

For `ready-for-agent` or `ready-for-human`, read
[Ready brief](references/ready-brief.md). Do not pre-plan implementation or copy
generic engineering guidance into the intake item.

When settled intake requires several independently completable implementation
units, recommend explicit [to-tickets](../to-tickets/SKILL.md) and stop before
marking the raw intake ready as one executable item.

## 4. Apply only authorized tracker effects

If no tracker mutation was requested, return the recommendation and stop.
Invoking this skill does not itself authorize comments, role changes, assignment,
or closure.

When mutation is authorized, prepare the complete effect set before the first
write: the concrete comment or brief, target category role, target state role,
conflicting role removals, relationship consequences that require read-back, and
close action. The planned final item must have exactly one configured category
role and one configured state role. If additional effects are required to leave a
valid configured state, show them before applying rather than creating a
false-ready item.

Immediately refresh the item before the first mutation. Compare the
decision-bearing body or discussion, category/state roles, relevant relationships,
and candidate identity when applicable. If material state drifted, discard the
stale effect set and recompute it. Do not apply newly required effects that exceed
the user's existing authorization.

Apply only the authorized effects through the configured tracker representation,
in prerequisite-first order. Post a required note or ready brief first; reconcile
the category role; remove conflicting state roles before applying the target
state; and close last. Never apply a ready state while a configured blocker or
required ready brief is unresolved. After an uncertain or partial result, read
back actual state before retrying and do not replay a comment, brief, or role
change that already succeeded. Add AI attribution only when repository policy
requires it.

## 5. Verify and stop

Read the item back and verify the required note or brief, exactly one configured
category role, exactly one configured state role, close state when applicable,
and any relationships whose semantics changed. If an effect failed or has an
uncertain result, report the applied, unknown, and remaining effects from observed
state. Do not claim rollback unless the tracker read-back proves it.

Complete when a queue scan remained read-only, or the selected item has one
supported disposition and every authorized tracker mutation has been read back.
Return the resulting state, material uncertainty, recovery work if any, and next
owner. Do not start implementation, diagnosis, review, ticket decomposition, or
other downstream workflow execution.
