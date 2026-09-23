---
name: wizard
description: Create a guided local script for a settled procedure that needs human identity, private input, dashboard access, or physical action. Use when explicitly requested and guidance reduces ordering, target-selection, or configuration mistakes; exclude unresolved design interviews and ordinary agent-executable work.
---

# Wizard

Create a checked script for a settled procedure whose required private or
human-only steps should not be performed or observed by the authoring agent. Real
secrets and private-session input/output remain with the human operator.

## 1. Admit the human-operated boundary

Use a wizard when part of the procedure genuinely requires private input, the
human's active identity/account, dashboard interaction, physical action, or
another step the agent should not execute or observe. If one manual instruction
is sufficient, return it directly. Do not replace ordinary agent-executable work
with a wizard.

Recover the settled outcome, target, and consequential choices from current
sources. Do not encode an unresolved product or effect decision as an interactive
prompt merely to keep the procedure moving.

For each stage establish the prerequisite, human action or input, target/effect,
success evidence, and failure or retry behavior. Inspect schemas, commands, and
consumers without reading existing secret values or asking the user to paste
credentials into chat.

## 2. Build the checked procedure

Use the requested or established repository/runtime location. Put disposable
one-off artifacts under an existing scratch convention when one exists; do not
create new installation, persistence, dependency, or ignore policy merely for the
wizard.

Read [Inputs, effects, and recovery](references/inputs-and-effects.md) when the
procedure captures values, persists data, invokes external tools, or mutates
state.

Before a consequential effect, display the actual target, active identity when
relevant, and effect. One confirmation may cover a clearly displayed bounded
group against the same target; require a new confirmation when identity, target,
or scope materially changes. Existing task authorization permits authoring the
effect; the runtime gate verifies that the human session is about to apply it to
the intended target.

Distinguish success, failure, cancellation, EOF, blocked prerequisites, and
unverified effects. Stop dependent stages when their prerequisites are not known
to hold.

## 3. Validate without real private input or effects

Check syntax and the branches that can materially change operator safety or
completion, including cancellation/EOF, failed commands, persistence failure,
target confirmation, and uncertain-effect recovery when applicable.

Use dummy values, stubs, or isolated local targets. Do not request real
credentials, open private dashboards, mutate real external state, or treat a
dummy-secret test as proof that every external tool handles real secrets safely.

Complete authoring only when the script can guide the admitted procedure without
exposing private input to the agent and its material failure paths have a defined
operator-visible outcome.

## 4. Deliver or privately launch

Creating the wizard authorizes its local artifact, not installation, commit,
publication, or execution of credentialed stages through agent-visible tools.

If the user explicitly asks to launch it and the host provides a human-visible
session whose input and output are not exposed to the agent, launch the checked
script there. Pass no secret through command arguments or the launch environment,
and do not read, poll, record, or capture that private session.

If such separation is unavailable, return the exact run command instead of using
an agent-attached terminal.

Return the script path or content, one run command, material effects, checks,
launch status when applicable, and unresolved manual details. Delivery or launch
does not establish that the human procedure itself succeeded.
