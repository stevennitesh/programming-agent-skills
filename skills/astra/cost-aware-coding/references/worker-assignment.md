# Worker assignment

Give capable workers a clear outcome and enough context to act independently.
The lead owns the assignment and consequential constraints; the worker owns the
implementation method and ordinary technical decisions within them.

## Assignment contract

Include the decision-bearing context that applies:

- **Outcome and scope:** accepted behavior, responsibilities, exclusions, and
  authorized effects.
- **Acceptance:** observable completion, required checks, and preservation
  requirements.
- **Codebase context:** relevant owners, source pointers, important interfaces or
  implementation constraints, and facts that would be expensive to rediscover.
- **Checkout and custody:** working path, base or candidate identity, existing
  work to preserve, and the actor holding write authority.
- **Support and decisions:** access to the bounded worker, agreed checkpoints,
  and consequential choices reserved for the lead or user.
- **Return:** candidate identity, material changes, decisive evidence, unresolved
  limits, and custody state.

Give important details directly and point to accessible sources for the rest.
Avoid importing the full lead conversation. For model overrides, pass the selected
model and effort explicitly under [Model policy](model-policy.md); a Sol assignment
uses `gpt-6.1-sol` with `high` or the lead-selected `max`. Prefer a fresh worker
context with a self-contained brief; with Codex multi-agent, `fork_turns="none"`
provides that boundary. Reuse the worker's own context for continuing work.

The worker may choose techniques, tools, implementation order, and local design
within the accepted constraints. Suggested mechanisms remain suggestions unless
a governing source makes them binding. Do not require lead approval for routine,
reversible implementation choices.

## Replacement and cleanup

When the assignment replaces or consolidates behavior, completion includes moving
affected callers and removing code, configuration, tests, and guidance made
obsolete by that change within scope. Preserve supported behavior and required
compatibility. Identify why any superseded path must remain and the removal
condition for temporary overlap. Consider supported entry points and indirect
consumers before treating a lack of direct references as evidence of disuse.

A test is obsolete when its asserted obligation is obsolete, not merely because
the implementation changed. Replace or retire tests coupled to removed internals
while preserving meaningful regression coverage for surviving behavior and
compatibility. Passing tests against only the new path do not establish that the
transition preserved supported consumers.

The worker chooses cleanup methods and sequencing as part of delivering the
assignment. No separate cleanup phase or repository-wide sweep is required.
Unrelated baseline cleanup remains outside the assignment unless requested.

## Bounded support

The default team has one Luna bounded-worker slot. The lead can assign it directly
or give Sol standing authority to use that slot within the assignment's scope and
budget. Identify who dispatches it and any existing agent handle so both actors
do not create duplicate helpers. When parallel-implement governs execution, its
coordinator owns dispatch.

A bounded assignment states the question or production rule, source material,
expected evidence or deliverable, and completion boundary. Inputs and outputs may
be large. For retrieval, return concise results with source locations and material
gaps. For bulk writing, provide the required facts, pattern or examples, and output
requirements; deliver the complete artifacts with a concise handoff summary.

Bounded support is read-only by default and uses fixed or independent inputs
while Sol writes. Writing or editing the delegated checkout requires an explicit
transfer of write custody; it must not create a second implementation writer.
Sol's freedom to use the helper does not authorize more implementation agents or
unrelated work.

## Questions and returns

Ask the lead when accepted meaning, architecture, scope, a significant unforeseen
constraint, or an important codebase question needs its judgment or knowledge.
State the question, decisive evidence, why it matters, and any recommendation.
Continue independent work while a nonblocking question is pending. Routine
implementation uncertainty remains the worker's responsibility.

Send meaningful questions, agreed checkpoint candidates, failures, and completion.
Do not send routine narration or progress reports just because time passed.

The worker preserves unrelated work and owns writes until it explicitly releases
custody. Before the lead accesses the mutable checkout, stop relevant writers and
subprocesses and report their state. A reviewable return includes that release,
the actual candidate, acceptance evidence, and consequential limits.

For follow-ups, preserve the established outcome and send changed context,
findings, acceptance, candidate identity, and renewed custody rather than rebuilding
the full brief. Keep useful worker context while the assignment remains coherent.
