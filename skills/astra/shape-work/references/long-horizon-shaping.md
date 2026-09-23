# Long-horizon shaping

Read when the destination is settled but the consequential decision space is too
large, dependent, or uncertain to settle reliably in one shaping pass or context.

This reference owns the low-resolution decision map. It does not require a tracker,
one decision per session, or a fixed workflow for resolving each question.

## Keep one destination and four unresolved states

State the destination: what must be true when shaping is complete.

Maintain only the decision context needed to advance toward it:

- **frontier:** a consequential question is precise and its prerequisites are
  settled, so it can be decided now;
- **blocked:** the question is precise but depends on unresolved evidence,
  authority, or another decision;
- **not yet specified:** an in-scope area of uncertainty is known, but the
  question itself cannot yet be stated precisely without guessing; and
- **out of scope:** the matter is deliberately outside this destination.

Keep settled decisions separately with enough rationale to prevent reopening them.
Do not turn "not yet specified" areas into premature tickets or invented questions.

## Advance the visible frontier

Resolve frontier decisions that materially unlock blocked work or make uncertain
areas precise. Use the main skill's existing research, prototype, domain, or
architecture routes when their evidence is actually needed.

After each material decision, recompute the map: newly precise uncertainty can
move onto the frontier or become blocked; invalidated questions can disappear;
newly excluded work moves out of scope. Preserve dependency direction instead of
asking questions whose premises are still unsettled.

Persist the map only when later sessions or decision owners would otherwise lose
the current destination, settled decisions, or unresolved-state distinctions.

Finish this branch when implementation can proceed without inventing a
consequential decision. If evidence or authority prevents that, return the exact
blocked questions and what would make them decidable.
