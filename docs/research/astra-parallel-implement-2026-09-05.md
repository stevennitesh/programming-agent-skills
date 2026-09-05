# Astra parallel implementation assessment

Date: 2026-09-05. Source rewrite and regression verification, not an agent
performance benchmark. Current candidate:
[parallel-implement](../../skills/astra/parallel-implement/SKILL.md).

## Decision

Keep parallel implementation as a specialist skill. Native agent tools supply
dispatch and status, but do not establish semantic independence, ownership of
shared runtime resources, valid integration evidence, or safe deletion authority.
Those are the value of this skill. Ordinary coding stays direct under the
engineering contract; there is no Astra implement prerequisite.

Keep the existing Python lane helper as a self-contained Astra copy, initially
byte-identical to custom, with the reviewed pending-receipt correction below.
Its size reflects tested destructive-operation and
recovery cases, not context agents must load. Rewriting it for brevity would
discard useful engineering without improving the common path. Both packages
run the same parameterized regression suite; future helper fixes must consider
both consumers. This avoids a runtime dependency on a removable custom skill.

The entrypoint owns admission, dispatch, landing, integrated proof, and completion.
Lane mechanics, exceptional recovery, and authorized tracker effects load only
at their triggers. Keep a compact root-owned run record and helper manifests;
do not introduce a scheduler service, multi-level planner hierarchy, or duplicate
state database for a bounded local delivery.

## Sources and selections

Compared local upstream snapshots; no upstream refresh was requested in this turn.

| Source | Snapshot | Useful selection / exclusion |
| --- | --- | --- |
| Custom parallel-implement, lane helper, references, tests | Existing checkout; fixes in `92c4816`, `535b642`, `9733d61` | Preserve frontier isolation, precise ownership, runtime paths, causal cross-item proof and recoverable cleanup. Remove stale implement/conflict skill prerequisites. |
| Matt Pocock engineering/implement | `3cca18b368ae95cdbdebbff572ccafa662551015` | Direct implementation is enough inside workers. Do not import mandatory TDD, final review, or implicit commits from a generic coding skill. |
| Pstack shared-state principle and poteto-mode orchestration/cleanup playbooks | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Separate mutable outputs first; use exclusive ownership when sharing is real. Bounded in-flight work and continuous draining. Exclude standing multi-day program machinery, fixed cloud/model policies, unconditional pushes, and forced worktree deletion. |
| Superpowers parallel dispatch, subagent-driven development, using-git-worktrees | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Fresh bounded context, explicit task returns, recognize host-managed isolation. Exclude mandatory per-item reviewers, fixed retry rounds, and a finishing-skill dependency. Host checkout isolation alone does not isolate sibling writers or provide helper cleanup receipts. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Reuse proven machinery and prefer serial execution when concurrency adds no value. Do not trade accepted scope or recovery safeguards for fewer lines. |
| Cursor plugins orchestrate handoffs (adjacent to Pstack) | Same cursor-plugins snapshot | Preserve partial failure evidence and bounded retries. Do not treat worker prose as verified state or import cloud/Slack infrastructure. |

## Failure-mode preservation map

