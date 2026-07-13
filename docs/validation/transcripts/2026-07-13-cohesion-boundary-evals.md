# Cohesion And Boundary Behavioral Evals

Date: 2026-07-13

Baseline: `d626637363a2258dbadea6555f696fd62aecfde3` plus the uncommitted cohesion implementation diff under review.

## Runtime And Confidence

- Runtime: current Codex desktop session with `codex-cli 0.144.0`; requested and resolved model details, reasoning settings, token use, latency, and cost were not exposed.
- Independent runner: available for fixture 28. The root started three direct fresh-context children with `fork_turns="none"`: `invocation_composition_audit`, `workflow_authority_audit`, and `context_validation_audit`. Each received the same factual pack frame plus one non-overlapping read-only evidence lane. The child tree contained no descendants.
- Contract simulation: fixtures 17-26 below record decisions recruited from current active source. They are contract coverage, not live workflow runs. Exact worktree, review, tracker, and conflicted-Git branches remain unexecuted where noted.
- Executable evidence: fixture 17 exercised the portable-owner validator contract; fixture 27 used injected filesystem failures, recovery, and an atomic competing-claim check in isolated pytest temporary directories; fixture 28 used live collaboration children followed by root verification.
- Fixtures 1-16 and the six requested end-to-end traces are recorded, with prompt, mutation, check, and residual-risk status, in [`2026-07-13-whole-pack-workflow-traces.md`](2026-07-13-whole-pack-workflow-traces.md).
- Repository fixture: the baseline above plus this uncommitted implementation diff.
- Dev environment: `requirements-dev.txt` resolves exactly `pytest 9.1.1`, `pytest-xdist 3.8.0`, and `PyYAML 6.0.3` in the repo `.venv`. The repo-owned validator is authoritative. The supplementary system `quick_validate.py` used for cross-checking had SHA-256 `5347a0a09cfb546bba1c0d1a30dae0a233d9a05f57bd4e7877155c588bcdabf7`.
- Mutations: the source pack and installed mirrors were intentionally updated before these passes. The prompt passes made no code, Git, tracker, or external mutation. Installer failure tests mutated only pytest temporary directories.

## Validation Baseline

```text
python -m pytest
106 passed, 4 skipped in 3.51s

python -m scripts.validate_skills --installed-root C:\Users\steve\.agents\skills --require-installed -v
Tracked files: 216
Skill folders: 25
Skill validation passed.

python -m scripts.install_skills --dry-run
Managed skills: 22 in C:\Users\steve\.agents\skills
Unchanged skills: 22
Global bootstrap: present

skill-creator quick_validate.py over skills/custom/* from the repo .venv
22 of 22 skills valid

python -m pip check
No broken requirements found.

git diff --check
git diff --cached --check
passed
```

The installed manifest SHA-256 was `ca5e2cfea7ceb061518622e3464c2901c1cbeb281a2f6c31abbb19e96fc85dd5` and recorded the complete source-tree hash set:

| Skill | SHA-256 |
| --- | --- |
| `codebase-design` | `34803b819b34c0af033c9881e0753c3ef3e29094bdef9172801ed831732675a3` |
| `convergent-pr-review` | `1ca78d72e143598c04ee5a005af8208197ebb26649c5a530a29c96393fce6bb3` |
| `diagnosing-bugs` | `5fac5920a53d29eb193c8850aa8ff40daf035f8c999cc862784aa7903d9fb589` |
| `domain-modeling` | `7b37fcab2ce1969d28f3ae8f5d756bc9d9a677185357fada3bb8f5e293840209` |
| `grill-with-docs` | `16324187b00683f86dd4dcfcf87ca982ee7c3545b311816d9a2d768872b0bbc2` |
| `grilling` | `62c84ff2e56f9f2b67bd4a34c60d9bca5c67f054aba5cce9416b7ef802d32351` |
| `handoff` | `a8d356c085c83dc3ac6a0dc130cf6f9d86a03f5b63f3be780b222e3af41005dd` |
| `implement` | `075280c0f98c9403ded92342f6245c8f061fb51cad5942d726ecf9d385dfa152` |
| `improve-codebase-architecture` | `a71e99e9dd0a478ca0092dd040c0a9a404d49c19e13c0fa1a2b89b773f1a7dbe` |
| `parallel-implement` | `f4e71732c62edf889c5935a7d47d167de12028bfa6db0098ca0b48661765552e` |
| `prototype` | `7699eb9b7a5fdb2c4f07976e2a6ea8ac2689ec7cad3bc1e786f87328f71b32dc` |
| `repo-bootstrap` | `01b1366d687284cefa5821201df0a7dd7da381c0257bbce0dd9679b21efb7d03` |
| `research` | `b3d22942a66b6ea5a553f8db5b06658e2addc1bad968319748c526e533c0ffbe` |
| `resolving-merge-conflicts` | `b010cba1f5a7b42b484785247b49187ba728732682ced83feea35f645749402e` |
| `review` | `a2d25840b831da0f07766ed6602f13f0f7a93034f01ba0b11c330202a588b0a4` |
| `skill-router` | `2e4c1a288ac1ea395de6afef0b6d2d658bfb11685c22b5eb3d04b84a1eb160b1` |
| `tdd` | `af62a382796bae044b68698f3c39b2e54e489cf04c1480d00963992f415b1dde` |
| `to-spec` | `556f1e42ac02d63413e0b4ef411ecf8a6d4cc805ca45f94cdd80f39cf9d2a7c3` |
| `to-tickets` | `db45166c203bb279ad5dbad9c03b695405fc5d2cf160e92c3bf2bd32307468f2` |
| `triage` | `31aeec15b232fcdfa4a364d5e953d4f0150ff98b9942ee844f34760eecb325ec` |
| `wayfinder` | `6f42eab1bffc91b919d990c42b5394630a756f2b561a070cbdc27cdcf1ff51ce` |
| `writing-great-skills` | `f8404380d4bff67b09724042fd6db68562d916e64342cc79781f96b11d6cdafd` |

## 17. Portable Fallback Adoption

Contract decision trace:

1. Inventory the portable title, owner-bearing preamble, generic engineering sections, verified commands, repo invariants, and settled setup choices.
2. Draft one installed-pack owner surface. Replace the portable title, owner preamble, and generic sections while preserving verified repo-specific material.
3. Show the exact setup delta and wait at the existing approval gate before file or tracker mutation.
4. After approved adoption, reject any `AGENTS.md` that still declares the portable owner.

Contract coverage: `6/6`. Critical failure in the simulated response: none. Behavioral run: not run.

Evidence: `test_portable_fallback_adoption_removes_the_portable_contract_owner` exercised both rejection of the portable owner and acceptance of an installed-pack primer. The setup-schema fingerprint and all three marker targets were refreshed.

## 18. Fresh-Context Convergent Review

Contract decision trace:

1. Pin one immutable review snapshot and build one complete reviewer brief.
2. Start each round-one reviewer as a direct child with `fork_turns="none"`; give it only the shared brief, assigned axis, lens, and output contract.
3. Keep parent hypotheses, preliminary findings, peer results, and the partial ledger out of round one. Reviewers inspect only and never fan out.
4. Wait for all requested lenses. Limit round two to named disputed ledger items, then verify survivors and drift at the root.

Contract coverage: `8/8`. Critical failure in the simulated response: none. Behavioral run: not run.

Residual risk: no live reviewer children sampled; independence and privacy are contract-verified only.

## 19. Parallel Worktree And Context Isolation

Contract decision trace:

- Treated context and checkout as **two isolations**. The root would create and preflight each detached worktree before dispatch.
- Each lane would be a direct fresh-context child with `fork_turns="none"`, an absolute assigned worktree, complete worker brief, and shell/edit boundary fixed to that checkout.
- A lane whose preflight resolves to the parent checkout, wrong base, or shared writer state blocks before edits. App-managed background tasks remain user-requested only.

Contract coverage: `7/7`. Critical failure in the simulated response: none. Behavioral run: not run.

Residual risk: no live child cwd or worktree behavior sampled.

## 20. Root-Owned Parallel Review

Contract decision trace:

- With four slots and a hot integrator, the slot lock reserves root plus integrator and admits two workers.
- Workers and integrator never spawn. The integrator lands serially, validates, returns a review-ready packet, and becomes idle.
- Only the orchestrator pins the candidate `HEAD`, invokes the selected formal review route, judges its return, and opens or keeps tracker Lock closed.

