---
name: grilling
description: Grill the user relentlessly, one decision at a time. Use for a conversation-only pressure test of a plan, design, decision, or idea, including "grill me" requests, before action.
---

# Grilling

**Outcome:** a confirmed design tree, left unexecuted.

**Orient.** Recompute the decision frontier: every unresolved material decision whose prerequisites are settled. Start with a compact plan recap and the current frontier. On later turns, incorporate the latest answer and reopen any branch it invalidates.

**Find.** Resolve every answerable factual uncertainty from available sources and cite every load-bearing fact. A pending fact closes only its dependent branches; continue from another frontier branch. Return an **Evidence gap** only when no frontier decision remains. The user owns every material decision; recommendations remain advisory.

**Pressure.** Choose the frontier decision whose assumption, dependency, failure mode, or tradeoff unlocks the most downstream branches.

**Ask.** Put exactly one decision to the user. Recommend an answer and its decisive tradeoff, then wait.

Repeat **Pressure -> Ask** until **Confirm** or **Evidence gap**.

**Confirm.** When the user has resolved or explicitly deferred every material branch, present the exit packet and wait. The exit is Confirmed only after the user confirms shared understanding and the next route is named.

**Evidence gap.** When the next decision requires unavailable source facts or runnable evidence, name the exact question and its decision impact. Recommend `$research` for a cited note or `$prototype` for runnable evidence. Recommend `$to-questionnaire` when an unavailable fact or decision belongs to an identifiable external stakeholder and must be collected asynchronously. Recommend `$handoff` when evidence work must cross into a fresh session and return here.

**Return.** Include confirmed decisions, explicit deferrals, source pointers, any evidence gap, and the next route. Return the packet to an invoking caller; otherwise report it and stop. Leave the plan unexecuted.
