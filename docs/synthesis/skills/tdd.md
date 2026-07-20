# TDD Runtime Design Synthesis

Status: exhaustive design reference for a future rewrite, not an executable contract.

Current runtime authority remains in:

- `skills/custom/tdd/SKILL.md`;
- `skills/custom/tdd/tests.md`, `mocking.md`, and `refactoring.md`;
- `skills/custom/tdd/agents/openai.yaml`;
- `docs/agents/engineering-contract.md` and the target repository's domain and validation contracts;
- the invoking caller's bounded scope and mutation authority;
- `docs/synthesis/skill-context-relationships.md` at the accepted composition boundaries.

Pack contract tests and behavior-evaluation definitions protect that runtime. The installed mirror under `C:/Users/steve/.agents/skills/tdd` is a deployment copy and future promotion target, not a second design authority.

This synthesis specifies the selected behavior, relationships, evidence, file placement, and proof needed to rewrite `$tdd` later. It does not change the current runtime, authorize installation, or turn source rationale into additional procedure.

## How To Read This Document

This document is exhaustive for accepted TDD behavior, material alternatives, owned relationships, extraction surfaces, and proof required for promotion. The eventual runtime should be much smaller.

It has four layers:

1. **Orientation** states the outcome, boundary, vocabulary, and explanatory flow.
2. **Normative Design** is the sole authority for proposed runtime behavior and relationships.
3. **Evidence And Rationale** preserves source pressure, deliberate non-changes, and deferred hypotheses without creating rules.
4. **Extraction And Verification** places and proves the design without redefining it.

Change behavior in Layer Two; explain it in Layer Three; place and prove it in Layer Four. The Normative Home Index assigns every concern one authority. The ownership map places changes, the staged protocol owns proof mechanics, and the acceptance matrix owns case coverage only. Correct any rationale, file-placement row, or acceptance case that disagrees with its Layer Two owner.

Use this index for direct navigation:

| Question | Owning section |
| --- | --- |
| What outcome and trade-off govern the rewrite? | [North Star](#north-star) and [Design Verdict](#design-verdict) |
| When may TDD start? | [Invocation And Admission](#invocation-and-admission) |
| What does TDD own and what remains with its caller? | [Authority And Mutation Boundary](#authority-and-mutation-boundary) |
| Which operation is legal now? | [Cycle State And Transition Contract](#cycle-state-and-transition-contract) |
| When is each operation complete? | [Operation And Completion Contracts](#operation-and-completion-contracts) |
| What makes one tracer bullet valid? | [Source Trace And Tracer-Bullet Contract](#source-trace-and-tracer-bullet-contract) |
| How are the proof seam and oracle selected? | [Proof Seam And Independent Oracle](#proof-seam-and-independent-oracle) |
| What if no red-capable harness reaches the behavior? | [Harness And Seam-Preparation Gate](#harness-and-seam-preparation-gate) |
| What counts as a valid RED? | [RED Validity Contract](#red-validity-contract) |
| What counts as GREEN? | [GREEN Contract](#green-contract) |
| When are doubles permitted? | [Test-Double Fidelity Contract](#test-double-fidelity-contract) |
| What may happen during REFACTOR? | [REFACTOR Contract](#refactor-contract) |
| When does the loop repeat or stop? | [Coverage And Repetition Contract](#coverage-and-repetition-contract) |
| Which references load for each branch? | [Runtime Context Loading Contract](#runtime-context-loading-contract) |
| What does TDD return? | [Return Contract](#return-contract) |
| Which capability owns each handoff? | [Relationship Ownership](#relationship-ownership) |
| Where does each rewrite change belong? | [Runtime Ownership And Change Map](#runtime-ownership-and-change-map) |
| What must pass before promotion? | [Staged Behavior-Evaluation Protocol](#staged-behavior-evaluation-protocol), [Migration And Acceptance Matrix](#migration-and-acceptance-matrix), and [Promotion Gate And Residual Gaps](#promotion-gate-and-residual-gaps) |

# Layer One: Orientation

## North Star

TDD owns one inner loop: prove one settled production behavior through an observed behavioral RED, the smallest GREEN implementation, and behavior-preserving REFACTOR, then return inspectable proof to the caller.

The loop is a design instrument, not a test-count target. It should:

- cross the highest meaningful caller-facing seam available in the bounded slice;
- derive expected behavior from an independent oracle;
- keep owned in-process behavior real;
- expose design pressure instead of hiding it behind private hooks or indiscriminate mocks;
- distinguish a valid behavioral failure from setup, harness, or unrelated failure;
- preserve correct assertions and unrelated work; and
- end with evidence that lets the caller continue delivery without reconstructing the cycle.

The invariant is blunt:

```text
No observed behavioral RED before production implementation, no TDD claim.
```

After-the-fact proof may be useful, but it is classified honestly and never promoted into RED evidence.

## Design Verdict

This table summarizes the selected design. It does not create runtime rules.

| Stratum | Selected shape | Rewrite status |
| --- | --- | --- |
| Core loop | `TRACE -> RED -> GREEN -> REFACTOR -> RETURN`, one tracer bullet at a time | Ready for later extraction from Layer Two |
| Invocation | Implicitly invocable for settled red-testable new behavior and fully known red-capable bugs | Preserve `allow_implicit_invocation: true` |
| Bug boundary | TDD starts only when expected behavior, exact symptom, cause, and a trusted red-capable reproduction are known | Keep disjoint from `$diagnosing-bugs` and prevent handoff bounce |
| Design boundary | Throwaway design questions go to `$prototype`; TDD proves production behavior | Preserve prototype as design evidence, never production proof |
| Test stance | Behavior-first and classicist by default; real owned code, local substitutes, fakes, then stubs, then mocks at true adapters | Extract between `SKILL.md`, `tests.md`, and `mocking.md` |
| Refactor stance | Refactor only while GREEN, preserve behavior and the current public contract, and stop at the bounded slice | Extract into `refactoring.md` with scoped follow-up routes |
| Return | One complete proof packet, or one honestly classified handoff, support gap, decision need, or after-the-fact result | Strengthen without adding a ledger or schema helper |
| Verification | Structural contracts plus control-based fresh-context behavior evaluation and mirror parity | Required before promotion |

The first rewrite should not add a state file, helper script, test-framework abstraction, generated packet schema, autonomous review, tracker mutation, or an encyclopedia of testing techniques. TDD is a compact inner loop whose precision comes from gates, not machinery.

## Delivery Boundary

TDD sits inside a caller-owned delivery flow:

```text
caller fixes scope and authority
  -> TDD proves one or more settled behaviors
  -> TDD returns proof
  -> caller resumes wider validation, review, Git, tracker, and closeout
```

Typical callers are `$implement`, a bounded Parallel Implement lane worker, or a user who directly owns the slice. `$diagnosing-bugs` may hand off only after it has established all four bug facts and must retain the original return owner.

TDD owns test and production edits needed for its bounded tracer bullets. It does not own issue selection, campaign scope, formal review, staging, commit, push, tracker mutation, publication, deployment, or delivery closeout.

## Leading-Word Runtime Model

The eventual skill should use a small stable vocabulary:

| Leading word | Runtime meaning |
| --- | --- |
| **TRACE** | Reconcile authority and evidence, then lock one behavior, source, seam, oracle, and focused command |
| **Tracer bullet** | One narrow vertical path whose observable outcome represents one materially distinct acceptance behavior |
| **RED** | Observe the focused test fail because the settled behavior is missing or wrong |
| **GREEN** | Make the smallest production change and prove the behavior plus nearby compatibility |
| **REFACTOR** | Improve structure while observable behavior and the current public contract stay GREEN |
| **RETURN** | Reconcile assigned coverage and emit one complete, honestly classified result |
| **Oracle** | An expectation derived independently from the production implementation |
| **Seam** | The highest useful stable interface or observable boundary through which the behavior can be proved |
| **Classicist** | Keep owned in-process collaborators real and replace only genuine boundaries with the least powerful adequate substitute |
| **Quarantine** | Temporarily set aside only current-cycle production implementation authored for this behavior so RED can be observed safely |

The words orient execution. The indexed Layer Two contracts decide admission, transitions, completion, proof, and Return.

## Cycle Vocabulary

| Term | Meaning |
| --- | --- |
| **Settled behavior** | An observable outcome whose source, public commitment, and expected result no longer require a user-owned decision |
| **Red-capable** | A repo-native automated path can exercise the selected seam and can fail specifically when the behavior is missing or wrong |
| **Behavioral RED** | An observed failure causally attributable to missing or wrong behavior, not to the test apparatus or unrelated state |
| **Focused command** | The narrowest repo-owned command that executes the tracer bullet and returns trustworthy diagnostics |
| **Nearest relevant group** | The smallest maintained test group that detects compatibility damage around the selected seam beyond the focused test |
| **Materially distinct behavior** | A branch, failure mode, boundary value, permission rule, state transition, integration effect, or migration risk with a different observable outcome or oracle |
| **Semantically equivalent variation** | Different data that exercises the same behavior, seam, and oracle without adding a new risk-bearing branch |
| **Seam preparation** | Bounded behavior-preserving work done before a claimed RED cycle solely to make the settled behavior red-testable |
| **After-the-fact proof** | Evidence added after production behavior already exists or when safe RED observation is impossible; useful validation, but not TDD evidence |

## End-To-End Explanatory Flow

```text
admit settled red-testable behavior
  -> TRACE one tracer bullet
  -> observe valid behavioral RED
  -> implement smallest GREEN
  -> run focused and nearest relevant proof
  -> optionally REFACTOR while GREEN
  -> choose next materially distinct behavior or RETURN
```

Failure branches return to their owner:

```text
unsettled bug fact ----------------------> diagnosing-bugs
throwaway design question --------------> prototype
unsettled commitment -------------------> caller decision
no authorized red-capable harness ------> support-gap result
immediate pass / invalid RED ------------> reassess test, seam, oracle, or need
out-of-slice GREEN cleanup --------------> recommend simplify-code and stop
bounded seam redesign outside slice ----> recommend codebase-design and stop
wide unclassified improvement ----------> recommend improve-codebase and stop
```

# Layer Two: Normative Design

## Normative Home Index

| Concern | Sole normative home |
| --- | --- |
| Invocation and eligibility | [Invocation And Admission](#invocation-and-admission) |
| Mutation and caller authority | [Authority And Mutation Boundary](#authority-and-mutation-boundary) |
| Legal next operation | [Cycle State And Transition Contract](#cycle-state-and-transition-contract) |
| Operation completion | [Operation And Completion Contracts](#operation-and-completion-contracts) |
| Tracer-bullet identity and source | [Source Trace And Tracer-Bullet Contract](#source-trace-and-tracer-bullet-contract) |
| Seam and oracle | [Proof Seam And Independent Oracle](#proof-seam-and-independent-oracle) |
| Missing harness and prefactor | [Harness And Seam-Preparation Gate](#harness-and-seam-preparation-gate) |
| Test shape | [Behavior-Test Contract](#behavior-test-contract) |
| Valid RED and quarantine | [RED Validity Contract](#red-validity-contract) |
| Minimal implementation and GREEN proof | [GREEN Contract](#green-contract) |
| Test-double use | [Test-Double Fidelity Contract](#test-double-fidelity-contract) |
| GREEN-only cleanup | [REFACTOR Contract](#refactor-contract) |
| Coverage and repeated cycles | [Coverage And Repetition Contract](#coverage-and-repetition-contract) |
| Runtime disclosure | [Runtime Context Loading Contract](#runtime-context-loading-contract) |
| Return forms and fields | [Return Contract](#return-contract) |
| Cross-skill boundaries | [Relationship Ownership](#relationship-ownership) |

## Invocation And Admission

Keep TDD implicitly invocable. The description must front-load two positive entry predicates and the two closest handoffs:

1. **New behavior:** the production behavior is settled, inside a bounded authorized slice, and a meaningful red-capable path is known or can be created within existing authority.
2. **Bug:** expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are all known before TRACE.

Reject or hand off before production mutation when any required fact is absent:

| Observed need | Result |
| --- | --- |
| Bug behavior, symptom, cause, or trusted red-capable reproduction is uncertain | Hand off to `$diagnosing-bugs`, retaining the original caller |
| The open question is throwaway design evidence rather than production proof | Hand off to `$prototype` |
| Product behavior, public contract, oracle authority, or another commitment is unsettled | Return a decision-needed result to the caller |
| Existing behavior needs only bounded behavior-preserving cleanup | TDD is not the owner; use the applicable simplification route |
| A diff needs review without implementation | TDD is not the owner; the caller selects review |
| Only after-the-fact validation is possible | Validation may proceed if authorized, but the result cannot be classified as TDD |

The admission check repeats at direct entry and after every handoff. Evidence may change eligibility; merely renaming the route may not. TDD and Diagnosis never bounce on the same unchanged facts.

## Authority And Mutation Boundary

The caller supplies or owns:

- the bounded slice and commitment boundary;
- authorization for production and test edits;
- selected acceptance criteria and any required proof breadth;
- review, staging, commit, tracker, push, publication, deployment, and closeout; and
- acceptance of residual risk outside the inner loop.

TDD may:

- inspect the Source Trace, repository, nearby tests, and repo-owned proof commands;
- edit tests and production code inside the authorized tracer-bullet slice;
- add the smallest repo-native automated harness inside scope;
- perform behavior-preserving seam preparation only under the gate below; and
- refactor current-slice code while GREEN.

TDD must not:

- add dependencies, services, public test hooks, persisted production instrumentation, or external mutations without authority;
- weaken settled behavior or a correct assertion to obtain GREEN;
- delete, overwrite, or quarantine user, pre-existing, or unrelated work;
- widen the commitment boundary, select additional delivery items, or create tracker work;
- stage, commit, push, publish, deploy, formally review, or close the caller's work; or
- represent after-the-fact proof, a prototype, manual observation, or structural proxy as observed RED.

Before resuming mutation after feedback, handoff, or wait, refresh Git and work state and reread every in-scope file to be touched, as required by the engineering contract.

## Cycle State And Transition Contract

Current evidence selects exactly one legal operation. This table is the sole transition authority.

| Current fact | Legal operation | Completion transition | Illegal shortcut |
| --- | --- | --- | --- |
| Entry predicates are not established | Admission or handoff | All predicates hold, or one typed non-TDD result returns | Editing a test or production code |
| Entry holds but no tracer bullet is locked | TRACE | Behavior, source, seam, oracle, and command are reconciled | Writing production implementation |
| TRACE exposes no authorized red-capable path | Harness or seam-preparation gate | Red-capable path exists under authority, or support gap returns | Manual proof treated as RED |
| Test has not run against the pre-implementation behavior | RED | Expected behavioral failure is observed and recorded | GREEN implementation begins |
| RED passes immediately, errors, or fails for another reason | Repair or reassess RED | Valid behavioral RED is observed, or non-TDD result returns | Treating any failure as RED |
| Valid RED is recorded | GREEN | Focused and nearest relevant proof pass through the selected seam | Refactoring, widening, or weakening the assertion |
| GREEN holds and no material cleanup is selected | Repeat-or-RETURN decision | Next distinct tracer bullet is locked, or RETURN begins | Adding future behavior under the current test |
| GREEN holds and material in-slice cleanup is selected | REFACTOR | Behavior and nearby compatibility remain GREEN after the move | Changing behavior or public contract |
| REFACTOR is GREEN | Repeat-or-RETURN decision | Next distinct tracer bullet is locked, or RETURN begins | Out-of-slice cleanup |
| Assigned criteria are proved, next work is equivalent, or a decision/gap blocks progress | RETURN | One complete typed result is reconciled | Claiming delivery closeout |

When the current fact is ambiguous, refresh evidence. Do not guess a later transition.

## Operation And Completion Contracts

| Operation | Complete only when |
| --- | --- |
| **TRACE** | One observable behavior, source, meaningful seam, independent oracle, and focused command are named; authority and material distinctness are reconciled |
| **RED** | The focused test ran before production implementation for this behavior and failed specifically because the behavior is missing or wrong; command, observed result, and causal explanation are retained |
| **GREEN** | The focused behavior passes through the chosen seam, the nearest relevant group passes, and the correct assertion remains intact |
| **REFACTOR** | Each selected move preserves observable behavior and the current public contract; focused proof ran after each move and the nearest relevant group passes before leaving the bullet |
| **RETURN** | Assigned acceptance coverage is reconciled; every implemented behavior has its proof; every skip, after-the-fact result, handoff, blocker, and residual risk is explicit; caller-owned closeout remains untouched |

An operation's artifact is not its completion. A test file, failing command, passing focused test, cleanup diff, or narrative summary cannot substitute for the owning completion row.

## Source Trace And Tracer-Bullet Contract

Reuse the caller's Source Trace when supplied. Otherwise trace the selected behavior to the governing request, acceptance criterion, public contract, domain decision, bug evidence when applicable, and repo validation authority.

Lock exactly one tracer bullet before RED:

- **Behavior:** one observable outcome in domain language;
- **Source:** the exact commitment or evidence that authorizes the expectation;
- **Seam:** the highest useful stable interface or observable boundary available in the bounded slice;
- **Oracle:** an expected result derived independently from production implementation; and
- **Command:** the focused repo-owned command that exercises the bullet.

Choose an acceptance-critical or highest-risk behavior first. When no path is proved and risk does not dictate otherwise, begin with the narrow happy path that crosses the real system. Do not batch horizontal layers or prewrite a suite of future tests before closing the current cycle.

Several assertions may jointly prove one behavior. One assertion per test is not a rule. One test may be insufficient when one behavior has several independently observable effects whose joint truth is the acceptance contract.

## Proof Seam And Independent Oracle

Choose the seam from repository evidence, not from convenience alone.

Prefer, in order:

1. the caller-facing interface where the accepted behavior is observed;
2. a stable module contract for dense in-process logic when it carries the behavior meaningfully;
3. a real boundary adapter contract when the external interaction itself is the behavior or risk.

Private helpers, internal call order, storage shape, and test-only production hooks are not preferred seams. If the behavior is difficult to reach, treat that pressure as evidence about ownership or interface depth before adding indirection.

The oracle must come from a specification, accepted literal, domain invariant, worked example, trusted fixture, independent implementation, or other source not computed by the production path under test. An assertion that reproduces the same algorithm, reads the value it claims to predict, or mirrors internal representation is not independent.

Ask the caller only when behavior, public contract, oracle authority, or another user-owned commitment remains unsettled. Technical seam choice stays agent-owned inside the bounded slice.

## Harness And Seam-Preparation Gate

If no red-capable harness reaches the chosen seam:

1. inspect maintained nearby tests and repo commands;
2. create the smallest repo-native automated check only when it stays inside the authorized slice;
3. avoid new dependencies, services, public hooks, or external mutation without explicit authority; and
4. return a support gap when a trustworthy RED still cannot be observed.

Manual proof is not RED.

Behavior-preserving seam preparation may occur before a claimed cycle only when existing focused tests already protect current behavior. Run that proof before the preparation, make the smallest reversible structural move, rerun it, and then begin a fresh RED cycle for the new behavior. If current behavior lacks trustworthy proof or the preparation widens scope, return support work instead.

Seam preparation never counts as GREEN for the new behavior and never authorizes a TDD claim by itself.

## Behavior-Test Contract

A focused behavior test should:

- name the domain behavior or accepted outcome;
- arrange meaningful state rather than internal implementation scaffolding;
- act through the selected seam;
- assert observable outcomes from the independent oracle;
- include the smallest setup that preserves semantic fidelity; and
- fail with diagnostics that distinguish missing behavior from harness failure.

Use semantic assertions instead of snapshots when the expected meaning can be stated directly. Use a snapshot only when the serialized or rendered shape is itself the maintained contract and review noise remains bounded.

For asynchronous behavior, wait on the observable condition or event with a bounded timeout and a useful failure diagnostic. Use elapsed delay only when time itself is the behavior; observe the trigger, derive the duration from the contract, and state why it proves the outcome.

Treat these as design-pressure signals:

- the name describes helpers, calls, layers, or storage rather than behavior;
- expected values are derived from production implementation;
- setup overwhelms the behavior;
- a private method or owned collaborator must be mocked to make the test possible;
- internal movement breaks the test without changing behavior; or
- semantically equivalent data variations multiply tests without adding an outcome or oracle.

Signals trigger reconsideration; they are not automatic reasons to delete a useful test.

## RED Validity Contract

Write and run the focused behavior test before production implementation for that behavior.

RED is valid only when all conditions hold:

- the test ran through the selected seam;
- it failed on the current pre-implementation behavior;
- the observed result matches the predicted missing or wrong behavior;
- setup, imports, collection, fixtures, syntax, environment, and unrelated baseline failures did not cause it; and
- the command and causal explanation are retained for Return.

Invalid RED branches:

| Observation | Required response |
| --- | --- |
| Test passes immediately | Reassess whether behavior already exists, the assertion is weak, the seam is wrong, or the test does not reach production; do not implement from that result |
| Test errors or fails in setup | Repair the test, fixture, command, or environment and rerun |
| Unrelated baseline failure masks the behavior | Isolate or report the baseline problem without claiming RED |
| Expected and observed failure differ | Reconcile the Source Trace, oracle, seam, and test before proceeding |
| Safe RED cannot be observed | Return after-the-fact or support-gap evidence and do not claim TDD |

When implementation for this behavior was authored during the current cycle before RED was observed, quarantine only that authored implementation, preserve all pre-existing and user work, run RED, then reconcile the quarantined change. Never delete or overwrite broad dirty state to manufacture a baseline.

## GREEN Contract

After valid RED, make the smallest production change that satisfies the tracer bullet. Avoid future behavior, speculative abstraction, unrelated fixes, and cleanup that is not needed to reach trustworthy GREEN.

Run:

1. the focused test; then
2. the nearest relevant maintained test group.

GREEN holds only when the behavior passes through the chosen seam, nearby compatibility passes, output is trustworthy, and the correct assertion remains intact.

Change the test only when new evidence proves its Source Trace, oracle, or seam was wrong. Record that correction and observe a new valid RED. Never relax a correct assertion, remove a required observable effect, or replace semantic proof with an easier internal assertion to manufacture GREEN.

If the focused test passes but nearby proof fails, remain in GREEN work. Determine whether the implementation caused the regression, the baseline is unrelated, or the selected behavior conflicts with another commitment. Repair only the authorized cause; return uncertainty or a decision need instead of broadening silently.

## Test-Double Fidelity Contract

Keep owned in-process modules behind the tested interface real. Replace only a genuine boundary adapter, using the least powerful adequate option:

1. real in-process code;
2. local substitute such as an in-memory store, isolated `.tmp/` filesystem, test database, or local emulator;
3. fake adapter preserving required behavior;
4. stub for one controlled response; and
5. mock adapter only when the external interaction contract is itself the behavior or risk.

Before adding a double, establish:

- the real seam it replaces;
- why real code or a local substitute is insufficient;
- every consumed success value, failure mode, side effect, ordering guarantee, and contract field relevant to the path;
- whether the test survives internal movement; and
- how fidelity will be checked.

When the repository has adapter contract tests, run the same contract against the double and the real or local implementation. Otherwise record the unverified fidelity risk. Assert calls or ordering only when that interaction is the public adapter contract under test.

If fidelity is unclear or double setup overwhelms the behavior, reconsider the seam. Keep provider and transport shapes behind a narrow domain-facing adapter. Put test setup, cleanup, and inspection in test utilities, not production interfaces.

## REFACTOR Contract

Refactor only while GREEN. Preserve observable behavior and the current public contract. Intended behavior or contract changes begin a new RED cycle.

Select one meaningful in-slice move at a time. Prefer moves that increase:

- **depth:** more useful behavior behind a smaller stable interface;
- **leverage:** one well-owned decision replaces repeated shallow mechanics; or
- **locality:** related behavior and knowledge move toward their owner.

Eligible moves include removing current-slice duplication, sharpening domain names, moving behavior to its owning module, deepening a shallow module, consolidating scattered decisions, and deleting implementation-detail tests only after stronger behavioral protection demonstrably supersedes them.

After each move, run the focused test. Before leaving the tracer bullet, run the nearest relevant group. Keep test-only hooks out of production interfaces.

Stop refactoring when the selected material cleanup is complete, the next move changes behavior or public contract, proof stops being GREEN, or the next improvement exceeds the bounded slice.

Out-of-slice results are evidence, not permission:

| Observed follow-up | Return boundary |
| --- | --- |
| Settled bounded behavior-preserving cleanup | Recommend `$simplify-code` and stop |
| One already-framed interface or seam question | Recommend `$codebase-design` and stop |
| Wide discovery or unclassified structural improvement | Recommend `$improve-codebase` and stop |

TDD does not create a tracker item or start the recommended capability.

## Coverage And Repetition Contract

After GREEN or REFACTOR, reconcile the assigned acceptance criteria and state-boundary obligations supplied by the caller or repo contract.

Start a new TRACE and RED cycle for each materially distinct acceptance behavior. Distinctness is semantic, not a test-count or line-count rule. A boundary value, failure, permission, state transition, integration effect, or migration case deserves another cycle when it changes the observable outcome, oracle, risk, or proof seam.

Stop when:

- every assigned behavior is proved;
- remaining inputs are semantically equivalent variations already covered by the same behavior and oracle;
- the next behavior requires a user-owned decision;
- the next work needs unavailable authority or a trustworthy harness; or
- a handoff owner must resolve uncertainty.

Do not infer new acceptance scope from nearby opportunities. Do not stop merely because one happy path passes when the assigned contract contains distinct failure, state, permission, or integration behavior.

## Runtime Context Loading Contract

Keep universal behavior in `SKILL.md`: outcome, admission, caller boundary, the five-operation spine, each operation gate, context pointers, Return, and completion.

Load additional context only when its predicate fires:

| Context | Load condition | Must not absorb |
| --- | --- | --- |
| `docs/agents/engineering-contract.md` | The caller did not already load the repo contract and the file exists | TDD-specific procedure |
| `docs/agents/domain.md` and routed domain source | Domain routing is needed and the file exists | General TDD rules |
| `tests.md` | Nearby tests do not settle test shape, oracle, async waiting, or seam | Admission, cycle state, or double procedure |
| `mocking.md` | A real boundary may require a test double | Generic test taste or refactor procedure |
| `refactoring.md` | GREEN holds and a material in-slice refactor is selected | RED, GREEN implementation, or wide cleanup |
| `$diagnosing-bugs` | A bug admission fact is uncertain | TDD implementation before causal proof |
| `$prototype` | The needed artifact is throwaway design evidence | Production proof or promotion |

Do not preload all references, source books, other skills, or testing taxonomies. A pointer is effective only when its trigger is sharp enough to load the reference at the moment it changes behavior.

## Return Contract

Every invocation returns exactly one result form.

### Proved TDD

- **Outcome:** `proved-tdd`;
- **Source Trace:** each behavior, source, seam, and oracle;
- **RED:** command, observed failing result, and why it was the expected behavioral failure;
- **GREEN:** focused and nearest-group commands with passing results;
- **Coverage:** assigned criteria and materially distinct branches proved, plus every justified skip;
- **Refactor:** each material move and proof, or `none`;
- **Work state:** files changed and preservation notes relevant to the caller;
- **Residual risk:** remaining uncertainty or `none`; and
- **Return owner:** the caller that resumes wider delivery.

### Non-TDD Evidence

- **Outcome:** `after-the-fact` or `support-gap`;
- **Reason:** why valid RED was absent or unsafe;
- **Evidence:** commands and observations actually obtained;
- **Work state:** tests or production changes retained, quarantined, or untouched;
- **Needed authority or support:** exact missing capability, or `none`;
- **Residual risk:** what the evidence cannot prove; and
- **Return owner:** the original caller.

### Handoff Or Decision

- **Outcome:** `handoff` or `decision-needed`;
- **Observed facts:** the admission or commitment facts established;
- **Missing fact or question:** the exact blocker;
- **Next owner:** one owning capability or the accountable caller;
- **Work state:** confirmation that unauthorized production mutation did not occur; and
- **Return owner:** the original caller retained across the handoff.

Completion is an inner-loop result, never delivery completion. A proved TDD packet does not imply formal review, commit, tracker closeout, push, publication, deployment, or release.

## Relationship Ownership

| Caller or callee | Relationship | TDD-owned boundary | Foreign owner retains |
| --- | --- | --- | --- |
| Direct user | Enter | Admit only a bounded settled red-testable behavior; return inner-loop proof | Scope decisions and wider closeout |
| `$skill-router` | Route | TDD description exposes the positive new-behavior and four-fact bug predicates | Router returns one route and stops |
| `$implement` | Invoke and resume | Execute red-green-refactor and return proof to the selected item owner | Fixed point, wider proof, review, Git, tracker, and Lock |
| `$parallel-implement` lane worker | Invoke and resume | Execute only the assigned lane's tracer bullets and return proof | Lane isolation, worker receipt, integration, review, ledger, and Release |
| `$diagnosing-bugs` | Mutual handoff | Enter TDD only after all four bug facts are known; hand uncertainty back without mutation or bounce | Causal loop, trusted reproduction, and original caller identity |
| `$prototype` | Hand off | Recognize a design-evidence question and stop production proof | Throwaway probe, verdict, cleanup, and artifact reconciliation |
| `$simplify-code` | Recommend and stop | Name settled bounded cleanup found while GREEN | Cleanup procedure and proof |
| `$codebase-design` | Recommend and stop | Name one already-framed out-of-slice seam or interface question | Design alternatives, choice, and caller-facing proof surface |
| `$improve-codebase` | Recommend and stop | Name wide or unclassified improvement evidence | Survey, classification, and next owner |

Relationship exclusions:

- TDD never invokes formal review, creates tracker work, commits, pushes, publishes, deploys, or closes delivery.
- TDD does not absorb Diagnosis, Prototype, Codebase Design, Simplify Code, or Improve Codebase procedure.
- Implement and Parallel Implement must point to TDD rather than copy red-green-refactor mechanics.
- Diagnosis and TDD repeat the four-fact predicate at their independently entered boundary because omission would reintroduce unsafe routing and bounce.

# Layer Three: Evidence And Rationale

## Source Pressure And Selected Use

The prior source-map synthesis is retained here as rationale. These sources inform the design; they do not become runtime dependencies.

| Source | Pressure retained in the design | Selected runtime use | Limit |
| --- | --- | --- | --- |
| Kent Beck, *Test-Driven Development: By Example* | Red-green-refactor is a design loop; write the next smallest useful test; observe RED before implementation | Five-operation spine, behavioral RED gate, smallest GREEN, new RED for behavior change | The rewrite adapts examples to repo-owned proof and caller authority |
| Martin Fowler, *Refactoring* | Refactoring changes structure while preserving observable behavior | GREEN-only REFACTOR, one move at a time, new RED for behavior or contract change | Broad cleanup remains outside TDD |
| Steve Freeman and Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* | Grow design from observable behavior and outside-in pressure | Tracer bullets, meaningful interfaces, boundary adapters | Local policy remains classicist by default rather than mock-led |
| Gerard Meszaros, *xUnit Test Patterns* | Precise double vocabulary, fixture trade-offs, and test smells matter | Fake/stub/mock distinctions, fidelity gate, test-pressure signals | Taxonomy stays in disclosed reference, not the common path |
| Michael Feathers, seam and legacy-code work | Tests gain control through useful seams; poor testability is design evidence | Seam selection, bounded seam preparation, no private test hooks | TDD does not absorb open-ended legacy discovery |
| Lasse Koskela, *Effective Unit Testing* | Tests should read as maintainable behavior specifications | Domain names, semantic assertions, implementation-coupling signals | Readability never substitutes for semantic proof |
| John Ousterhout, *A Philosophy of Software Design* | Deep modules and small interfaces reduce cognitive load | REFACTOR pressure toward depth, leverage, and locality | TDD does not mandate new abstractions or seams |
| Martin Fowler, *Mocks Aren't Stubs* | Classicist and mockist styles carry different coupling | Real owned code and local substitutes before mocks | Interaction tests remain valid when interaction is the adapter contract |
| Martin Fowler, *Test Double* | Shared double vocabulary prevents vague "mock everything" behavior | Least-powerful adequate substitute order | Labels alone do not prove fidelity |

Primary source links retained from the earlier synthesis:

- Beck: <https://www.oreilly.com/library/view/test-driven-development/0321146530/>
- Fowler, *Refactoring*: <https://martinfowler.com/books/refactoring.html>
- Freeman and Pryce: <https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/>
- Meszaros: <https://martinfowler.com/books/meszaros.html>
- Feathers, seam reference: <https://martinfowler.com/bliki/LegacySeam.html>
- Koskela: <https://www.manning.com/books/effective-unit-testing>
- Ousterhout: <https://web.stanford.edu/~ouster/cgi-bin/book.php>
- Fowler, *Mocks Aren't Stubs*: <https://martinfowler.com/articles/mocksArentStubs.html>
- Fowler, *Test Double*: <https://martinfowler.com/bliki/TestDouble.html>

## Why Observed RED Is Non-Negotiable

A passing test shows compatibility with current code; it does not show that the test detects the missing behavior. Observed behavioral RED supplies the negative control for the test itself. Without it, a weak assertion, wrong seam, fixture shortcut, or already-existing behavior can masquerade as proof.

This is why the design classifies after-the-fact checks honestly instead of banning them. They may improve coverage, but they answer a different evidence question.

## Why One Tracer Bullet At A Time

One vertical cycle keeps cause and effect legible: the failing expectation, production response, design pressure, and refactor all concern the same behavior. Horizontal batches of tests or implementation layers defer feedback and make it easier to satisfy the wrong abstraction.

The discipline is semantic, not microscopic. A tracer bullet may cross several modules and use several assertions when that is the smallest path that proves one acceptance behavior.

## Why The Oracle Is Separate From The Seam

The seam answers where behavior is observed. The oracle answers why the expected result is correct. A public interface with an implementation-derived expectation still produces circular proof; an independent literal asserted against a private helper still chooses a weak seam. The design therefore locks both.

## Why Classicist Is The Default

Keeping owned modules real preserves the design pressure that TDD is meant to reveal. Mocking them can make a shallow interface appear testable while coupling tests to calls rather than behavior. Genuine external boundaries are different: a faithful fake, stub, or mock may be the only safe deterministic way to exercise the owned path.

The fidelity gate prevents convenience doubles from silently deleting failure behavior, side effects, contract values, or ordering guarantees consumed by production.

## Why REFACTOR Is Scoped And GREEN

GREEN makes structural change observable and reversible. Restricting REFACTOR to behavior-preserving in-slice moves prevents the pleasant momentum of cleanup from smuggling new behavior or adjacent redesign into the tracer bullet.

Depth, leverage, and locality are directional pressures, not mandatory outcomes. Retaining a simple current design is valid when further movement adds scope or complexity.

## Why References Stay Conditional

The five-operation spine is the common path. Detailed test examples, double mechanics, and refactor heuristics matter only under specific evidence states. Keeping them behind sharp pointers protects the runtime's information hierarchy while still making non-intuitive mechanics available before they change action.

## Current Evidence Baseline

The current repository already protects several TDD contracts:

- structural tests require `TRACE`, `RED`, `GREEN`, `REFACTOR`, and `RETURN` in order;
- disclosed-file tests require `tests.md`, `mocking.md`, and `refactoring.md`;
- routing tests require the four-fact bug boundary and non-bouncing Diagnosis relationship;
- relationship tests cover the Diagnosis, Prototype, Simplify Code, Codebase Design, and Improve Codebase edges;
- the core-workflow evaluation defines immediate-pass RED, setup error, unrelated failure, assertion weakening, nearby regression, behavior-changing refactor, distinct boundary behavior, implementation-derived oracle, owned-module mocks, low-fidelity fakes, out-of-slice cleanup, and incomplete packet cases; and
- the canonical and installed TDD files were hash-equal when this synthesis was authored.

This is structural and historical evidence, not proof that the proposed rewrite improves runtime behavior. Future evaluation must lock a fresh control at extraction time.

## Deliberate Non-Changes

- Keep TDD implicitly invocable; settled red-testable behavior should not require a human to remember an explicit-only command.
- Keep the five-operation linear spine; a persistent campaign state machine would exceed the inner loop's needs.
- Keep caller-owned scope and closeout; TDD must remain composable inside ordinary and parallel delivery.
- Keep the four-fact bug predicate explicit at every independently entered boundary.
- Keep manual proof outside RED while allowing it to be reported honestly as supplementary evidence.
- Keep one test capable of several assertions when they jointly prove one behavior.
- Keep focused module tests valid when a stable module contract carries semantic behavior.
- Keep mocks available for true adapter contracts; reject only indiscriminate or owned-module mocking.
- Keep source books out of runtime context.
- Keep the installed mirror unchanged until the coordinated canonical candidate passes and synchronization is separately authorized.

## Rejected Machinery

- a helper script or JSON schema for the proof packet;
- a cycle ledger or persisted TDD state file;
- one file per operation;
- framework-specific commands in the universal skill;
- mandatory test counts, assertion counts, coverage percentages, or test pyramids;
- snapshot prohibition as a universal rule;
- automatic property-based, fuzz, mutation, contract, or end-to-end test generation;
- mock-first outside-in implementation;
- public production hooks solely for tests;
- automatic issue creation for support or refactor work; and
- formal review, Git, tracker, or release procedure inside TDD.

Each adds context or authority without strengthening the universal behavioral gate.

## Deferred Hypotheses

These may be explored later only after an observed failure justifies them:

- whether a short machine-readable proof-packet shape improves caller resumption enough to justify compatibility cost;
- whether explicit property, metamorphic, contract, or mutation-testing pointers improve specific domain branches without bloating the common path;
- whether the phrase `seam preparation` steers more reliably than `GREEN prefactor` in fresh-context evaluation;
- whether performance, concurrency, or nondeterministic behavior needs a dedicated TDD reference beyond repo-owned proof discipline; and
- whether repeated behavior evaluations expose a need to split test taste into distinct conditional references.

None is part of the first rewrite unless promoted into Layer Two with a demonstrated failure, owner, and verification plan.

# Layer Four: Extraction And Verification

## Proposed Runtime Semantic Surface

The eventual runtime should expose this semantic order:

1. **Frontmatter description:** positive new-behavior and four-fact bug triggers; Diagnosis and Prototype handoffs.
2. **Outcome and boundary:** one inner loop, observed RED invariant, caller-owned closeout.
3. **Context pointers:** engineering/domain contract plus conditional test, double, and refactor references.
4. **TRACE:** admission refresh, Source Trace, tracer bullet, seam, oracle, command, and harness gate.
5. **RED:** pre-implementation execution, validity branches, quarantine, and evidence.
6. **GREEN:** minimal implementation, focused and nearby proof, correct-assertion protection.
7. **REFACTOR:** GREEN-only in-slice moves and routed out-of-slice follow-ups.
8. **RETURN:** distinctness decision, typed proof or non-TDD result, residual risk, original caller.
9. **Completion:** every claimed behavior crossed all applicable gates and appears in Return.

The main skill should stay compact. Branch-specific examples and mechanics belong in the three disclosed references under their indexed owners.

## Runtime Ownership And Change Map

| Bundle | Runtime surface | Owns | Proposed delta | Must not absorb |
| --- | --- | --- | --- | --- |
| `T1` | `skills/custom/tdd/SKILL.md` | Invocation, boundary, five-operation spine, universal gates, context pointers, Return, completion | Extract Layer Two into concise positive contracts; preserve blunt RED invariant and original caller | Detailed examples, double taxonomy, broad refactor guidance, source rationale, caller closeout |
| `T1` | `skills/custom/tdd/agents/openai.yaml` | Implicit invocation policy and discoverability metadata | Preserve `allow_implicit_invocation: true`; align description behavior through the skill frontmatter | Procedure or duplicated gates |
| `T2` | `skills/custom/tdd/tests.md` | Test shape, semantic assertions, oracle examples, async waiting, design-pressure signals | Add only examples needed to make the Behavior-Test contract operational | Admission, state transitions, doubles, refactor routes |
| `T3` | `skills/custom/tdd/mocking.md` | Substitute order, adapter boundary, fidelity gate, contract-test pressure | Reconcile every consumed success/failure behavior and interaction-contract exception | Generic test taste, owned-module procedure, provider-specific setup |
| `T4` | `skills/custom/tdd/refactoring.md` | GREEN-only moves, depth/leverage/locality, proof cadence, scoped follow-ups | Make stop and routing boundaries checkable | New behavior, wide cleanup, tracker mutation, full foreign-skill procedure |
| `T5` | `docs/synthesis/skill-context-relationships.md` | Accepted cross-skill edge index | Keep each TDD edge once and aligned with the four-fact predicate and caller-return boundary | TDD procedure |
| `T5` | `tests/test_skill_pack_contracts.py` | Structural and relationship regressions | Protect semantic surface, references, invocation policy, return fields, and edge ownership without brittle prose coupling | Claims of behavioral improvement |
| `T5` | `docs/validation/evals/core-workflows.md` and evaluation transcripts | Behavior scenarios, rubrics, controls, variance, residual gaps | Expand the TDD tracer-bullet evaluation into staged positive and negative cases | Runtime rules or uninspected string-match proof |
| `T5` | installed TDD mirror | Deployed runtime parity | Synchronize only after canonical validation and separate authorization; verify hashes | Independent edits or partial promotion |
| `T0` | this synthesis | Design authority before extraction | Preserve accepted design, rationale, ownership, and proof plan | Executable runtime authority |

## Staged Extraction Plan

Build one coordinated canonical candidate before installed promotion.

| Stage | Bundles | Extraction outcome | Stage boundary |
| --- | --- | --- | --- |
| `I1` | `T1` | Extract invocation, boundary, transition, operation, context, Return, and completion contracts into the main runtime surface | Every universal Layer Two concern has one concise home and all pointers resolve |
| `I2` | `T2`, `T3`, `T4`, `T5` relationships | Reconcile test taste, doubles, refactoring, and composition without copying foreign procedure | Each branch-specific concern has one owner and the relationship map matches both endpoints |
| `I3` | `T5` tests, evaluations, and mirror | Add structural protection, run control-based behavioral proof, validate canonical source, then perform separately authorized mirror synchronization | Every applicable acceptance row passes, residual gaps meet the promotion gate, and source/mirror hashes agree |

Do not synchronize after `I1` or `I2`. Partial installation would advertise a mixed contract.

## Staged Behavior-Evaluation Protocol

Evaluation phases gate behavior promotion, not partial installation.

| Phase | Claims proved | Representative cases |
| --- | --- | --- |
| `E0`: Control lock | The current skill or no-candidate-guidance arm exhibits the targeted failure on a fixed realistic task | One control per promoted behavioral claim |
| `E1`: Invocation and attention | Correct entry, four-fact bug routing, caller boundary, operation selection, and conditional context loading | Settled new behavior, each missing bug fact, design question, after-the-fact-only path, wrong-reference preload |
| `E2`: Ordinary cycle | TRACE, seam, oracle, valid RED, minimal GREEN, nearby proof, repeated distinct behavior, and complete Return work together | Happy path, stable module seam, multiple observable effects, state branch, equivalent data variation |
| `E3`: Failure and design pressure | Invalid RED, quarantine, harness gap, async proof, doubles, refactor limits, and handoffs preserve truth and authority | Immediate pass, setup error, unrelated failure, assertion weakening, owned-module mock, low-fidelity fake, behavior-changing refactor, out-of-slice cleanup |
| `E4`: Integrated promotion | Relationships, canonical files, structural contracts, installation, and mirror parity agree | Focused and full tests, validator, changed-file read-back, installation dry-run, hash parity |

For each promoted behavioral claim, fix the repository snapshot, prompt, Source Trace, authority, tools, runtime, model, reasoning tier, skill hash, proof commands, and rubric across arms. Run at least five independent fresh-context samples per arm. Use the current skill as control where behavior overlaps and a no-candidate-guidance control for genuinely new behavior. Stop when the control does not exhibit the claimed failure.

Judge behavior, not template echoes. Record invocation, selected operation, references loaded, mutation sequence, commands, observed RED cause, GREEN proof, assertion changes, doubles, refactor scope, Return completeness, token/time evidence when available, protocol deviations, variance, worst outcome, and residual gaps.

An evaluation phase passes only when the control demonstrates the failure, the candidate materially reduces it, variance narrows or does not expose a worse tail, and no new critical failure appears.

## Migration And Acceptance Matrix

This matrix supplies cases and verification. It does not create runtime rules or file placement.

| Stage / phase | Bundles | Behavior and normative owner | Positive case | Negative control | Verification |
| --- | --- | --- | --- | --- | --- |
| `I1 / E1` | `T1` | [Invocation](#invocation-and-admission) | Settled red-testable new behavior enters; a fully known red-capable bug enters | Each bug fact is missing in turn; unsettled behavior, design evidence, cleanup, review-only, or after-the-fact-only work enters TDD | Invocation-policy test plus fresh-context route samples |
| `I1,I2 / E1` | `T1,T5` | [Bug handoff](#relationship-ownership) | Diagnosis returns all four facts and TDD retains the original caller | Diagnosis and TDD bounce on unchanged facts or each claims caller closeout | Relationship regression and multi-turn behavior samples |
| `I1 / E1,E2` | `T1` | [TRACE](#source-trace-and-tracer-bullet-contract) | One acceptance behavior locks source, seam, independent oracle, and command | A horizontal layer, vague behavior, private helper, implementation-derived oracle, or unowned commitment proceeds | Packet-shape contract plus behavior evaluation |
| `I1,I2 / E2,E3` | `T1,T2` | [Harness](#harness-and-seam-preparation-gate) | The smallest repo-native harness reaches the seam, or protected seam preparation stays behavior-preserving before a fresh RED | Manual proof counts as RED; an unproved prefactor, new dependency, service, or public hook is added silently | Harness fixtures, before/after proof, and authority scenarios |
| `I1,I2 / E2,E3` | `T1,T2` | [Behavior test](#behavior-test-contract) | Domain-named test acts through a meaningful seam, uses semantic assertions, and condition-waits with diagnostics | Helper-call naming, circular oracle, snapshot substitution, raw sleep, or setup-heavy shallow seam is accepted without reconsideration | Representative test-design samples and rubric inspection |
| `I1 / E2,E3` | `T1` | [RED](#red-validity-contract) | Focused pre-implementation test fails for the predicted missing behavior and records the observed cause | Immediate pass, collection/setup error, unrelated failure, or mismatched failure is called RED | Failure-injection fixtures and proof-packet assertions |
| `I1 / E3` | `T1` | [Quarantine](#red-validity-contract) | Only current-cycle authored implementation is set aside and reconciled; user and dirty work remain | Broad reset, deletion, or overwrite manufactures RED | Dirty-worktree scenario and changed-file read-back |
| `I1 / E2,E3` | `T1` | [GREEN](#green-contract) | Smallest production change passes focused and nearest proof through the seam | Correct assertion is weakened, future behavior is added, or focused pass hides nearby regression | Diff inspection, focused/group fixtures, and behavior evaluation |
| `I2 / E2,E3` | `T2` | [Coverage](#coverage-and-repetition-contract) | Distinct failure, boundary, permission, state, or integration behavior starts another cycle; equivalent data stops | Happy path ends assigned work early or equivalent variants inflate tests | State/branch matrices and semantic-distinctness samples |
| `I2 / E3` | `T3` | [Doubles](#test-double-fidelity-contract) | Owned modules stay real; a boundary fake preserves every consumed success/failure contract or records risk | Owned module is mocked, interaction details replace outcomes, or the fake omits a consumed failure mode | Adapter contract fixtures and fidelity rubric |
| `I2 / E3` | `T4` | [REFACTOR](#refactor-contract) | One depth, leverage, or locality move preserves behavior and nearby proof | New behavior, public-contract change, test-only hook, proof failure, or wide cleanup continues under REFACTOR | Before/after behavior proof and scope scenarios |
| `I1,I2 / E1,E3` | `T1,T4,T5` | [Follow-up routing](#relationship-ownership) | Settled cleanup, bounded seam design, or wide improvement returns one recommendation and stops | TDD starts the next skill, mutates a tracker, or sends every cleanup to the same owner | Relationship test and fresh-context classification samples |
| `I1,I2 / E1-E3` | `T1-T4` | [Context loading](#runtime-context-loading-contract) | Only the triggered reference loads at the evidence gap or GREEN refactor | All sources and references preload, or a required double/refactor reference is skipped | Reference-resolution tests and context traces |
| `I1 / E2,E3` | `T1` | [Return](#return-contract) | Proved TDD, after-the-fact/support gap, and handoff/decision results are truthfully typed and retain the caller | A passing test implies TDD, an incomplete packet claims completion, or inner-loop proof claims review/commit/closeout | Return-shape tests and incomplete-packet negative controls |
| `I1-I3 / E4` | `T1-T5` | [Runtime ownership](#runtime-ownership-and-change-map) | Canonical references resolve, relationships agree, focused and full validation pass, and authorized mirror hashes match | Procedure duplicates into callers, structural tests substitute for behavior, or partial source reaches the mirror | Focused tests, full pytest, validator, install dry-run, both diff checks, read-back, and mirror parity |

## Promotion Gate And Residual Gaps

A critical failure blocks promotion regardless of averages:

- TDD is invoked for an unsettled behavior or bug missing any of the four facts;
- production implementation begins before valid behavioral RED;
- an immediate pass, setup error, unrelated failure, manual check, prototype, or after-the-fact test is represented as RED;
- the oracle is circular or a weaker seam substitutes for an available meaningful one;
- a correct assertion is weakened to obtain GREEN;
- owned behavior is mocked away or a boundary double omits a consumed contract without recorded risk;
- REFACTOR changes behavior, public contract, or scope without a new RED cycle;
- user or unrelated work is overwritten, quarantined, staged, committed, or otherwise mutated;
- a handoff loses the original caller or bounces without new evidence;
- a proof packet is incomplete or inner-loop completion is represented as delivery closeout; or
- canonical and installed runtime surfaces are partially synchronized or disagree.

Promote a behavioral claim only when E0 demonstrates its failure, the candidate materially reduces it, variance does not reveal a new unstable tail, and no critical failure appears. Structural tests protect order, references, policies, fields, and relationships; they never establish runtime improvement by themselves.

A residual gap blocks promotion when it affects invocation, authority, behavioral RED truth, seam or oracle integrity, assertion preservation, double fidelity, refactor scope, caller identity, Return completeness, or installed parity. Noncritical uncertainty may remain only when the promotion record names its evidence limit, operational consequence, and later validation owner.

## Completion Criterion For The Future Rewrite

The rewrite is complete only when every normative concern has one indexed home; the main skill exposes the proposed compact semantic surface; every entry, transition, operation, context pointer, Return form, and completion gate is discoverable; the three disclosed references own their branches without duplicating the common path; every relationship agrees at both endpoints and in the relationship map; each promoted behavioral claim has a failing E0 control and passes its applicable E1 through E4 phases; no critical or promotion-blocking residual gap remains; canonical focused and full validation pass; diff checks are clean for the rewrite; and the separately authorized installed mirror matches the validated source exactly.
