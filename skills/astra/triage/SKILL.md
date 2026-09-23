---
name: triage
description: Classify raw tracker issues and configured external PR or MR intake into one supported next state or bounded handoff. Use only for explicit triage requests; exclude project-created ready work, implementation, deep diagnosis, and code review.
---

# Triage

Turn raw tracker intake into an evidence-supported next state without implementing
the request.

## 1. Read the intake and tracker contract

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If the
required tracker or role mapping is missing or incompatible, recommend
[repo-bootstrap](../repo-bootstrap/SKILL.md) and stop. Include external PR or MR
intake only when the tracker configuration permits it.

For a queue overview, read
[Attention scan](references/attention-scan.md) and remain read-only. Otherwise
read the selected item's body, decision-bearing discussion, current roles,
relevant relationships, and useful attachments.

When the maintainer names an exact state, skip discovery that cannot change that
instruction, but inspect enough current state to avoid fabricating verification,
an invalid role combination, or a stale handoff.

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

Separate observations from hypotheses. Use the cheapest safe check that can
support the disposition. A failed reproduction does not prove a report false.
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

When mutation is authorized, prepare the concrete comment or brief, category
role, state role, and close action. If additional effects are required to leave a
valid configured state, show those effects before applying them rather than
creating a false-ready item.

Refresh the item before writing when intervening activity could change the
disposition. If decision-bearing state drifted, reconcile it before mutation.

Apply only the authorized effects through the configured tracker representation.
Post a required note or ready brief before state transition and close last. Add AI
attribution only when repository policy requires it.

## 5. Verify and stop

Read the item back and verify the changed fields and relationships. If an effect
failed or has an uncertain result, inspect actual state before retrying and report
the applied, unknown, and remaining effects.

Complete when a queue scan remained read-only, or the selected item has one
supported disposition and every authorized tracker mutation has been read back.
Return the resulting state, material uncertainty, and next owner. Do not start
implementation or downstream workflow execution.
