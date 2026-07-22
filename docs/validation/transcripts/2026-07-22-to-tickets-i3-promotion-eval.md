# To Tickets I3 Promotion Evaluation

Date: 2026-07-22

Decision: **promotion-ready** for the exact canonical To Tickets runtime hash
`E4D07BC78CD55E0DC5572105732800D2A6C1F2DCC6CF8D7DB1AB56C206653F1F`.

This record consolidates the completed I3 structural proof and E0 behavioral
sampling. It authorizes a later, separately bounded installation decision. It
does not install, synchronize a mirror, edit runtime or tests, or claim live
provider effectiveness.

## Authority And Scope

The evaluation covered only the load-bearing To Tickets semantic changes and
their integrated handoffs. Controls and candidates used fixed fixtures, fixed
root-held rubrics, five fresh samples per arm when an arm was admitted, no
mutation, and no downstream route execution. A candidate arm was not run when
the installed control already satisfied the claim.

The following residual claims remain outside promotion evidence:

- comparative economics when deciding whether support work should be separate;
- behavior against a live tracker provider.

## Fixed Identities And Runtime

### Candidate and proof hashes

| Surface | SHA-256 | Role |
| --- | --- | --- |
| Pre-blast-repair canonical `skills/custom/to-tickets/SKILL.md` | `CB934C4B1FA1EE375F172E90CF19EBC19E38FBCA717A002EE436EC9FCE975C0F` | Candidate used by all admitted clusters before the blast-radius ordering repair |
| Final canonical `skills/custom/to-tickets/SKILL.md` | `E4D07BC78CD55E0DC5572105732800D2A6C1F2DCC6CF8D7DB1AB56C206653F1F` | Promotion candidate; used only for the affected state/migration rerun after repair |
| Current structural proof `tests/test_skill_pack_contracts.py` | `BC6213A65BE6489DAC01BE90CB25863F3DA7A5FD2D95CB8C16B01BD417591D79` | Current structural assertions, including blast-radius ordering |
| Current To Tickets synthesis | `85B7E2D63178A736F47D2A4F4818E3CEB088CA5BBF7D027EE704E7E6005E7052` | Design authority read-back |

The pre-repair hash was frozen during I2 as a protected To Tickets hash and no
To Tickets runtime edit intervened before the bounded blast-radius repair. The
post-repair hash was recomputed from the current canonical file during this
consolidation pass.

### Installed-control hashes

The E4 integrated-handoff control froze every participating installed skill:

| Installed skill | SHA-256 |
| --- | --- |
| To Spec | `B7E05A55F30AA16A385360183281C516CF10223EC27F348C50F9039315BAC86E` |
| To Tickets | `DE1EE5CF231E2DDCC0C47CC20F9260B6EAE52D2C89FC52126C6B03F5C6835AAE` |
| Triage | `3A1CE646FD247181D3D4AE5758A55B1E16F0573A465D5B5DD8CE4F24636F3EC4` |
| Implement | `01A6C78E9D02A9951472B7D0A59479F4A2DB60A26184C337E876CCC20E0FE1B3` |
| Parallel Implement | `9523EC92901B97C9FC009C7C74B54A1D76D7ECEBB3F54597537FCA735A34E071` |
| Wayfinder | `2301B07E6C162CD3F8F946E4B7001E30FAD7137752C53518CFB171DF75958522` |

### Model, tier, and tools

- Model: every arm inherited the same session model without an override. The
  exact backend model identifier and build telemetry were not exposed and are
  unavailable.
- Tier: every arm inherited the same session tier without an override. Exact
  backend tier telemetry was not exposed and is unavailable.
- Tools: sampled workers were instructed to use no tools and made no mutation,
  dispatch, invocation, or auto-start. Root work was limited to fixture
  construction, frozen-hash read-back, rubric judgment, and aggregation.
- Repository state: the installed-control or canonical candidate named by the
  arm was frozen. Candidate arms changed only the supplied skill text; prompt,
  rubric, authority, tools, and repository snapshot stayed fixed.

