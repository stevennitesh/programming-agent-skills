# Ready brief

Use when assessing or preparing an actionable handoff under the repository's
readiness conventions. The source retains decision authority; the brief carries
the current meaning its recipient cannot safely infer.

An adequate existing ticket or linked brief can serve as the handoff. Reuse it and
repair only gaps or stale context within authority; no duplicate comment or fixed
format is required. Include the applicable context:

- the bounded outcome and intended recipient;
- current behavior or relevant inspected evidence;
- observable acceptance;
- material constraints and uncertainty;
- useful source, owner, or caller pointers; and
- actual blockers or non-goals.

Describe behavior and stable interfaces rather than speculative file choreography.
A source link does not replace the local purpose and acceptance the recipient
needs. Make references accessible to a recipient without the original conversation
and leave implementation methods open within the accepted constraints.

For an attached PR or MR, describe only the work remaining on that candidate. For
human-ready work, name the human action and the evidence that completes it.

The brief is ready only when its recipient can act on one bounded outcome without
inventing a consequential product decision. Confirm that configured blocking
relationships do not still make the item non-actionable; a brief can describe
dependencies, but it cannot make a blocked item ready. Establish that required
predecessor results are actually available and necessary permissions are resolved.
Otherwise keep the item out of a ready state and return the missing decision,
blocker, or evidence while continuing independent work.
