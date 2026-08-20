# Test doubles

Keep owned in-process code real. Prefer a local substitute such as an in-memory
store, isolated filesystem, test database, or local emulator. Add a test double
only at a real boundary adapter when the actual dependency is external, slow,
nondeterministic, unsafe, or cannot provide the required failure isolation.

Match the dependency behavior the tested path consumes, including relevant
results, side effects, failures, and contract values. If fidelity remains
unclear, use the real or local implementation or report the unverified risk.

Assert caller-visible state or results by default. Verify calls, arguments,
ordering, or counts only when that interaction is part of the contract.

Do not create a production interface solely for a test double. If substitute
setup overwhelms the behavior, reconsider the test boundary instead of adding
more mocking machinery.
