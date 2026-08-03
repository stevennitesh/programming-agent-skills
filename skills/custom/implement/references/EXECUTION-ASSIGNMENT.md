# Execution Assignment and Worker Return Contract

This is the implement-owned boundary for one delegated worker attempt.
`$implement` owns the contract; `$parallel-implement` may consume it without
invoking the full single-item delivery lifecycle. The contract creates no
dispatch authority and never grants delivery completion.

## Version and validation

The current packet version is `schema_version: 1`. Both packet kinds are
strict objects: missing fields, unknown fields, unsupported versions, malformed
identities, and extra authority fail before execution credit. Validate untrusted
packets with `../scripts/execution_assignment.py`:

- `validate_execution_assignment(packet)` validates one assignment without
  rewriting or normalizing its bytes.
- `validate_worker_return(packet, assignment)` first validates the assignment,
  then binds the Return to its assignment, attempt, and actor.

Validation failure returns the exact field error to the delivery coordinator.
It authorizes no mutation, retry, scope expansion, or status inference.
Unsupported versions explicitly return to the `$implement` contract owner for
recovery and are never coerced.

## Execution Assignment

An Execution Assignment contains exactly:

- `assignment_id`, `attempt_id`, and pre-spawn `actor_id`;
- content-bound `source`, `parent`, and `ticket` identities;
- exact repository `base` and assigned `checkout`;
- ready dependency state and the active claim;
- requested semantic profile with the complete agent-type, model, and reasoning
  tuple from the canonical runtime-profile resolver;
- the content-bound base64 Executor Capsule bytes;
- non-empty write scope, exclusions, permissions, and proof obligations; and
- canonical Return and failure policies.

Write scope and exclusions use canonical repository-relative POSIX paths.
A trailing slash denotes a directory subtree; a path without it denotes one
exact file. Absolute paths, drive-qualified paths, backslashes, traversal,
embedded NUL, noncanonical segments, and duplicate entries fail closed. The only assignment
permissions are, in order, `read-repository`, `write-authorized-scope`, and
`run-proof`; tracker, Git delivery, integration, review, dispatch, installation,
publication, and delivery-completion authority cannot be added as strings.
Requested bindings use the canonical matcher, including its documented
`serial-integrator` high-reasoning escalation; no local profile exception is
created here.

The Return policy permits exactly `done`, `blocker`, `needs-feedback`, and
`transport/binding-failure`, and sets `delivery_completion` to false. The
failure policy maps repository contradiction to `needs-feedback`, authority
gaps to `blocker`, and runtime-binding mismatch to
`transport/binding-failure`.

The assignment is one bounded attempt, not a ticket, plan, campaign, provider
task, or delivery claim. Its capsule is a derived identity-bound input. Capsule
compilation and drift policy belong to their later owner; this boundary only
proves that supplied bytes are valid base64 and match their declared SHA-256.

## Worker Return

A Worker Return contains exactly:

- the assignment, attempt, actor, and observed provider task identities;
- one canonical status;
- final checkout path, `HEAD`, and clean state;
- candidate `HEAD` or explicit absence;
- acceptance-to-evidence rows;
- written paths and unrelated-work preservation;
- risk or blocker evidence; and
- the recovery owner.

`done` requires one candidate matching final checkout `HEAD`, a clean checkout,
one evidence row for every assigned proof-obligation ID, in-scope non-excluded
written file paths, preserved unrelated work, and no blocker or recovery owner.
Unknown or duplicate proof IDs fail for every status; `done` also fails when an
assigned obligation is missing. Every other status requires both blocker
evidence and a recovery owner and claims no completion.

The provider task ID is observed at runtime, so the pre-spawn assignment cannot
bind it. The Return must still carry it as a non-empty identity; the later
runtime-receipt owner decides whether the observed task and model binding earn
execution credit.

## Authority and public projection

Assignment and Return packets cross coordinator/worker custody and are
untrusted until validation succeeds. Unknown fields fail closed, including
attempts to add claim, tracker, integration, review, residual-risk, Lock,
commit, installation, publication, dispatch, or delivery authority.

Public projections carry only the minimum contract identities and evidence.
They exclude secrets, prompts, unrelated task content, and local session paths.
The complete tracker snapshot remains campaign authority during compatibility;
it is not copied into this shared contract or made the worker's default source.

## Compatibility and closure

`$parallel-implement`'s `WORKER-BRIEF.md` and ledger validation remain the
campaign compatibility adapter until the parent graph's T5 proves shared-lane
composition. T5 owns deduplication and may remove or redirect that duplicate
field meaning only after equivalent campaign proof passes. This contract does
not activate delegated dispatch or change current delivery defaults.
