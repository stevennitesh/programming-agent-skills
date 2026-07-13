---
name: tdd
description: "Use for red-testable new behavior. Use for bug fixes only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. Hand off bugs when the exact symptom, cause, or trusted red-capable reproduction is uncertain to $diagnosing-bugs; hand off throwaway design questions to $prototype."
---

# Test-Driven Development

Build one **tracer bullet** at a time:

**RED -> verify RED -> GREEN -> verify GREEN -> REFACTOR**

**No observed RED, no TDD.** After-the-fact checks may supplement RED evidence; they do not replace it.

**Boundary:** own this inner loop only. The caller owns bounded scope, review, staging, commit, tracker or external mutation, publishing, and closeout.

Hand off to `$diagnosing-bugs` for a bug when the exact symptom, cause, or trusted red-capable reproduction is uncertain; it owns that diagnostic loop through regression proof. Use `$tdd` directly only when expected behavior, the exact symptom, the cause, and a trusted red-capable reproduction are known. Hand off to `$prototype` for throwaway design questions.

Read [tests.md](tests.md) only when test shape, oracle, or seam remains unclear after inspecting nearby tests; read [mocking.md](mocking.md) before adding a test double; read [refactoring.md](refactoring.md) only while GREEN.

## Principles

- **Tracer bullet:** prove one narrow observable behavior through the highest useful public interface or seam. Finish its vertical cycle before writing the next test.
- **Test oracle:** trace expected outcomes to an independent source: acceptance criteria, a specification, a known-good literal, a fixture, or a worked example. Never derive the oracle from the production implementation.
- **Interface pressure:** hard-to-test behavior exposes a shallow, coupled, or misplaced seam. Do not add private or test-only hooks to escape that pressure.
- **Classicist:** prefer real in-process code and local substitutes. Use fakes, stubs, or mocks only at real boundary adapters.

## Preconditions

Apply the caller-loaded engineering contract when supplied; otherwise read `docs/agents/engineering-contract.md` when present before changing repo behavior.

When exploring the codebase, follow `docs/agents/domain.md` when present. Otherwise use the relevant context map, glossary, ADRs, and nearby code.

Reuse the caller's **Source Trace** when supplied. Otherwise trace the behavior, acceptance criterion, public contract, and test oracle to the request, work item, specification, bug repro, or repo contract.

Choose the technical seam from repo evidence. Ask only when the behavior, public contract, acceptable oracle, or a user-owned commitment remains unsettled.

If no red-capable harness reaches the seam, return that gap to the caller. Create the smallest repo-native automated check only when it stays inside the assigned scope. Do not silently add dependencies, services, or public test hooks. Manual proof is not RED.

## Workflow

### 1. Lock The Next Tracer Bullet

Name:

- the observable behavior;
- its source or acceptance criterion;
- the public interface or seam;
- the test oracle;
- the focused test command.

Choose the smallest acceptance-critical or highest-risk behavior. If no path is proven and risk does not dictate otherwise, start with the happy path.

Add another tracer bullet only for a materially distinct behavior, branch, failure mode, permission boundary, state transition, integration seam, or migration risk. Use focused module tests for dense pure logic when they remain behind a meaningful interface.

Stop when remaining cases are data variations of behavior already proved.

A **GREEN prefactor** may expose a useful seam only when existing focused tests already protect behavior. Otherwise return it as support work instead of widening the TDD slice.

### 2. RED

Write one focused test in domain language. Exercise real code paths where practical and assert observable outcomes rather than internal calls.

Run the focused test before writing production code.

Pass the **RED gate** only when:

- the test fails;
- the failure is expected;
- missing or wrong behavior caused the failure;
- setup, imports, fixtures, typos, and unrelated breakage did not cause it.

If the test passes immediately, stop. The behavior may already exist, the assertion may be weak, or the seam may be wrong. Do not edit production code from that test.

If the test errors, repair the test or setup and rerun until it fails for the expected behavioral reason.

**Exploration quarantine:** set aside only implementation authored for this behavior during the current cycle. Preserve user and pre-existing work. If RED cannot be observed safely against a baseline, return after-the-fact proof and do not claim TDD.

### 3. GREEN

Write the smallest production change that makes the focused test pass.

Do not add future behavior, broad cleanup, speculative abstractions, or unrelated fixes.

Run the focused test, then the nearest relevant test group.

Pass the **GREEN gate** only when:

- the focused test passes;
- the behavior works through the chosen interface or seam;
- nearby tests still pass;
- output is trustworthy.

Change the test only when its Source Trace, oracle, or seam was wrong. Do not relax a correct assertion to manufacture GREEN.

### 4. REFACTOR

Refactor only while GREEN.

Follow [refactoring.md](refactoring.md). Keep behavior unchanged, make one meaningful move at a time, and rerun the focused test after each move.

Prefer deeper modules and simpler interfaces over shallow pass-through helpers. New behavior starts a new RED cycle.

Before leaving the tracer bullet, rerun the nearest relevant test group.

### 5. Repeat Or Stop

Pick the next materially distinct behavior in the assigned slice and repeat.

Stop when the assigned acceptance criteria are proved, the next case is only a data variation, or a remaining behavior requires a user-owned decision.

## Proof Packet

Return:

- **Source Trace:** behavior source, acceptance criterion, seam, and oracle;
- **RED:** command and expected failure;
- **GREEN:** command and passing result;
- **Coverage:** nearest relevant validation, broader validation, or skipped reason;
- **Refactor:** material cleanup or `none`;
- **Residual risk:** remaining uncertainty or blocker.

## Completion Criteria

Complete only when each implemented behavior in the assigned slice crossed the RED gate before its production implementation, crossed the GREEN gate through the chosen interface or seam, stayed GREEN through refactoring, received relevant validation, and appears in the proof packet.

If RED was not observed safely, report the result as after-the-fact proof, not TDD.