These unavailable backend identifiers limit reproduction of the exact serving
environment, but do not create an arm-to-arm confound because no override was
introduced within a cluster.

## Fixed Prompt And Rubric Registry

The exact older worker prompt bodies and raw responses were not persisted and
have no durable locator. They are not reconstructed here. The surviving fixed
prompt contracts and pre-registered root rubrics are recorded below. Each
candidate arm reused its control fixture unchanged and replaced only the
installed control skill with the canonical candidate.

### E0-1: vertical slices, tracer bullets, and support work

Fixed task contract:

- default work must be a vertical delivery slice, not automatically a tracer;
- a genuine early-learning thin real path must still be recognized as a tracer;
- support and horizontal work must not regress.

Pre-registered candidate rubric:

- pass: `0/5` default-tracer errors, correct genuine-tracer recognition, and no
  support/horizontal regressions;
- evidence gap: `1/5` default-tracer error or inconsistent genuine-tracer
  recognition;
- fail: `2+/5` errors or any support/horizontal regression.

### E0-2: blockers, serial constraints, and ready-frontier truth

Fixed task contract:

- predecessor outcome consumed means a true blocker;
- overlap, order, or a shared resource without consumption is not a blocker;
- the graph is acyclic;
- the ready frontier excludes blocked, claimed, or unready work but includes
  dependency-ready work even when shared resources force serial execution;
- disjoint filenames do not prove independence.

Pre-registered candidate rubric:

- pass: ready frontier correct in `5/5`, with the other four invariants `5/5`;
- evidence gap: frontier correct in `4/5` with no other regression;
- fail: frontier correct in `3/5` or fewer, or any blocker, serial, cycle, or
  filename regression.

### E0-3: execution economics and parallel eligibility

Fixed task contract:

- tiny adjacent work stays serial or coalesced;
- substantial isolated work may be parallel-eligible;
- semantic ownership, production scope, proof seams, scarce resources, and
  serial tripwires can disqualify parallelism;
- the execution profile is complete;
- Parallel Implement retains runtime-width and worker-count authority.

Pre-registered candidate rubric:

- pass: runtime width and worker count explicitly assigned to
  `$parallel-implement` in `5/5`, while the other four results stay `5/5`;
- evidence gap: authority correct in `4/5` with no regression;
- fail: authority correct in `3/5` or fewer, or any economics/profile
  regression.

### E0-4: next-action routing

Fixed task contract:

- empty frontier returns the named blocker;
- explicit parent delivery recommends `$parallel-implement` regardless of
  initial width;
- one ready or serial-constrained ticket recommends `$implement`;
- multiple substantial independent tickets recommend `$parallel-implement`;
- uncertain economics or independence recommends the first ticket through
  `$implement`;
- exactly one recommendation is returned and not started.

A single installed-control failure was required to admit a candidate arm. The
control did not fail, so candidate improvement was not tested or credited.

### E0-5: admission, Source Trace, coverage, and ticket quality

Fixed task contract:

- material decision gaps stop before slicing or mutation;
- every source commitment receives exactly one owning disposition;
- no commitment is invented;
- tickets retain Source Trace, observable acceptance, meaningful proof, and
  scope fences;
- technique remains implementation-owned;
- separated support work names the actual delivery ticket, local proof, and
  comparative economic justification.

Candidate pass required all six criteria in `5/5`. Integration proof could
reference a commitment but could not duplicate its ownership, and support work
had to name the actual delivery ticket rather than an intermediate component.
Any `4/5` target result meant no material improvement; any regression in the
other four criteria failed the cluster.

### E0-6: state-boundary proof and compatibility migration

Fixed stateful-migration task contract:

- cover relevant initial, current, legacy, access-path, profile, and lifecycle
  branches;
- use meaningful branch proof rather than broad-suite substitution;
- preserve compatible Expand, operable/releasable Migrate, and delayed
  Contract;
