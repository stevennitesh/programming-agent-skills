# Lean Engineering Defaults And Source Vocabulary

Status: active

Baseline: clean repository HEAD
`5d5705eea1827fa7627d74e0621a050e7125ad02` on 2026-08-11. That commit
partially projected source vocabulary, but left contradictory prose checks,
duplicated doctrine, and universal workflow expansion. Re-read each target
before editing and preserve unrelated work.

## Objective

Make high-quality code the ordinary default while keeping specialist methods
and coordination conditional. Prefer established engineering vocabulary when
it preserves the repository's meaning and recruits useful prior practice. Use
plain descriptive language when no established term fits. Retain a local term
only when it names an exact behavior-bearing protocol or artifact.

This plan records future implementation work. This edit performs no
installed-mirror synchronization, staging, commit, push, publication,
historical rewrite, or machine-schema migration.

## User Policy

- Favor complex behavior made simple over simplistic behavior or elaborate
  process.
- The normal path is direct implementation plus the smallest check capable of
  disproving the claim.
- Keep the always-loaded engineering contract compact. Put specialist detail
  behind an observable condition and its existing owner.
- Security and production/SRE work are explicit-request-only. Generic risk,
  file type, external input, a release label, or source prestige cannot activate
  them.
- Preserve an explicit existing security, privacy, authorization, production,
  or data-integrity contract touched by the requested change; do not expand the
  task into specialist analysis, hardening, deployment, or operations work.
- A dormant branch creates no checklist row, `N/A`, artifact, reviewer, or
  explanation obligation.
- Validators enforce machine-checkable structure, not preferred prose.

## Always-Loaded Quality Core

The shared contract should compress ordinary engineering into these defaults:

1. Preserve the explicit request, accepted behavior, applicable context-scoped
   Ubiquitous Language, preconditions, postconditions, invariants, applicable
   contracts, and unrelated work.
2. Trace the current behavior owner and real callers. Change the smallest
   repository-native path that minimizes total caller, maintainer, migration,
   operational, coordination, and proof burden; do not create an orphan
   component, speculative layer, or parallel V2 path.
3. At a changed boundary, validate action-driving input against its functional
   contract and preserve data identity, integrity, provenance, schema, units,
   ordering, and lifecycle where applicable. Do not weaken existing
   authorization, privacy, or secret-handling guarantees. This is ordinary
   correctness, not authority for a security program.
4. Preserve conceptual integrity and essential complexity while removing
   demonstrated accidental complexity. Use information hiding and deep
   modules to contain change, not to justify more interfaces.
5. Make interfaces easy to use correctly and hard to misuse. Prefer clear
   names, explicit data relationships, local ownership, and readable control
   flow. Define errors out of existence where the accepted behavior
   permits it.
6. Apply DRY to knowledge and policy, not repeated syntax. Apply yagni to
   speculative capability. Prefer bounded duplication to the wrong
   abstraction when meanings, owners, change rates, or failure modes differ.
7. Run the smallest claim-matched check at the real caller or closest
   observable boundary. Require a discriminating independent oracle when a
   behavioral claim could otherwise self-confirm. Prefer state verification;
   use behavior verification only when the interaction is itself a
   responsibility or is necessary for failure isolation.
8. Remove or justify paths made obsolete or contradictory by the change.
   Report only material skipped proof or Residual Risk that limits the claim.

Use Ousterhout's change amplification, cognitive load, unknown unknowns, deep
module, shallow module, information hiding, and pass-through method only where
they sharpen a design judgment. Use Brooks's essential complexity, accidental
complexity, and conceptual integrity where they preserve problem meaning.
These are diagnostic concepts, not mandatory scorecards or Return fields.

`Proof Seam` and `Change Closure` may remain as repository-local protocol terms
because they currently encode distinct cross-skill behavior. Add no new
capitalized local vocabulary. A test exercises a Proof Seam; it is not itself
the seam. Prefer a concrete test, fixture, check, workflow, or artifact over the
invented label `Proof lane`.

## Conditional Activation

A positive predicate activates its branch. A closest non-trigger is not weak
positive evidence. Untriggered branches stay silent.

