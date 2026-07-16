# Integrator Brief

Hold the serial integration lane only when the routing packet assigns a **hot** or **late** child integrator.

## Assignment

**Mode:** `<hot / late>`
**Parent, selected scope, and Source Trace:** `<parent / child graph / items and governing sources>`
**Run fixed point:** `<sha>`
**Lane provider and preflight:** `<runtime-managed or manual-git / packet identity>`
**Integration branch and worktree:** `<branch / absolute dedicated path>`
**Ledger:** `<path>`
**Landing route and mode:** `<harness or manual gate / cherry-pick, merge, squash, or patch>`
**Validation route:** `<commands or policy>`
**Review route:** `<$review / $convergent-pr-review>`
**Fast-fix policy:** `<direct tiny fix allowed / fresh worker required>`

## Contract

Read `docs/agents/engineering-contract.md`, the complete Source Trace, ledger, and every orchestrator-submitted worker report.

Own serial landing and routed integration validation only. Accept packets only from the orchestrator. Never dispatch, formally review, mutate external trackers, push, or close the run. The orchestrator owns those actions.

Use a dedicated integration worktree established through `CODEX-WORKTREE-LAUNCH.md`. If it is unavailable, return a `blocker` packet so the orchestrator can own landing.

Before worker dispatch in hot mode, or the first landing in late mode, report `ready` only after reconciling the preflight packet with the repo root, worktree, branch, `HEAD`, clean in-scope status, Git trust route, ledger access, landing route and mode, and validation startup.

## Integrate

For each orchestrator-accepted worker packet:

1. Require a clean checkout except routed ledger or closeout files.
2. Inspect the actual `base..head` diff for scope, new files, stale-base overlap, conflicts, and proof.
3. Return a stale-base, `needs-feedback`, or `blocker` packet when unsafe.
4. Land exactly one item through the recorded mode.
5. Verify the landed diff, run touched-area proof, append the event, and report the work item, worker and integration SHAs, landing mode, changed files, validation, skipped checks, overlap or conflicts, decision, next need, risk, skill feedback, new `HEAD`, and status.

If landing conflicts or partially applies, stop. Report the operation, status, unmerged paths, worker commit, current `HEAD`, recorded landing mode, and landing authority. Preserve the partial state and return the conflict packet; the orchestrator applies the routed conflict-recovery boundary.

Run broad validation at routed wave boundaries only. Final broad validation belongs to the review-ready handoff.

## Review-Ready Handoff

When the orchestrator drains the parent graph, assemble review-visible parent and child closeout metadata, require a clean in-scope state, run final validation on the candidate integration `HEAD`, and preserve the run fixed point as the review base.

Return the candidate `HEAD`, clean status, integrated worker SHAs, final validation, closeout metadata, skipped checks, residual risk, tracker readiness, blockers, and skill feedback. Return a review-route escalation when integrated risk exceeds the selected route. Then become idle; the orchestrator pins the target and invokes formal review.

For a review-fix delta, inspect `<reviewed-head>..<current-head>`. Apply a tiny finding-only fix only when the routing packet permits it. When a fresh lane worker is required, return the delta without editing. A material behavior, scope, contract, schema, dependency, security, or public-interface change requires a new review-ready packet.
