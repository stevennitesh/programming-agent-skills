# Test shape

Test one caller-visible behavior through the highest useful stable interface.
The test should survive internal movement. One behavior may need several
assertions when they jointly prove its observable result or effects.

Derive the expected result independently from the code under test. Prefer a
known-good literal, worked example, accepted specification, or hand-checked
fixture. Before keeping a test, name the realistic production break it catches.
A test that can fail only when its own setup changes is not useful protection.

Prefer state and results over internal call choreography. Interaction
verification is appropriate when the interaction itself is contractual or
provides necessary failure isolation.

A characterization test records actual legacy behavior when intended behavior
is unavailable. It does not establish correctness or supply a corrective RED.

Extend or parameterize an existing test when the same interface, oracle, and
outcome prove equivalent inputs. Keep separate tests for distinct behavior,
invariants, state transitions, failure modes, risks, or useful failure
isolation. Test count and coverage percentage are not targets.

Prefer no new test to one dominated by implementation details, timing,
unrelated global state, broad harness work, or disposable setup. Use the nearest
useful non-TDD proof and report the gap when a trustworthy test would cost more
than the behavior warrants.
