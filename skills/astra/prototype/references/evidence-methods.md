# Evidence methods

Read the section for the uncertainty being tested. These methods refine the
experiment; they do not start a design review or production verification workflow.

## State, logic, or integration behavior

Expose the relevant initial state, action, observed result, and resulting state
through the interface the question concerns. Exercise ordering, rejected actions,
or interrupted transitions when they could change the answer. For human judgment,
use domain labels and a resettable walkthrough; a script with visible inputs and
outputs is enough for an objective rule.

Keep incidental I/O and nondeterminism out of a logic model. When concurrency,
persistence, serialization, or a remote protocol is the question, exercise that
mechanism in an authorized isolated environment instead of simulating away its
failure mode. Use actual output across the boundary when translation matters.
Distinguish demonstrating a possible outcome from proving it cannot occur.

## Visual layout or interaction

Reproduce the surrounding layout, representative data density, and relevant
screen sizes. Use the repository's components when their behavior matters; a
standalone artifact is sufficient when they do not. Stub effects unrelated to
the question and make simulated behavior apparent to the reviewer.

Build one direction for a feasibility question. When comparing credible designs,
hold purpose, data, and constraints constant and give each option a clear label
and an easy way to compare. Vary the property under decision; structural variety
is useful for layout choices, while color-only variants can answer a color choice.
No fixed variant count or switching implementation is required.

Inspect the actual rendered surface and drive the interactions that matter.
A screenshot can establish layout, not keyboard behavior, focus movement, or
task completion. If the target surface cannot be inspected, label that gap.
Technical operation does not establish user preference; keep a requested human
evaluation pending until the feedback arrives.

## Performance or other variable measurements

Name the metric and unit, workload, baseline or alternatives, comparison rule,
and environment factors that could change the result. Ensure alternatives
perform equivalent work and verify their outputs; faster incomplete work is
not a successful comparison.

Collect enough observations to expose variation that could reverse the decision.
Account for warmup, cache state, ordering, and background load when material.
Report the distribution or range relevant to the claim rather than only the
best run. If differences are within the observed noise, return an inconclusive
comparison or narrow the claim.

Keep measured results tied to their workload and environment. A local benchmark
does not certify a production SLO, and a larger workload or changed success rule
requires new evidence. Do not invent a performance threshold when the missing
decision is how much cost or latency the product can accept.