| Branch | Activate exactly when | Closest non-trigger and default |
| --- | --- | --- |
| Codebase Design | One consequential responsibility, interface, ownership, seam, substitution, or migration decision is unresolved. | A clear current-owner path. Implement directly. |
| TDD protocol | The user explicitly requests test-first or RED-GREEN-REFACTOR, or an explicit repository policy requires it. | Ordinary feature or bug work that still needs tests. Test normally without claiming TDD. |
| Independent Change Review | The user or repository explicitly requires review; the candidate recombines mutations from two or more independent authors; or focused proof establishes behavior but a material shared-contract or irreversible-migration acceptance judgment still warrants fresh independent judgment and review is the lowest-burden way to obtain it. | Every candidate, PR, large diff, novelty, one delegated edit, release label, generic risk, or missing required proof. Use direct diff read-back and focused proof; missing proof stops rather than routing to review. |
| High-Assurance Review | The user explicitly names it or approves one exact invocation packet. | Security, production, release, severity, or uncertainty alone. Do not recommend or invoke it automatically. |
| Delegation | The user explicitly requests subagents, or an explicitly invoked skill owns required fanout. | Multiple files, spare agents, possible parallelism, or an independently ownable subtask. Work directly. |
| State and lifecycle reasoning | Requested behavior materially depends on reachable states, transitions, ordering, retry, resume, cancellation, persistence, or concurrency. | Asynchronous syntax or hypothetical combinations. Test the enumerable behavior directly. |
| Formal methods | The user or repository explicitly requires a formal specification, model checker, solver, or formal verification. | Stateful, concurrent, mathematical, high-risk, or invariant-bearing code by itself. Ordinary state reasoning remains available without formal machinery. |
| Property-based testing | A stable property and independent oracle range over a broad or combinatorial domain, credible generators and shrinking exist, and generation discriminates better than a small example table. | Many edge cases, a regression, or desire for more coverage. Prefer examples or an exhaustive small table. |
| Test doubles | A real dependency cannot provide deterministic, fast, or safe proof and the double has an explicit fidelity contract. | Convenience or difficult setup alone. Prefer real in-process behavior. |
| Characterization test | Actual legacy behavior must be recorded while intended behavior is unavailable. | Settled expected behavior. A characterization test establishes actuality, not correctness, cause, or a corrective RED. |
| Negative control | A validator, hook, policy check, dependency rule, or other enforcement boundary changes. | Ordinary behavior code. One representative failing violation is sufficient unless mutable state can contaminate later checks. |
| Performance | An explicit budget or acceptance criterion exists, or comparable evidence shows material cost on a supported workload. | Loops, allocations, suite duration, file size, or generic “make it faster.” Do not add optimization machinery. |
| Accessibility | A changed user-facing surface can alter semantics, labeling, focus, keyboard behavior, contrast, motion, or assistive-technology behavior. | Backend or data-only work. Full WCAG conformance work requires an explicit commitment or claim. |
| Security | The user or accepted task explicitly names a security objective, assessment, hardening requirement, or security acceptance criterion. | External input, auth/secrets code, hypothetical harm, severity, or supported risk alone. Preserve touched guarantees; otherwise do no security program. |
| Production/SRE | The user or accepted task explicitly names deployment, production access/configuration, incident work, operability, observability/SLI, SLO, capacity/load, cutover, rollback, or production evidence. | Application code, a “production implementation,” deployment files, release status, or proving a real runtime caller. Do no production/SRE work. |

Real-caller integration is ordinary correctness. Replace generic “production
caller/path” wording with “real caller,” “entry path,” or “runtime path” unless
an actual production environment is explicitly in scope.

## Source Vocabulary Placement

Use source vocabulary at the narrowest owner where it changes judgment:

| Owner | Established vocabulary to use |
| --- | --- |
| Engineering contract | Ubiquitous Language; preconditions, postconditions, invariants; conceptual integrity; essential/accidental complexity; information hiding; deep/shallow module; change amplification; cognitive load; unknown unknowns; DRY; yagni; state/behavior verification; refactoring |
| Codebase Design | responsibility, interface, module, information hiding, deep module, seam, enabling point, behavioral subtyping, preconditions/postconditions/class invariants, wrong abstraction |
| TDD references | RED-GREEN-REFACTOR; state verification; behavior verification; characterization test; properties, generators, and shrinking; Test Double; Dummy Object; Test Stub; Test Spy; Mock Object; Fake Object |
| Audit and Change Review | Code smell as an investigation lead; Hyrum's Law only for observable compatibility; safety/liveness only for activated state work; source-specific specialist vocabulary only after its branch activates |
| Simplify Code and Diagnosis | Refactoring, wrong abstraction, characterization test, change amplification, cognitive load; no source slogan that changes no action |

Source provenance belongs here and in research evidence, not as an
author-by-author runtime checklist:

- Parnas, [On the Criteria To Be Used in Decomposing Systems into
  Modules](https://doi.org/10.1145/361598.361623): information hiding and
  changeable design decisions.
- Brooks, [No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf):
  essential and accidental complexity; conceptual integrity.
- Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/):
  Ubiquitous Language and context-scoped domain models.
