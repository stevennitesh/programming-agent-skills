---
name: tdd
description: 'Test-driven development. Use only when the user explicitly requests TDD, test-first work, or RED-GREEN-REFACTOR, or applicable repository policy requires TDD. Requests for tests, integration tests, regression tests, or coverage alone do not trigger it.'
---

# Test-driven development

Deliver one settled observable behavior through:

**RED -> GREEN -> REFACTOR**

**No observed behavioral RED, no TDD.** After-the-fact proof can still be
useful, but it cannot replace RED evidence or justify a TDD claim.

Admit only under the description's explicit user or repository-policy trigger.
Ordinary implementation may add or change tests without invoking TDD. The
caller retains scope and later delivery; this skill owns the inner loop.

Read [Test shape](references/TEST-SHAPE.md) only when the useful test boundary
or independent expected result remains unclear after inspecting nearby tests.
Read [Test doubles](references/TEST-DOUBLES.md) before adding a test-specific
substitute.

## RED

Choose one accepted observable behavior, the highest useful stable interface
that exposes it, an independently derived expected result, and the focused test
command. Before writing the test, name the realistic production break it should
catch. If the behavior, oracle, authority, or a safe red-capable check is
unavailable, stop before production mutation and report that material gap.

Reuse or extend the narrowest existing behavior test or case table that can
express the behavior. If none reaches it, create the smallest repo-native check
whose signal justifies its cost. Do not add a dependency, service, public test
hook, broad fixture, or brittle mock merely to satisfy TDD. An honest gap is
better than a bad test.

Run the focused test. Continue only when it fails because the accepted behavior
is missing or wrong, not because setup, imports, fixtures, typos, environment,
or unrelated code failed. An immediate pass is not RED. If a trustworthy RED
cannot be observed safely, do not claim TDD or delete pre-existing work to
recreate the ritual.

## GREEN

Make the smallest acceptance-complete implementation change that makes the
focused test pass. Change a correct assertion only when its accepted behavior,
oracle, or chosen interface was wrong.

Run the focused test and the nearest checks justified by repository policy,
shared impact, or concrete risk. Keep unrelated baseline failures separate.

## REFACTOR

Remove slice-local duplication or awkwardness while the behavior stays green.
New behavior or a public-contract change starts another RED.

Complete when the selected behavior crossed observed RED before its
implementation and remains green under the relevant proof. Return concise prose
naming the observed RED, final GREEN and nearby proof, and any material gap.
