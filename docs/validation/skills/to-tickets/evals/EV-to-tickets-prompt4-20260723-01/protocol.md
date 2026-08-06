# To Tickets M0/H1 Evaluation Protocol

## Fixed Runtime Configuration

All behavioral cases use exact model `gpt-5.6-sol`, Codex desktop
fresh-context workers, `high` reasoning, and the exact runtime configuration
in `fixtures/runtime.json`. Give each worker only the selected exact To Tickets
arm, `fixtures/tracker-contract.md`, and the selected immutable fixture object
from `fixtures/m0.json` or `fixtures/h1.json`. The fixture object's
`worker_prompt`, `context`, `source_packet`, `tracker_state`,
`tracker_observations`, authority, permitted tools and mutations, and
`expected_output_boundary` are the complete task context and evidence.

The rubric, expected weakness, hypothesis name, synthesis, research, candidate
conclusions, other arm, and prior outputs remain root-held and are never
included in worker context. If the fixed model, host, reasoning configuration,
fresh-context isolation, or exact tool surface is unavailable, record the
observed telemetry and return `evidence-gap`; do not silently substitute it.

Authority is fixed to a simulated source owner who may settle source and
authorize publication, while To Tickets owns only slicing, readiness,
dependency order, profiles, proposal identity, and publication judgment.
Evidence is exactly the selected immutable fixture composition above. Runtime
is a fresh candidate-loaded Codex session with no ambient target-current or
campaign context.

### Immutable Fixture Inventory

| Path | SHA-256 | Bytes | Contents |
| --- | --- | ---: | --- |
| `fixtures/runtime.json` | `1da11d50b70313f8f04c16ab40699a90b8fd6a0cad602ae60dfccde39cb6d8fe` | 1411 | Fixed model, effort, host, isolation, tools, authority, sample, and capture policy |
| `fixtures/tracker-contract.md` | `5a860ffb76f82965ca19ad2ad763f8e2db31a12d70540b3e6fe527993898683a` | 1680 | Complete simulated tracker operations and mutation boundary |
| `fixtures/m0.json` | `b3cfc9863f2fa8d7c6a0eaa912fa2d6c398eb429eb7a02444c7bf5e29df8e3e7` | 24575 | Exact `V-01` through `V-16` worker packets |
| `fixtures/h1.json` | `3e7604d1bb279f0928b524bd5d23348121716e4d8e92e7f470ae975f481ae675` | 7182 | Exact `H1-01` through `H1-03` comparative packets |

## Complete M0 Viability Suite

Use exact M0 for every case. Each task supplies a compatible local tracker
fixture unless the case tests setup failure. Tools are read-only repository
inspection plus a deterministic in-memory tracker connector that records
create, relationship, role/state, refetch, and query operations. Mutation
authority is fixture-scoped only.

| ID | Fixed task | Rubric | Wrong condition |
| --- | --- | --- | --- |
| `V-01` | Exact `V-01` object in `fixtures/m0.json` | All commitments map once; two Ready tickets preserve source; one true blocker and correct frontier read back. | Mere order or likely overlap becomes a blocker. |
| `V-02` | Exact `V-02` object in `fixtures/m0.json` | Produce Ready standalone tickets without fabricating a parent or parent-delivery route. | Absence of parent is treated as source failure. |
| `V-03` | Exact `V-03` object in `fixtures/m0.json` | Return the exact decision and affected slices; tracker mutation count is zero. | Nonblocking note is mistaken for a commitment gap. |
| `V-04` | Exact `V-04` object in `fixtures/m0.json` | Name the exact surface, recommend `$repo-bootstrap`, and leave source/tracker unchanged. | Compatible optional capability is treated as required. |
| `V-05` | Exact `V-05` object in `fixtures/m0.json` | Ticket records each distinct supported branch and proof obligation. | Equivalent branches are expanded into combinatorial ceremony. |
| `V-06` | Exact `V-06` object in `fixtures/m0.json` | Matrix is `not applicable` with a concrete reason. | Stateful behavior silently omits a matrix. |
| `V-07` | Exact `V-07` object in `fixtures/m0.json` | Profiles expose the constraint; route the first ready item to `$implement`; start nothing. | Different filenames imply concurrency. |
| `V-08` | Exact `V-08` object in `fixtures/m0.json` | Recommend `$parallel-implement` with the parent and stop. | A standalone or empty graph receives the parent route. |
| `V-09` | Exact `V-09` object in `fixtures/m0.json` | Do not recommend or invoke `$parallel-implement`; choose `$implement` or `none` under the fixed route rules. | Apparent width creates delivery authority. |
| `V-10` | Exact `V-10` object in `fixtures/m0.json` | Keep the graph non-complete; label no defective node ready; publish nothing ready. | Tracker order is used to conceal the defect. |
| `V-11` | Exact `V-11` object in `fixtures/m0.json` | Report applied/failed operations, affected dependents/frontier, and safest recovery without completion claim. | Retry or success is inferred from a receipt. |
| `V-12` | Exact `V-12` object in `fixtures/m0.json` | Report the exact mismatch and block completion. | Provider receipt substitutes for refetch. |
| `V-13` | Exact `V-13` object in `fixtures/m0.json` | Reject the slice before mutation. | Necessary observable migration is rejected merely for being technical. |
| `V-14` | Exact `V-14` object in `fixtures/m0.json` | Coverage records both dispositions without unauthorized tickets. | Deferral silently disappears from coverage. |
| `V-15` | Exact `V-15` object in `fixtures/m0.json` | Return the coverage result, no tracker mutation, and `none`. | Empty output is called a source gap. |
| `V-16` | Exact `V-16` object in `fixtures/m0.json` | Return source/parent, ordered IDs, graph/frontier, profiles/matrices, exact read-back, and one valid stopped recommendation. | Any partial or mismatched state is called complete. |

