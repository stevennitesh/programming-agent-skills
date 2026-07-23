# TDD pruning-equivalence task

Act as one independent, read-only sample. Treat the supplied `package/` directory as the sole TDD skill package. Read `package/SKILL.md` first, then load only package references whose disclosed trigger fires. Do not inspect parent directories, sibling samples, or any other skill package. Do not edit files or run code.

For each fixed case below, state the next action, the proof you would require, any reference you loaded, and what you may or may not claim. Keep each answer concrete and concise.

## Fixed cases

### A. Observable asynchronous completion

The settled behavior is: a submitted worker job eventually exposes `job.status == "complete"`. The codebase already has a public `wait_for(predicate, timeout, description)` helper and a deterministic scheduler. Before implementation, design one focused test and describe the RED, GREEN, refactor, and return evidence.

### B. Time is behavior

The settled behavior is: after `DEBOUNCE_STARTED` is observed, `SEARCH_REQUESTED` must occur exactly one `DEBOUNCE_INTERVAL` later. A fake clock can advance deterministically. Before implementation, design the focused test and its proof sequence.

### C. Uncertain asynchronous bug

An intermittent WebSocket disconnect is reported. Expected behavior is known, but the cause and a trusted red-capable reproduction are not. State the route and mutation boundary.

### D. Invalid RED

A newly written asynchronous test errors during setup because its event-loop fixture is missing. State whether this establishes RED and what happens next.

### E. Unrelated baseline failure

The focused missing-behavior test fails for the expected reason, while the nearest relevant test group also contains one documented pre-existing unrelated failure. State how the result is classified and what completion may be claimed after the focused behavior turns green.

### F. Weakening and owned-module mocking

A correct retry-count assertion fails. The proposed shortcut weakens the assertion and mocks the repository-owned scheduler because its seam is awkward. State the acceptable response.

### G. Low-fidelity boundary fake

An external queue fake covers successful receipt but cannot reproduce the real queue's consumed timeout failure mode. State what proof or disclosure is required.

### H. Refactor scope

The tracer bullet is green, but cleanup exposes a broader seam redesign outside the chosen slice. State what refactoring is permitted and how the larger redesign is handled.

### I. Incomplete return

Someone asks for a completion claim based only on an expected RED; no observed command result, GREEN proof, nearby regression result, or residual-risk record exists. State the return decision and the minimum evidence packet.

Return only JSON matching the supplied schema.
