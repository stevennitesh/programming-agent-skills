# Inputs, effects, and recovery

Apply the branches the generated procedure actually needs. Prefer established
repository utilities over a new general wizard framework.

## Private and structured input

- Capture secrets with non-echoing native input in the operator's private terminal.
  Refuse insecure fallback if secure input is unavailable. Hidden prompts alone
  do not make an agent-attached or recorded terminal private.
- Keep values as data. Do not use `eval`, source an input file as code, or build
  shell commands from responses. Use argument arrays for non-secret parameters
  and a tool's documented stdin or secure input mechanism for secrets. Avoid
  secret-bearing command lines, diagnostic output, transcripts, and incidental
  temporary files. Do not enable shell tracing around private inputs.
- Validate public identifiers and input shape before effects. Treat whitespace,
  quotes, backslashes, dollar signs, and newlines according to the destination's
  actual parser; do not silently trim meaningful bytes. Reject unsupported input
  clearly. Do not invent a credential format check stronger than the provider's.
- Distinguish cancel, EOF, blank input, and an explicit request to retain an
  existing value. Never display the existing secret as a default. Do not overwrite
  it with an accidental blank or treat a closed prompt as consent.

## Secret destinations and local updates

Resolve the exact destination and its intended consumer. A project secret file is
an intentional output, not a scratch channel. Before writing, ensure it is not
already tracked and that Git ignores the exact path; an ignore rule does not
untrack a file. For non-Git locations, check the intended privacy/access boundary.
Do not weaken permissions or overwrite an unexpected symlink target to proceed.

Preserve unrelated keys, comments, and meaningful formatting. For ambiguous
duplicate keys, fail with an actionable explanation or apply the consumer's
documented semantics; do not silently assume first- or last-wins. Serialize for
the actual `.env`, JSON, YAML, or other consumer and verify by parsing dummy data
with that consumer when practical. Regex replacement is not a universal serializer.

Avoid truncating existing configuration on a failed write. Use the repository's
established safe update mechanism; if atomic replacement requires a temporary
secret-bearing file, give it the destination's restrictive protection before
writing, keep it in the intended protected directory, and clean it on failure.
Do not create plaintext backup copies or weaken existing access protections.
If safe persistence is unavailable, stop that stage rather than improvise storage.

## External effects and uncertain outcomes

Bind each mutation to the explicit account, project/repository, environment,
resource, and scope it actually affects. Do not rely silently on a CLI's current
directory or default account. Recheck identity/target if either changes after the
operator confirms. A confirmation covers the displayed operation, not later
different targets. Do not collect values for environments outside the request.

Check command exit status and read back an observable postcondition. For secrets
that cannot be retrieved, verify their exact scope/name and available fresh
metadata; describe value equality as unproved. Metadata alone does not establish
that an application can use the credential. When no useful postcondition is
observable, leave the mutation manual and unverified. A pause or affirmative response is
operator-reported completion, not an independent check.

After a timeout or partial failure, inspect current state before retrying. Use
documented idempotent updates or stable operation identifiers when available;
do not blindly repeat key creation, charges, deletion, or cutover actions. Preserve
recoverable state and name the remaining action. Do not automatically roll back
completed external changes when rollback could destroy work or has unknown effects.
Checkpoint only non-secret status and resource identifiers when useful, and verify
them against live state on resume. Stop dependent stages while prerequisites are
unverified; independent stages may continue only when that is safe and explicit.