- do not automatically treat migration phases as vertical product slices;
- keep blast-radius controls separate through exposure, health, and rollback;
- exclude irrelevant axes with evidence rather than blind enumeration.

Initial candidate rubric:

- pass: all six criteria `5/5`;
- evidence gap: blast-radius control `4/5` with no other regression;
- fail: blast-radius control `3/5` or fewer, or any other regression.

The clarified affected-rerun condition required health, compatibility, and
rollback evidence before advancing the risk-bearing backfill from `1%` to
`10%` to `100%`.

### E0-7: approval, publication, read-back, and recovery

Fixed provider-fixture task contract:

- exact proposal approval precedes mutation;
- material drift requires reconciliation and fresh approval;
- blockers publish first while parent intent and lifecycle remain preserved;
- read-back includes affected dependents and the resulting frontier;
- partial failure exposes applied, failed, and unknown state without duplicate
  retries;
- the result returns recovery state and stops before implementation.

Any installed-control failure was required to admit a candidate arm. No live
tracker mutation was in scope.

### E4: integrated handoffs

The fixed prompt used all seven cases below:

1. To Spec `S-11`: read-back omitted decision D4, metadata remained `Draft`,
   the draft still existed, and slicing was requested.
2. To Spec `S-12`: exact body and `Open` metadata read back, cleanup verified,
   and slicing was requested.
3. Triage `T-20`: a valid, verified, Ready-for-agent To Tickets packet with no
   explicit correction request.
4. Implement selection: `I1` and `I2` both Ready and tied by tracker policy,
   with no explicit target and valid shaping.
5. Implement shaping: explicitly selected `I3` lacked observable acceptance
   and a proof seam and combined three independent outcomes.
6. Parallel Implement `P-40`: `P1` was complete; `P2` was labeled Ready but
   lacked semantic owner, production scope and exclusions, public proof seam
   and focused proof, size, shared-resource declaration, serial tripwire, and
   supported stateful branches; none could be inferred.
7. Wayfinder `W-50`: closure was otherwise verified and had several candidate
   delivery slices, but no source-traced parent specification; that parent was
   the next durable artifact.

The rubric required verified parent publication before To Tickets, no retriage
of valid output, local Implement selection ambiguity, only shaping-defect
returns, a complete Parallel Implement execution profile with no partial
dispatch, Wayfinder closure through To Spec, and every explicit-only successor
recommended at most once and never started.

## Results And Claim Dispositions

`P` means the root-held semantic rubric passed. `F` means at least one target
criterion failed. `—` means the arm was correctly not run. Where raw outputs
are unavailable, sample identities are intentionally not invented.

| Cluster | Installed control | Canonical candidate | Disposition |
| --- | --- | --- | --- |
| E0-1 slices/tracers/support | `2/5` default-tracer errors; control failure established | `5/5` pass on every registered criterion | Accept improvement |
| E0-2 blockers/serial/frontier | Red control; isolated frontier failure, exact failing-sample count unavailable | `5/5` frontier and `5/5` other invariants | Accept improvement |
| E0-3 economics/parallel authority | Red control; isolated runtime-width/worker-count ownership failure, exact failing-sample count unavailable | `5/5` authority and `5/5` preserved economics/profile criteria | Accept improvement |
| E0-4 next-action routing | `5/5` pass | — | No control failure; structural ownership only, no behavioral-improvement credit |
| E0-5 admission/coverage/quality | Red control with one linked coverage/support failure; exact failing-sample count unavailable | `5/5` on all six criteria | Accept improvement |
| E0-6 state/migration | Red control isolated to blast-radius timing; exact failing-sample count unavailable | Initial candidate `4/5` blast timing and `5/5` otherwise; repaired candidate `5/5` on all six | Accept repaired improvement |
| E0-7 approval/publication/recovery | `5/5` pass | — | No control failure; structural/no-op, no behavioral-improvement credit |
| E4 integrated handoffs | `5/5` pass on all six handoff criteria | — | No control failure; structural/no-op, no behavioral-improvement credit |

