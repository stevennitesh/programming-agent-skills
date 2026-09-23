---
name: writing-for-agents
description: Write or audit instructions another agent will execute, including skills, AGENTS.md, agent-facing guides or prompts, and continuation handoffs. Exclude product shaping and ordinary prose editing.
---

# Writing for agents

Write the minimum guidance that helps a capable agent make the intended decisions
with the context it will actually receive. Preserve the user's settled choices,
the document's authority, and any constraints the receiver cannot infer. For an
audit, return findings without editing.

## 1. Identify the receiver, authority, and outcome

Establish the receiving agent's task, baseline capabilities, available context,
and how this document reaches it. Read the relevant caller or pointer and the
source that owns the rules. Distinguish settled requirements and project facts
from recommendations, examples, and historical evidence.

Make the intended outcome, authorized effects, material constraints, and
completion condition clear. Prescribe a method or sequence when dependencies,
fragile operations, or an accepted workflow make that method consequential.
Otherwise leave valid implementation and reasoning strategies open.

Do not ask for narrated reasoning merely to make the instruction look rigorous.
Ask for observable evidence, a concise decision rationale, or an explicit
uncertainty when one is useful to judge the result.

For a worker assignment, deliver the bounded task, essential role and authority
boundaries, necessary context, acceptance, and expected return in its prompt or
an explicitly loaded source. Do not assume the worker inherits the caller's
context. Keep orchestration decisions with the caller.

When preparing a continuation handoff for another agent or fresh context, read
[Continuation handoffs](references/continuation-handoffs.md). That reference owns
the packet and its checks; writing a handoff does not execute the next step or
transfer authority.

When creating a skill or changing its discovery, packaging, or invocation
behavior, read [Skill authoring](references/skill-authoring.md).

When migrating instructions to another model or host, deciding whether a method
still earns its place, materially changing a skill's behavior, or claiming that
wording improves agent performance, read
[Behavior evaluation](references/behavior-evaluation.md).

## 2. Put information where the decision needs it

Keep information every applicable run needs in the main instruction. Put
substantial branch-specific detail behind a pointer that states when to read it.
If agents miss a reference, improve its trigger before copying the whole reference
into the always-loaded document.

Organize material for how it will be used: procedure when order is consequential,
reference when facts need lookup, and explanation when reasons or tradeoffs affect
judgment. Split content when different readers or branches need it at different
times, not to satisfy an arbitrary file-size target.

Give each rule one authoritative home and point to procedures owned elsewhere.
Prefer current code, configuration, command help, schemas, and maintained
documentation over copied mechanical facts unless the instruction adds a
convention, reason, expensive-to-discover fact, or required interpretation.

Before adding prose for a recurring mechanical invariant, ask whether a type,
schema, configuration constraint, lint rule, canonical helper, runtime check, or
small deterministic script can enforce it more reliably. Put the enforcement at
that owner and keep agent-facing prose only when it still carries decision
context, authority, rationale, recovery semantics, or a conditional pointer the
mechanism cannot express.

When changing an instruction's meaning, trigger, ownership, or authority, inspect
directly affected callers and competing current guidance. Reconcile useful
material and retire obsolete current pointers within scope. Keep historical
evidence distinguishable from instructions still in force.

For replacing specs or plans, follow
[Document reconciliation](../shape-work/references/document-reconciliation.md).

## 3. Write literal, decision-changing guidance

Put conditions and prerequisites before the actions they govern. Address the
executing reader directly and name other actors explicitly. Attach words such as
"only," "unless," and "after" to one clear obligation. Prefer positive target
behavior; use prohibitions for concrete boundaries or likely harmful
misinterpretations.

State what must be true when the work is complete. Prefer a precise completion
condition over extra intermediate steps that merely encourage diligence.

Use examples, templates, and exact output shapes when they remove meaningful
ambiguity or protect an easily omitted requirement. For conditional behavior,
name an observable trigger. For a hard boundary, state both the prohibited effect
and the permitted next action.

Preserve the distinction between requirements, recommendations, defaults, and
examples. Read each obligation as something a capable agent may enforce literally.
Do not turn a past incident, preferred technique, or plausible future concern into
a universal requirement.

Make every instruction earn its context:

- Does it change a likely decision for the intended receiver?
- Does it provide information or authority the receiver cannot otherwise obtain?
- Does it prevent a credible failure or preserve a required contract?
- Would removing it leave the intended behavior materially less reliable?

Correct advice that the intended receiver already follows reliably can still be
a no-op. Delete repeated defaults, generic exhortations, stale facts, defensive
scaffolding retained for earlier models, and procedural ceremony that does not
change the accepted outcome.

Do not prune project meaning, user-settled decisions, repository-specific
conventions, authorization, custody, effect boundaries, required acceptance
semantics, recovery contracts, or fragile ordering merely because they seem
obvious. Model capability cannot recover information or authority the receiver
was never given.

## 4. Check the receiving behavior

Read the result as a future agent with only the context it is expected to receive.
Check whether it can identify:

- when the guidance applies;
- what outcome and boundaries govern the task;
- what context or conditional reference it needs;
- what remains its judgment;
- what evidence matters; and
- when the requested work is complete.

Look for unintended behavior introduced by the instruction: unnecessary stops,
questions, delegation, artifacts, reviews, tests, context loading, or scope
expansion. Confirm that the user's settled choices and existing authorization
survived the edit.

For changed discovery or conditional guidance, trace at least one representative
applicable case and one realistic nearby case that should not activate it.
Confirm required guidance is encountered before the decision it governs without
loading unrelated procedures.

Check affected links, frontmatter, and other machine-read structure. For an
executable recipe, exercise the changed path when authorized and useful. Report
what was not verified.

Structural validity, editorial review, or a successful example does not establish
that wording improves agent behavior. Use
[Behavior evaluation](references/behavior-evaluation.md) when the requested claim
requires that evidence.

Finish when the intended receiver can act within its authority, reach the required
outcome with the context available to it, and recognize completion without
inventing missing policy. Report the material change and any consequential
verification gap concisely.
