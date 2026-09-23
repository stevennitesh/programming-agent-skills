# Inputs, effects, and recovery

Read the branches the generated procedure actually needs. Prefer established
repository utilities over a new wizard framework.

## Private and structured input

Capture secrets with non-echoing native input in the operator's private session.
Refuse an insecure fallback when secure input is unavailable. A hidden prompt in
an agent-attached or recorded terminal is not private.

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

Bind each mutation to the explicit account, project or repository, environment,
resource, and scope it affects. Do not rely silently on a CLI's default account or
current directory. Recheck identity and target when either changes after
confirmation.

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
