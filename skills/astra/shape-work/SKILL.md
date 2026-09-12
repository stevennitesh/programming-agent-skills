---
name: shape-work
description: Clarify or stress-test an idea into an implementable outcome, capture a useful specification, or directly reconcile domain meaning, invariants, context relationships, and settled decisions. Use for shaping work or requested domain-record updates; exclude routine vocabulary lookup, straightforward implementation, and delivery-ticket decomposition.
---

# Shape work

Make consequential decisions clear enough to build the intended outcome, using
conversation, evidence, and a specification only when useful. Preserve the
requested scope; shaping alone does not authorize implementation.

For direct domain-modeling or settled-decision capture, follow
[Domain modeling](references/domain-modeling.md) without a feature interview.

## 1. Establish the outcome and known decisions

Identify the problem, intended beneficiary, desired outcome, and decisions already
made. Use the supplied conversation, brief, issue, or audit findings; inspect
decision-bearing references and relevant repository contracts. Distinguish settled
requirements, current implementation facts, recommendations, and assumptions.
Capture settled input without restarting an interview or seeking approval again.
Revisit only choices affected by new evidence. Assumptions and deferrals are not
accepted requirements.

Look up accessible facts instead of asking the user to retrieve them. When a
proposed solution depends on an existing capability, verify enough of its actual
behavior to avoid promising something it cannot do. Correct incidental factual
errors; surface contradictions that would change an accepted commitment.

## 2. Resolve the decisions that affect the outcome

When the mechanism is still open, check whether an existing capability or smaller
change achieves the intended outcome. Explain any meaningful loss or ceiling;
do not silently simplify accepted requirements.
Separate the required outcome from a proposed mechanism. When the choice matters,
compare genuinely different approaches, including no software change when credible;
investigate the assumption most likely to invalidate the choice before refining it.

Ask only about unresolved choices that materially affect behavior, scope,
constraints, acceptance, or tradeoffs, one question or a small independent group
at a time. Wait for answers before dependent questions or decisions; continue
useful independent work when available. Incorporate each answer without asking
permission to proceed or repeating unchanged questions. Once the necessary
choices are settled, continue to acceptance and capture within the requested scope.

Use concrete scenarios to challenge vague agreement. Explain a recommendation
and its decisive tradeoff when the evidence supports one, while eliciting
participant-held facts neutrally. Technical decisions within settled requirements
are yours to recommend and resolve within authorization; product priorities and
accepted meaning belong to their decision owner. Do not invent their answer.

When shaping establishes, changes, or exposes a conflict in domain terms,
invariants, responsibilities, or relationships, read
[Domain modeling](references/domain-modeling.md) and
reconcile relevant current meaning before building dependent decisions. Resolve
collisions in the conversation; accumulate useful record changes rather than
interrupting to write or seek approval after every answer.

For an unresolved architecture choice, use `$codebase-design` when available and
useful. For an empirical question, use `$prototype` or available evidence-gathering
tools within scope. These are methods, not installation prerequisites. Keep a
conclusion conditional when the necessary evidence or owner is unavailable.
Record what remains unknown, its impact, and what would resolve it.

Summarize a complex synthesis for review when it could conceal a material
misunderstanding; this does not reopen choices already made.

## 3. Make behavior and acceptance precise

Describe a representative caller journey from initiating input to observable
outcome. Specify materially different rejection, partial-success, or state behavior
when it affects the outcome. State what must remain true and what evidence could
distinguish success from a plausible wrong result. Avoid implementation recipes
unless a particular mechanism is itself a settled constraint.

Could two reasonable implementations satisfy the wording but produce materially
different outcomes? Resolve unintended ambiguity or identify the remaining
decision; preserve deliberate implementation freedom within accepted behavior.

For composed results, durable state, conflicting rules, or measured claims, read
[Acceptance meaning](references/acceptance-meaning.md). Preserve consequential
semantics without enumerating irrelevant cases. Keep unresolved choices visible;
do not fill gaps with plausible prose merely to make a specification look complete.

## 4. Capture only what future work needs

Assess whether settled decisions warrant a context update or ADR, using
[Domain modeling](references/domain-modeling.md) when they do. Context records
preserve durable meaning and invariants; ADRs preserve useful decision rationale;
specifications define what this work must deliver. Update the existing owner
rather than duplicating it. Apply changes within existing authority; otherwise
recommend the destination, concrete proposed change, and why future work needs it,
bundling any missing approval into one question. Do not create records merely to
complete a set, or block independent authorized work on optional documentation.

Keep a small outcome in the conversation when that is sufficient. Produce or
update a durable specification when requested or needed for multiple sessions,
delivery slices, or owners. Read [Durable decisions](references/durable-decisions.md)
when writing a spec or updating domain records.
Follow the repository's configured destination; a spec need not be a tracker
parent. External publication requires authority for that effect; a local draft
can still make progress.

A useful result contains the problem and outcome, scope and consequential
exclusions, settled behavior and constraints, acceptance, and material uncertainty.
Add source pointers and rationale that help a fresh agent preserve the decisions.
Omit empty sections and exhaustive user-story catalogs. Reuse the existing owner
of a decision rather than creating competing current documents.

## 5. Return or continue within scope

Do not label work ready when implementation would need to invent consequential
policy. If blocked, return the exact decisions or evidence still needed.

Once behavior is sufficiently settled, continue authorized implementation within
the active workflow's ownership and approval boundaries. Tickets are optional
unless requested or required by that workflow. Use
`$to-tickets` when the user requests ticketing, including a single ticket.
When durable delivery boundaries or coordination would benefit from tickets,
suggest that explicit next step; do not start it merely because it could help.
Neither a spec nor tickets are a prerequisite for ordinary coding. Creating
plans does not itself authorize implementation, publication, or delegation.
