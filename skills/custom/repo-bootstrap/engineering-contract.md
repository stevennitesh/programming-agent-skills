# Engineering Contract

Explore imaginatively. Converge under proof. Simplify ruthlessly.

This contract teaches shared engineering judgment. It is not a workflow,
checklist, review gate, completion format, or authority to mutate anything.
Follow the user, repository instructions, accepted domain decisions, and
current source. Skills own procedures and stopping conditions.

## Understand before changing

Trace the request through the code that owns the behavior, its real callers,
data flow, and existing proof. Preserve accepted behavior, domain meaning,
contracts, and unrelated work. Surface a consequential ambiguity instead of
inventing product intent.

Work in a **bounded slice**, the smallest useful change that preserves the
requested outcome and can produce meaningful evidence.

## Design for simplicity

Choose the smallest integrated design that makes the behavior clear. Subtract,
reuse, or replace before adding another path. Keep behavior in its current
owner unless moving it solves a demonstrated ownership problem.

Model the domain with clear data shapes, explicit relationships, and
representations that make invalid states difficult to express. Prefer small
interfaces, local state, readable control flow, and modules that hide their
internal complexity.

An abstraction earns its cost by hiding meaningful complexity or owning
policy. Collapse pass-through wrappers and seams that support no real
variation.

Start with the language, framework, repository conventions, existing
abstractions, and installed dependencies. Add an abstraction, dependency,
adapter, cache, configuration option, concurrency mechanism, or compatibility
path only for supported variation or demonstrated value. Prefer bounded
duplication to an abstraction that joins different meanings or owners.

Fix the cause across affected callers instead of guarding one symptom. Trust
internal types and established invariants. Validate untrusted,
machine-consumed input once at the boundary that owns it, then pass a valid
internal representation onward.

Keep framework, transport, and storage representations at the edge. Pass
domain values into core logic and prefer explicit results over hidden mutation.
Derive secondary state from one source of truth instead of synchronizing
copies.

## Implement the whole change

Preserve the behavior and failure semantics the accepted contract exposes.
Handle state, retry, recovery, cancellation, concurrency, compatibility, and
observability only when reachable behavior or a supported requirement makes
them relevant.

Remove code, callers, flags, configuration, tests, and documentation displaced
by the change. Keep an older path only for a named compatibility, migration,
recovery, or ownership need.

Update documentation when the public contract, operator procedure, skill
usage, or a durable non-obvious decision changes. Readable code needs no
restating comment.

## Prove the claim

Run the nearest useful check that can fail for the changed behavior. Prefer the
real caller or artifact over an isolated implementation detail. Add or change
a test when repository policy requires it or when it is the cheapest durable
protection for meaningful behavior.

Broaden proof only for shared impact, repository policy, or a concrete risk.
When the implementation could confirm its own mistake, use an independent
oracle. If safe execution is unavailable, use the strongest safe proxy and
state what remains unproved.

## Activate protection from evidence

Protection follows a concrete trigger. Destructive work needs an exact target
and approval. External durable mutation needs authority and read-back.
Concurrent writers need isolated ownership and one integrator. Formal review
needs a fixed candidate. Operations that can partially succeed need a recovery
path. Consequential performance, capacity, reliability, latency, cost, or
resource claims need comparable measurement.

An inactive condition creates no checklist, artifact, reviewer, status field,
or explanation obligation. Use TDD only when the user explicitly requests
test-first work or repository policy requires it. Delegate only when the user
explicitly requests subagents or an invoked skill owns required fanout. Use
independent review, security work, deployment, or production operations only
when the user, repository, or accepted task activates them.
