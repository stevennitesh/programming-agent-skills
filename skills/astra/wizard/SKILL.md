---
name: wizard
description: Guide a human through terminal steps requiring private input or human-only action, with a safe handoff back. Exclude ordinary agent-executable work.
---

# Wizard

Prepare the smallest useful terminal handoff for a private or human-only step
that blocks the requested work. Real secrets and private-session input/output
remain with the human operator. Establish how non-secret completion evidence can
unblock already-authorized work.

## Separate the human step from agent work

Use a wizard when part of the procedure genuinely requires private input, the
human's active identity/account, dashboard interaction, physical action, or
another step the agent should not execute or observe. Reuse an established login
command, credential-entry utility, or setup procedure when it meets the need.
If one instruction suffices, return it directly; add a small script or wrapper
when guidance, validation, or recovery earns it. Complete authorized non-private
preparation and leave ordinary agent-executable work with the agent.

Recover the settled outcome, target, and consequential choices from current
sources. Do not encode an unresolved product or effect decision as an interactive
prompt merely to keep the procedure moving.

Identify what the human must do, the intended target and effect, what establishes
the prerequisite, and how failure or retry will work. Inspect schemas, commands,
and consumers without reading existing secret values or asking the user to paste
credentials into chat. A full plan for the surrounding task is not required to
prepare a well-defined private step.

## Prepare a clear terminal interaction

Choose the shell, language, interaction style, and validation method suited to the
host and repository. Prefer existing mechanisms and the requested or established
artifact location; put disposable artifacts under the existing scratch convention.
Make necessary scoped setup corrections within existing authority, such as an
ignore rule for the intended secret file. Preserve unrelated configuration and
avoid adding infrastructure merely to host the wizard.

Tell the human what they need, where to obtain it, its intended destination, the
next action, and how to cancel or recover. Display the target without displaying
secret values. Keep prompts focused on decisions and actions the human must take.

Read [Inputs, effects, and recovery](references/inputs-and-effects.md) when the
procedure captures values, persists data, invokes external tools, mutates state,
or exposes completion status for the agent.

Before a consequential effect, display the actual target, active identity when
relevant, and effect. An explicit action such as saving to the displayed target
can supply confirmation; do not add redundant approval prompts. One confirmation
may cover a bounded group against the same target. Reconfirm when identity,
target, or scope materially changes. This runtime check establishes the human's
intended target and does not expand the task's existing authority.

Distinguish success, failure, cancellation, EOF, blocked prerequisites, and
unverified effects. Stop dependent stages when their prerequisites are not known
to hold.

## Check and repair without private input

Check syntax and the branches that can materially change operator safety or
completion, including cancellation/EOF, failed commands, persistence failure,
target confirmation, and uncertain-effect recovery when applicable. Choose
proportionate checks for the actual procedure; no fixed test suite is required.

Use dummy values, stubs, or isolated local targets. Do not request real
credentials, open private dashboards, mutate real external state, or treat a
dummy-secret test as proof that every external tool handles real secrets safely.
Repair ordinary script or setup defects within scope and rerun affected checks
without renewed permission. Include any exported completion status in the checks
so it cannot report success after a failed prerequisite or expose dummy secrets.

Complete preparation only when the chosen procedure can guide the human without
exposing private input to the agent and its material failure paths have a defined
operator-visible outcome.

## Deliver or privately launch

Stay within existing authority for installation, commits, publication, and external
effects. Authoring the procedure does not authorize executing its private stages
through agent-visible tools.

When launch is part of the request and the host provides a human-visible session
whose private input and output are not exposed to the agent, launch the checked
procedure there. Verify the host's separation rather than inferring it from a
visible window or masked prompt. Pass no secret through command arguments or the
launch environment, and do not read, poll, record, or capture that private session.

If such separation is unavailable, return the exact run command instead of using
an agent-attached terminal.

Return the script path when applicable, exact run command, material effects,
checks, launch status, and what the human should report without private details.
Delivery or launch does not establish that the human procedure itself succeeded.

## Hand back control when the prerequisite is established

Distinguish preparation, human-reported completion, and a verified prerequisite.
Use a deliberate non-secret return path: a concise report from the human may
suffice; a narrowly defined status result or safe consumer check may be useful.
Apply the reference's handoff rules and match the evidence to the actual blocker.
Do not infer application readiness merely because a credential was stored.

For an authoring-only request, the checked procedure and run instructions complete
the task. During broader authorized work, continue independent work while the
human acts, then resume dependent work once the prerequisite is established to
the required level. If that remains unavailable, report the specific manual step
or verification gap without requesting private transcripts or secret values.