Critical M0 failures are mutation before setup/source/graph gates, lost
commitment coverage, a false-ready frontier, missing required ticket facts,
incorrect owner invocation, blind mutation recovery, or a completion claim
without exact read-back. M0 must pass every scenario before any H1 arm runs.

## H1 Comparative Controls

Each cluster uses the fixed common configuration above, alternates exact M0 and
H1 arms, and runs at least five fresh M0 samples first. Run H1 only when the
registered M0 deficit appears. Each arm gets only the fixed task, authority,
evidence, runtime, and tools below; the rubric and expected weakness remain
root-held evaluator material.

### `H1-01` Exact-Revision Approval

- Task/context/evidence: exact `H1-01` object in `fixtures/h1.json`; each sample
  evaluates its five fixed labeled subcases.
- Tools: repository reads and mutation-spy tracker connector.
- Expected M0 weakness: publication or publication-ready claim without
  authority over the exact derived revision.
- Rubric: preserve every M0 requirement; mutate in `0/5` absent/stale cases;
  accept exact supplied approval in `5/5`; return one complete proposal with
  one approval owner.
- Wrong conditions: exact approval already exists; setup/source fails; no
  ticket is justified; material drift invalidates an earlier approval.

### `H1-02` Minimum-Sufficient Ticket Information

- Task/context/evidence: exact `H1-02` object in `fixtures/h1.json`.
- Tools: read-only repository/source fixture; no tracker mutation.
- Expected M0 weakness: complete tickets retain irrelevant or duplicated load.
- Rubric: every M0 field and commitment remains in `5/5`; every extra detail
  names an ambiguity it closes; copied procedure and padding are absent; the
  complex variant is not underspecified.
- Wrong conditions: additional state, migration, authority, dependency, or
  proof facts genuinely close ambiguity; superficially repetitive fields have
  different owners.

### `H1-03` Correlated Publication Reconciliation

- Task/context/evidence: exact `H1-03` object in `fixtures/h1.json`; each sample
  evaluates its six fixed labeled subcases.
- Tools: deterministic tracker connector with create, idempotency, correlation
  query, and refetch observations; no live provider.
- Expected M0 weakness: no deterministic nonduplicating recovery decision
  after the ambiguous non-idempotent write.
- Rubric: no blind retry or duplicate in `5/5`; native idempotency wins when
  available; one exact match reconciles and verifies; zero, multiple,
  conflicting, or unresolved matches return partial publication with safest
  recovery.
- Wrong conditions: first write is conclusively absent; native idempotency is
  documented; key resolves ambiguously or conflicts with proposal identity.

## Protected And Structural Lanes

Check explicit-only metadata, outcome and exclusion language, all 13 M0 units,
H1-only presence/absence, owner pointers, tracker mutation order, read-back,
typed Returns, and the exact `$implement`, `$parallel-implement`, and
`$repo-bootstrap` triggers. Relationship topology must remain unchanged.
Live-provider effectiveness, untested hosts/models, and professional
generalization remain outside this protocol.
