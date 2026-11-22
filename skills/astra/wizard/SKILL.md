---
name: wizard
description: Guide a human through terminal steps requiring private input or human-only action, with a safe handoff back. Exclude ordinary agent-executable work.
---

# Wizard

Handle the authorized work around a private or human-only step. Keep secrets
and private-session input and output with the human.

## Prepare the step and its check

Identify the exact blocker, intended target, and the action that needs the
human. Do the authorized setup and ordinary repairs yourself. Use safe
observations to establish current state when they can spare the human a step
and still satisfy the requested outcome.

Choose the verification before handing off. Prefer an existing read-only
status check or a minimal authorized operation through the actual consumer.
Match the evidence to the blocker and intended account, project, or environment.
Use [Non-secret completion handoff](references/inputs-and-effects.md#non-secret-completion-handoff)
to decide what the check can safely expose to the agent.

## Hand off the human action

Reuse an established login, credential-entry tool, or other suitable procedure.
Check the entry point in the intended shell or app and resolve relevant target
and permission prerequisites through safe checks. Give the human the exact
action, its target or effect, and what happens next. A familiar login can take
one instruction. Include cancellation or retry guidance when it affects the
outcome.

Add a script when it materially helps with validation, persistence, or recovery.
For custom input capture, secret storage, consequential effects, or new status
output, use the applicable branches of
[Inputs, effects, and recovery](references/inputs-and-effects.md). Exercise
authored entry points and material failure and cancellation paths with dummy
values or isolated targets. Repair scoped defects and report any material check
you could not exercise.

When launch is requested, verify that the host provides a human-visible session
with private input and output. Keep secrets out of launch arguments and
environment overrides. Keep the session outside agent observation, recording,
and polling. If private launch cannot be verified, give the exact action for
the human to run privately. Use the authority already granted for each effect.

## Verify and resume

When the request is to author a procedure, deliver the checked instructions or
script. In a broader task, continue independent work while the human acts.
Use a safe completion signal to run the planned check when needed. A brief
“done” suffices when you need the human to signal. Reuse a fresh result that
already establishes the prerequisite.

If the human alone can observe the outcome, ask for the specific non-secret
fact that can establish the prerequisite. Keep human-reported completion and
independent verification distinct. Resume the authorized dependent work once
the evidence satisfies the blocker. Otherwise report the exact remaining gap.