- Meyer, [Design by Contract](https://se.inf.ethz.ch/~meyer/publications/old/dbc_chapter.pdf):
  preconditions, postconditions, and invariants.
- Ousterhout, [Complexity](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=complexity):
  change amplification, cognitive load, and unknown unknowns; [Modular
  Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign)
  and [Exception Handling](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=exceptions):
  deep/shallow modules, pass-through methods, and defining errors out of
  existence.
- Bloch, [How to Design a Good API and Why It Matters](https://www.infoq.com/articles/API-Design-Joshua-Bloch/):
  easy correct use and resistance to misuse.
- Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html),
  [Refactoring](https://martinfowler.com/bliki/DefinitionOfRefactoring.html), and
  [Yagni](https://martinfowler.com/bliki/Yagni.html): state/behavior
  verification, behavior-preserving refactoring, and the XP practice yagni;
  [Code Smell](https://martinfowler.com/bliki/CodeSmell.html): an investigation
  lead rather than a defect by itself.
- Beck, [Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd): the small
  test-first cycle represented here as RED-GREEN-REFACTOR.
- Feathers, [Working Effectively with Legacy Code sample](https://www.informit.com/content/images/9780131177055/samplepages/0131177052.pdf):
  seam and enabling point; [author interview](https://www.infoq.com/podcasts/working-effectively-legacy-code/):
  characterization tests record actual rather than correct behavior.
- Liskov and Wing, [A Behavioral Notion of Subtyping](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf):
  behavioral subtyping.
- Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction):
  unsharing and duplication before a false abstraction.
- Meszaros, [Test Double Patterns](https://ptgmedia.pearsoncmg.com/images/9780131495050/samplechapter/0131495054_CH23.pdf):
  Test Double taxonomy.
- Claessen and Hughes, [QuickCheck](https://doi.org/10.1145/351240.351266):
  properties and generated cases; the canonical TDD reference must also source
  any adopted shrinking semantics.
- The Pragmatic Programmer, [DRY extract](https://media.pragprog.com/titles/tpp20/dry.pdf):
  knowledge-level DRY.
- Hyrum Wright, [Hyrum's Law](https://www.hyrumslaw.com/): observable behavior
  can acquire dependents beyond the promised contract.
- NASA, [Verification and Validation](https://www.nasa.gov/reference/2-4-distinctions-between-product-verification-and-validation/):
  requirements conformance versus intended purpose in the intended environment.

## Vocabulary Disposition

- Keep established terms only at their behavior owner; do not project phrases
  across every skill.
- Keep stable machine identities such as `source_trace`, `epoch_lock`, schema
  IDs, paths, and frozen evidence unchanged.
- Keep an existing local term only when removing it would lose an exact gate,
  artifact identity, or Return meaning. Describe it explicitly as local rather
  than claiming it is source-native.
- Retain `Source Trace` where it names the repository's exact source packet.
  Use lowercase traceability only for the generic quality of being traceable.
- Delete the `Integrated shape`, `Proof lane`, `Behavior-Owned Test Portfolio`,
  generic capitalized `Lock`, and `Author Lock` labels. Preserve Integrated
  shape's load-bearing total-burden comparison in direct prose; otherwise keep
  necessary behavior by naming the concrete artifact or action.
- Replace `Removal Trigger` with removal condition.
- Replace `state testing` and `interaction testing` with Fowler's state
  verification and behavior verification.
- Delete “test as first user,” “fast, high-quality feedback,” and other slogans
  when the following rule already owns the behavior.
- Use verification for conformance to specified requirements and validation
  for intended purpose in the intended environment.
- Do not rename a stable protocol field to a near-synonym merely because a
  source uses a related noun.

## Exact Change Inventory

| Owner | Files | Required outcome |
| --- | --- | --- |
| Active context | `AGENTS.md`, `CONTEXT.md`, `docs/plans/README.md` | Keep boot text small; route this plan while active; remove universal deployment/review language from shared context. |
| Shared core | `docs/agents/engineering-contract.md`, `skills/custom/repo-bootstrap/engineering-contract.md`, `AGENTS_PORTABLE_FALLBACK.md` | Replace the 256-line mixed contract with the compact quality core plus short trigger pointers; update both managed copies atomically. Make the portable fallback a standalone global `AGENTS.md` for users without installed skills; repositories still own local commands, invariants, and sources. |
| Review decision | `docs/adr/0015-lean-quality-defaults-and-conditional-workflow-expansion.md` | Supersede ADR-0013's universal Implement review and narrow ADR-0014's incomplete nomenclature migration; preserve both historical ADRs. |
| Ordinary implementation | `skills/custom/implement/SKILL.md`, its metadata and handoff reference | Remove default Charter, Repair budget, mandatory reviewer, repeated Hyrum prose, and production-caller wording. Require current owner, real callers, focused proof, diff/read-back check, obsolete-path cleanup, and honest Residual Risk. |
| Parallel implementation | `skills/custom/parallel-implement/SKILL.md` and metadata | Keep lane isolation and one final independent review for genuinely independently authored integration; use runtime-path language; do not imply production/SRE scope. |
| Design | `skills/custom/codebase-design/{SKILL.md,DIRECT-DESIGN.md,DEEPENING.md,DESIGN-IT-TWICE.md}` | Keep the ordinary interface packet small; load substitution, migration, state, security, production, and performance concerns only through their predicates. Use the source vocabulary above. |
| Testing | `skills/custom/tdd/{SKILL.md,tests.md,mocking.md,refactoring.md}` and metadata | Keep TDD invocation conditional; correct Fowler/Meszaros terms; add bounded characterization, Test Double, and property-testing branches without new phases or Return fields. |
| Diagnosis, simplification, audit, review | Directly affected canonical skills and existing references | Remove duplicated doctrine and slogans; preserve their gates and Returns; activate specialist coverage only from the table. |
| Relationship owners | `docs/synthesis/skill-context-relationships.md`, applicable runtime profiles and core-workflow evals | Make Implement-to-Change-Review conditional; preserve final review for independently authored integration and explicit-only High Assurance. |
| Pack composition owner | `docs/synthesis/skill-pack.md`, `tests/test_first_fresh_epoch.py`, and affected composition proof | Add one revision-plus-one amendment for the behavioral review-routing change and regenerate only affected fingerprints and integration evidence. Do not amend the baseline for prose-only vocabulary changes. |
| Active vocabulary callers | `skills/custom/to-spec/SKILL.md`, `skills/custom/to-tickets/SKILL.md`, `skills/custom/triage/AGENT-BRIEF.md`, `skills/custom/writing-great-skills/SKILL.md`, `docs/synthesis/methods/deploy-prompts.md`, and directly asserting tests | Remove only the retired human-facing labels and production-caller wording named above; preserve behavior and machine identities. |
| Mechanical projection | `skills/custom/repo-bootstrap/scripts/validate_setup.py`, `skills/custom/repo-bootstrap/setup-schema.json`, `scripts/validate_skills.py`, `tests/test_skill_pack_contracts.py` | Delete source-phrase policing and broad vocabulary-projection tests. Validate owners, managed identity, pointers, and observable activation contracts. Refresh digests only after wording freezes. |

Do not create new security, SRE, accessibility, formal-methods, property-testing,
or “lean implementation” skills. Use the current owner and an existing
branch-only reference; add a small reference only when the existing owner
cannot remain readable without it.

## Execution Order

1. Snapshot the current files and classify every planned instruction as Keep,
   Collapse, Disclose, or Delete.
2. Add the successor ADR, then amend the Pack Composition Baseline only for
   the review-routing behavior change.
3. Compact both engineering-contract copies and the root portable fallback.
4. Simplify Implement and its relationship to Change Review; then update
   Parallel Implement and High Assurance only where their routing text depends
   on that decision.
5. Update Codebase Design and TDD branch owners, then the directly affected
   Diagnosis, Simplify, Audit, and Review text.
6. Remove validator prose policing and replace phrase projection with
   owner-specific structural assertions.
7. Freeze wording, update managed markers and the setup digest, then run
   focused structural tests, skill validation, and diff checks.
8. Run applicable behavioral evaluation, followed by the full suite and
   install dry-run because shared context and composition changed.
9. Stop before installation synchronization or Git delivery unless separately
   authorized.

Do not revise the Pack Composition Baseline or regenerate semantic fingerprints
merely to rename human-facing prose. The Implement review-routing change is
behavioral, so its one revision-plus-one amendment is required for coherence.

## Proof And Behavioral Evaluation

Structural proof must establish ownership and branching, not source-phrase
presence:

- both engineering-contract copies match except for the managed marker;
- the setup digest matches the frozen final wording;
- no validator requires author names, book titles, or literature phrases;
- each changed branch has an observable positive condition and resulting
  action; add a closest non-trigger only where demonstrated ambiguity requires
  it;
- ordinary Implement can finish with focused caller proof and no reviewer;
- independently authored final integration still receives review;
- High Assurance, security, and production/SRE remain explicit-only;
- no new TDD phase, Return field, finding field, checklist, score, or mandatory
  artifact appears.

Use `skills/custom/writing-great-skills/BEHAVIOR-EVALS.md` for each registered
`quality-lift` wording claim. Freeze control/candidate bytes, rubric, runtime,
and protected behavior. Run controls first; stop at
`reject-no-control-deficit` when the deficit is absent; sample the candidate
only after the control deficit appears; judge the contribution from those
candidate samples; and sample selected wrong conditions only after the
candidate contributes. An `accept` decision is required for retained
judgment-changing wording. Pure nomenclature uses structural proof.

Candidate pairs, selected only for behavior changed by the final delta:

- small local fix / shared public-contract migration;
- ordinary tests / explicit TDD request;
- real runtime caller / explicit production deployment;
- functional validation at a trust boundary / explicit security hardening;
- enumerable examples / broad generated property;
- ordinary state transitions / explicit formal verification;
- suspected slowness / measured budget violation;
- backend change / changed interactive UI;
- one-owner edit / independently owned parallel work;
- repeated syntax with distinct meaning / duplicated policy knowledge.

Run:

- `python -m scripts.pytest_focused`
- `python -m scripts.validate_skills`
- `python -m pytest`
- `python -m scripts.install_skills --dry-run`
- `git diff --check`
- `git diff --cached --check`

## Deliberate Non-Changes

- No author checklist in runtime context.
- No new review system or universal independent reviewer.
- No security, production/SRE, threat-model, ASVS, SSDF, SLO, incident,
  deployment, or release-readiness work without explicit scope.
- No full WCAG conformance claim without explicit scope.
- No universal TDD, property testing, formal methods, mutation testing,
  performance benchmarking, matrix, scorecard, or negative-control ceremony.
- No source-vocabulary enforcement in validators.
- No new branded phases, fields, ledgers, locks, portfolios, or artifacts.
- No rewrite of historical ADRs, synthesis, research, validation, or run logs.
- No machine identity or frozen-baseline migration solely for prose; the one
  review-routing successor is behavior, not nomenclature.
- No installed-mirror synchronization, staging, commit, push, or publication.

## Completion

The work is complete when ordinary engineering uses the compact quality core,
each changed heavier branch has an observable activation condition, security
programs and production/SRE are explicit-only, ordinary trust/data correctness
remains active, source vocabulary is precise without phrase projection,
obsolete universal ceremony is removed, accepted behavioral evaluation
supports judgment changes, and repository checks pass.
