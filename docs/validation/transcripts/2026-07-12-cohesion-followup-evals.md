# Cohesion Follow-Up Behavioral Evals

Date: 2026-07-12

Baseline: `2449758fab65f2d11fec1a5d188661c003e1c75f`

## Runtime And Confidence

- Runtime: current Codex desktop session; requested and resolved model details,
  reasoning settings, token use, latency, and cost were not exposed.
- Independent runner: unavailable. `codex-cli 0.144.0` could not authenticate
  inside the sandbox, and the approved external run remained blocked by the
  private-workspace data boundary before sampling.
- Fallback: separated current-session passes. These passes are behavioral but
  non-independent, so confidence is reduced.
- Offline runner: unavailable; Ollama and LM Studio were not installed.
- Repository fixture baseline: the commit above plus the three uncommitted eval
  and active-status documentation changes under review.

## Skill Hashes

Each repo source matched its installed mirror before the passes.

| Skill | SHA-256 |
| --- | --- |
| `implement` | `947db1f8524dfc962ac28ba80d37d01c8eb7ba597a8bd557f56fcb71e2bad130` |
| `diagnosing-bugs` | `6d3a309f2e411731e1e58380c6e3f33eb2cc090515f3de0bb032b51f0b569959` |
| `to-spec` | `16866527dbadb669e38787de4d3cd87195806c945670f926d9cfb4566297de8a` |
| `codebase-design` | `ee08367b48ea214cc72349c98d1dfd5f868e295d611d9b7dbf7f631066e97fc2` |
| `review` | `ce57ebe178148d99f391d1fe0f727da0c1b32380f1d2fc9420d2a0b08a057b0a` |
| `convergent-pr-review` | `eb6c8101fbffd463bfec49a05c134d0cc5800a50a7bc484ec86eabef9f26548c` |
| `resolving-merge-conflicts` | `4fad93ce608a88b94f2a72ce63f4074acc011c37732abd4182adf47d0d315a56` |
| `repo-bootstrap` | `0a3652d978905d624b0de318909edf746c70df4bec298957dc19815a9ad42d10` |

## 12. Implement Selection Authority

