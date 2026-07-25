---
name: to-spec
description: Explicitly turn one named settled source into one verified durable parent specification; exclude shaping, ticket slicing, implementation, and delivery.
---

# To Spec

Turn one identity-bearing source with settled commitment authority into one
durable, verified parent specification in the configured issue tracker. The
parent owns intent for later implementation slicing. A disposable local draft
may support synthesis, but only a publication read-back makes the tracker
packet authoritative.

## Ownership

The user and accepted source own outcome, commitments, acceptance, scope,
exclusions, supported behavior and states, public and data contracts, security
and privacy posture, compatibility, migration, rollback, and tradeoffs.
Repository domain documents and ADRs own accepted language and durable
decisions; consume them without changing domain truth.

`docs/agents/issue-tracker.md` owns tracker transport, packet location,
relationships, and Mutation read-back. `docs/agents/triage-labels.md` owns
role-to-label mapping. Load `$codebase-design` only when settled module,
interface, seam, adapter, leverage, depth, locality, or caller-facing proof
vocabulary is needed; retain specification decisions and completion here.

This skill owns source coverage, synthesis, the disposable draft, frozen
publication packet, one authorized create or exact reuse, verification,
failure Return, and completion. `$to-tickets` owns implementation slicing and
Ready-for-agent children. `$repo-bootstrap` owns setup repair.

## Admit

Begin only on a direct explicit request for one parent specification from one
named source in one target repository. Accept a direct settled packet or an
exact verified return from one allowed caller: a `Confirmed`
`$grill-with-docs` packet with its current Domain Delta; a closed Wayfinder map
whose destination is settled parent-spec source; a verified selected
improvement routed as specification-ready; or a verified audit finding or
cohesive cluster with fixed expectation and evidence. Preserve caller payload
identities, the intact confirmed packet and Domain Delta, and Wayfinder
resolution pointers.

Before drafting for publication, read the target `AGENTS.md` and its routed
tracker, label, domain, and engineering contracts. Verify create, inspect,
relationship, and complete read-back operations. If any required surface is
missing or incompatible, return `setup-precondition` with the missing surface,
observed and preserved state, and one unstarted `$repo-bootstrap`
recommendation.

Read the complete source and every decision-bearing pointer, bind their exact
identities, and require source-owned outcome, scope, acceptance, supported
behavior, applicable contracts, and material choices to be settled or
explicitly deferred by their owner. A caller return never waives sufficiency.
On missing access, identity, authority, acceptance, supported behavior, an ADR
conflict, or another ambiguous or contradictory source fact, return
`source-gap` naming the field, owner, inspected evidence, and re-entry
condition; make no tracker mutation.

Inspect the complete relevant tracker state before creation. Classify verified
absence, exact existing equality, divergence, and unknown state. Divergent,
similar, stale, claimed, or indeterminate state returns
`existing-state-conflict` with candidate identities, observed difference or
uncertainty, and the smallest needed authority; do not create or update.

## Synthesize

Build one title and parent body that account for:

- outcome and Source Trace with exact source identities;
- in-scope commitments, exclusions, non-goals, and owner-bounded deferrals;
- observable behavior, acceptance, supported paths, states, transitions,
  edge cases, and failures;
- applicable public interfaces, caller obligations, data contracts, ordering,
  and errors;
- applicable security, privacy, permissions, trust, and irreversible-state
  constraints;
- applicable compatibility, migration, rollback, and cutover obligations;
- accepted domain terms, governing ADRs, and surfaced conflicts;
- proof seams, proof lanes, and evidence required for acceptance; and
- risks, residual gaps, and constraints needed by later slicing.

Test each listed aspect family against source-visible triggers. Include every
applicable obligation and omit empty or ceremonial sections for irrelevant
families; never compress, relabel, or discard source-required content merely
to shorten the packet.

Use headings that fit the source. Map every in-scope commitment to a body
passage or acceptance criterion, and map every specification commitment back
to its exact authority. A deferral names its owner and boundary. Reject an
unresolved material choice, orphan, contradiction, vague or unverifiable
acceptance, invented role, child implementation ticket, or parent
Ready-for-agent state with `source-gap` before publication.

## Freeze

After source and coverage gates pass, write only
`.tmp/to-spec/<source-slug>.md`. Read back its exact bytes, correct synthesis
defects, and freeze the source identity, title, body, packet digest, applicable
source-authorized role operations, and intended tracker transition. Confirm
that the explicit invocation authorizes exactly that frozen one-parent
operation. A changed packet, ambiguous target, unsafe draft path, or missing
mutation authority returns `existing-state-conflict` with the exact authority
needed and no tracker mutation.

## Publish

Reuse only an existing parent whose complete normalized packet and applicable
state are exact. Otherwise create once, and only after verified absence.
Immediately refetch the unique create before applying only source-authorized,
applicable metadata through mapped label strings. Never invent a label,
category, or parent Ready-for-agent state.

After every transition, refetch the complete affected parent state and compare
title, body, comments, roles, labels, assignee, state, open or closed status,
relationships, and affected frontier with the frozen plan. Stop further
mutation on the first failed, partial, stale, mismatched, or indeterminate
operation. Return `publication-recovery` with the frozen packet identity,
applied and failed operations, observed tracker state, preserved draft, and
safest tracker-owned recovery action. Never repeat an indeterminate create.

Delete the draft only after verified new publication or exact reuse. Preserve
it with its exact identity whenever recovery evidence remains necessary.

## Return

Return exactly one status:

- `setup-precondition`: missing or incompatible configured setup, its observed
  and preserved state, and one unstarted `$repo-bootstrap` recommendation;
- `source-gap`: the exact affected field, owner, inspected evidence, re-entry
  condition, and unchanged tracker state;
- `existing-state-conflict`: candidate identities, observed difference or
  uncertainty, and the smallest authority needed, with no create or update;
- `publication-recovery`: frozen packet identity, applied and failed
  operations, observed state, preserved draft, and safest recovery action; or
- `ready-spec`: source identity, verified parent pointer and identity,
  publication or reuse proof, residual gaps, and one unstarted `$to-tickets`
  recommendation.

## Completion

Complete only on `ready-spec` when source authority, bidirectional commitment
coverage, the parent packet, applicable roles and state, publication or exact
reuse, complete read-back, and truthful draft disposition all verify;
unrelated state is preserved; one next recommendation is returned; and no
successor starts.

Never shape an unsettled request, research, run a design investigation, mutate
domain truth, approve an ADR, slice tickets, triage, implement, review,
install, deliver through Git, or execute downstream work. Change no source,
domain, code, child-ticket, Git index, `HEAD`, remote, installation, or
unrelated worktree state. Stop after the first supported Return.
