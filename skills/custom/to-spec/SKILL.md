---
name: to-spec
description: Explicitly turn one settled source into a verified durable parent specification when several slices, multi-session coordination, or a lasting decision boundary justify it. Return one bounded item to Implement when a spec would add no value.
---

# To Spec

Publish one durable parent decision contract from settled source. Record what
was decided without reopening the decision, planning implementation, or
starting downstream work.

## Admit

Accept one identity-bearing settled source: a direct packet, a confirmed Grill
With Docs result with its current domain result, a read-back closed
Wayfinder map whose delivered closing evidence satisfies its closing condition,
or a verified Audit candidate with settled direction and boundaries.

Use To Spec only when a parent contract is useful across several delivery
slices or sessions, for durable coordination, or as a lasting decision
boundary. If the source already defines one bounded implementation with enough
accepted behavior and evidence to implement and verify it, return `not needed`
with the exact source and recommend unstarted `$implement`. Create nothing.

The source and its owners retain purpose, outcome, scope, exclusions,
commitments, acceptance, public and data contracts, security and privacy
posture, compatibility, migration, and tradeoffs. If a material decision,
authority, acceptance fact, or source identity is missing, contradictory, or
inaccessible, return the exact gap, its owner, inspected evidence, and re-entry
condition. Do not choose a resolver or make the missing decision.

## Read

Read the repository instructions, complete source, every decision-bearing
pointer it names, and only the routed domain records, ADRs, and current-state
material needed to preserve the source faithfully. Use the project's own
language.

Treat cited code and configuration as evidence, not as permission for a new
repository survey or architecture choice. If direct evidence corrects an
incidental current-state statement without changing a commitment, record the
correction and pointer in the Source Trace. If it changes a commitment, return
the contradiction to its owner.

## Write

Freeze one title, body, and intended parent state that a fresh agent can use
without inventing a decision. Include, when material:

- source identity and owners;
- problem, outcome, scope, and exclusions;
- settled behavior, decisions, constraints, and materially different
  scenarios;
- caller-visible interfaces, authoritative data shapes and invariants, and
  state or failure behavior;
- trust-boundary, security, privacy, compatibility, migration, cutover,
  rollback, or removal obligations;
- observable acceptance, the cheapest credible evidence authority, and honest
  residual uncertainty;
- deferrals, risks, and the downstream boundary.

Omit empty sections. Trace every material commitment to source authority. Use
a detailed crosswalk only for conflicting or multi-owner inputs. Cover states
only where behavior materially differs. At an external or trust boundary,
state the authoritative representation and observable invalid-input behavior;
do not prescribe redundant internal validation.

When accepted behavior spans several stages, include one representative
ordinary caller journey from initiating input to terminal caller-visible
outcome. For durable state on that journey, state what persists, what produces
it, which ordinary caller consumes it, how it affects that caller, and the
observable outcome.

When behavior retries, escalates, or gathers additional evidence, define each
reachable terminal outcome whose caller-visible behavior materially differs.
Include continued disagreement or insufficient evidence after the declared
limit, exhaustion, and failure when those are terminal outcomes. When
escalation materially changes a request profile, state the initial and
escalated profiles and their observable limits or effects.

When the accepted contract defines an identity or duplicate field as derived
from authoritative content, name the authoritative representation and require
derivation from it. If input can supply both, define the observable outcome for
contradictory values; do not silently reconcile them.

When a caller-visible interface combines independently requested items, state
whether missing, unsupported, or invalid state is item-local or rejects the
whole request. When typed or provenance-bearing results have materially
different empty, partial, reported, or derived states, name the authoritative
schema, require those states to remain type-compatible, and define what each
contribution-level identity or status describes. Name any governing version
identity and the observable changes that advance it.

Paths may support a source claim, but ticket slices, expected writes, concrete
commands, test ownership, dependency order, and implementation technique stay
downstream. Include code only when a source-authorized prototype fragment is
itself the clearest settled contract.

## Publish

Read `docs/agents/issue-tracker.md` only after the durable-parent branch wins.
Verify the required inspect, create, and read-back routes. If setup is missing
or incompatible, leave state unchanged, recommend `$repo-bootstrap`, and stop.

Inspect the intended parent target. Reuse only when exactly one parent matches
the frozen title, body, and intended state. Create only from verified absence
and only with authority for that parent. Multiple matches, divergent state, or
unknown state returns the observed identities and the smallest source or
authority change needed. Do not overwrite or reconcile implicitly.

Perform at most one parent create. Create no children, labels, source or domain
changes, code, Git state, installation state, or downstream work. Read the
durable parent back. Require one returned identity and pointer, and verify its
title, body, and state against the frozen expectations. If publication fails,
is partial, or remains unknown, report the input and observed durable state
with the safest recovery. Never retry an indeterminate create blindly.

Return `ready spec` with the durable pointer, exact source identity, verified
publication or reuse, and material residual gaps. Recommend unstarted
`$to-tickets` when several valuable implementation slices or durable tracker
coordination remain; otherwise recommend unstarted `$implement`. Invoke
neither.

## Completion

Complete through either branch: `not needed` returns the exact bounded source,
performs no mutation, and leaves `$implement` unstarted; a published or reused
parent preserves every material source commitment, lets a fresh agent recover
the same scope and caller-visible contract without inventing a decision, was
read back from durable state, and starts no downstream work.
