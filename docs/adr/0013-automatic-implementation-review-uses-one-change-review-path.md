# Automatic Implementation Review Uses One Change Review Path

**Status**: superseded by ADR-0015

## Context

Implementation previously selected Change Review for ordinary candidates and
High-Assurance Review for release or supported-risk candidates. In practice,
that routing decision added coordination before judgment and made the presence
of risk select a second review system. Supported risk changes what a reviewer
must inspect; it does not require a different owner or terminal contract.

The user requires a workflow that can choose the best efficient solution for
the use case, simplify it to the smallest integrated shape, and avoid automatic
ceremony. Independent review remains valuable, but automatic reviewer fanout
does not.

## Decision

Every Implement candidate uses one fresh `ordinary-reviewer` through Change
Review with the Runtime Profiles Sol/high binding. Every final integrated
Parallel Implement candidate uses one fresh `integration-reviewer` through
Change Review with the Sol/xhigh binding. Supported risk changes applicable
coverage and checks inside Change Review rather than selecting another skill.

High-Assurance Review is explicit-only. It runs only when a user names it or
approves one exact caller-owned invocation packet that names it. Implement,
Parallel Implement, Change Review, and Skill Router neither invoke nor
recommend it automatically.

## Considered Options

- Keep automatic risk-based routing. Rejected because the routing ceremony is
  independent of the actual finding work and can block an otherwise reviewable
  candidate.
- Remove independent review. Rejected because a fresh fixed-snapshot judgment
  catches integration, proof, and Change Closure defects without requiring a
  second implementation workflow.
- Embed optional reviewer fanout inside Change Review. Rejected because it
  recreates implicit High Assurance under another name.

## Consequences

- Change Review accepts ordinary, release, and supported-risk implementation
  candidates and scales coverage to supported facts.
- High-Assurance Review retains its two-core-reviewer protocol for explicit use
  without becoming an automatic escalation.
- Runtime Profiles owns the two automatic review bindings; delivery skills own
  which of those profiles applies.
- ADR-0011 is superseded. Its historical rationale remains evidence for the
  earlier two-route policy.
