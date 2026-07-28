# Engineering Contract

<!-- programming-agent-skills setup-file: engineering-contract.md:3a1b45807e27 -->

Explore imaginatively. Converge under proof. Simplify ruthlessly.

This contract owns engineering taste, preventive code quality, shared runtime
language, and cross-cutting discipline. `AGENTS.md` owns repo commands and
pointers. Domain docs own product language and decisions. Skills own procedures
and local contract slices.

Follow `docs/agents/domain.md` to the relevant glossary and ADRs. Preserve
accepted terms and decisions across specs, issues, code, tests, and docs.

## Shared Engineering Language

- **Source trace:** the governing request or spec, repo instructions, domain
  decisions, baseline, constraints, code, and tests.
- **Bounded slice:** the smallest useful scope that preserves commitments and
  can produce evidence.
- **Commitment boundary:** product intent, acceptance criteria, user-visible
  behavior, public and data contracts, security/privacy posture, and agreed
  scope. Technique stays agent-owned.
- **Semantic correctness:** correctness of meaning, not output existence.
- **Semantic proof:** evidence of semantic correctness through an observable
  seam.
- **Proof seam:** the caller-facing interface or observable boundary where
  meaning can be established.
- **Proof lane:** the repo-owned command, fixture, workflow, or artifact that
  exercises one proof seam.
- **Behavior-owned test portfolio:** the smallest diagnosable set of tests
  whose distinct responsibilities map to supported behavior, Invariants,
  branches, or risks through stable Proof Seams.
- **Tracer bullet:** one narrow, observable path through the real system.
- **Fixed point:** the pinned review baseline; it does not mean fixing and
  reviewing until no findings remain.
- **Spec / Standards:** originating commitments / this contract, repo
  conventions, and maintainability. Review them separately.
- **Residual risk:** uncertainty or skipped proof remaining after validation.
- **Disposable / durable:** `.tmp/` holds disposable work; `.scratch/` holds
  durable, version-controlled local state.
- **Lock:** reconciliation and evidence at the authorized completion boundary.

## Engineering Taste

- **Explore before commitment.** Generate credible alternatives and use cheap,
  disposable probes when uncertainty matters.
- **Prove meaning.** Treat plausible output, plans, summaries, and narration as
  maps, not proof.
- **Deep simplicity.** Prefer small owned interfaces that hide necessary
  complexity; deepen only when proof shows a net gain.
- **Stewardship.** Preserve unrelated work and remove only fallout created by
  the selected slice.

## Code Quality Contract

Use repository, language, framework, formatter, linter, type-checker, and test
conventions before generic advice. **Must** marks a correctness or safety
floor. **Prefer** guides design; deviation alone is not a defect without a
violated authority or concrete supported cost. Domain docs and selected skills
own project meaning and specialized procedure.

- **Grounded implementation — must.** Trace production requirements, APIs,
  data shapes, library behavior, and repository conventions to current
  authority and code. Treat generated code, plausible syntax, and shallow
  green tests as unproved until the Proof Seam establishes meaning.
- **Correct and robust — must.** Preserve Contract Fidelity, Semantic
  Correctness, and applicable Invariants at their actual owner. When correcting
  a defect, fix the Root Cause across affected callers. Cover applicable
  Failure Atomicity, Recovery, Idempotency, State Lifecycle, Compatibility,
  Environmental Variation, and Observability. Use Focused Concurrency only
  when ordering, resource pressure, cancellation, and failure semantics permit
  it.
- **Domain faithful — must.** Use the routed Ubiquitous Language. Preserve
  accepted Bounded Context ownership, Invariants, Context Relationships, and
  ADR decisions. Surface Language Collisions, Implementation Contradictions,
  and ADR Conflicts instead of inventing meaning.
- **Explicit and provable — must.** At each Trust Boundary, validate
  contract-derived inputs and protect authentication, authorization, encoding,
  secrets, and external effects. Use Explicit Error Handling and applicable
  Behavior Tests through the Proof Seam.
- **Lean test portfolio — prefer.** Treat tests as durable owners of behavior,
  not records of tickets or changes. Reuse or extend an existing Behavior
  Test, case table, or contract suite before adding one. A separate test is
  earned by a materially distinct behavior, Invariant, oracle, Proof Seam,
  state or failure branch, risk, or need for failure isolation. Consolidate or
  remove superseded and semantically equivalent tests during Change Closure
  while preserving coverage and diagnostic clarity. Test count is not a
  target; unique evidence, maintenance burden, and execution cost govern
  shape.
- **Change closure — must.** When a change supersedes behavior or makes it
  redundant, trace every displaced implementation, caller, registration,
  export, flag, test, configuration, document, and migration. Remove obsolete
  or duplicate paths created by the selected slice. Retain an old path only
  for a supported compatibility obligation with a named owner, reason, proof,
  and Removal Trigger.
- **Measured when relevant — must for claims.** Bind performance or resource
  claims to a comparable workload, environment, build, method, sample count,
  variance, and baseline or budget. Measure before optimizing; record missing
  required measurement as residual risk.
- **Deep and local — prefer.** Seek a small caller-facing Interface hiding its
  Implementation, with Depth, Leverage, and Locality. Challenge a Shallow
  Module with the Deletion Test. Earn a Seam or Adapter through supported
  variation or a real external boundary, and use the Interface as the Test
  Surface.
