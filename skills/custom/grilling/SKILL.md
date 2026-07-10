---
name: grilling
description: Grill the user relentlessly, one decision at a time. Use when the user wants a conversation-only interview that pressure-tests a plan or design before building.
---

# Grilling

Walk the plan's **design tree** dependency-first. Pressure-test every material branch, one decision per turn.

**Facts are found; decisions are owned.** Inspect code and docs for answerable facts and name the source of every load-bearing fact. Put every material commitment to the user; recommendations remain advisory.

Start with a compact plan recap and the root uncertainty.

Each turn: **Recap** the latest answer; **Pressure** one assumption, dependency, failure mode, or tradeoff; **Ask** exactly one unresolved decision that unlocks the most downstream branches; **Recommend** an answer and its decisive tradeoff; **Wait**.

Reopen branches invalidated by later answers.

Hold the **commitment boundary**. Grilling owns the interview; execution starts later, after user confirmation.

Stop only through one exit:

- **Confirmed:** every material branch is resolved or explicitly deferred. Present a compact exit packet; exit only after the user confirms it and the next route is named.
- **Evidence gap:** the next branch depends on source facts or runnable evidence unavailable in the conversation. Name the exact question and its decision impact; recommend `$research` or `$prototype`. Recommend `$handoff` when the evidence work needs a fresh session and its answer must return here.

The **exit packet** contains confirmed decisions, explicit deferrals, source pointers, any evidence gap, and the next route.

When another skill invokes grilling, return the exit packet to that caller. Otherwise report it and stop. Grilling leaves the plan unexecuted.
