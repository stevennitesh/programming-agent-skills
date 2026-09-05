# Recovery

Read for interrupted, failed, or off-contract work. Reconstruct the run from
actual Git, helper, process, and applicable tracker state before resuming.
Retained packets identify the owned set; directory names alone do not.

| Observation | Next safe action |
| --- | --- |
| Silence or missed checkpoint | Inspect actor and command-session status, then lane state. Silence is not cancellation. |
| Transient provider failure | Preserve the actor's evidence; use the host's bounded retry policy. Do not loop retries or create duplicate actors. |
| Worker needs replacement | Stop the previous actor and attached writers; confirm quiescence, inspect work, then transfer exclusive custody and the actual partial state. Never start a second actor while the first may write. |
| Dirty or off-contract return | Preserve it. Normal resume/landing eligibility is false. Under exclusive custody inspect and repair the owned partial state with the original worker, or transfer it after confirmed termination. Do not reset, discard, or invent a commit just to satisfy eligibility. Reinspect before normal work or landing. |
| Integration advanced | Recheck semantic and proof interference. Incorporate the new integration commit in the same lane without rewriting shared refs; rerun affected proof. The manifest's original base remains provenance, not the current development tip. |
| Active Git conflict | Preserve conflict state and stop other integration writers. Inspect both intended behaviors and resolve within authority, using a conflict skill if available and useful. Return substantive item conflicts to its owner. Recheck composed behavior; never choose ours/theirs solely to get a clean merge. |
| Scope or permission gate blocks a descendant | Stop affected dispatch; let safe valid work finish, land and clean eligible items, and preserve incomplete work. Do not claim the gated item or treat the pause as permission to delete it. |
| Prepare fails after partial effects | Inspect the named checkout, registration, and helper state; retain error evidence. No worker starts without a successful packet. Do not delete or reuse uncertain residuals. |
| Cleanup partially succeeds or command errors | Read back registration, checkout, receipt, and runtime state. Use the helper's exact retry for eligible named residuals; preserve and report others. Never replace receipt recovery with manual recursive deletion. |
| HEAD changes during cleanup verification | Previous cleanup/retry recommendations are invalid. Reacquire custody, inspect the new candidate and affected proof, then verify again with its full commit ID. |

The helper cannot observe actor liveness, verify code semantics, discover forgotten
lane packets, or exclude an unrelated concurrent actor. The root enforces one
owner of integration and helper operations; serialize helper mutations. A host
that cannot enforce checkout placement or exclusive ownership cannot safely run
this concurrent method. Preserve state and use serial implementation instead.

Use the [normal cleanup safeguards](agent-lanes.md#cleanup) on recovery retries
too. A pending cleanup receipt blocks normal resume or landing; finish the
eligible cleanup retry or preserve and report the residual state.
