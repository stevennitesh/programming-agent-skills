# Quantitative evidence

Read when a decisive claim reports a quantity, benchmark, or quantitative method.

Establish the quantity actually measured: units and scale, denominator, population
or market, window, sampling interval, aggregation/estimator, timestamp semantics,
revision/vintage, and missing-data assumptions as relevant. Do not equate missing
with zero or silently compare totals with rates, unlike windows, or unlike cohorts.
Check whether a displayed label matches the computed quantity.

For a method, establish equations/algorithm, input definitions, transformation
order, parameters, assumptions, calibration basis, and validation target. Separate
the definition from a particular implementation and evidence of effectiveness.
Use reproducible calculations for derived decisive numbers when practical and
retain input provenance; arithmetic cannot repair incompatible source semantics.

For performance claims, compare equivalent work under relevant conditions and
account for warmup, caching, repeated measurements, noise, and displaced costs.
Adaptive selection on the same evaluation data can inflate the apparent benefit;
distinguish exploration/calibration from independent validation. Do not call a
published benchmark proof of performance in an untested target environment.

A demonstrated mismatch is a mismatch, not merely conflicting opinions. If the
computation or mapping cannot be established, state the unknown quantity or step.
