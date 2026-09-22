# Durable decisions

Read when a specification or domain update is useful. Capture decisions for a
future reader, not a transcript of the conversation.

## Choose the owner

Follow repository guidance for specifications, domain records, and decision
records when present. Prefer an existing owner. When no authoritative destination
is available or writable, keep a local draft or state the proposed destination
rather than silently changing repository conventions.

For domain meaning or ADR rationale, use
[Domain modeling](domain-modeling.md). For replacing or retiring competing current
documents, use [Document reconciliation](document-reconciliation.md).

## Preserve the contract, not the process

Capture only what future work needs to preserve the accepted result:

- intended outcome and relevant purpose;
- scope and consequential constraints;
- settled behavior and accepted meaning;
- acceptance that distinguishes material failure; and
- material uncertainty or unresolved owner-held decisions.

Keep proposed implementation mechanisms distinct from accepted requirements.
Preserve rationale only when it can change later decisions. Link existing owners
instead of copying their contents.

A small schema, example, or code pointer can express a settled rule when it is
more precise than prose. Do not freeze speculative file lists, implementation
sequences, test ownership, model settings, worker state, or orchestration mechanics
into the durable contract.

When coordinated delivery also needs a plan, keep accepted commitments distinct
from the adaptable delivery approach. Execution workflows own worker assignments,
custody, checkpoints, repair accounting, and run state.

Read the result as a fresh implementer. They should be able to recover the intended
outcome and acceptance without inventing consequential policy.

## Publish only within authority

A requested local specification or domain update may be written under repository
rules. External tracker or publication effects require authority for that target.

Reuse an existing matching artifact when possible. Do not overwrite ambiguously
owned or divergent content merely to create a canonical-looking document.

After an authorized write, read back the intended content and identity when the
effect is consequential. If creation or update has an uncertain result, inspect
actual state before retrying.

Publication does not imply ticketing, readiness, implementation, delegation,
commit, push, or deployment authority.
