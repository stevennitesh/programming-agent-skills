# TDD Skill Synthesis

This note maps the books and supporting references behind the local `$tdd` skill and its supporting files:

- `/home/steve/.agents/skills/tdd/SKILL.md`
- `/home/steve/.agents/skills/tdd/tests.md`
- `/home/steve/.agents/skills/tdd/mocking.md`
- `/home/steve/.agents/skills/tdd/refactoring.md`

The local skill pack stance is: classicist TDD by default, tracer-bullet vertical slices, behavior through meaningful interfaces, fakes before mocks, and refactoring only while GREEN.

## Primary Sources

### Kent Beck - Test-Driven Development: By Example

Source: https://www.oreilly.com/library/view/test-driven-development/0321146530/

Use for:

- RED -> GREEN -> REFACTOR discipline
- writing the next smallest useful test
- proving the test can fail before writing production code
- letting each cycle teach the next design move

Maps to:

- `SKILL.md`: the core TDD loop
- `tests.md`: RED must fail for the expected behavior reason
- `refactoring.md`: new behavior starts a new RED cycle

Skill-pack takeaway:

TDD is not "write tests around code." It is a design loop. The skill should keep RED explicit because RED proves the test can catch the missing behavior.

### Martin Fowler - Refactoring

Source: https://martinfowler.com/books/refactoring.html

Use for:

- behavior-preserving design improvement
- changing structure without changing observable behavior
- small safe moves with tests as guardrails
- stopping refactors from smuggling in new behavior

Maps to:

- `refactoring.md`: refactor only while GREEN
- `SKILL.md`: one green refactor after the minimal implementation

Skill-pack takeaway:

Refactoring belongs after GREEN. If the public interface or behavior must change, that is not refactoring inside the current cycle; start a new RED cycle.

### Steve Freeman and Nat Pryce - Growing Object-Oriented Software, Guided by Tests

Source: https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/

Use for:

- growing design through tests
- testing from the outside of a behavior
- using interfaces to discover object/module responsibilities
- seeing tests as pressure on design, not just verification

Maps to:

- `SKILL.md`: tracer-bullet vertical slices
- `tests.md`: behavior through the public interface
- `mocking.md`: adapters and seams where a boundary needs a double

Skill-pack takeaway:

Use the outside-in/design-pressure lesson, but adapt the mocking style to this pack: prefer real in-process code and fakes; mock only at true system boundaries.

### Gerard Meszaros - xUnit Test Patterns

Source: https://martinfowler.com/books/meszaros.html

Use for:

- test double vocabulary: fake, stub, mock
- test smells
- fixture setup tradeoffs
- keeping tests readable and maintainable

Maps to:

- `mocking.md`: fake/stub/mock distinctions
- `tests.md`: red flags and test smell calibration

Skill-pack takeaway:

The vocabulary matters because it prevents sloppy "mock everything" behavior. The file should teach when each double preserves behavior and when it hides design trouble.

### Michael Feathers - Working Effectively with Legacy Code

Source: https://martinfowler.com/bliki/LegacySeam.html

Use for:

- seam vocabulary
- tests as a way to get control over hard-to-change code
- recognizing when poor testability is design feedback
- safely changing legacy code by finding or creating a useful seam

Maps to:

- `SKILL.md`: highest useful public interface or seam
- `mocking.md`: doubles only at real seams
- `refactoring.md`: no private seams or test-only hooks

Skill-pack takeaway:

If behavior is hard to test, do not immediately reach for mocks or private hooks. Treat the pain as evidence about the module interface or seam.

### Lasse Koskela - Effective Unit Testing

Source: https://www.manning.com/books/effective-unit-testing

Use for:

- test readability
- maintainable test names
- tests that express behavior instead of implementation
- avoiding brittle, over-specified tests

Maps to:

- `tests.md`: good names, red flags, behavior/specification framing
- `mocking.md`: avoiding interaction-coupled tests unless the interaction is the contract

Skill-pack takeaway:

Good tests read like useful specifications. A product owner, caller, or future maintainer should understand what behavior the test protects.

### John Ousterhout - A Philosophy of Software Design

Source: https://web.stanford.edu/~ouster/cgi-bin/book.php

Use for:

- deep modules
- simple interfaces hiding complexity
- reducing cognitive load
- design feedback when interfaces are shallow or leaky

Maps to:

- `SKILL.md`: interface as test surface
- `refactoring.md`: depth, leverage, locality
- `mocking.md`: painful tests as evidence of a shallow or wrong seam

Skill-pack takeaway:

TDD should not produce shallow helper piles. GREEN refactors should deepen modules, shrink interfaces, and improve locality.

## Supporting References

### Martin Fowler - Mocks Aren't Stubs

Source: https://martinfowler.com/articles/mocksArentStubs.html

Use for:

- distinguishing classicist and mockist TDD styles
- understanding when interaction tests create coupling
- motivating the local skill stance: classicist by default

Maps to:

- `mocking.md`: "classicist by default"

Skill-pack takeaway:

The local skill deliberately prefers real code, local substitutes, and fakes. Mocks are reserved for adapter contracts where the interaction itself is the behavior or risk.

### Martin Fowler - Test Double

Source: https://martinfowler.com/bliki/TestDouble.html

Use for:

- shared vocabulary around test doubles
- avoiding vague "mock" wording when fake or stub is more precise

Maps to:

- `mocking.md`: fake, stub, mock definitions

## Concept Map By File

### `SKILL.md`

Primary concepts:

- RED -> GREEN -> REFACTOR
- one tracer bullet at a time
- vertical slices, not horizontal batches
- behavior through the highest useful public interface or seam
- use `$diagnosing-bugs` before `$tdd` when repro or root cause is uncertain

Best sources:

- Beck for the loop
- GOOS for growing design through tests
- Feathers for seams
- Ousterhout for interface pressure and depth

### `tests.md`

Primary concepts:

- tests read like specifications
- names describe domain behavior
- assertions prove observable outcomes
- bad tests couple to helpers, private methods, internal calls, and storage shape

Best sources:

- Beck for expected RED
- Koskela for readable tests
- Meszaros for test smells
- Feathers for useful seams

### `mocking.md`

Primary concepts:

- classicist by default
- real in-process code before doubles
- local substitutes before fakes
- fakes before mocks
- mocks only when the adapter contract is the behavior or risk
- never mock owned modules behind the tested interface

Best sources:

- Meszaros for double vocabulary
- Fowler for classicist vs mockist framing
- GOOS for boundary pressure, adapted carefully
- Feathers for seam discipline

### `refactoring.md`

Primary concepts:

- refactor only while GREEN
- behavior-preserving moves only
- no test-only hooks
- no new behavior during refactor
- deepen modules, improve locality, preserve or intentionally change the public interface through a new RED cycle

Best sources:

- Fowler for refactoring discipline
- Beck for returning to RED for new behavior
- Ousterhout for deep modules and simple interfaces
- Feathers for seams and testability

## Practical North Star

The skill pack is in the right direction when it produces tests that:

- start RED for the expected reason
- prove user- or caller-visible behavior
- cross a meaningful interface or seam
- avoid mocking owned modules
- use fakes/stubs/mocks only to replace real boundaries
- allow refactoring without breaking behavior
- reveal design problems instead of hiding them behind test-only hooks

The goal is not maximum test count. The goal is confidence, design feedback, and behavior protected through the right interface.
