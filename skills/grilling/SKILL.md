---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

# Grilling

Interview the user relentlessly until you and the user share the same understanding of the plan, its trade-offs, and the next step.

Start by briefly restating the plan and naming the first uncertain branch.

Walk the design tree one dependency at a time. Ask the highest-leverage unresolved question first: the answer that blocks the most later decisions.

For each turn, use this order:
1. Recap what is already decided or learned in the conversation.
2. Analyze what that implies and where the design pressure is.
3. Ask one highest-leverage unresolved question.
4. Analyze the plausible answers and trade-offs.
5. Recommend one answer and explain why.

Recap is chat-only. If the user asks to save the interview, save it as a normal artifact, not in `CONTEXT.md` or ADRs.

Ask one question at a time, then wait for the user's answer. Multiple questions at once are bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

After each user answer, treat it as the next turn's Recap step before opening the next branch.

Stop when the plan has no major unresolved branches, or when the next artifact, skill, or implementation step is clear.