The control failure counts intentionally establish existence, not prevalence.

### Per-sample availability

Raw E0-1 through E0-7 worker outputs were ephemeral and are unavailable. No
durable transcript, worker identifier, or exact raw-output locator survived;
this record therefore preserves only the contemporaneous root judgments and
aggregates above. It does not reconstruct individual samples.

The five E4 raw outputs remained available in the active task at consolidation
time. Their semantic decisions are transcribed below; formatting emphasis was
removed, but no decision was added:

| Sample | A1 | A2 | B | C1 | C2 | D | E |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Failed read-back; retain draft; report missing D4 and wrong Draft state; no slicing successor | Return S-12; recommend To Tickets; not started | Accept Ready; no retriage; recommend Implement; not started | Ask for explicit I1/I2 target locally | Return unsliced I3 with acceptance/proof/splitting defects; recommend To Tickets; not started | Reject graph; dispatch nothing; exhaustive P2 repair; recommend To Tickets; not started | Recommend To Spec once; not started |
| C2 | Retain draft and repair D4/Open read-back; no successor | Return S-12; recommend To Tickets; not started | Accept Ready; no retriage; recommend Implement; not started | Ask for one explicit target locally | Return unsliced I3 with acceptance/proof/splitting defects; recommend To Tickets; not started | Dispatch nothing; exhaustive repair; recommend To Tickets; not started | Return W-50; recommend To Spec; not started |
| C3 | Retain draft; report missing D4 and Draft state; no successor | Return S-12; recommend To Tickets once; not started | Accept Ready; no retriage or mutation; no successor | Ask for explicit target locally; no successor | Return I3 with shaping defects; recommend To Tickets once; not started | Dispatch nothing; exhaustive repair; recommend To Tickets once; not started | Recommend To Spec once; not started |
| C4 | Preserve draft; repair and reread missing D4/Open; no successor | Return S-12; recommend To Tickets; not started | Accept Ready; no retriage; recommend Implement; not started | Ask user to choose I1/I2 locally | Return I3 with all shaping defects; recommend To Tickets; not started | Reject graph; dispatch nothing; exhaustive repair; recommend To Tickets; not started | Recommend To Spec once; not started |
| C5 | Publication failed; repair S-11 and reread; no successor | Return control; recommend To Tickets; not started | Accept T-20 without correction or re-entry; no successor | Ask locally for explicit I1/I2 target | Return shaping-unready I3; recommend To Tickets; not started | Exhaustive repair for every missing field; recommend To Tickets; no partial dispatch | Recommend To Spec; not started |

All five E4 samples passed every required handoff criterion. The table is now
the durable locator for the available sample decisions; the original complete
worker prose was not separately persisted.

## Blast-Radius Repair And Affected Rerun

The first state/migration candidate arm met the pre-registered evidence-gap
condition: `4/5` applied blast-radius control at the right time, while every
other state and migration criterion remained `5/5`. The failing output exposed
a coherent ordering ambiguity: it checked health and rollback after completing
the migration instead of before expanding the risk-bearing backfill.

One bounded semantic repair changed only the canonical To Tickets runtime and
one structural assertion. The runtime now requires migration or backfill risk
to advance in batches through stable exposure boundaries and requires health,
compatibility, and rollback evidence before each expansion. The structural
assertion protects that ordering semantically rather than matching exact prose.

Only the affected five-sample state/migration candidate arm was rerun. Its
locked installed control was not rerun, and no other cluster was rerun. The
repaired candidate passed all six criteria in `5/5` samples. The promotion hash
is the resulting `E4D07...53F1F` canonical file.

## Worst Cases, Variance, And Protocol Notes

- E0-1 worst control: two of five samples defaulted to tracer terminology. The
  candidate had no registered error. Candidate support-work explanations still
  varied in comparative economic reasoning; that was not a pre-registered
  failure for the fixture.
