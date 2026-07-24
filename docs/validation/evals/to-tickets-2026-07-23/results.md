# To Tickets Prompt 4 Evaluation Results

## Terminal Continuation

This file preserves the original `needs-more-evidence` judgment and its
contaminated captures as history. Deploy Prompt 4 subsequently resumed with
clean worker/evaluator isolation. The authoritative terminal result is
[`isolation-v2/results.md`](isolation-v2/results.md):

- decision `accepted`;
- H1-01 `rejected-no-control-deficit`;
- H1-02 `rejected-regression`;
- H1-03 `rejected-no-control-deficit`; and
- V1 exact M0 package
  `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9`.

## Decision

`needs-more-evidence`

The exact M0 runtime passes the complete semantic viability suite. No H1 unit
is accepted or rejected because every fixed comparative fixture exposes
candidate behavior in the worker-visible `expected_output_boundary`. This
violates the uncontaminated-control requirement in
`writing-great-skills/BEHAVIOR-EVALS.md`. V1 remains unset.

## Identity Read-Back

| Input | Exact SHA-256 | Result |
| --- | --- | --- |
| Git `HEAD` | `dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6` | Unchanged before evaluation |
| M0 checkpoint payload | `c4238c81fa861543f492de8db11e5111c8517e4fa071aaf6628b286b2ad90a2f` | Match |
| Research note | `89e871beb4aec140bd4e5b1e4a69f753f6353ef50a187a91cdb0162aee512363` | Match |
| M0 package tree | `c226ca3541cf336fa606799b5e9f7ca538609575e3d73576bacbfda728bff7e9` | Match |
| H1 package tree | `73e2e5ec0d721251abdccf828937f025738d21da85661c15cc6115f011752bdf` | Match |
| Candidate workspace | `ec6f18308521d750966908308be6b1b3bbded9d0c0a444802f92b96d77d52d3c` | Match |
| Current canonical | `f652f1fb12787a482dcde59771e7b50f8dd5f7a890981df6acede35dc8a47758` | Comparison only |
| Protocol | `dc677c12b2058f34611301dc38a051facad058cca3c04765f49df56bf24a5a49` | Match |
| Runtime fixture | `1da11d50b70313f8f04c16ab40699a90b8fd6a0cad602ae60dfccde39cb6d8fe` | Match |
| Tracker fixture | `5a860ffb76f82965ca19ad2ad763f8e2db31a12d70540b3e6fe527993898683a` | Match |
| M0 fixture | `b3cfc9863f2fa8d7c6a0eaa912fa2d6c398eb429eb7a02444c7bf5e29df8e3e7` | Match |
| H1 fixture | `3e7604d1bb279f0928b524bd5d23348121716e4d8e92e7f470ae975f481ae675` | Match |

No runtime, protocol, fixture, manifest, relationship, canonical, installed,
or test byte changed during Prompt 4.

## M0 Intent-Fidelity Audit

Every instruction-bearing M0 passage maps to one frozen unit `M0-01` through
`M0-13`. The runtime contains the cheapest neutral local behavior needed for
the settled outcome, setup gate, Source Trace, exhaustive coverage, bounded
slicing, Ready contract, dependency graph, execution profiles, state matrix,
pre-mutation freeze, ordered publication, read-back, stopped recommendation,
and typed completion.

The M0 runtime does not contain:

- proposal-revision approval or stale-approval behavior from `H1-01`;
- the minimum-sufficient-detail steering sentence from `H1-02`;
- provider-native idempotency, correlation keys, or reconcile-before-retry
  behavior from `H1-03`; or
- current-only automatic parallel routing, tracer-purpose, progressive
  exposure, or blind retry behavior.

Result: no intent leakage, research leakage, current-only behavior, or
beyond-minimum unit was found. No M0 repair or refreeze was needed.

## Complete M0 Viability Suite

Each row is one fresh exact-M0 context. `Pass` means the root inspected the
complete response and operation log against the registered semantic rubric.

