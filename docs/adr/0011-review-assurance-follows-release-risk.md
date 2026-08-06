# Review Assurance Follows Release Risk, Not PR Container

The review family previously routed every local pull request to the
high-assurance path. That made the transport container a proxy for assurance
need, sent ordinary PRs through fresh-context review, and let optional
improvement advisories compete with the release gate. Implement, Parallel
Implement, Change Review, High-Assurance Review, and Skill Router all depend
on one stable routing boundary.

**Status**: superseded by ADR-0013

`$change-review` owns every Change review candidate, including an ordinary PR.
It pins one snapshot, judges Spec and Standards separately through the shared
Finding Contract, and returns coverage plus one gate decision.

`$high-assurance-review` owns every High-assurance review candidate: a release
candidate or a diff or PR with a Supported high-risk trigger. A trigger
requires a changed surface, supported scenario, reachable behavior or failure
path, and concrete impact. PR existence, diff or repository size, severity
labels, and hypothetical edge cases do not qualify.

High-Assurance Review uses two fresh core lanes, at most one specialist for a
frozen supported trigger, and coordinator-only finding admission. Both core
lanes are required for a passing decision; the coordinator never substitutes
for a missing reviewer. Risk remains cross-cutting rather than becoming a third
review axis.

Review gates return admitted findings and residual risk only. Non-defect
improvement opportunities belong to Audit Codebase or Simplify Code; the shared
Advisory Contract is retired. Implementation callers choose exactly one review
route; review skills return route mismatches to those callers and never route to
each other. Implementation callers retain Repair, mutation, Lock, and
successor-snapshot authority.

## Considered Options

- Route every PR to High-Assurance Review. Rejected because PR packaging does
  not establish release or supported-risk pressure and adds unnecessary
  review coordination.
- Use one review skill that chooses reviewer fanout internally. Rejected
  because ordinary judgment and coordinator-only convergence have different
  authority, capacity, and terminal contracts.
- Keep an optional advisory lane in review gates. Rejected because opportunity
  discovery is unbounded, does not affect release acceptance, and already has
  dedicated owners.

## Consequences

- Review callers and Skill Router select by release state and supported risk,
  not PR existence.
- The shared Finding Contract owns classification and risk admission for both
  review skills.
- Historical review synthesis and validation remain evidence for their exact
  prior bytes; current amendment notes identify the new runtime boundary.
- Revision 3 of the `FCE-20260727-01` Pack Composition Contract records the
  current names and release-or-supported-risk route. Earlier slices remain
  historical evidence for their exact prior identities.
- Exact wording efficacy still requires Behavioral Proof. Structural and
  deterministic tests establish contract shape and compatibility, not
  fresh-context steering quality.
