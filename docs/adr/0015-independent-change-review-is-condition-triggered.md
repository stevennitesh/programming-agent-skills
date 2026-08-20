# Independent Change Review Is Condition-Triggered

**Status**: superseded by ADR-0016

## Context

ADR-0013 made High-Assurance Review explicit-only but still required one
independent Change Review for every Implement and Parallel Implement candidate.
That universal gate adds coordination even when claim-matched proof, final diff
and state read-back, and Change Closure establish an ordinary change.

Independent review remains useful when an authority requires it, when a final
candidate recombines mutations from independent authors, or when proved
behavior still leaves a material cross-owner or irreversible acceptance
judgment that should not rest with its implementer alone. Review cannot replace
missing required proof.

## Decision

Ordinary implementation completes through claim-matched proof at a real caller
or observable boundary, final diff and repository-state read-back, Change
Closure, and honest reporting of material skipped proof and Residual Risk.

Invoke Change Review only when:

- the user or repository explicitly requires independent review;
- the final candidate contains mutations from two or more independent authors;
  or
- focused proof establishes behavior, but a material shared-contract or
  irreversible-migration acceptance judgment still warrants fresh independent
  judgment and Change Review is the lowest-burden way to obtain it.

Candidate size, PR or release packaging, novelty, one delegated edit, file
type, external input, generic or supported risk, security or production
adjacency, and reviewer availability do not activate review. Missing required
proof stops the work; it is not a review trigger or Residual Risk. An
untriggered branch creates no reviewer, packet, `N/A`, artifact, or explanation.

When review activates, Change Review remains read-only and judges one immutable
candidate. Supported facts expand ordinary candidate-scoped coverage only
within the accepted request and repository contracts. They do not authorize a
security assessment, security hardening, deployment, operations, SRE work, or a
specialist lane.

High-Assurance Review remains explicit-only. Security and production/SRE
specialist work likewise requires an explicit objective. Risk facts alone
select none of them.

This decision supersedes ADR-0013. ADR-0014 remains accepted.

## Consequences

- Implement and single-author Parallel Implement may complete without an
  independent reviewer when no trigger applies.
- Recombined independently authored mutations receive one final independent
  review after all writers are idle.
- The existing `ordinary-reviewer` and `integration-reviewer` profiles remain
  available and bind only an activated review branch.
- Review findings grant no mutation or successor-snapshot authority; the
  implementation caller retains repair and completion.
- The Pack Composition Baseline requires one revision-plus-one behavioral
  amendment. Historical evidence and machine identities remain unchanged.