| Case | Result | Root judgment |
| --- | --- | --- |
| `V-01` | Pass | Two Ready tickets cover every commitment once; exact blocker `T-101 -> T-102`; frontier `[T-101]`; exact read-back |
| `V-02` | Pass | Two standalone Ready tickets; no fabricated parent or parent-delivery route |
| `V-03` | Pass | Exact channel-scope decision and both affected commitments; zero mutations |
| `V-04` | Pass | Exact missing blocker representation; `$repo-bootstrap`; zero mutations |
| `V-05` | Pass with deviation | Complete distinct snapshot matrix and proof; worker preserved state because prompt forbids publication while boundary requires it |
| `V-06` | Pass with deviation | `not applicable` matrix with pure/stateless reason; worker preserved state under the same publication contradiction |
| `V-07` | Pass | Profiles expose shared semantic owner and scarce fixture; `$implement`; no delivery start |
| `V-08` | Pass | Explicit parent-delivery authority routes verified parent to `$parallel-implement`; stopped |
| `V-09` | Pass | Three independent items, no `$parallel-implement`, recommendation `none` |
| `V-10` | Pass | Cycle and false-ready risk named; no Ready node or mutation |
| `V-11` | Pass | Applied first create, failed second create, affected frontier and nonduplicating recovery; no completion claim |
| `V-12` | Pass | Backlog/readiness mismatch blocks completion despite successful receipts |
| `V-13` | Pass | Unsupported folder-preparation slice rejected; behavior ticket owns observable folder creation |
| `V-14` | Pass | C1 ticket, C2 explicit deferral, C3 exclusion; no unauthorized work |
| `V-15` | Pass | Verified no-delta coverage result; zero mutations; `none` |
| `V-16` | Pass | Exact ordered IDs, `T-161 -> T-162`, frontier `[T-161,T-163]`, profiles, matrices, and read-back |

Aggregate: `16/16` semantic passes, `0` critical failures, `2` protocol
deviations. Worst case: `V-05`/`V-06` could not satisfy both contradictory
publication instructions; the conservative no-mutation response protected
authority and still established the registered matrix behavior.

## H1 Comparative Controls

### `H1-01` Exact-Revision Approval

Contribution mode: `quality-lift`.

Registered deficit: M0 publishes or claims publication-ready without authority
over the exact derived revision.

| Sample | A absent | B exact | C stale | D drift | E no-ticket | Observed deficit |
| --- | --- | --- | --- | --- | --- | --- |
| M0-01 | Stop, 0 mutation | Publish PR-41 | Stop, 0 mutation | Stop, 0 mutation | No-ticket | No |
| M0-02 | Stop, 0 mutation | Publish PR-41 | Stop, 0 mutation | Stop, 0 mutation | No-ticket | No |
| M0-03 | Stop, 0 mutation | Publish PR-41 | Stop, 0 mutation | Stop, 0 mutation | No-ticket | No |
| M0-04 | Stop, 0 mutation | Publish PR-41 | Stop, 0 mutation | Stop, 0 mutation | No-ticket | No |
| M0-05 | Stop, 0 mutation | Publish PR-41 | Stop, 0 mutation | Stop, 0 mutation | No-ticket | No |

Aggregate: registered deficit `0/5`; exact M0 behavior was viable in `5/5`.
Variance: none on the authority decision. Worst case: none. Critical failures:
none. H1 samples were correctly not run.

Decision-bearing deviation: the fixed worker-visible boundary says A/C/D
“must stop before mutation under H1.” The controls therefore received the
candidate conclusion. `rejected-no-control-deficit` cannot be admitted from
these samples; the unit remains provisional.

### `H1-02` Minimum-Sufficient Ticket Information

Contribution mode: `quality-lift`.

Registered deficit: complete M0 tickets retain irrelevant or duplicated load.

| Sample | M0 viability | Irrelevant source load retained | Registered deficit |
| --- | --- | --- | --- |
| M0-01 | Pass | Yes: ticket fences and coverage repeat narrative, mockups, renaming, tracker procedure, and pleasantries | Yes |
| M0-02 | Pass | Yes: both ticket bodies and coverage repeat the irrelevant set | Yes |
| M0-03 | Pass | Yes: ticket fences and coverage retain irrelevant material | Yes |
| M0-04 | Pass | Yes: coverage retains narrative, pleasantries, mockups, and tracker procedure | Yes |
| M0-05 | Pass | Yes: ticket fences, coverage, and operation-log body repeat the irrelevant set | Yes |

M0 aggregate: deficit `5/5`; all required migration, rollback, restart,
state-matrix, proof, and stateless-display facts survived.

| Sample | H1 viability | Irrelevant source load retained | Material lift |
| --- | --- | --- | --- |
| H1-01 | Pass | Yes: both ticket fences and coverage retain the irrelevant set | No |
| H1-02 | Pass | Yes: both ticket fences and coverage retain the irrelevant set | No |
| H1-03 | Pass | Yes: scope fence and coverage retain irrelevant material | No |
| H1-04 | Pass | Yes: bodies and coverage retain irrelevant material | No |
| H1-05 | Pass | Yes: body/coverage retain narrative and tracker procedure | No |

H1 aggregate: required facts survive `5/5`, but the registered signal-density
deficit also survives `5/5`. No material improvement is demonstrated.
Variance: output length and repetition vary materially, but the failure is
stable. Worst case: samples M0-01/M0-02 and H1-01/H1-02 duplicate the full
ticket payload again inside the operation log. Critical regressions: none.

