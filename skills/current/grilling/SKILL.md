---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

# Grilling

This is the interview primitive. Resolve a plan by walking the **design tree** one dependency at a time until shared understanding is reached.

Start by restating the plan and naming the first uncertain branch.

Each turn: **recap, pressure, ask, trade off, recommend**.

Ask one highest-leverage unresolved question, then wait. The question should be the answer that blocks the most later decisions.

If code can answer the question, inspect code instead of asking.

After each user answer, treat it as the next turn's recap before opening the next branch.

Durable memory: recommend `$grill-with-docs`; do not write `CONTEXT.md` or ADRs from this skill.

Stop when the plan has no major unresolved branches, or when the next artifact, skill, or implementation step is clear.
