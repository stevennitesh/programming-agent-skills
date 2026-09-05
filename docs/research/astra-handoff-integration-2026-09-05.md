# Handoff integration into Astra writing-for-agents

Date: 2026-09-05. Assessment and validation record, not runtime instructions.

## Decision and composition

Integrate handoff authoring into
[writing-for-agents](../../skills/astra/writing-for-agents/SKILL.md) through a
[conditional continuation reference](../../skills/astra/writing-for-agents/references/continuation-handoffs.md).
No standalone Astra handoff skill or legacy route is needed. The entry description
now includes continuation handoffs and excludes app task movement/creation.
Ordinary progress reports do not load the reference.

Writing-for-agents owns the packet's meaning and presentation. Parallel Implement
continues to own claims, receipts, actor quiescence, custody, and recovery; context
hygiene owns assessment of durable lessons. A written packet does not enact a
transfer, start work, create a task, or save a memory. Separate explicit requests
retain their existing authority instead of requiring repetitive approvals.

## Custom parity and changes

The custom handoff skill supplied objective/boundary, accepted decisions, pending
work, exact identities, dirty ownership, authority, evidence pointers, drift
checks, and one safe next action. All remain, conditional on their relevance.
The cold-receiver check and protection against overwriting or falsely declaring
an incomplete packet usable also remain.

Deliberate changes:

- Support receivers on another host or checkout. Uncommitted work and temporary
  evidence do not travel with a branch; state missing transfers as preconditions.
- Permit an inline packet when a local note is unnecessary or no ignored scratch
  destination exists. Do not require repo-bootstrap just to summarize context.
- Follow a user-selected destination; a requested tracked handoff follows the
  repository's publication policy. Default disposable notes must be ignored.
- Preserve conversation-only reasoning that durable pointers cannot recover.
- Distinguish reported, checked, committed, integrated, and published outcomes.
- Remove hardcoded host compaction commands and mandatory file-only delivery.

## Upstream ideas

Compared existing local snapshots; no fetch was performed for this task.

| Source | Revision | Selection |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | `skills/productivity/handoff/SKILL.md`: preserve focus, reference existing artifacts, redact sensitive material. Exclude mandatory OS-temp storage and suggested-skills list. |
| Pstack / cursor-plugins | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Pstack's context-window principle favors selective context. The adjacent orchestrate plugin's `references/handoffs.md` adds downstream access/relay, partial failure records, and useful deviations. Reject treating worker claims as verified fact, unsanitized forwarding, automatic retries, and its planner protocol. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `writing-plans/SKILL.md` execution handoff confirms that next execution choices can matter. No automatic execution menu or required subskill is imported: describe only a concrete applicable next route. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | No handoff-specific guidance found in the skill scan. General simplification adds no rule beyond writing-for-agents' existing pruning method. |

## Verification scope

Two fresh-context reviewers independently challenge custom/evidence/access parity
and composition/authority/upstream omissions. Review targets remain frozen during
review. Their tabletop scenarios cover a cross-host receiver with uncommitted work,
private logs, conversation-only decisions, and stale proof; and an active campaign
with uncertain writer liveness, changed spec, retained receipts, and no ignored
scratch destination. Both reviewers passed with no actionable findings: the first
confirmed that inaccessible evidence, conversation-only meaning, dirty work, and
old proof remain explicit; the second confirmed that actor liveness, custody,
receipts, and memory stay with their current owners. Root clarified that the
scratch-directory example is illustrative, not a pack-wide path requirement.

The package validator, repository skill validator, and all 10 focused tests passed
on the initial candidate. These establish structure and existing pack compatibility,
not superior continuation behavior. The tabletop probes are document interpretation
checks, not independent end-to-end execution experiments. No real task, campaign,
Git state, tracker, or installed global skill was changed by this integration.
