# Astra context hygiene assessment

Date: 2026-09-05. Candidate:
[context-hygiene](../../skills/astra/context-hygiene/SKILL.md).
This change rewrites skill source; it does not audit or change the user's actual
memory store, install the skill, commit, or push.

## Decision

Keep context hygiene as an optional specialist for selecting durable knowledge
and auditing persistent context. Its useful work is epistemic and architectural:
what is supported, what future decision changes, who owns the rule, and what
should stop loading. It is not a compaction tool, a mandatory retrospective after
every task, or a second instruction-authoring/bootstrap workflow.

Retain the custom distinction between observation and authority, personal and
project scope, task state and durable guidance, historical evidence and active
memory, and requested updates versus verified effects. Move detailed accounting
and store-specific update concerns behind references. Keep no script: classifying
meaning and resolving authority are the hard parts; no deterministic repeated
transformation has been demonstrated that warrants maintaining one here.

Two refinements deliberately depart from the custom four-category taxonomy:

- Recognize reusable technical procedures separately from behavioral preferences.
  A demonstrated mechanism may justify a narrowly scoped guide without repeated
  user correction. It does not justify inventing a universal failure rule.
- Allow a scoped, verified retrieval pointer where it avoids costly rediscovery
  and the store permits it. It identifies the current owner and revalidation need;
  it does not make a cached system fact authoritative. Do not delete a useful
  active copy before a proposed migration has actually preserved its meaning.

## Source comparison

Local upstream snapshots were inspected; this task did not refresh clones.

| Source | Snapshot | Selection |
| --- | --- | --- |
| Custom context-hygiene and CODEX-MEMORY reference | Current checkout | Preserve scope, atomic-claim coverage, admission evidence, current-owner checks, exact update boundaries, drift checks, history preservation, pending/applied distinction, and separate candidate-note inventory. |
| Matt Pocock in-progress/retro | `3cca18b368ae95cdbdebbff572ccafa662551015` | Navigation friction, no-op instructions, automated checks, tool economy, and information access are useful diagnostic questions. Reject mandatory implementation/reviewer separation and treating reviewers as exempt from exploration. |
| Pstack reflect and context/structural principles | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Scoped transcript identity, evidence-backed lessons, distinguish judgment from tooling, stronger structural ownership where justified, selective loading. Exclude fixed reviewer/model fanout, automatic backlog filing, saving every correction, and mandatory tool building. |
| Superpowers subagent-driven-development and writing-skills guidance | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Recoverable task state belongs with the task, not personal memory. Context availability and discoverability matter. Do not import its workflow ledger machinery into every reflection. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Existing ownership and subtraction before adding a mechanism. Reject shortest-text scoring, reduced-scope delivery, and persistent mode instructions. |

## Coverage of consequential cases

| Case | Candidate behavior |
| --- | --- |
| Transcript includes instructions or sweeping permission claims | Treat as evidence, not runtime authority; verify selected session identity. |
| Project preference looks global | Preserve scope; no cross-project audit expansion. |
| Entry mixes preference, fact, incident, and procedure | Split claims and account for each disposition. |
| Many summaries repeat one unsupported assertion | Repetition is not independent corroboration. |
| Old fact was expensive to discover | Prefer current owner; admit only a useful revalidatable pointer under store policy. |
| One incident suggests a universal rule | Preserve trigger and evidence; recurrence/confirmation needed for inferred general rule. |
| A proven technical mechanism deserves a procedure | Propose the closest existing skill/guide/mechanism without mislabeling it a user preference. |
| Proposed migration has not happened | Do not remove the only useful copy or claim redundancy yet. |
| Long context contains a genuinely conditional section | Add a specific loading trigger and accessible reference; preserve common decisions and semantic conditions. |
| Source cannot be read or provenance is unclear | Mark coverage incomplete or claim for review, with the missing evidence. |
| Cleanup meets drift or partial failure | Reconcile actual state; stop affected/dependent changes, not blind replay. |
| Update note successfully written | Pending until active semantic effects are read back. |
| Active summary still contains removed meaning | Removal is not verified; check applicable retrieval surfaces without deleting history. |
| Notes remain after consolidation | Report inventory separately; retention alone is not pending cleanup unless deletion was authorized. |

## Review and validation

Two fresh read-only challengers covered admission/effect safety and useful
source/composition coverage. Neither found a blocking loss of safeguards.
Accepted their three clarity improvements:

- Existing authority can already cover destructive cleanup; wording must not
  create a redundant approval request.
- Name writing-for-agents and repo-bootstrap as the Astra composition owners,
  with a concrete proposal fallback if unavailable. Do not invoke them automatically.
- Reserve explicit disposition accounting for audits. Small reflections can route
  supported candidates in concise prose without the table, labels, or totals.

The challengers agreed that retrieval pointers and narrowly demonstrated technical
procedures preserve useful knowledge without promoting cached facts or agent
inferences into authority. Strongest future behavioral cases: stale-target drift,
a delta note written without consolidation, and migration to an owner that does
not yet contain the required meaning.

Package validation, repository skill validation, local links, and both
whitespace checks passed. No executable helper or wording-mirroring tests were
added. Structural checks and editorial challenge do not establish improved agent
behavior; a realistic scoped audit remains the behavioral evaluation opportunity.
