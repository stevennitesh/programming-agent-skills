---
name: writing-for-agents
description: Write or audit a selected agent instruction, skill, or handoff. Exclude routine worker dispatch, repository-wide context work, and product shaping.
---

# Writing for agents

Make a selected instruction usable by its receiver: clear intent, necessary
context, effect boundaries, and recognizable completion, with freedom over
methods. An audit alone returns findings; apply separately authorized fixes within
scope. Routine worker dispatch uses its execution owner's contract and needs no
authoring phase.

Initial guidance and setup migration belong to [repo-bootstrap](../repo-bootstrap/SKILL.md);
maintenance across repository context belongs to [context-hygiene](../context-hygiene/SKILL.md).
This skill owns the content of the selected artifact, not those wider workflows.

## Write for the actual receiver

Establish what the receiver can see or retrieve. Preserve the accepted outcome,
decisions, constraints, authorized effects, recovery boundaries, and acceptance.
Separate requirements from defaults, proposals, examples, and history; do not
invent policy to fill a consequential gap.

Supply essential non-inferable facts and accessible source pointers rather than
unrelated conversation history. For assignments, include scope, write ownership,
required proof, and expected return without assuming inherited context. Leave
orchestration with its execution owner.

Let the receiver choose investigation, tools, and implementation methods. Prescribe
order or technique only for a governing requirement, dependency, or fragile
operation. Use concrete examples for consequential ambiguity and fixed output
shapes only when a consumer needs them. Request useful evidence and uncertainty,
not narrated reasoning or generic exhortations.

## Keep instructions lean and owned

Put shared requirements at their owner and conditional detail behind a clear
trigger. Reference changing facts and procedures instead of copying them; use
existing mechanical enforcement where appropriate. Remove repeated defaults,
generic advice, and unnecessary scaffolding without losing authority, custody,
acceptance, recovery, or necessary ordering. One incident alone does not justify
a universal rule.

Reconcile directly affected readers and competing guidance when meaning,
discovery, or authority changes. Preserve history. For displaced or conflicting
accepted sources, use [Document reconciliation](../shape-work/references/document-reconciliation.md);
that does not require a wider context audit.

Read the relevant branch only:

- [Skill authoring](references/skill-authoring.md): discovery, invocation,
  packaging, or model/host adaptation.
- [Long-running instructions](references/long-running-instructions.md): steering,
  continuation, and durable progress requirements.
- [Continuation handoffs](references/continuation-handoffs.md): a fresh receiver
  resuming accepted work.
- [Behavior evaluation](references/behavior-evaluation.md): consequential method
  changes or claims of effectiveness.

Read the result with the receiver's expected context. Check retained obligations,
unintended scope or approval stops, links, and machine-read structure; consider an
applicable request and near-miss when discovery changes. Exercise executable
instructions when useful and authorized. Package and editorial checks do not
prove better agent behavior. Return the artifact or findings and material limits.
