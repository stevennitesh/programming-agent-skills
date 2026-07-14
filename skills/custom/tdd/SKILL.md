---
name: tdd
description: "Use for tracer-bullet red-green-refactor on red-testable new behavior. For bugs, use only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. Hand off bugs when the exact symptom, cause, or trusted red-capable reproduction is uncertain to $diagnosing-bugs; hand off throwaway design questions to $prototype."
---

# Test-Driven Development

Own one inner loop:

**TRACE -> RED -> GREEN -> REFACTOR -> RETURN**

**No observed RED, no TDD.** After-the-fact proof may supplement RED evidence; it cannot replace it.

The caller owns bounded scope, review, staging, commit, tracker or external mutation, publishing, and closeout.

Hand off to `$diagnosing-bugs` when a bug's exact symptom, cause, or trusted red-capable reproduction is uncertain; it returns regression proof to the original caller. Hand off throwaway design questions to `$prototype`.

Read [tests.md](tests.md) only when test shape, oracle, or seam remains unclear after inspecting nearby tests. Read [mocking.md](mocking.md) before adding a test double. Read [refactoring.md](refactoring.md) only while GREEN.

## 1. TRACE

Apply the caller-loaded engineering contract when supplied; otherwise read `docs/agents/engineering-contract.md` when present. Follow `docs/agents/domain.md` when present for domain routing.

Reuse the caller's **Source Trace** or trace the behavior to its request, acceptance criterion, public contract, and independent oracle.

Lock one **tracer bullet**:

- one observable behavior;
- its source or acceptance criterion;
- the highest useful public interface or seam;
- an independent oracle;
- the focused test command.

Choose the seam from repo evidence. Ask only when behavior, public contract, oracle, or a user-owned commitment remains unsettled.

If no red-capable harness reaches the seam, create the smallest repo-native automated check only within scope. Do not add dependencies, services, or public test hooks without authority. Manual proof is not RED.

A GREEN prefactor may expose the seam only when focused tests already protect existing behavior; otherwise return the gap as support work.

## 2. RED

Write one focused behavior test and run it before production implementation.

RED passes its gate only when the test fails for the expected missing or wrong behavior—not from setup, imports, fixtures, typos, or unrelated breakage.

If it passes immediately, reassess the behavior, assertion, and seam. If it errors, repair the test or setup and rerun.

Quarantine only implementation authored for this behavior during the current cycle. If RED cannot be observed safely against the baseline, return after-the-fact proof and do not claim TDD.

## 3. GREEN

Make the smallest production change that satisfies the tracer bullet.

Run the focused test, then the nearest relevant test group. GREEN requires the focused behavior through the chosen seam and passing nearby tests.

Change the test only when its Source Trace, oracle, or seam was wrong. Preserve a correct assertion.

## 4. REFACTOR

Refactor only while GREEN. Follow [refactoring.md](refactoring.md), rerun the focused test after each move, and run the nearest relevant test group before the next tracer bullet.

Behavior or interface changes start a new RED cycle.

## 5. RETURN

Repeat only for materially distinct acceptance behavior. Stop when the assigned criteria are proved, remaining cases are data variations, or the next behavior requires a user-owned decision.

Return:

- **Source Trace:** behavior, source, seam, and oracle;
- **RED:** command and expected behavioral failure;
- **GREEN:** command and passing result;
- **Coverage:** relevant validation or skipped reason;
- **Refactor:** material cleanup or `none`;
- **Residual risk:** remaining uncertainty or blocker.

Complete only when every implemented behavior crossed observed RED before production implementation, crossed GREEN through its chosen seam, stayed GREEN through refactoring, received relevant validation, and appears in the proof packet.
