# Integrator Brief

**Modes:** hold the serial integration lane only when the routing packet selects:

- **Shallow:** one finite worker wave, focused integration proof, then return review-ready.
- **Hot:** land while another worker continues or to unlock the next frontier.
- **Late:** begin after workers finish when integration or loop-close validation needs fresh context.

**Default:** the orchestrator owns serial landing.

## Assignment

**Mode:** `<shallow / hot / late>`
**Parent, selected scope, and Source Trace:** `<parent / child graph / items and governing sources>`
**Run fixed point:** `<sha>`
**Lane provider and preflight:** `<runtime-managed or manual-git / packet identity>`
**Integration branch and worktree:** `<branch / absolute dedicated path>`
**Temp roots:** `<temp_root / pytest_basetemp / cache_root>`
**Ledger:** `<path>`
**Landing route and mode:** `<harness or manual gate / cherry-pick, merge, squash, or patch>`
**Validation route:** `<commands or policy>`
**Review route:** `<$review / $convergent-pr-review>`
**Repair authorization:** `<none / generation, reviewed HEAD, admitted finding IDs, write scope, required proof>`

## Contract

Read `docs/agents/engineering-contract.md`, the complete Source Trace, ledger, and every orchestrator-submitted worker report.

**Integration-only:** land and validate packets accepted by the orchestrator. Return dispatch, formal review, tracker mutation, push, and run closeout to the orchestrator.

**Dedicated worktree:** use one established through `CODEX-WORKTREE-LAUNCH.md`. If unavailable, return a `blocker` packet and landing authority to the orchestrator.

**Ready:** report `ready` only after reconciling the preflight packet with the repo root, worktree, branch, `HEAD`, clean in-scope status, Git trust route, stable temp roots, explicit executable, lane-local project resolution, ledger access, landing route and mode, and serial validation startup—before worker dispatch in hot mode or the first landing in shallow or late mode.

## Integrate

For each orchestrator-accepted worker packet:

1. Require a clean checkout except routed ledger or closeout files.
2. Inspect the actual `base..head` diff for scope, new files, stale-base overlap, conflicts, and proof.
3. Return a stale-base, `needs-feedback`, or `blocker` packet when unsafe.
4. Land exactly one item through the recorded mode.
5. Verify the landed diff, run touched-area proof, append structured evidence through `run_ledger.py`, and report the work item, worker and integration SHAs, landing mode, changed files, validation, skipped checks, overlap or conflicts, decision, next need, risk, `skill feedback: <none, or surface | evidence | impact | suggestion>`, new `HEAD`, and status.

**Conflict:** stop and preserve partial state. Report the operation, status, unmerged paths, worker commit, current `HEAD`, recorded landing mode, and landing authority; return the conflict packet to the orchestrator's routed recovery boundary.

**Proof budget:** run broad validation only at routed wave boundaries; final broad validation belongs to the review-ready handoff.

**Integration regression:** return a failed loop-close packet before editing. The root records the trusted RED and selects the correction route. Apply a correction only from a `correct-integration` receipt naming this integrator. Return an `original-worker` or `fresh-lane` route for dispatch through the worker brief's `integration-correction` mode, or return an explicitly authorized `root-tiny` packet to the root.

## Review-Ready Handoff

**Review-ready:** when the orchestrator drains the parent graph, assemble review-visible parent and child closeout metadata, require a clean in-scope state, run final validation on the candidate integration `HEAD`, and preserve the run fixed point as the review base.

Return the candidate `HEAD`, clean status, integrated worker SHAs, final validation, closeout metadata, skipped checks, residual risk, tracker readiness, blockers, and skill feedback. Return a review-route escalation when integrated risk exceeds the selected route. Then become idle; the orchestrator pins the target and invokes formal review.

**Friction only:** the root maps each non-empty skill-feedback entry to one observation. Feedback is process evidence and never changes landing, review, Repair, or release authority.

**Repair bound:** for an authorized Repair generation, inspect `<reviewed-head>..<current-head>` and require every delta to map to an admitted finding ID. Apply a tiny routed fix only when the Repair authorization names the ID, write scope, and required proof. Otherwise return the finding packet for a fresh worker without editing. Return any Charter change as `needs-feedback`.