- E0-2 worst control: at least one output omitted dependency-ready work from
  the frontier when a shared resource required serial execution. The candidate
  was `5/5` with no blocker, cycle, serial, or filename regression.
- E0-3 worst control: at least one output retained runtime-width or worker-count
  authority outside Parallel Implement. The candidate was `5/5`. One judgment
  was corrected when a recommendation was initially read as an invocation;
  the text had not started the successor, so no failure was charged.
- E0-4 had no control failure. Routing remained a structural ownership rule and
  received no candidate-improvement credit.
- E0-5 worst control linked duplicate/missing commitment ownership with support
  work naming an intermediate component rather than the delivery ticket. The
  candidate was `5/5`; the supplied fixture contained comparative facts, so it
  did not close the broader support-economics gap.
- E0-6 worst initial candidate delayed exposure health and rollback checks until
  after migration. The bounded repair removed that variance in the affected
  rerun.
- E0-7 had no control failure. It remains structural/no-op evidence, not a
  behavioral improvement claim.
- E4 had no semantic failure. The only observed variance was optional routing
  after valid Triage output: three samples recommended Implement and two
  stopped without a successor. Both behaviors preserved the tested
  no-retriage and no-auto-start boundary.

No sample mutated a tracker, invoked or dispatched implementation, synchronized
the installed mirror, or tested execution economics during a cluster that
excluded it.

## Canonical Validation Evidence

The completed I3 authoring and correction passes recorded:

- `59` focused contract tests passed for the bounded provider-parity repair;
- the full repository suite passed with `191 passed, 4 skipped`;
- `python -m scripts.validate_skills` passed;
- `git diff --check` and `git diff --cached --check` passed;
- the structural To Tickets test protects vertical/tracer/support distinctions,
  blockers versus serial constraints, the state matrix and execution profile,
  migration versus blast radius, exact approval and freshness, complete
  read-back and partial recovery, typed returns, routing priority, and the stop
  boundary;
- the blast-radius correction's focused structural assertion and full suite
  passed again; and
- the final canonical hash was read back as
  `E4D07BC78CD55E0DC5572105732800D2A6C1F2DCC6CF8D7DB1AB56C206653F1F`.

These checks establish canonical structure and repository consistency. They do
not independently establish behavioral effectiveness; the admitted behavioral
claims rely on the sampled clusters above.

## Residual Evidence Gaps

### Support-work comparative economics

- Limit: candidate outputs did not consistently explain why a separated
  support ticket was more economical than inclusion in its named delivery
  ticket when comparative facts were not supplied. The successful E0-5 fixture
  supplied those facts, so it cannot close the general judgment claim.
- Consequence: support work can satisfy ownership, naming, scope, and proof
  rules while the split-versus-inline economic judgment remains variably
  justified. Promotion must not claim improved comparative-economic judgment.
- Owner: Writing Great Skills owns a future isolated behavioral evaluation;
  To Tickets owns any later semantic repair only if that evaluation admits one.
  Parallel Implement continues to own runtime width, not this slicing choice.

### Live-provider publication and recovery

- Limit: approval, publication, read-back, affected-dependent, ready-frontier,
  and partial-recovery behavior used fixed provider fixtures. No GitHub,
  GitLab, or local tracker was mutated.
- Consequence: the evidence proves contract-shaped decisions, not provider API
  effects, idempotency behavior, receipt fidelity, or recovery under real
  transport failure. Promotion must not claim live-provider effectiveness.
- Owner: the tracker contract and provider operations own live mutation
  semantics; Writing Great Skills owns any later behavioral claim about skill
  use of those semantics. A future live-provider evaluation requires separate
  mutation authority.

Neither gap contradicts the admitted semantic improvements or the structural
no-op dispositions. Both remain explicit limits after promotion.

## Promotion Decision

**promotion-ready**

