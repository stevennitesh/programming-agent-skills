---
name: triage
description: Sort raw tracker issues and configured external PR or MR intake into one honest disposition or concise handoff, then apply authorized tracker changes with read-back. Exclude project-created ready work, implementation, deep diagnosis, and code review.
---

# Triage

Turn raw tracker intake into an honest next state without implementing it.

## 1. Read the intake

Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either
is missing or incompatible, recommend `$repo-bootstrap` and stop. Include an
external PR or MR only when the tracker configuration permits it.

For a queue overview, read [ATTENTION-SCAN.md](ATTENTION-SCAN.md), return the
items needing attention, and make no changes. Otherwise read the complete
selected item, its decision-bearing discussion, current roles, relevant links,
and useful attachments.

When the maintainer names an exact state, skip discovery that cannot change
that instruction. Inspect enough current context to write the required note and
do not present skipped verification as completed.

## 2. Judge the disposition

Choose the configured category and the next honest state. Inspect current
behavior, tracker history, and the likely owner only as far as they can change
that choice. Search for an existing implementation, duplicate, prior fix, or
settled rejection when the evidence makes one plausible. Match meaning and
cause, not keywords or a visible symptom alone.

Separate observations from hypotheses. Run only the cheapest safe check needed
to support the disposition. A failed reproduction does not prove a report
false. When readiness requires deep causal investigation, recommend
`$diagnosing-bugs` and stop with the evidence intact. When an attached diff
needs fixed-candidate code judgment, recommend `$change-review` instead.

If reporter facts are missing, ask the few specific questions that would
change the disposition. If product intent or another owned decision remains
open, name the decision and owner rather than choosing a heavier workflow for
the user.

## 3. Write the handoff

State the recommended category and state, the evidence that supports them, and
material uncertainty. For `needs-info`, preserve what is already settled and
ask actionable questions. For a rejection or duplicate, give the reason and
the existing item or decision when one exists.

For `ready-for-agent` or `ready-for-human`, read
[AGENT-BRIEF.md](AGENT-BRIEF.md). Keep the handoff bounded. Do not pre-plan the
implementation or repeat generic engineering guidance.

When settled intake needs several independently completable implementation
slices, preserve the source, recommend explicit `$to-tickets`, and stop before
changing readiness.

## 4. Apply authorized effects

If no tracker change was requested, return the recommendation and stop. A
request that names the target and every durable effect authorizes only those
effects. Preview any generated note, brief, additional role change, or close
action the request did not already approve, then wait for approval.

If the requested effects cannot leave one configured category role, one
configured state role, and any required ready brief, show the smallest
additional effects and wait. Do not create a false-ready or invalid item to
honor a narrower request.

Refresh the item before writing when later activity could change the decision.
If the refresh changes the disposition, note, roles, or close state, stop and
obtain approval for the revised effects.
Apply only the approved comment, one configured category role, one configured
state role, and close action. Post the required note or brief first, replace
roles second, and close last. Follow the tracker contract for transport and
recovery. Add AI attribution only when the repository's tracker policy requires
it.

## 5. Verify and stop

Read the item back and verify the intended effects. Refresh dependents only
when the change can alter their readiness. If an effect is failed or uncertain,
do not retry blindly; report what applied, what remains unknown, and the safest
recovery.

Complete when the attention scan stayed read-only, or the selected item has one
supported disposition and every authorized tracker effect has been read back.
Report the resulting state, material uncertainty, and next owner. Leave code
changes and downstream work unstarted.
