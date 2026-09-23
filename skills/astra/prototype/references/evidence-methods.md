# Evidence methods

Read only the section for the uncertainty being tested. These methods refine the
experiment; they do not start a design review or production verification workflow.

## State, logic, or integration behavior

Expose the relevant initial state, action, observed result, and resulting state
through the interface the question concerns. Exercise ordering, rejection, or
interruption only when those conditions can change the answer.

Keep incidental I/O and nondeterminism out of a logic model. When concurrency,
persistence, serialization, or a remote protocol is the deciding property,
exercise that mechanism in an authorized isolated environment rather than
simulating away its failure mode.

Use actual produced output across a boundary when translation matters. Demonstrating
one possible outcome does not prove another outcome cannot occur.

## Visual layout or interaction

Reproduce enough surrounding layout, representative data density, and relevant
screen size for the decision. Use repository components when their behavior affects
the result; otherwise a standalone artifact can be sufficient. Make simulated
behavior clear and stub effects unrelated to the question.

When comparing credible designs, hold purpose, data, and constraints constant and
vary the property under decision. No fixed variant count or switching mechanism is
required.

Inspect the rendered surface and drive the interactions that matter. A screenshot
can establish layout, not keyboard behavior, focus movement, or task completion.
Technical operation does not establish user preference; requested human judgment
remains a separate input.

## Performance or other variable measurements

Name the metric and unit, workload, decision criterion, and environment factors
that could change the conclusion. For comparisons, identify the baseline or
alternatives and ensure they perform equivalent useful work with valid outputs.

Collect enough observations to expose variation that could reverse the decision.
Account for warmup, cache state, ordering, and background load when material.
Report the distribution or range relevant to the claim rather than only the best
run. Treat differences inside observed noise as inconclusive or narrow the claim.

Keep measurements tied to their workload and environment. A local benchmark does
not certify a production SLO, and a changed workload or success rule requires new
evidence. Do not invent a threshold when the unresolved decision is how much cost,
latency, or quality loss the product can accept.
