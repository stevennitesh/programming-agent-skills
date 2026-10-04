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

Classify claimed defects as:

- **admitted:** it satisfies the main review finding standard;
- **disproved:** current evidence shows the claimed problem does not apply;
- **unclear:** a material premise or owner-held decision is missing; or
- **superseded:** the candidate or governing decision changed so the comment no
  longer addresses the current state.

Human or automated review can supply evidence and attention, but it does not
silently override a user-settled product or architecture decision.

## Apply corrections only within authority

When changes are authorized, apply supported corrections and other authorized
improvements, distinguishing required fixes from optional changes. Include
necessary in-scope consequences and preserve stable finding identities when the
feedback already has them.

Review the successor against the intended outcome and the behavior affected by
the correction or improvement. Do not broaden into unrelated cleanup merely
because a reviewer mentioned it.

External replies, comment resolution, publication, merge, and acceptance of
residual risk remain separately authorized effects.