Decision-bearing deviation: the fixed worker-visible boundary directly says
irrelevant history, speculation, pleasantries, and copied tracker procedure
must be absent. That is the comparative rubric outcome, so neither arm is an
uncontaminated sample. The observed H1 failure cannot establish a causal
`rejected-regression` disposition; the unit remains provisional.

### `H1-03` Correlated Publication Reconciliation

Contribution mode: `quality-lift`.

Registered deficit: M0 lacks deterministic nonduplicating recovery after an
ambiguous non-idempotent create.

| Sample | Native A | Exact match B | Zero C | Multiple D | Conflict E | Conclusive F | Observed deficit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0-01 | Native create | Reconcile | Partial/no retry | Partial/no retry | Partial/no retry | Failure/no retry | No |
| M0-02 | Native create | Reconcile | Partial/no retry | Partial/no retry | Partial/no retry | Failure/no retry | No |
| M0-03 | Native create | Reconcile | Partial/no retry | Partial/no retry | Partial/no retry | Failure/no retry | No |
| M0-04 | Native create | Reconcile | Partial/no retry | Partial/no retry | Partial/no retry | Failure/no retry | No |
| M0-05 | Native create | Reconcile | Partial/no retry | Partial/no retry | Partial/no retry | Failure/no retry | No |

Aggregate: registered deficit `0/5`; all samples made one create attempt,
queried correlation in B-F, reconciled one exact match, and made no blind
retry. H1 samples were correctly not run. Critical failures: none.

Variance: samples 01, 04, and 05 call A/B published while samples 02 and 03
return partial publication because the fixed tool surface omits separate
parent/role/state operations. The nonduplicating recovery decision is stable,
but the typed completion result is materially variant. Worst case: sample 03
returns partial for all six subcases.

Decision-bearing deviation: the fixed worker-visible boundary directly
prescribes native idempotency, exact-match reconciliation, partial recovery,
and no retry. The control receives the candidate conclusion.
`rejected-no-control-deficit` cannot be admitted; the unit remains
provisional.

## Protected And Structural Lanes

Deterministic inspection establishes:

- both runtimes remain explicit-only;
- every `M0-01` through `M0-13` passage remains present in both arms;
- only H1 contains the provisional approval, minimum-sufficient-detail, and
  correlation passages;
- owner pointers and the exact `$repo-bootstrap`, `$implement`, and
  `$parallel-implement` stopped triggers remain present;
- item-first publication, relationship/role/state order, read-back, safe
  partial Returns, and typed completion remain present; and
- relationship topology remains unchanged.

The Prompt 3 candidate verifier passes against the unchanged exact identities.
Structural proof does not cure the behavioral control contamination.

## Configuration, Telemetry, And Residuals

- Fixed configuration used: `gpt-5.6-sol`, high reasoning, Codex desktop,
  fresh independent context per sample, exact selected arm, fixture tracker,
  and fixture-scoped tools and mutation authority.
- Raw capture inventory: 36 files — 16 M0 viability, 15 M0 comparative
  controls, and five conditional H1 samples for `H1-02`.
- Capture normalization: eight Markdown hard-break trailing-space pairs in
  three raw files were removed after capture so the repository whitespace
  contract could pass; response text and operation-log meaning are unchanged.
- Available telemetry: declared model, reasoning effort, host, arm, fixture,
  complete response, and simulated operation log.
- Unavailable telemetry: backend model build, seed, temperature, sampling
  parameters, token counts, hidden system prompt, independent host attestation,
  and live-provider timing or consistency observations.
- Protocol deviations:
  1. `V-05` and `V-06` contradict publication authority at the fixed worker
     prompt/output boundary.
  2. Every H1 fixture exposes its candidate outcome through
     `expected_output_boundary`; this is decision-bearing control
     contamination.
  3. `H1-03` typed completion varies because the fixture asks for publication
     while omitting separate parent/role/state operations.
  4. Repository validation required nonsemantic trailing-space normalization
     in three otherwise complete raw captures.
- Residual transfer gap: behavior outside the exact model, host, reasoning,
  fixtures, tool surface, authority, and simulated connector remains unproved.
- Live-provider effectiveness, provider-native idempotency, correlation query
  semantics, eventual consistency, and duplicate avoidance remain unproved.

## Required Re-Registration

Keep the task, source packets, authority, tools, mutation observations, model,
host, reasoning, and rubrics fixed. Move evaluator outcomes and candidate
language out of worker-visible input; replace
`expected_output_boundary` with a neutral output-shape boundary; resolve the
`V-05`/`V-06` publication contradiction; and make `H1-03` publication
operations internally complete or explicitly partial. Refreeze protocol and
fixture identities, then rerun only affected Prompt 4 proof.

Until that evidence exists:

- M0 is viable but is not V1;
- H1 units remain provisional;
- exact M0, H1, workspace, current, and relationship identities stay
  unchanged;
- V1 and P1 are unset; and
- the Pruning Pass is not authorized.
