# High-Assurance Review Synthesis

Status: current runtime summary.

Runtime authority is `skills/custom/high-assurance-review/`.

High-Assurance Review owns one explicitly user-selected fixed code candidate and
returns one terminal read-only decision through two fresh whole-candidate
Change Review passes. Typical candidates are the integrated result of a ticket
graph or an exact PR before merge. Both reviewers inspect behavior and
engineering quality with different primary emphasis. Before dispatch, the
coordinator resolves governing sources and identifies material handoffs affected
by the change. Both lanes independently inspect the actual representation
through its real consuming caller, reusing candidate-bound proof. The
coordinator verifies coverage, real-caller reach, and finding candidates against
the shared Finding Contract. The result names the reviewers and the
fresh-context and author-separation basis for the claimed independence.

No workflow selects High-Assurance Review automatically. The user owns its
invocation. PR presence, release status, and risk do not select it. The
coordinator retains read-only finding admission and terminal decision authority.
