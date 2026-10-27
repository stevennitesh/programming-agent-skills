---
name: wizard
description: Guide a human through terminal steps requiring private input or human-only action, with a safe handoff back. Exclude ordinary agent-executable work.
---

# Wizard

Prepare the smallest useful terminal handoff for a requested private or human-only
step. Real secrets and private-session input/output stay with the human. Define
the non-secret evidence needed to unblock already-authorized work.

## Separate the human step from agent work

Identify the step requiring private input, the human's active identity, dashboard
or physical interaction, or another action the agent should not execute/observe.
Complete authorized non-private preparation yourself. Reuse an established login,
credential-entry tool, or procedure; one instruction may suffice. Add a script
only when guidance, validation, or recovery earns it.

Recover the settled outcome, target, and consequential choices from current
sources. Do not turn an unresolved product/effect decision into an interactive
prompt. Inspect schemas, commands, and consumers without reading existing secrets
or asking for credentials in chat. A surrounding task plan is unnecessary for a
well-defined private prerequisite.

## Prepare a clear terminal interaction

Use a suitable host/repository shell and established artifact location; disposable
files follow local scratch conventions. Make necessary scoped setup repairs, such
as an ignore rule for the intended secret file, without changing unrelated
configuration or adding infrastructure merely to host the procedure.

Tell the human what they need, where to obtain it, the intended target/effect,
next action, completion evidence, and cancel/retry path. Display no secret values.
Keep prompts focused on human decisions and actions. For captured values,
persistence, external tools/effects, or exported completion status, read
[Inputs, effects, and recovery](references/inputs-and-effects.md). That reference
owns secure input, destination checks, consequential-effect confirmation, safe
persistence/retry, and non-secret handoff.

Distinguish success, failure, cancellation, EOF, blocked prerequisites, and
unverified effects. Stop dependent stages until their prerequisites hold.

## Check and repair without private input

Check syntax and material safety/completion branches: cancellation/EOF, command
and persistence failure, target confirmation, uncertain outcomes, and exported
status where applicable. Use dummy values, stubs, or isolated local targets;
never obtain real credentials, open private dashboards, or mutate real external
state for testing. Dummy-secret checks do not prove external tools handle real
secrets safely.

Repair ordinary script/setup defects within scope and rerun affected checks
without renewed permission. The procedure must guide the human without exposing
private input to the agent, give material failures an operator-visible outcome,
and prevent exported status from reporting success after a failed prerequisite
or leaking dummy secrets. No fixed test suite is required.

## Deliver or privately launch

Authoring grants no new installation, commit, publication, or external-effect
authority, and does not authorize private stages through agent-visible tools.

When launch is requested, verify the host provides a human-visible session whose
input/output the agent cannot observe. A visible window or masked prompt does
not prove separation. Pass no secret in launch arguments/environment; never read,
poll, record, or capture the private session. If separation is unavailable, return
the exact run command instead of using an agent-attached terminal.

Return any script path, exact command, material effects, checks, launch status,
and the non-secret result the human should report. Delivery/launch does not
establish that the human procedure succeeded.

## Hand back control when the prerequisite is established

Use the reference's non-secret handoff rules to distinguish prepared procedure,
human-reported completion, and verified prerequisite. Match fresh evidence to the
actual blocker; storing a credential alone does not prove application readiness.
Never request private transcripts or secret values to close the gap.

Authoring-only work ends with the checked procedure and run instructions. During
broader authorized work, continue independent tasks while the human acts, then
resume dependent work once the prerequisite is established to the required level.
Otherwise report the specific manual step or verification gap.