Contract coverage: `6/6`. Critical failure in the simulated response: none. Behavioral run: not run.

Residual risk: slot and agent-lifecycle enforcement were not exercised against a live collaboration runtime.

## 21. Convergent Review Decision

Contract response:

| Ledger | Decision |
| --- | --- |
| Current, full confidence, no blocker, no required skip | `pass` |
| Current, no blocker, reduced confidence or non-blocking `not checked` | `pass with residual risk` |
| Accepted blocker or provisional disputed / `not checked` blocker | `blocked` |
| Target, required lens, verification, required Spec, or drift gate unresolved | `incomplete` |

Disputed items remain visible in their axis. No `candidate` or `unverified` item may survive. The review root owns the decision; the caller owns residual-risk acceptance for Lock.

Contract coverage: `5/5`. Critical failure in the simulated response: none. Behavioral run: not run.

## 22. Parallel Recovery And Outcome

Contract decision trace:

- Reconcile the ledger with Git, worktree, agent, claim, and tracker state before dispatch; do not redispatch or reland reconciled events.
- Keep `needs-feedback` open for one delta and do not land it.
- Pause the partial cherry-pick, record exact Git state, and invoke `$resolving-merge-conflicts` only inside its authority boundary.
- Preserve dirty or uncommitted worker state when cleanup lacks authority. Return `partial` or `blocked` without inventing an approved closeout `HEAD`, completed review, tracker lock, or push.

Contract coverage: `7/7`. Critical failure in the simulated response: none. Behavioral run: not run.

Residual risk: no live stale ledger or partial Git operation sampled in this pass.

## 23. Disjoint Bug Routing

Contract response:

- If the exact symptom, cause, or trusted red-capable reproduction is uncertain, `$diagnosing-bugs` retains the causal evidence loop and original return owner.
- `$tdd` becomes eligible only when expected behavior, exact symptom, cause, and a trusted red-capable reproduction are known before Phase 1.
- `$implement`, both inner-loop skills, the router, and the composition map use that same fact set. The TDD test reference points back to the runtime owner instead of restating a weaker rule.

Contract coverage: `5/5`. Critical failure in the simulated response: none. Behavioral run: not run.

Evidence: `test_bug_routing_is_disjoint_and_non_bouncing` passed.

## 24. Required Spec Closeout

Contract response:

- `$implement` sends `Spec required: yes` with the selected item, acceptance criteria, Source Trace, fixed point, and immutable review tree.
- `$parallel-implement` sends `Spec required: yes` with the run Source Trace, selected items, acceptance criteria, fixed point, integration `HEAD`, and full diff.
- Either review route returns `incomplete` before review or reviewer dispatch when authoritative Spec cannot resolve; a risk lens cannot replace it and Lock stays closed.
- Standalone review defaults to `Spec required: no` and may explicitly skip only the optional Spec axis.

Contract coverage: `5/5`. Critical failure in the simulated response: none. Behavioral run: not run.

Evidence: `test_implementation_closeout_requires_the_spec_axis` passed.

The same contract test also verified that serial Lock accepts `pass with residual risk` only under named authority and that review-route handoffs preserve the caller's Spec requirement, sources, fixed point, and captured target.

## 25. Merge Conflict Read-Only Inspection

Contract response:

- Status, explanation, or review grants neither reconciliation nor finish authority.
- The resolver performs State and three-way Trace, reports both authorities, inspected paths, uncertainty, and exact remaining state, then stops.
- Files, index, commits, and Git-operation state remain unchanged. A separate request to resolve permits in-scope reconciliation; finishing remains separately authorized.

Contract coverage: `5/5`. Critical failure in the simulated response: none. Behavioral run: not run.

Evidence: `test_merge_conflict_resolution_is_three_way_and_finish_bounded` passed.

Authorized reconciliation now requires every in-scope entry to be reconciled. Any blocked path returns a blocked outcome and cannot satisfy reconciliation completion.

Residual risk: the read-only branch was contract-tested, not run against a live conflicted fixture.

## 26. Curated Fresh-Context Scouts

Contract response:

- Independence-bearing design, research, and architecture scouts start as direct fresh-context children with `fork_turns="none"` when supported.
- Each gets a complete factual frame, bounded pressure or evidence lane, mutation boundary, and output contract. Parent hypotheses, preferred answers, peers, editing, external mutation, and fan-out stay out.
- The main agent alone compares or synthesizes. Partitioned continuity work may fork only the minimum necessary recent context and is not described as independent.

Contract coverage: `6/6`. Critical failure in the simulated response: none. Behavioral run: not run.

Evidence: `test_independent_scouts_receive_curated_fresh_context` passed.

Residual risk: fixture 28 live-sampled the same direct-child, fresh-context, read-only, no-fan-out protocol for a pack audit. The exact design/research/architecture branches and continuity branch in this fixture remain contract-tested rather than live-sampled.

## 27. Transactional Pack Install

Executable failure injections covered:

1. second skill swap failure;
2. managed-skill retirement failure;
3. manifest write failure after replacement;
4. global-bootstrap write failure after replacement;
5. rollback restore failure followed by another install attempt against a deliberately corrupted manifest;
6. recovery from that preserved snapshot back to the byte-identical prior pack, followed by a successful current-source install;
7. corrupted backup snapshot rejection against persisted original digests;
8. process-level exclusion of concurrent recovery;
9. interruption during `preparing` followed by safe pre-mutation cleanup;
10. preparation failure plus transaction-cleanup failure, followed by safe recovery;
11. traversal-bearing manifest rejection;
12. conflicting unmanaged same-name preservation;
13. modified managed overwrite preservation;
14. modified managed retirement preservation;
15. different skill roots contending on one shared global bootstrap target;
16. an incomplete root-A transaction blocking root B through their shared global claim, followed by recovery and successful root-B install;
17. refusal to claim a byte-identical unmanaged same-name tree;
18. rejection of a forged transaction-prefix directory;
19. rejection of recovery state redirected to another global target;
20. rejection of omitted prior-snapshot metadata against the claimed immutable plan;
21. rejection of a post-mutation state downgraded to a pre-mutation phase while independent claims retain the mutation marker;
22. rejection of a global target inside the managed skills tree, including the manifest path;
23. rejection of global targets colliding with lock, claim, or transaction coordination paths before lock acquisition;
24. post-global-step manifest revalidation and full rollback after injected manifest corruption.
25. conservative recovery when a crash leaves mixed mutation markers across shared operation claims;
26. rejection of a managed skills root nested below the global target before either target is created;
27. refusal of symlink or Windows reparse entries, including a deterministic reparse-metadata test when live symlink creation is unavailable;
28. empty-directory drift detection while preserving format-1 hashes for ordinary file-only trees.
29. recovery refusal and snapshot preservation when a live skill, manifest, or global instruction file matches neither the prior nor planned identity;
30. preservation and pre-mutation refusal for pre-existing skill and manifest temporary-name collisions;
31. preservation and blocking of an orphaned operation claim whose transaction snapshot is missing;
32. lexical rejection of top-level target and coordination-entry symlink or reparse metadata before following it;
33. exclusive temporary creation plus atomic global-bootstrap replacement, including cleanup and rollback after an injected replace failure;
34. cleanup-only recovery of a verified committed transaction after claim cleanup fails.
35. post-crash preservation and refusal for unknown managed-tree and manifest temporary siblings;
36. atomic quarantine-and-verify when a live edit lands between identity checking and rollback;
37. installed-validator rejection of link or reparse metadata on the installed root and manifest;
38. a verified unchanged install returning without a transaction or rewrite;
39. reconciliation of verified preparing-state and transaction-state temporary files after crash boundaries.
40. cleanup of empty or truncated pre-mutation preparation residue and safe discard of a truncated pending state when the committed transaction state remains valid;
41. atomic displacement of updated and retired live trees into the owned transaction instead of recursive pre-terminal deletion;
42. persistence of `rolled-back` before recursive cleanup of complete rollback quarantines.
43. preservation and refusal when a post-crash edit changes an applied displacement inside the owned transaction.
44. recovery from a process interruption between atomic displacement of the prior tree and publication of the planned tree;
45. reconciliation of complete `rolled-back` or `recovery-incomplete` pending state written from a marker-bearing `prepared` transaction.

