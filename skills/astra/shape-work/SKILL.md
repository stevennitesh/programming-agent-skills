---
name: shape-work
description: Clarify or stress-test an idea into an implementable outcome, capture a useful specification, or directly reconcile domain meaning, invariants, context relationships, and settled decisions. Use for shaping work or requested domain-record updates; exclude routine vocabulary lookup, straightforward implementation, and delivery-ticket decomposition.
---

# Shape work

Make the important decisions clear enough to build the intended outcome. Combine
conversation, evidence, and optional specification without requiring separate
interview and transcription stages. Preserve the user's chosen scope: a shaping
request ends with understanding; a request to shape and implement may continue
once its consequential decisions are settled.

For a direct domain-modeling or settled-decision capture request, read
[Domain modeling](references/domain-modeling.md) and follow that path directly.
It can return a clarified distinction, verified record update, no change, or
precise unresolved question without a feature specification or implementation
handoff. Do not reopen settled meaning merely to run the interview below.

## 1. Establish the outcome and known decisions

Identify the problem, intended beneficiary, desired outcome, and decisions already
made. Use the supplied conversation, brief, issue, or audit findings; inspect
decision-bearing references and relevant repository contracts. Distinguish settled
requirements, current implementation facts, recommendations, and assumptions.
Do not restart an interview when the user asks to capture already-settled work.

Look up accessible facts instead of asking the user to retrieve them. When a
proposed solution depends on an existing capability, verify enough of its actual
behavior to avoid promising something it cannot do. Correct incidental factual
errors; surface contradictions that would change an accepted commitment.

## 2. Resolve the decisions that affect the outcome

When the mechanism is still open, check whether an existing capability or smaller
change achieves the intended outcome. Explain any meaningful loss or ceiling;
do not silently simplify accepted requirements or reopen an explicit choice.
Separate the required outcome from a proposed mechanism. When the choice matters,
compare genuinely different approaches, including no software change when credible;
investigate the assumption most likely to invalidate the choice before refining it.

Ask about choices whose answers could materially change behavior, scope, a
constraint, acceptance, or a consequential tradeoff. Work on decisions whose
prerequisites are known; an unresolved branch need not block independent work.
Several related decisions can belong to one conversation. Ask the most useful
question first, or a small group of independent questions when that is easier to
answer. Do not dump every conceivable question or repeat an unchanged one.

Use concrete scenarios to challenge vague agreement. Explain a recommendation
and its decisive tradeoff when the evidence supports one, while eliciting
participant-held facts neutrally. Technical decisions within settled requirements
are yours to recommend and resolve within authorization; product priorities and
accepted meaning belong to their decision owner. Do not invent their answer.

When a term, invariant, or relationship changes or conflicts with current domain
meaning, read [Domain modeling](references/domain-modeling.md) and resolve the
collision before building dependent decisions. Clarifying meaning does not require
writing a record after every answer.

For an unresolved architecture choice, use `$codebase-design` when available and
useful. For an empirical question, use `$prototype` or available evidence-gathering
tools within scope. These are methods, not installation prerequisites. Keep a
conclusion conditional when the necessary evidence or owner is unavailable.
Record what remains unknown, its impact, and what would resolve it.

An explicit choice settles that choice. Summarize a complex synthesis for review
when it could conceal a material misunderstanding; do not require another approval
for a decision already made. A deferral is not a decision, and an assumption is
not an accepted requirement. Revisit only decisions affected by new evidence.

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

Keep a small outcome in the conversation when that is sufficient. Produce or
update a durable specification when requested or needed for multiple sessions,
delivery slices, or owners. Read [Durable decisions](references/durable-decisions.md)
when writing a spec or updating domain records.
For a domain distinction arising during shaping, also read
[Domain modeling](references/domain-modeling.md) before reconciling its record.
Follow the repository's configured destination; a spec need not be a tracker
parent. External publication requires
authority for that effect, while a local draft can still make progress.

A useful result contains the problem and outcome, scope and consequential
exclusions, settled behavior and constraints, acceptance, and material uncertainty.
Add source pointers and rationale that help a fresh agent preserve the decisions.
Omit empty sections and exhaustive user-story catalogs. Reuse the existing owner
of a decision rather than creating competing current documents.

## 5. Return or continue within scope

Return an implementable outcome, a durable spec when useful, or the exact decisions
and evidence still needed. Distinguish confirmed choices from proposals. Do not
label work ready when implementation would need to invent consequential policy.

For one coherent outcome, authorized implementation can proceed directly. Use
`$to-tickets` when the user requests ticketing, including a single ticket.
When durable delivery boundaries or coordination would benefit from tickets,
suggest that explicit next step; do not start it merely because it could help.
Neither a spec nor tickets are a prerequisite for ordinary coding. Creating
plans does not itself authorize implementation, publication, or delegation.
