---
name: tdd
description: 'Test-driven development. Use only when the user explicitly requests TDD, test-first work, or RED-GREEN-REFACTOR, or applicable repository policy requires TDD. Requests for tests, integration tests, regression tests, or coverage alone do not trigger it.'
---

# Test-Driven Development

Own one inner loop:

**TRACE -> RED -> GREEN -> REFACTOR -> RETURN**

**No observed RED, no TDD.** After-the-fact proof may supplement RED evidence;
it cannot replace it.

Admit only under the description's explicit user or repository-policy trigger.
Requests for ordinary tests alone use ordinary implementation without a TDD
packet. Do not require an existing harness before admission: TRACE owns finding
or creating the smallest authorized red-capable check, and returns any meaning,
oracle, support, or authority gap before behavior mutation.

The caller owns bounded scope, review, staging, commit, tracker or external
mutation, publishing, and closeout.

When a hard, intermittent, performance, environment-only, production-only, or
causally ambiguous bug needs dedicated investigation, return
`diagnosis-required` with the intact facts to the caller and stop. An initially
unknown cause does not exclude an ordinary deterministic bug from TDD when its
behavior, symptom, and independent oracle are settled. Return
`design-evidence-required` only when no hard failure requires diagnosis and RED
would encode an unmade
design decision: several live alternatives remain and the choice needs a
runnable, interactive, or measured verdict rather than a test of accepted
behavior. This is not implementation proof because no single accepted behavior
and independent oracle yet decide the choice.

Return the intact facts to the caller and stop with:

- the settled source, constraints, and non-diagnostic facts;
- the exact unresolved design question and live alternatives;
- the decision owner and return owner;
- the discriminating cases, observation, and verdict criteria needed, including
  any unknown criterion; and
- why an implementation RED cannot answer the question without assuming the
  decision.

Read [tests.md](tests.md) only when test shape, oracle, or seam remains unclear
after inspecting nearby tests. Read [mocking.md](mocking.md) before adding a
Test Double. Read [refactoring.md](refactoring.md) only while GREEN.

## 1. TRACE

Apply the caller-loaded engineering contract when supplied; otherwise read
`docs/agents/engineering-contract.md` when present. Follow
`docs/agents/domain.md` when present for domain routing.

Reuse the caller's **Source Trace** or trace the behavior to its request,
acceptance criterion, public contract, and independent oracle.

Choose one **tracer bullet**:

- one observable behavior;
- its source or acceptance criterion;
- the highest useful public interface or seam;
- an independent oracle;
- its existing test owner, if any; and
- the focused test command.

Choose the seam from repo evidence. Ask only when behavior, public contract,
oracle, or a user-owned commitment remains unsettled.

If no red-capable harness reaches the seam, create the smallest repo-native
automated check only within scope. Do not add dependencies, services, or public
test hooks without authority. Manual proof is not RED.

A GREEN prefactor may expose the seam only when focused tests already protect
existing behavior; otherwise return the gap as support work.

## 2. RED

Create one focused RED before implementation. Extend the narrowest
existing behavior test, case table, or contract suite when it can express the
tracer clearly. Add a test only when the tracer has a distinct proof
responsibility; do not overload unrelated behavior.

RED passes its gate only when the test fails for the expected missing or wrong
behavior—not from setup, imports, fixtures, typos, or unrelated breakage.

If it passes immediately, reassess the behavior, assertion, and seam. If it
errors, repair the test or setup and rerun.

Quarantine only implementation authored for this behavior during the current
cycle. If RED cannot be observed safely against the baseline, return
after-the-fact proof and do not claim TDD.

## 3. GREEN

Make the smallest implementation change that satisfies the tracer bullet.

Run the focused test, then the nearest relevant test group. GREEN requires the
focused behavior through the chosen seam and passing nearby tests.

Change the test only when its Source Trace, oracle, or seam was wrong. Preserve
a correct assertion.

## 4. REFACTOR

Refactor only while GREEN. Follow [refactoring.md](refactoring.md), rerun the
focused test after each move, and run the nearest relevant test group before the
next tracer bullet.

Behavior or interface changes start a new RED cycle.

## 5. RETURN

Repeat only for materially distinct acceptance behavior. Stop when the assigned
criteria are proved, remaining cases are semantically equivalent data variations
already covered by the same behavior and oracle, or the next behavior requires a
user-owned decision.

Return:

- **Source Trace:** behavior, source, seam, and oracle;
- **RED:** command, observed failing result, and why it is the expected
  behavioral failure;
- **GREEN:** command and passing result;
- **Test portfolio:** reused, extended, added, consolidated, or removed proof,
  with its distinct responsibility;
- **Coverage:** relevant verification or skipped reason;
- **Refactor:** material cleanup or `none`;
- **Residual risk:** remaining uncertainty or blocker.

Complete only when every implemented behavior crossed observed RED before its
implementation, crossed GREEN through its chosen seam, stayed GREEN
through refactoring, received relevant verification, has an accounted test
responsibility, and appears in the proof packet.