The first four restored every prior skill tree, retirement, manifest byte, and global instruction byte, then removed the transaction snapshot and operation claims. Updated and retired live trees moved atomically into the owned transaction; recovery recognized the valid missing-live gap between displacement and publication, and recursive cleanup began only after `committed` or `rolled-back` was durable. Unknown post-crash edits to those displacements were preserved and blocked recovery. The rollback-failure case persisted `rollback-incomplete`, original tree/file digests, exact errors, and claims in every mutated resource parent. A later root sharing the global target refused to install until recovery completed. Recovery rejected a corrupted backup, forged path, redirected target, altered immutable plan, and downgraded mutation phase without deleting the snapshot, then restored and verified the original prior pack after each injected fault was removed. Deterministically ordered OS-backed locks excluded concurrent operations; shared claims kept incomplete work visible after the locks released and independently bound mutation start. Target topology rejected managed-tree and coordination collisions before acquiring locks. Post-global verification reparsed the complete manifest and rolled back injected corruption. Empty or truncated preparation residue was safely cleared before mutation, and pending recovery outcomes from a marker-bearing `prepared` state reconciled against the immutable plan. The atomic active claim already contained `preparing` state, and unsafe manifest paths, every unmanaged same-name tree, or locally modified managed trees failed before mutation.

Executable coverage: `45/45` required outcomes. Critical failure: none.

Evidence: `tests/test_install_skills.py` returned 53 passed and three platform-skipped live-symlink tests; deterministic Windows target, coordination-entry, and tree reparse-metadata regressions ran. The full suite returned 106 passed and four platform-skipped live-symlink tests. Validator tests separately proved installed-manifest format, source, source-hash, required-manifest, entry-type, empty-directory, root/manifest redirect, unique setup-marker, and section-scoped portable-owner enforcement.

## 28. Skill-Authorized Delegation

Observed live decision trace:

1. Invocation of `$writing-great-skills` supplied delegation authority; the root did not ask for a second confirmation.
2. The root started three direct children with `fork_turns="none"`, the same factual pack brief, and distinct invocation/composition, workflow/authority, and context/validation evidence lanes.
3. Every lane was read-only, self-contained, excluded parent conclusions and peer results, prohibited fan-out, and returned evidence rather than an audit verdict owned by the child.
4. The root inspected the returned source locations, rejected or deferred unproven expansion, added RED tests for confirmed defects, implemented the fixes, and reran source and installed validation.
5. The collaboration tree showed exactly the root plus three completed direct children and no descendants.

Score: `7/7`. Critical failure: none.

Evidence: live child results; `test_writing_great_skills_authorizes_bounded_direct_subagents`; the portable-owner, composition, review-acceptance, manifest-integrity, recovery, and process-lock regressions; 106-pass full-suite and installed-mirror gates.

## Result

| Fixture | Coverage | Critical failure | Evidence mode |
| --- | ---: | --- | --- |
| Portable Fallback Adoption | 6/6 | None | Contract simulation plus validator test |
| Fresh-Context Convergent Review | 8/8 | None | Contract simulation only |
| Parallel Worktree And Context Isolation | 7/7 | None | Contract simulation only |
| Root-Owned Parallel Review | 6/6 | None | Contract simulation only |
| Convergent Review Decision | 5/5 | None | Contract simulation only |
| Parallel Recovery And Outcome | 7/7 | None | Contract simulation only |
| Disjoint Bug Routing | 5/5 | None | Contract simulation plus regression |
| Required Spec Closeout | 5/5 | None | Contract simulation plus regression |
| Merge Conflict Read-Only Inspection | 5/5 | None | Contract simulation plus regression |
| Curated Fresh-Context Scouts | 6/6 | None | Contract simulation; protocol live-sampled in fixture 28 |
| Transactional Pack Install | 45/45 | None | Executable filesystem/process tests |
| Skill-Authorized Delegation | 7/7 | None | Live |

Verdict: all twelve fixtures have complete current contract coverage without a simulated critical failure; only fixtures 27 and 28 are full executable/live behavioral runs. The strongest evidence is the live skill-authorized delegation run, executable installer safety/recovery matrix, 106-pass full suite, and source/mirror validation. Exact parallel-worktree execution, connector partial failure, live partial-Git recovery, serial Lock, and conflict reconciliation remain contract-verified rather than behaviorally executed in this audit.
