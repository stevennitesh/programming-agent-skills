# Measurement integrity

Read when variation, repeated tuning, or tradeoffs could change the keep decision.
Use the smallest method that makes the comparison trustworthy; no universal sample
count, significance threshold, or benchmark framework is required.

## Compare equivalent useful work

Match the input scale, relevant configuration, runtime or build mode, concurrency,
and measured boundaries closely enough for the requested claim.

Verify useful output independently of the optimization metric. Omitted work, lower
precision, skipped validation, stale results, or reduced quality are not valid
performance gains unless the corresponding tradeoff was explicitly accepted.

If work moves to another process or later stage, include the downstream cost when
the requested outcome requires it. A faster first response does not establish
faster task completion. Account for material secondary costs such as memory growth,
retry amplification, or quality loss.

## Distinguish signal from environmental drift

Account for warmup, cache state, process reuse, thermal state, background load,
ordering, and resource contention when they can change the conclusion. Separate
processes or checkouts do not establish measurement independence when candidates
share scarce resources.

Use paired, alternating, or otherwise comparable runs when environmental drift
could determine the winner. Report the range or distribution relevant to the
claim rather than only the best sample.

Tail-latency, reliability, or failure-rate claims require exposure capable of
supporting that claim; an average alone is insufficient. Differences inside the
observed noise are inconclusive, not wins rounded into existence.

State sampling limits rather than treating a finite clean run as proof of all
future behavior.

## Avoid selecting a lucky or overfit winner

Repeated attempts on the same benchmark create selection pressure. For variable
measurements, confirm the final candidate with fresh runs not used to select it.
For deterministic metrics, verify the final candidate; repetition alone does not
create independent evidence.

When the claim concerns generalization across inputs, reserve representative
evaluation cases or a held-out workload from iterative selection. Once tuning uses
that evaluation result, it becomes development evidence; obtain new independent
confirmation or narrow the claim.

A deliberately optimized fixed workload is valid when that is the requested
objective. Do not generalize the result to other inputs merely by collecting more
samples of the same narrow case.

## Change the ruler honestly

Make sure the measurement can detect differences large enough to matter before
trusting a flat score.

If the harness, workload, or scoring method changes materially, rerun both the
baseline and candidate under the revised method. Do not compare numbers produced
under incompatible rulers.

Preserve earlier measurements as observations under their original conditions,
not as evidence for the revised comparison.
