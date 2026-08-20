# Measure prototype

Use this branch for one comparative design question whose latency, throughput,
resource use, variability, or scaling observations may vary. It does not
diagnose an unexplained slowdown, certify a production baseline, or prove an
SLO.

Before running, name the alternatives, metric and unit, representative
workload, comparison rule, and environment facts that can change the result.
Use existing repository measurement tools when suitable. Keep the alternatives
isolated and run them under the same material conditions.

Collect enough observations to expose variability that could change the
answer. Do not report only the best run. Account for warmup, cache state,
ordering, or environmental noise only when it is material. Do not change the
workload or rule after seeing decisive results.

The evidence is the observed comparison under the declared workload and rule.
Report material variability and any limits on production extrapolation. A
changed workload or rule is a new question.