| Failure or costly mistake | Candidate owner / evidence |
| --- | --- |
| Artificial file slices share behavior or proof | Admission checks behavior, callers, fixtures, config and external resources; enabling changes precede consumers. |
| Serial frontier pays unnecessary isolation cost | Exclusive integration checkout when no other writer; concurrent siblings use exact shared base; descendants use integrated predecessor HEAD. |
| Worker operates in wrong checkout or shares runtime | Exact worker packet, pre-mutation identity check, helper manifest paths and off-contract proof invalidation. |
| Dirty current checkout is swept into campaign | Preserve unrelated work; clean separate integration baseline or resolve prerequisite within authority. |
| Duplicate worker after silence/failure | Inspect, stop and confirm previous actor; exclusive custody before replacement; bounded host retry policy. |
| Dirty interrupted worker can neither resume nor safely disappear | Recovery distinguishes supervised repair of partial state from normal eligibility; preserve work and reinspect. |
| Serial worker commit applied twice | Verify in place; already landed. |
| Textually clean merge changes accepted meaning | Recheck intervening semantic/proof inputs, update same lane and rerun affected proof. |
| Cleanup rejects landed work after cherry-pick | Preserve commit ancestry using fast-forward/merge, not squash/cherry-pick. |
| Passing worker tests miss broken composition | Root passes actual produced/persisted result through real transformations and consumer; validates material failure paths. |
| Checkout normalization changes bytes/identities | Rerun affected proof in integration checkout. |
| Prepare partly fails or lane reuse targets wrong base | Exact-base/reuse checks, runtime probes, conservative rollback, retained partial-failure evidence. |
| Deletion targets dirty, unintegrated, nested, unregistered or redirected state | Named direct-child validation, manifests, clean/ancestry checks, reparse-point handling; retain uncertainty. |
| Runtime enumeration or cleanup fails | Preserve registered lane and recovery state; continue other named safe lanes; report exact failure. |
| Git removes worktree but reports an error or leaves residue | Registration/path read-back and durable receipt-based retry. |
| Receipt cannot be read back | Stop before unregistering; exact evidence survives. |
| Identity/ancestry drifts before unregistering | Helper rechecks repository/lane HEAD, registration, status and ancestry. |
| Access failure is mistaken for absence | `path_present` exposes errors other than FileNotFoundError; final verification treats uncertainty as failure. |
| Final HEAD changes after scan | Clear cleanup/retry actions and preserve unfinished lanes; prove and verify new candidate. |
| One lane or residual helper state omitted at finish | Root retains all packets; verify-cleanup receives entire explicit set at full proved commit ID. |
| Tracker duplicate claim, premature readiness or parent closure | Conditional live read-back, actual dependency outcomes, active-owner checks and complete-graph parent gate; subsets cannot close parent. |
| Ignored artifact or live process lost in cleanup | Root establishes ignored artifacts are disposable and confirms process/session quiescence; helper success cannot prove either. |

## Verification and limits

The 34 existing lane tests now run against both self-contained helpers, plus one
Astra-only regression for the new pending-receipt guard: 69 passed in 17.28 seconds
on Windows, including real Git worktree creation, integration, and cleanup plus
injected failure cases. Shared fixtures avoid duplicating test bodies. The 10
focused repository contract checks also passed. Skill package validation,
repository skill validation, all five local reference links, and both whitespace
checks passed on the final skill candidate.

The helper is not a sandbox, process supervisor, or multi-coordinator lock. Root
custody remains a precondition. Its runtime violation scan recognizes specific
cache locations, not every tool's side effect. It verifies the supplied lane set,
not forgotten packets. Review and tests do not establish agent-level adherence,
speedup, or immunity to unrelated concurrent filesystem mutation.

## Challenger reconciliation

Two fresh read-only challengers reviewed separate seams against a frozen candidate:
failure/recovery parity and orchestration/source coverage. Both rechecked the final
changes and reported no remaining blockers in their reviewed passages.

- Accepted: place ignored-artifact disposal checks on ordinary cleanup, not only
  in a recovery reference that a successful run might never load.
- Accepted: persist the compact root run record under run-scoped scratch and
  reconcile it with actual state after context loss before redispatch.
- Accepted: establish commit authority for any committing worker, including a
  serial worker, rather than covering concurrent lanes alone.
- Accepted after discussing the intended recovery path: a pending receipt can
  survive failed cleanup while runtime directories remain valid. The inherited
  helper could then report normal resume eligibility. Astra now requires an
  absent receipt for normal resume/landing; cleanup eligibility remains available.
  The added test exercises actual preparation, receipt persistence, CLI inspection,
  and successful cleanup retry. This is the only executable difference from custom.

The reviewers agreed that the remaining upstream ceremony did not justify adding
mandatory reviewer rounds, planner hierarchies, services, or publication defaults.
No commit, push, or global installation is part of this change.