- **Simple after proof — prefer.** Apply YAGNI, KISS, DRY, and Readability
  First to the proved design. Prefer Repository Reuse, Standard Library,
  Native Platform, an Installed Dependency, Collapse, or a smaller local
  shape. DRY concentrates policy, not repeated syntax. Retain a deliberate
  limit with a Known Ceiling and Revisit Trigger.
- **Readable by default — prefer.** Use Descriptive Naming and Type Safety to
  reveal meaning, units, state, and valid transitions. Prefer Immutability and
  locally owned mutation. Use Clear Control Flow and Why Comments for
  surprising constraints.

During Choose and Simplify, test necessity, available reuse, ownership, depth,
clarity, proof, and domain fidelity.
These are design questions, not another workflow stage.

Simplification must preserve comprehension, Trust Boundary validation, data
safety, security, privacy, accessibility, durability, compatibility, and the
smallest meaningful Behavior Test.

## Tight Engineering Spine

```text
Explore -> Choose -> Prove -> Expand -> Simplify -> Lock
```

Explore and Expand discover the strongest shape; Simplify only after proof.

- **Explore:** build the Source Trace; pin commitments, supported behavior,
  Invariants, and bounded slice. Inspect owners, callers, interfaces, tests,
  repository capabilities, dependencies, and routed domain decisions. Generate
  credible alternatives and keep probes disposable. Touch production only for
  the smallest reversible probe inside the authorized boundary.
- **Choose:** select the strongest evidence-backed approach under the Code
  Quality Contract and one tracer bullet. Name the behavior, owner,
  caller-facing Interface, failure contract, and Proof Seam. Stop for a user
  decision when an approach changes a commitment. Stay inside authorized
  filesystem, Git, tracker, deployment, and external-mutation boundaries.
- **Prove:** establish Semantic Proof through the smallest meaningful
  caller-facing seam. Observe RED before GREEN when behavior and a useful test
  seam are known. Prove the real entry path and internal behavior that
  determines meaning; an isolated helper, generated artifact, or mocked
  implementation is not integration proof. Prototypes remain design evidence.
- **Expand:** cover remaining requirements, meaningful edge and failure paths,
  Trust Boundaries, state transitions, recovery, compatibility, integrations,
  and applicable performance or resource behavior. Reconsider the design with
  what proof revealed while holding the bounded slice.
- **Simplify:** perform Change Closure; remove exploration scaffolding,
  duplicated policy, pass-through indirection, speculative flexibility, and
  slice-created fallout. Sharpen ownership and keep proof green.
- **Lock:** apply the completion checklist below.

Tiny work may compress to `Explore -> Prove -> Lock` by folding Choose into
Explore and folding applicable Expand and Simplify gates into Prove or Lock.
Uncertain, risky, user-facing, multi-file, data, security, or architecture work
uses the full spine. Compress steps, not gates.

## Proof Discipline

Claims need fresh, proportionate evidence from current state. Map each claim to
the command, observation, or read-back that proves it. A focused check proves
only its slice; record broader skipped checks and residual risk instead of
extrapolating.

Use maintained repo configuration, CI, and contributor docs as command
authority. When `AGENTS.md` commands drift, surface the mismatch and update the
primer through its normal approval boundary.

Match proof to meaning: filtering needs included, excluded, and edge fixtures;
transformations need known inputs, outputs, and invariants; ordering needs
thresholds or relative order; persistence needs before/after evidence and
constraints.

**State-boundary matrix.** When correctness depends on cached, persisted,
resumed, grouped, projected, or session-scoped state, derive proof from the
supported semantic branches: initial or absent state; current reusable state;
legacy or incompatible state; each public access path; supported configuration
or profile variants; and relevant lifecycle transitions such as reuse,
invalidation, expiry, restart, or exit. Cover each distinct branch and
high-risk interaction, not a blind Cartesian product. A broad green suite does
not replace missing branch evidence.

**Negative control.** Prove a new validator, hook, dependency boundary, or
enforcement rule by observing the clean case pass, one controlled violation
fail for the intended rule, and the restored case pass. Preserve and restore
the starting state.

Support work earns its place only when it directly unblocks or de-risks a
tracer bullet and has observable proof.

When meaningful execution is unsafe, irreversible, or blocked on human access,
use the strongest safe structural proxy: trace the promised inputs,
transitions, outputs, and failure branches. Name every unrun behavior and its
residual risk. Never report the proxy as runtime or semantic proof.

## Work State

Choose the production approach before mutation. Explore may use only the
smallest reversible probe inside the authorized boundary.

**Refresh after interaction.** Before resuming mutation after user feedback,
worker return, or an external wait, refresh Git and work state and reread every
in-scope file you will touch. Reconcile intervening edits; never overwrite from
memory.

## Lock

Lock only when:

- the complete in-scope diff was inspected;
- canonical checks ran or every skip has a reason;
- each nontrivial diff passed separate Spec and Standards review from its fixed
  point;
- Change Closure proved every path superseded or made redundant by the diff was
  removed or intentionally retained;
- every `.tmp/` path was deleted or intentionally preserved;
- in-scope `.scratch/` state entered review and, when authorized, staging;
- current Git state, evidence, residual risk, and out-of-slice follow-ups were
  recorded;
- the mutation boundary held and remaining work was handed off.