Fixture: [Implement Selection Authority](../evals/core-workflows.md#12-implement-selection-authority)

Observed response:

- Parent-spec case: treated the spec as selection context, not implementation
  scope. Because no repo-visible policy selected one next item, the pass
  recommended `$to-tickets` and stopped before Context Intake or mutation.
- Explicit blocked-item case: stopped on item B, named its blocker, left ready
  item C unselected, and preserved tracker state.
- Neither case split, relabeled, promoted, reprioritized, substituted, or began
  implementation.

Score: `4/4`

Critical failure: none.

Evidence: the decision trace named one selection authority, one next owner, no
permitted mutation, and a stop before Context Intake in both branches.

Observed drift: none.

Follow-up: none.

## 13. Local Tracker Review Visibility

Fixture: [Local Tracker Review Visibility](../evals/core-workflows.md#13-local-tracker-review-visibility)

Observed response:

1. Stage the complete selected-work diff.
2. Add the provisional local closeout packet with `Review: pending`, set the
   item to `implemented`, release its claim, read it back, and stage the tracker
   file with the code.
3. Capture the immutable review tree and run exactly the selected review route
   over code and tracker state together.
4. Apply the first review finding, run targeted proof, refresh the provisional
   packet, restage the complete diff, capture a new review tree, and rerun the
   same review route.
5. After acceptance, replace only `Review: pending` with the actual result,
   read it back, restage, pass the delta and index locks, and commit the approved
   lock tree.

The response explicitly rejected committing `Review: pending` or adding the
tracker packet after formal review.

Score: `4/4`

Critical failure: none.

Evidence: the tracker packet entered the first review snapshot; the finding
created a new review target; the review-result field was the only post-acceptance
metadata delta.

Observed drift: none.

Follow-up: none.

## 14. Diagnosis Return Ownership

Fixture: [Diagnosis Return Ownership](../evals/core-workflows.md#14-diagnosis-return-ownership)

Observed response:

- Authorized implementation case: `$implement` retained owner status and
  invoked `$diagnosing-bugs` in fix mode. Diagnosis owned the tight loop,
  load-bearing repro, hypotheses, discriminating probes, cause gate, causal fix,
  regression proof, original-scenario proof, and cleanup. It then returned its
  packet to `$implement`, which retained review, staging, one commit, tracker
  closeout, and Lock.
- Standalone diagnosis-only case: diagnosis could use only reversible
  instrumentation and disposable `.tmp/` evidence. It retained no production
  behavior change, returned the diagnosis packet, recommended `$implement` as
  the one next owner, and stopped.

Score: `5/5`

Critical failure: none.

Evidence: both branches named one return owner and kept review, commit, and
tracker mutations outside diagnosis.

Observed drift: none.

Follow-up: none.

## 15. Composition Verb Semantics

Fixture: [Composition Verb Semantics](../evals/core-workflows.md#15-composition-verb-semantics)

Observed response:

- Parent-spec case: `$to-spec` **Loads** `$codebase-design` vocabulary. The
  design reference supplies `deep module`, `interface`, `seam`, `adapter`,
  `depth`, `leverage`, and `locality`; it does not emit a design packet.
  `$to-spec` retains source trace, proof seam, parent-spec publication,
  read-back, and completion ownership.
- High-risk PR case: `$review` **Hands off** to
  `$convergent-pr-review` and stops. The callee owns the pinned snapshot,
  reviewer passes, ledger, survivor verification, drift check, and final review
  report. The caller does not run a duplicate ordinary review or resume.

Score: `5/5`

Critical failure: none.

Evidence: each case used one declared composition verb, one output owner, and
one completion owner.

Observed drift: none.

Follow-up: none.

## 16. Merge Conflict Finish Boundary

Fixture: [Merge Conflict Finish Boundary](../evals/core-workflows.md#16-merge-conflict-finish-boundary)

Fixture commits:

- base `f646c11`: addition only;
- current `1815a1c`: subtraction branch intent;
- merging `19891be`: multiplication branch intent.

State evidence before reconciliation:

```text
## main
UU calculator.py
A  test_multiply.py
```

`git ls-files -u` exposed stages 1, 2, and 3 for `calculator.py`. Source trace
showed the base addition behavior, current-side subtraction behavior, and
merging-side multiplication behavior. The operation was a merge, so `ours` was
the current `main` result and `theirs` was `feature`.

Observed mutation: edited only `calculator.py` and preserved all three
operations behind one `calculate` function. No `git add`, commit, abort, or
continuation command ran. The merge-created staged addition of
`test_multiply.py` was left untouched.

Proof:

```text
Ran 3 tests in 0.000s
OK
No conflict markers
git diff --check: passed
```

Remaining state:

```text
## main
UU calculator.py
A  test_multiply.py
```

The worktree file was reconciled, while the index remained unmerged and the
merge remained in progress exactly because finish authority was withheld.

Score: `6/6`

Critical failure: none.

Observed drift: none.

Follow-up: none.

## 17. Portable Fallback Adoption

Fixture: [Portable Fallback Adoption](../evals/core-workflows.md#17-portable-fallback-adoption)

Inventory evidence:

- no remote and no existing installed-pack setup marker;
- `AGENTS.md` carried the `Portable Engineering Contract` heading;
- verified commands: `python -m unittest discover tests` and
  `git diff --check`;
- preserved invariants: integer-cent monetary values and the `ledger` package
  as the public interface;
- Local Markdown tracker, default local status vocabulary, and single-context
  domain layout were supplied as settled choices;
- `docs/agents/` and `CONTEXT.md` were absent;
- `.tmp/` was ignored and `.scratch/` remained trackable;
- the recorded test command passed one test.

Exact proposed `AGENTS.md`:

```markdown
# Repository Instructions

## Commands

- Focused and full tests: `python -m unittest discover tests`
- Whitespace: `git diff --check`

## Repository Invariants

- Keep monetary values as integer cents.
- Preserve the `ledger` package as the public interface.

## Agent skills

<!-- programming-agent-skills setup-schema: 1:427ef8595173 -->

This repo uses the Programming Agent Skills engineering pack.

AGENTS primes. Repo-local docs teach. Skills execute.

Before nontrivial coding, read `docs/agents/engineering-contract.md`.

### Pointers

- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label roles: `docs/agents/triage-labels.md`
- Domain docs and ADR routing: `docs/agents/domain.md`
- Engineering contract: `docs/agents/engineering-contract.md`
```

Exact proposed local contracts:

| Target | Source and transformation | SHA-256 before transformation |
| --- | --- | --- |
| `docs/agents/issue-tracker.md` | Byte-for-byte `skills/custom/repo-bootstrap/issue-tracker-local.md` | `544358eb4c0392a9b3b21bd4725d077b2cc0cc41ab4d46730e1f314236246bc7` |
| `docs/agents/triage-labels.md` | Byte-for-byte `skills/custom/repo-bootstrap/triage-labels.md` | `44059f0e8016ce5c7f4081d34db6af3453e9e8ccd42f73f3513ca846693102d0` |
| `docs/agents/domain.md` | `skills/custom/repo-bootstrap/domain.md` with `<single-context \| multi-context>` replaced by `single-context` | `ead167c8bedea51d978c7ef37e89272d81806d4fa832a5fb1b7d14312f2a51ba` |
| `docs/agents/engineering-contract.md` | Byte-for-byte `skills/custom/repo-bootstrap/engineering-contract.md` | `3faa0a2b59ee573af6988d24b3d0890614f14eaef4eba454dce98394cdd87ed3` |

`.gitignore` needs no delta: `.tmp/` is already ignored and `.scratch/` is
trackable. Local Markdown creates no external labels. Provisioning would wait
for approval, then verification would run `validate_setup.py`, smoke-read the
local tracker surface, run `python -m unittest discover tests`, run
`git diff --check`, and read back every changed file.

Mutation evidence:

```text
before tree: 4e1c1d3dc0754b5766a09d993b99fe0d88610c9e
after tree:  4e1c1d3dc0754b5766a09d993b99fe0d88610c9e
before AGENTS.md sha256: 37467b407bf7a3ffbfc714db991e8e42e367f8fa25f0ba2c7a42940f4c4bb19a
after AGENTS.md sha256:  37467b407bf7a3ffbfc714db991e8e42e367f8fa25f0ba2c7a42940f4c4bb19a
git status: clean
```

The pass stopped at Draft. It did not keep two contract owners, reopen settled
choices, write target files, or claim setup complete.

Score: `5/5`

Critical failure: none.

Observed drift: none.

Follow-up: none.

## Result

| Fixture | Score | Critical failure | Runtime change |
| --- | ---: | --- | --- |
| Implement Selection Authority | 4/4 | None | None |
| Local Tracker Review Visibility | 4/4 | None | None |
| Diagnosis Return Ownership | 5/5 | None | None |
| Composition Verb Semantics | 5/5 | None | None |
| Merge Conflict Finish Boundary | 6/6 | None | None |
| Portable Fallback Adoption | 5/5 | None | None |

Verdict: all six focused fixtures passed without a critical failure. No runtime
skill wording or invocation-policy change is supported by this evidence.

Residual risk: the passes were separated but not independent. Rerun the same
fixtures with an isolated external or offline agent when the workspace policy
permits a sanitized runner; use this record as the comparison baseline.
