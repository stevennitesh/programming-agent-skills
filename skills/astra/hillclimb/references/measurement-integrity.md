# Measurement integrity

Read when variation, repeated tuning, or tradeoffs could change the keep decision.
Use the smallest method that makes the comparison trustworthy; no universal sample
count, significance threshold, or benchmark framework is required.

## Compare equivalent work

Match input scale, configuration, runtime/build mode, concurrency, and measured
start/end boundaries. Verify useful outputs independently of the metric. Catch
omitted work, lower precision, skipped validation, stale results, or changed quality
that make a candidate look cheaper without delivering the accepted outcome.

If work is deferred or moved to another process, include the downstream cost when
the requested outcome requires it. A faster first response may be a real gain,
but it does not establish faster task completion. Check secondary consequences
that matter, such as memory growth from caching or retry load from lower latency.
Keep any user-approved tradeoff explicit; do not infer acceptance of quality loss.

## Distinguish signal from environmental drift

Account for warmup, cold versus warm cache, process reuse, thermal state, background
load, ordering, and resource contention when material. Do not benchmark competing
candidates simultaneously against shared scarce resources. Parallel implementation
attempts require explicit delegation authority and independent state; their mere
separate checkouts do not establish measurement independence.

Use paired or alternating baseline/candidate runs when drift could determine the
winner. Report the relevant range or distribution rather than the best sample.
For tail-latency or reliability claims, gather exposure capable of supporting that
claim; an average alone is insufficient. Within-noise differences are inconclusive,
not wins rounded into existence. State sampling limits without pretending a finite
run proves all future behavior.

## Avoid selecting a lucky or overfit winner

Repeated attempts on the same benchmark create selection bias. Confirm the final
choice with fresh runs not used to select it. When tuning for generalization across
inputs, reserve representative evaluation cases or a held-out workload and keep
its results out of iterative selection. If you tune after seeing that evaluation,
it becomes development evidence; obtain new independent confirmation or narrow
the claim. Do not call a repeatedly inspected set held out.

The workload must represent the user's intended use, including materially different
sizes or states where regressions could offset the gain. A deliberate optimization
for one fixed workload is valid when that is the requested objective; say so instead
of claiming broader improvement. More samples of the same narrow input do not prove
generalization to other inputs.

## Change the ruler honestly

Verify sensitivity to plausible meaningful differences before trusting a flat
score. If the harness changes, record why and rerun both sides under the new method.
Do not compare an old baseline measured one way with a new candidate measured
another. Preserve prior results as observations under their original conditions,
not evidence for the revised comparison.
