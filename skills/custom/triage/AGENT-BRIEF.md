# Ready briefs

Write a brief only for work moving to `ready-for-agent` or `ready-for-human`.
The source retains decision authority. The brief carries enough current meaning
for its recipient to start without inventing product intent.

Describe behavior and stable interfaces rather than file choreography. Current
owner or entry-path pointers are useful evidence; line numbers and speculative
file lists are not.

Include:

- the bounded outcome and recipient;
- current behavior, inspected evidence, and material uncertainty;
- observable acceptance;
- material source, owner, or caller pointers; and
- non-goals and actual blockers.

For an attached PR or MR, describe only the work left on the existing diff. For
human-ready work, name the human act and its completion evidence. Add interface,
state, migration, compatibility, security, recovery, or proof detail only when
the request makes it material.

The brief is ready when its recipient can act on one bounded outcome without a
new product decision. Otherwise keep the item out of a ready state and report
the missing decision or evidence.
