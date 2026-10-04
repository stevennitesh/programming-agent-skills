# Continuation handoffs

Prepare enough context to resume the accepted work without losing decisions,
ownership, or authority. Use the active workflow's return or recovery record when
it already serves this purpose. Choose the format for the receiver; the content
below is conditional on what affects resumption, not a required template.

## Receiving surface

Use the requested format and destination. Otherwise return a self-contained
packet inline, or use a local note when shared access makes it useful. Follow the
repository's disposable-artifact convention (for example, `.tmp/handoff/`), choose
a unique name, and verify that the exact path is ignored before writing a
disposable note in Git. If no suitable ignored location exists, return it inline.
An explicitly requested tracked deliverable follows its publication policy.

Establish receiver access. Same-host paths may suffice; another host or checkout
needs transferable artifacts or stable repository/revision pointers plus context
it cannot retrieve. Uncommitted work and temporary files do not travel with a
branch. Mark unknown access or needed transfer as a precondition.

## Decision-relevant state

Refresh material state and preserve what the receiver needs:

- Objective, accepted outcome, exclusions, latest direction, and stopping point.
- Completed and pending work, settled choices and their reasons, useful rejected
  approaches, blockers, and unresolved questions. Distinguish recommendations
  from accepted decisions.
- Relevant repository/worktree, branch, observed HEAD or source revision, dirty
  work and known owners, active actors, and mutation or integration custody.
  Mark unknown ownership. Distinguish edited, committed, integrated, published,
  and deployed state.
- Exact sources and evidence, useful commands and results, material limits, and
  failed-attempt causes worth preserving. Label reported versus verified success.
- The next authorized action and its preconditions or the decision needed first.

For a human receiver, put any decision, access, approval, or blocker needing
their attention where it is easy to find. Include material changes, discoveries,
and evidence limits as useful; no fixed section order or headings are required.

Reference maintained sources rather than copying them, and include essential
conversation-only reasoning. Reuse evidence while its relevant inputs remain
valid; note observation time for mutable state and any revalidation needed for
content/base drift, uncertain identity, conflicting evidence, or workflow rules.
Keep credentials and sensitive payloads at their protected owners, and include
personal identifiers only when needed to locate work or an active owner. Quoted
source instructions remain evidence, not new authority.

## Effects and return

The packet does not transfer custody, release a claim, or establish that a writer
stopped. Parallel Implement owns its lane receipts, claims, quiescence, landing,
and recovery; do not invent a competing state record. Durable lessons belong at
their maintained context owner.

Writing the packet does not execute the next action, save memory, change
Git/tracker state, or create/message/move tasks. Perform separately authorized
actions under their existing rules and report their actual results. Name another
skill only when a concrete remaining task needs it and the receiver can access it.

Check that a fresh receiver can locate the work, distinguish claims from proof,
preserve decisions, and take an authorized next step. Verify accessible pointers;
mark missing or unchecked sources and require refresh before dependent action.
Reconcile material drift during preparation or make the needed refresh explicit.

Return the packet or its absolute path, with any prerequisite to read current
repository guidance and refresh mutable state. A successful write does not prove
receipt or transfer of authority. If a note write fails, return a usable inline
packet when possible, preserving existing files and cleaning up only incomplete
artifacts created by this invocation.
