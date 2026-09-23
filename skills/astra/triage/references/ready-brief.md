# Ready brief

Use only when an intake item is moving to `ready-for-agent` or
`ready-for-human`. The source retains decision authority; the brief carries the
minimum current meaning its recipient cannot safely infer.

Include:

- the bounded outcome and intended recipient;
- current behavior or relevant inspected evidence;
- observable acceptance;
- material constraints and uncertainty;
- useful source, owner, or caller pointers; and
- actual blockers or non-goals.

Describe behavior and stable interfaces rather than speculative file choreography.
A source link does not replace the local purpose and acceptance the recipient
needs.

For an attached PR or MR, describe only the work remaining on that candidate. For
human-ready work, name the human action and the evidence that completes it.

The brief is ready only when its recipient can act on one bounded outcome without
inventing a consequential product decision. Confirm that configured blocking
relationships do not still make the item non-actionable; a brief can describe
dependencies, but it cannot make a blocked item ready. Otherwise keep the item out
of a ready state and return the missing decision, blocker, or evidence.
