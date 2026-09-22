# Planned delivery

Use when the user requests coordinated serial delivery with checkpoints or when a
wrong early interface, persisted representation, or integration decision would
make later delegated work materially expensive to redo.

The lead owns checkpoint selection and review. The worker owns implementation
within the current assignment.

## Choose meaningful checkpoints

Reuse the accepted plan or shaping result; do not create a plan merely to use this
reference. A checkpoint is useful when early evidence can prevent consequential
downstream rework, not simply because a task has several steps.

Define the checkpoint's work boundary, accepted behavior, and required evidence
once. Final integrated review remains necessary even when intermediate checkpoints
pass.

Suggested implementation mechanisms remain adaptable unless they are accepted
constraints.

## Advance serially

Assign work through the next meaningful checkpoint using the main skill's worker
assignment and custody contract.

When the worker returns a stable candidate and releases custody, review only the
behavior the checkpoint claims to establish plus affected earlier integration.
Future work outside that boundary is not a checkpoint defect.

Return required implementation corrections through the main skill's recovery path.
After a checkpoint is accepted, continue with the next assignment without reopening
settled decisions.

If accepted meaning must change while assignments or proof already depend on it,
use
[Active delivery revisions](../../shape-work/references/active-delivery-revisions.md)
before resuming affected work.

## Confirm the whole outcome

After the final worker return, review the complete accumulated in-scope candidate
against the original accepted outcome. Reuse checkpoint evidence only while later
changes leave its relevant code, inputs, and assumptions valid.

Completion requires the whole outcome, required proof, and final candidate review;
checkpoint passes are not substitutes for integrated acceptance.
