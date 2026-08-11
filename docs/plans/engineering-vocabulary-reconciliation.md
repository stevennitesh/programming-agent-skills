# Engineering Vocabulary Reconciliation

Status: ready for implementation planning

Captured: 2026-08-11 at repository HEAD
`4cf8412d3b4f5ce692d2c1c63325a72c17664010`, including the existing dirty
worktree as inspected evidence. Re-read every target before editing; this note
does not authorize overwriting unrelated work.

## Objective

Make the engineering contract and canonical skills use established engineering
vocabulary where it preserves meaning and reduces explanation. Keep a
repository-local term only when it compresses a unique, behavior-bearing
contract. Keep the result lean: shared philosophy and concepts belong in the
engineering contract; procedures, gates, proof mechanics, and Return contracts
stay with their skill owners.

This note is the execution map. It does not authorize installation, staging,
commit, push, publication, or rewriting historical evidence.

## Contract Questions

Do not add an author-by-author checklist. Embed exactly these three questions
beside the contract principles they exercise:

1. **Data and invalid states:** Can the data structures and their relationships
   make this invalid state or special case impossible?
2. **Abstraction and ownership:** Before extracting, splitting, or unifying
   code, does the new shape give shared meaning or supported variation a
   clearer owner and lower total caller and maintainer burden—or merely trade
   visible repetition for more names, branches, interfaces, and hops?
3. **Evidence discrimination:** For every test used to support a claim, what
   incorrect behavior would it reject, and is its oracle independent of the
   failure mode being tested?

These questions cover the useful review pressure without making a person's
reputation an authority.

## Source-To-Runtime Map

| Source | Vocabulary or contribution to adopt | Runtime owner |
| --- | --- | --- |
| Linus Torvalds | Data structures and their relationships; make special cases disappear in the model | Engineering contract question 1; Codebase Design orientation |
| Robert C. Martin | Actor or reason to change; policy/detail dependency direction | Codebase Design and Audit Design Lens |
| Martin Fowler | State verification, behavior verification; code smells are investigation leads; behavior-preserving refactoring | TDD and Change Review |
| Kent Beck | Keep behavior and structure changes separate; simple design; small GREEN refactorings | Contract question 2 and TDD refactoring |
| Michael Feathers | Seam, Enabling Point, characterization test, sensing and separation | Codebase Design, TDD, Diagnosis, Simplify Code |
| Dan Abramov | Judge abstraction by changeability and concrete outcomes, not “clean code” aesthetics | Contract question 2 |
| Sandi Metz | Wrong abstraction; duplication can be cheaper; tests as clients of public interfaces; incoming/outgoing message distinctions | Contract, Codebase Design, Simplify Code, TDD |
| John Ousterhout | Change amplification, cognitive load, unknown unknowns, deep modules, information hiding, shallow modules, pass-through methods | Engineering contract and Codebase Design |
| Hyrum Wright and Google | Hyrum's Law, actual caller dependence, define errors out of existence, discriminating review evidence | Engineering contract, Audit Reliability, Change Review |
| *The Pragmatic Programmer* | DRY is about knowledge; tracer bullets; prove assumptions | Contract, Parallel Implement, Triage |
| Dave Farley | Fast, high-quality feedback and empiricism | Engineering contract; skill-local wording only when it changes an action or gate |

Primary references:

- Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- Martin Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- Martin Fowler, [Code Smell](https://martinfowler.com/bliki/CodeSmell.html)
- Michael Feathers, [Looking Back at Working Effectively with Legacy Code](https://www.infoq.com/podcasts/working-effectively-legacy-code/)
- Dan Abramov, [Goodbye, Clean Code](https://overreacted.io/goodbye-clean-code/)
- John Ousterhout, [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)
- Google, [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- Google, [The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html)
- *The Pragmatic Programmer*, [Tips](https://pragprog.com/tips/)
- NASA, [Distinctions between product verification and validation](https://www.nasa.gov/reference/2-4-distinctions-between-product-verification-and-product-validation/)
- NIST SP 800-128, [Guide for Security-Focused Configuration Management](https://csrc.nist.gov/pubs/sp/800/128/upd1/final)
- W3C, [Data Catalog Vocabulary](https://www.w3.org/TR/vocab-dcat-3/)

## Engineering Contract Changes

Update these atomically:

- `skills/custom/repo-bootstrap/engineering-contract.md`
- `docs/agents/engineering-contract.md`

Retain and sharpen:

- Hyrum's Law once, at the shared contract owner.
- “Define errors out of existence.”
- Ousterhout's three complexity symptoms and deep-module vocabulary.
- Cohesion, coupling, and essential versus accidental complexity.
- Fast, high-quality feedback as shared philosophy.
- `Proof Seam`: the caller-facing boundary where meaning is verified. A test
  exercises the Proof Seam; the test is not itself the seam.
- `Change Closure`: remove or justify displaced, redundant, or contradictory
  paths.

Add or correct:

- DRY applies to shared knowledge or policy, not every repeated line. Prefer
  duplication over the **wrong abstraction** when meanings, owners, change
  rates, or failure modes differ.
- Use Fowler's **state verification** and **behavior verification**, replacing
  “state testing” and “interaction testing.” Prefer state verification through
  stable caller-facing interfaces. Use behavior verification only when the
  interaction is itself part of the responsibility or is needed for failure
  isolation.
- A **characterization test** records actual current behavior. It does not by
  itself establish intended behavior, correctness, or a corrective RED.
- Define **Traceability** as a current, bounded chain from governing request
  and authority through the behavior owner and real callers to the observable
  proof boundary and evidence.

Replace:

| Current term | Replacement |
| --- | --- |
| Source Trace | Traceability in human-facing text; retain `source_trace` machine fields for compatibility |
| Integrated shape | The smallest repository-native path through the current behavior owner and real callers |
| Proof Lane | Repository-owned proof mechanism, or the concrete fixture/check/workflow/artifact |
| Removal Trigger | Removal condition |
| Generic capitalized Lock | The actual action: define, authorize, baseline, freeze, verify, or record acceptance |

## Pack Vocabulary Changes

Record one nomenclature ADR that supersedes names without rewriting the
accepted historical decisions.

| Current term | Replacement | Compatibility rule |
| --- | --- | --- |
| Fresh Composition Epoch | Keep | It uniquely names the pack-wide evidence reset and recomposition process |
| Pack Composition Contract | Pack Composition Baseline | Retain v1 schema IDs and paths unless a separate machine-format migration is authorized |
| Research Catalog | Evidence Catalog | Retain current module and schema identities |
| Research Card | Evidence Record | Retain `RC-*` identities |
| Deploy Campaign | Skill Change-Control Method | Update active callers; leave historical run evidence unchanged |
| Contract Lock | Define and Authorize Change | Stage heading and active references |
| Candidate Lock | Baseline and Verify Candidate | Stage heading and active references |
| Behavioral Proof | Validate Behavior | Conditional stage; use validation for intended effect |
| Release | Promote Canonical Skill | Change only this method stage; other genuine release uses remain |
| Author Lock | No label | “Before Author mode returns…” followed by the existing read-back obligations |
| epoch Lock | Epoch Acceptance Record | Retain machine field `epoch_lock` unless separately migrated |

Use **verification** for conformance to specified deterministic requirements
and **validation** for intended behavior or effect.

The marker-bounded JSON in `docs/synthesis/skill-pack.md` is a frozen baseline.
Changing embedded `Proof Lane` or `epoch Lock` text requires a revision-plus-one
amendment and regeneration of affected semantic fingerprints, blueprints,
slices, and integration evidence. Do not mutate the accepted revision in place.

## Skill Changes

### Codebase Design

Files:

- `skills/custom/codebase-design/SKILL.md`
- `skills/custom/codebase-design/DIRECT-DESIGN.md`
- `skills/custom/codebase-design/DEEPENING.md`
- `skills/custom/codebase-design/DESIGN-IT-TWICE.md`

Changes:

- Add Feathers's **Enabling Point**: where behavior or dependency selection
  occurs at an earned Seam.
- Preserve the caller-facing Interface as the Proof Seam; tests exercise it.
- Prefer deep, somewhat-general-purpose Modules whose Interfaces hide decisions
  and do not accumulate caller-specific special cases.
- Trace material data structures, ownership, and relationships.
- Diagnose wrong abstraction, mixed actors or reasons to change, weak cohesion,
  harmful coupling, policy depending on details, and obscured data relations.
- Compare unsharing, inlining, or bounded duplication before adding parameters,
  conditional paths, or another layer.
- State that characterization tests freeze observed legacy behavior, not intent.

### TDD

Files:

- `skills/custom/tdd/SKILL.md`
- `skills/custom/tdd/tests.md`
- `skills/custom/tdd/mocking.md`
- `skills/custom/tdd/refactoring.md`

Changes:

- Use state verification and behavior verification consistently.
- Treat tests as clients of the public interface; remove “test as first user.”
- State-verify incoming/public results. Behavior-verify outgoing commands only
  when sending is the owned responsibility or necessary for failure isolation.
- Add the characterization-test limitation.
- Replace `Behavior-Owned Test Portfolio` or bare `Test Portfolio` with a plain
  **Test Ownership** rule: each supported behavior has one canonical test
  owner; supporting tests cover distinct risks.
- Keep `RED -> GREEN -> REFACTOR`. Do not add a `TIDY` phase or new Return field.

### Diagnosing Bugs

File: `skills/custom/diagnosing-bugs/SKILL.md`

- Before corrective regression proof, state that a characterization test may
  record actual behavior or protect unaffected legacy behavior but cannot
  establish expected behavior, cause, or the corrective RED.
- Remove a redundant fast-feedback slogan if it changes no action or gate.

### Audit Codebase

Files:

- `skills/custom/audit-codebase/DESIGN-LENS.md`
- `skills/custom/audit-codebase/CODING-PRACTICES-LENS.md`
- `skills/custom/audit-codebase/RELIABILITY-LENS.md`
- `skills/custom/audit-codebase/QUALITY-LENS.md`

Changes:

- Design: add wrong abstraction, Enabling Point, actor/reason, policy/detail
  inversion, cohesion/coupling, and material data relationships as evidence
  prompts.
- Coding practices: smells and refactoring names are investigation vocabulary,
  not findings or prescribed remedies.
- Reliability: ask which actual dependencies callers rely upon; keep this
  source-neutral because Hyrum's Law is already in the shared contract.
- Quality: preserve demonstrated-cost admission.
- Do not add Candidate Contract fields or finding rows solely to carry source
  vocabulary.

### Change Review

Files:

- `skills/custom/change-review/FINDING-CONTRACT.md`
- `skills/custom/change-review/SMELL-BASELINE.md`
- `skills/custom/change-review/SKILL.md`

Changes:

- Use state verification and behavior verification in Proof Discipline.
- State: “Treat smells as investigation leads, not defects or findings.”
- A new or changed test must discriminate the supported broken case.
- When changing a validator, hook, policy check, or enforcement boundary, use
  an applicable negative control to show a controlled violation failing for
  the intended reason. Do not require mutation controls universally.
- Remove repeated Hyrum explanation; inherit it from the contract.
- Preserve all finding fields, severities, admission gates, remediation
  classes, and Return authority.

### Simplify Code

File: `skills/custom/simplify-code/SKILL.md`

- Add the wrong-abstraction response: delete, unshare, inline, or accept bounded
  duplication before parameterizing a false common abstraction.
- Keep each cut a small behavior-preserving refactoring.
- Treat characterization tests as observed-behavior evidence only.

### Remaining Active Skills

- `parallel-implement`: retain one tracer bullet through the production path.
- `triage`: retain tracer bullet as a learning role, not a slice type or
  completion claim.
- `implement`: remove its duplicated Hyrum paragraph.
- `to-spec` and `to-tickets`: vocabulary-only updates for Traceability, removal
  condition, and repository-owned proof mechanism.
- `high-assurance-review`: no source-specific edit; it consumes the shared
  Finding Contract.
- `writing-great-skills`: remove the Author Lock label while retaining read-back,
  proof, unrelated-work, and stop-before-delivery behavior.

## Current-WIP Corrections

Before adding more vocabulary, reconcile the existing dirty candidate:

- Delete
  `test_source_derived_vocabulary_projects_to_affected_skill_slices` from
  `tests/test_skill_pack_contracts.py`.
- Remove source-phrase literals such as Hyrum/complexity/testing vocabulary from
  `skills/custom/repo-bootstrap/scripts/validate_setup.py`.
- Do not make the validator police prose. ADR-0004 assigns it publishing and
  structural hygiene, not language enforcement.
- Remove duplicated Hyrum paragraphs from Implement and Change Review.
- Correct every claim that a test itself is the Proof Seam.
- Remove no-op source slogans from skills when they add no behavior, condition,
  gate, or stopping rule.
- Preserve behavior-bearing ownership, Return, closure, and proof obligations
  while replacing labels.

## Tests And Behavioral Evaluation

Replace broad vocabulary-projection assertions with owner-specific behavior
assertions in `tests/test_skill_pack_contracts.py`:

- shared concepts appear at the engineering-contract owner;
- TDD and the Finding Contract use state/behavior verification consistently;
- characterization tests are actual-behavior evidence, not correctness or RED;
- wrong-abstraction actions appear only in Codebase Design and Simplify Code;
- smells remain leads rather than findings;
- conditional negative controls remain conditional;
- no new TDD phase, Return field, finding field, or universal ceremony appears.

The exact wording changes judgment, so structural tests are insufficient. Use
`skills/custom/writing-great-skills/BEHAVIOR-EVALS.md`:

1. Freeze the accepted control and exact candidate bytes.
2. Run at least five fresh entry-positive control/candidate pairs.
3. Admit the wording only if it changes the intended judgment or action without
   weakening established behavior.
4. Then run wrong-condition pairs, including:
   - an already-deep cohesive module;
   - genuinely shared knowledge where duplication is harmful;
   - a characterization test being mistaken for correctness;
   - an interaction that is genuinely contractual;
   - a low-risk change where a negative control is unnecessary.
5. Evaluate behavior, not phrase echo.

## Execution Order

1. Capture current repository state and protect unrelated dirty work.
2. Add the nomenclature ADR.
3. Update `CONTEXT.md` ownership and preferred terms.
4. Update both engineering-contract copies atomically.
5. Amend the Pack Composition Baseline and regenerate only affected derived
   evidence.
6. Update Codebase Design and TDD, then Audit, Review, Diagnosis, Simplify, and
   vocabulary-only callers.
7. Reconcile validators and owner-specific tests.
8. Recalculate `setup-schema.json`'s contract digest and all managed markers
   only after wording is frozen.
9. Run behavioral evaluation.
10. Run:
    - `python -m scripts.pytest_focused`
    - `python -m scripts.validate_skills`
    - `python -m pytest`
    - `python -m scripts.install_skills --dry-run`
    - `git diff --check`
    - `git diff --cached --check`
11. Stop before installed-mirror synchronization, staging, commit, push, or
    publication unless separately authorized.

## Deliberate Non-Changes

- No author-by-author runtime checklist or celebrity authority.
- No SOLID checklist, tiny-function rule, “clean code” score, or universal
  abstraction prescription.
- No universal negative-control or mutation-testing ceremony.
- No characterization test promoted to a correctness oracle.
- No smell promoted to a defect or finding.
- No tracer bullet promoted to a ticket type, slice type, or completion claim.
- No routing, relationship, Return, tracker, Git, or installation-state change
  unless a concrete renamed artifact requires it.
- No rewriting of historical research, accepted ADRs, validation runs, or
  frozen evidence as though they were current instructions.

## Completion Boundary

The vocabulary reconciliation is complete only when active owners and callers
are cohesive, frozen baseline changes have valid successor evidence, the
behavioral evaluation supports the judgment changes, all repository checks
pass, and displaced terminology is removed or explicitly retained for machine
compatibility.

Research status: answered. The source-to-runtime mapping and active repository
surface were inspected on 2026-08-11. Remaining uncertainty is implementation
drift after this capture; resolve it by rereading each owner before mutation.
Additional source searching is unlikely to change the selected leading terms.

Caller-use boundary: this note supports a later authorized implementation. It
does not itself change canonical vocabulary or authorize delivery.

Return owner: repository maintainer.

Next: none.
