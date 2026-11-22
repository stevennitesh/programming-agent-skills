# Inputs, effects, and recovery

Read the branches the chosen procedure actually needs. Prefer established
repository utilities over a new wizard framework.

## Private and structured input

Capture secrets with non-echoing native input in the operator's private session.
Refuse an insecure fallback when secure input is unavailable. A hidden prompt in
an agent-attached or recorded terminal is not private. Check the input API's
failure behavior; for example, Python's `getpass` can warn and fall back to stdin
when echo-free input is unavailable, so that fallback must be rejected.

Keep captured values as data. Do not use `eval`, source responses as code, build
shell commands from private input, enable shell tracing around secrets, or place
secrets in command lines, diagnostics, transcripts, or incidental temporary
files. Use the destination tool's documented secure input mechanism.

Validate public identifiers and input shape according to the actual destination
parser. Preserve meaningful whitespace and special characters, and do not invent
credential-format restrictions stronger than the provider's.

Treat cancel, EOF, blank input, and an explicit request to retain an existing
value as different states. Never display the existing secret as a default or
overwrite it because a prompt closed or returned blank.

## Secret destinations and local updates

Resolve the exact destination and consumer before writing. For a project secret
file, establish that the exact path is untracked and ignored; an ignore rule does
not untrack an existing file. For other locations, preserve the intended access
boundary. Do not weaken permissions or follow an unexpected symlink target to
proceed.

Preserve unrelated keys and meaningful formatting. Follow the consumer's
documented duplicate-key semantics or fail when they are ambiguous. Serialize for
the actual format rather than relying on regex replacement as a universal writer.

Do not truncate existing configuration before a replacement is known to be
usable. Use the established safe-update mechanism. If atomic replacement requires
a secret-bearing temporary file, protect it like the destination, keep it in the
intended protected location, and clean it after failure. Do not create plaintext
backup copies. Stop the stage when safe persistence is unavailable.

## External effects and uncertain outcomes

Before a consequential effect, display the actual target, active identity when
relevant, and effect. An explicit action such as saving to that displayed target
can confirm intent; avoid redundant approval prompts. One confirmation may cover
a bounded group against the same target. Reconfirm when identity, target, or scope
materially changes. This runtime check establishes the human's intended target
without expanding the task's existing authority.

Bind each mutation to the explicit account, project or repository, environment,
resource, and scope it affects. Do not rely silently on a CLI's default account or
current directory.

Check command status and an observable postcondition. When a secret value cannot
be read back, verify its exact scope/name and available fresh metadata and leave
value equality unproved. Metadata also does not prove that the application can
use the credential. If no useful postcondition is observable, report the effect as
manual or unverified rather than manufacturing proof.

After timeout, partial failure, or any uncertain effect, inspect current state
before retrying. Prefer documented idempotent updates or stable operation
identifiers when available; do not blindly repeat key creation, charges, deletion,
or cutover actions.

Preserve completed external effects unless rollback is itself authorized and
understood. Record only non-secret recovery state such as resource identifiers and
completion status, then verify it against live state on resume. Stop dependent
stages while prerequisites remain unverified.

## Non-secret completion handoff

Choose the smallest proof sufficient for the blocker. Prefer current, target-bound
evidence the agent can obtain safely. If application readiness is the blocker,
use the application's configured credential path for a minimal authorized
check. A stored value, provider acceptance, and successful application use
establish different facts. An exit status suffices when the command's meaning
and bound target establish the prerequisite.

Constrain success and failure output before it reaches the agent. Keep private
diagnostics and transcripts inside the private process or session. Leave
credential files and environment dumps outside the verification path. Return
only selected non-secret fields tied to the current task and target. Validate
new status output with dummy inputs, including failure and cancellation. A
success signal requires a confirmed prerequisite for the current attempt.

Use a human acknowledgement as a signal to run the check when needed. If the
agent has no safe way to observe the prerequisite, ask for only the relevant
non-secret observation and attribute it to the human. Continue or report a gap
according to what that evidence establishes. Reuse existing status checks and
task records when useful. If interrupted, retain the target, pending action,
and verification step in the existing task record when available.
