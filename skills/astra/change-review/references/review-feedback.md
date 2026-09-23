# Review feedback

Read when the user supplies review comments, findings, or requested corrections
and wants them assessed, answered, or applied to a fixed candidate.

Treat each feedback item as a technical claim or proposed correction, not as
authority over accepted behavior.

## Reconcile each item

Bind the feedback to the actual candidate and identify the obligation, failure
scenario, or maintainability cost it claims. Check the current code, accepted
requirements, supported versions, repository policy, and relevant history far
enough to determine whether the claim holds here.

Classify each item as:

- **admitted:** it satisfies the main review finding standard;
- **disproved:** current evidence shows the claimed problem does not apply;
- **unclear:** a material premise or owner-held decision is missing; or
- **superseded:** the candidate or governing decision changed so the comment no
  longer addresses the current state.

Human or automated review can supply evidence and attention, but it does not
silently override a user-settled product or architecture decision.

## Apply corrections only within authority

If fixes are already authorized, implement only admitted corrections and any
necessary in-scope consequences. Preserve stable finding identities when the
feedback already has them.

Review the successor against the admitted item and the behavior affected by its
correction. Do not broaden into unrelated cleanup merely because a reviewer
mentioned it.

External replies, comment resolution, publication, merge, and acceptance of
residual risk remain separately authorized effects.