Promote only exact canonical hash
`E4D07BC78CD55E0DC5572105732800D2A6C1F2DCC6CF8D7DB1AB56C206653F1F`.
The candidate materially improved every cluster whose installed control
demonstrated an admitted failure, the sole evidence-gap cluster passed after one
bounded repair and affected-only rerun, and no control-clean cluster received
behavioral-improvement credit. Canonical proof passes, no sampled critical
regression remains, and the two residual gaps are bounded, owned, and excluded
from the promotion claim.

Installation and mirror synchronization remain separately authorized work.

## Installation Evidence

Installation date: 2026-07-22

Installation decision: **complete** for the dry-run-approved coordinated skill
cohort. No source edit, behavioral rerun, commit, or push was performed.

### Dry-run lock

The supported transactional installer reported:

```text
Managed skills: 25 in C:\Users\steve\.agents\skills
Updated skills: implement, parallel-implement, repo-bootstrap, to-tickets, triage, wayfinder
Unchanged skills: 19
Global bootstrap: present
```

The six proposed updates exactly matched the canonical skill directories with
changes in the authorized I2/I3 worktree. No unrelated managed skill or global
bootstrap change appeared, so installation was admitted.

### Synchronization

The transactional installation completed:

```text
Installed 25 custom skills into C:\Users\steve\.agents\skills
Global bootstrap: present
```

The installer synchronized the complete managed snapshot transactionally, but
only the six dry-run-listed skills changed. A post-install dry-run reported all
`25` managed skills unchanged and the global bootstrap still present.

### Canonical-to-installed parity

Installed-manifest tree hashes matched the canonical tree hashes for the full
managed pack. The changed cohort was:

| Skill | Canonical tree SHA-256 | Installed tree SHA-256 | Result |
| --- | --- | --- | --- |
| Implement | `ef2a52520462266ad0af171869d516c709ba57e737dcf9658e0a3cbb643af8bc` | `ef2a52520462266ad0af171869d516c709ba57e737dcf9658e0a3cbb643af8bc` | exact |
| Parallel Implement | `93c15edf0f386cc6f05b9a9320b7ad3b694eda6782d57675035bda964e4aaa5c` | `93c15edf0f386cc6f05b9a9320b7ad3b694eda6782d57675035bda964e4aaa5c` | exact |
| Repo Bootstrap | `2652077dcd3e6b7867bf83ccaff3fcef52c2d2cb6e07b9aa91fd0096614b232d` | `2652077dcd3e6b7867bf83ccaff3fcef52c2d2cb6e07b9aa91fd0096614b232d` | exact |
| To Tickets | `7ea48719bd9bae2993817c193b283c35a1b41bcd6132ef835b7288a9571808e8` | `7ea48719bd9bae2993817c193b283c35a1b41bcd6132ef835b7288a9571808e8` | exact |
| Triage | `db6a05911706ff858637a205bd35aeaeb36b0ddff3b2da34f8efb65f2fd5d678` | `db6a05911706ff858637a205bd35aeaeb36b0ddff3b2da34f8efb65f2fd5d678` | exact |
| Wayfinder | `400f0e26a65243d7e263150086b1df4362b43f57bf5fd62dff8e2572ae0e722e` | `400f0e26a65243d7e263150086b1df4362b43f57bf5fd62dff8e2572ae0e722e` | exact |

The To Tickets canonical and installed `SKILL.md` file hash is the accepted
promotion hash
`E4D07BC78CD55E0DC5572105732800D2A6C1F2DCC6CF8D7DB1AB56C206653F1F`.

### Post-install verification

```text
python -m scripts.validate_skills \
  --installed-root C:\Users\steve\.agents\skills \
  --require-installed
Skill validation passed.

python -m scripts.install_skills --dry-run
Managed skills: 25 in C:\Users\steve\.agents\skills
Unchanged skills: 25
Global bootstrap: present

git diff --check
passed

git diff --cached --check
passed
```

This installation establishes canonical-to-installed byte parity for the
accepted cohort. It does not widen the behavioral claims or close the recorded
support-economics and live-provider residual gaps.
