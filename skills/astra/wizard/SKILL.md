---
name: wizard
description: Create a guided local script for a settled procedure that needs human identity, private input, dashboard access, or physical action. Use when explicitly requested and guidance reduces ordering, target-selection, or configuration mistakes; exclude unresolved design interviews and ordinary agent-executable work.
---

# Wizard

Turn a bounded human-operated procedure into a checked interactive script. Keep
the operator informed about progress, destinations, and remaining work. The
authoring agent does not receive real secrets or supervise the private session.

## 1. Establish the procedure

Inspect the requested outcome, repository conventions, available runtime, and
existing automation. Separate authorized agent-executable preparation from steps
that need the human. Use a wizard when coordinating those steps earns its cost;
return one simple manual instruction directly when a script adds no value.
Do not replace ordinary implementation with a human-operated script.

Recover settled decisions from current sources. If a consequential target or
choice remains open, resolve it with its owner rather than encoding a guess.
Continue independent authoring where that gap does not affect correctness.
For third-party commands or dashboard steps, verify current official instructions;
do not invent navigation or silently expand the procedure to every CI variable.

Map each stage to its prerequisite, human action, captured values and their
sensitivity, exact destination/effect, and evidence of success. Inspect schemas,
examples, and consumers without reading existing secret values. Never ask the
user to paste credentials into chat. Summarize consequential scope or effect
choices when needed; do not ask again about decisions the user already made.

## 2. Build the smallest useful guide

Use an available repository runtime or the operator's native shell. Prefer one
script with only the helpers it needs; do not install dependencies to run it.
Use the requested destination, otherwise a unique path under the repository's
ignored scratch convention. A repeatable repository workflow belongs in its
normal scripts location when requested. If no suitable scratch path exists,
return the script content and intended path without changing ignore policy.

Before effects, preflight required tools and non-secret configuration. Show the
procedure's targets and effects, then guide one focused stage at a time with
stage progress and clear instructions before requesting input. Open a verified
URL when useful and print a manual fallback if opening fails. Do not clear away
instructions or identifiers the operator still needs. Support cancellation and
distinguish it from successful completion; EOF is not approval or a default value.

Read [Inputs, effects, and recovery](references/inputs-and-effects.md) when the
procedure captures values, writes files, calls external tools, or changes state.
Keep harmless navigation free of repeated confirmation. Before a destructive
action or durable external mutation, show the exact target and active identity
where applicable, and require the operator's informed confirmation. Existing
task authority lets the agent author the stage; the runtime gate confirms the
actual target the human is about to affect.

Stop dependent stages on failure, cancellation, or uncertain effects. Preserve
completed progress without recording secrets. A rerun must inspect actual state
before replaying a possibly completed mutation. Finish with completed, skipped,
blocked, and unverified outcomes as applicable, not an unconditional success banner.

## 3. Check without running the human procedure

Run the available syntax/parser or lint check. Trace inputs to their destinations
and effects to their targets, confirmation, success evidence, and recovery path.
Test meaningful supported branches using dummy inputs and isolated local targets:
creation/update, escaping, cancellation/EOF, failed commands, and partial recovery
where applicable. Do not mirror script wording in tests or require a framework.

During validation, do not request real credentials, open dashboards, change real
configuration, or perform durable external mutations. Use stubs or a no-effects
test path when needed. Check that test output and error handling do not expose
dummy secret markers, while recognizing that this does not prove every external
tool is safe with real credentials. State what remains for the operator to verify.

## 4. Deliver or launch within scope

A request to create a wizard authorizes its local artifact, not installation,
commits, publication, or running credentialed stages in the agent's tools. If the
user also asks to run it or be walked through the procedure, launch the checked
script in a separate visible terminal whose input and output are not attached
to the agent. Pass no secret through arguments or launch environment. Do not
read, poll, record, or capture that session. If that separation is unavailable,
return the exact run command and explain the gap instead of using an attached
terminal. An explicit launch request needs no extra confirmation just to open it.

Return the script path or content, one run command, effects, checks, launch status,
and unresolved manual details. Complete when the checked, secret-free script
covers the admitted procedure and can be run in the intended environment. Script
delivery or launch does not establish that the human procedure succeeded.
