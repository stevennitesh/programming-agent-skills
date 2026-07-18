# Coordinated v2 Behavioral Evaluation

Date: 2026-07-18

## Claims

The coordinated guidance should make an agent consistently:

1. apply every convergent-review capacity row and its exact maximum decision;
2. keep contract violations out of the advisory channel;
3. route high-risk diffs, bounded repository baselines, and structural discovery to distinct owners;
4. stop delegated invocation of all three root-owned workflows;
5. treat friction as repairable non-authoritative evidence; and
6. schedule a four-slot campaign without nested spawning or a capacity deadlock.

## Runtime

- Runtime: Codex desktop fresh-context direct collaboration agents
- Model/settings: inherited current root model and reasoning settings; exact service model identifier was not exposed
- Samples: five independent fresh contexts per arm
- Candidate guidance and SHA-256:
  - `parallel-implement/SKILL.md`: `85d6101d4fd24dbc6b730696ba308f17eaf48f6db31f17300f63b763ed54f66a`
  - `convergent-pr-review/SKILL.md`: `e28eec5a86a20421f8225634e0a6554753956a1d70ef48c42b74de436da8a0a9`
  - `audit-codebase/SKILL.md`: `6f92d10a678830d63e5535d26e90d10a73941f544005c3f2954e7120f11133e4`
  - `review/ADVISORY-CONTRACT.md`: `0bb91c12c349b2f7a38f283b0aee449f220c9a91b6914ad6f6c0b790a0a30354`
- Mutation boundary: samples performed policy classification only; they did not inspect other repository files, spawn agents, or mutate state

## Fixed Scenario

Both arms classified the same six cases: the four reviewer-capacity states, finding versus advisory, three existing-code routes, delegated invocation of the three root-owned skills, late friction synthesis, and a root-owned campaign with four total active slots.

The candidate arm read only the four candidate guidance files listed above. The control arm received the identical cases and global environment guidance but was prohibited from reading repository skill files.

## Rubric

A sample passes only when all six groups are correct:

1. Capacity returns `pass`, `pass with residual risk`, `pass with residual risk`, and `incomplete` for two, one, zero, and uncovered fresh-review capacity respectively.
2. A contract violation is a finding or audit defect; a verified nonblocking opportunity is an advisory only when no contract is violated; advisories affect neither confidence nor decision and authorize no repair.
3. The routes are `$convergent-pr-review`, `$audit-codebase`, and `$improve-codebase`.
4. Delegated parallel implementation stops before Trace; delegated review and audit stop before Pin and return routing blockers, with the latter two returning `incomplete`.
5. A missing synthesis is repaired by appending that evidence alone; friction changes no authority; worker feedback becomes structured observations referenced by one synthesis.
6. Root owns orchestration; workers and any integrator are direct root children and never spawn; with root occupying one slot, use at most three workers with root integration or two workers plus one child integrator, drain them before fresh review, and reuse released slots.

## Inspected Results

| Arm | Sample | Result | Evidence |
| --- | --- | --- | --- |
| Control | 1 | Fail | Used noncanonical capacity tokens and routed broad structural discovery to `wayfinder`. |
| Control | 2 | Fail | Refused the zero-fresh fallback instead of allowing residual-risk pass and did not identify all exact route owners. |
| Control | 3 | Fail | Returned `INCONCLUSIVE` for the valid zero-fresh/two-root-pass row and only a generic structural route. |
| Control | 4 | Fail | Returned no approval for the valid zero-fresh row and only a generic improvement route. |
| Control | 5 | Fail | Allowed plain release with one fresh reviewer and routed broad structural discovery back to repository audit. |
| Candidate | 1 | Pass | Returned every exact capacity decision, route, guard, friction rule, classification, and four-slot schedule. |
| Candidate | 2 | Pass | Returned every exact decision and explicitly reserved one slot for an integrator when two workers run. |
| Candidate | 3 | Pass | Returned every exact decision, including blocker override, lens reset, and both valid four-slot shapes. |
| Candidate | 4 | Pass | Returned every exact decision and left a spare slot for review replacement or challenge. |
| Candidate | 5 | Pass | Returned every exact decision and separated worker, integration, review, Repair, and successor-review waves. |

Every output was inspected against every rubric group; this judgment does not rely on string search alone.

## Judgment

- Control full-rubric failure rate: `5/5`
- Candidate full-rubric failure rate: `0/5`
- Candidate per-group failures: `0/30`
- Variance: controls disagreed on zero-reviewer degradation and structural routing; candidates converged on all decision-bearing predicates while varying only harmless scheduling phrasing
- Critical regressions observed: none

The candidate materially reduces the reproduced failures and eliminates decision-bearing variance in this scenario.

## Residual Gap

This is a read-only orchestration-decision evaluation, not a fault-injected scheduler benchmark. It proves the agents select a non-deadlocking four-slot shape and the exact degraded-capacity decisions. Runtime ledger transitions, receipt concurrency, Windows proof transport, and filesystem mutation ordering remain covered by executable tests rather than this wording evaluation.
