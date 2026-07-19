# Performance Lens

Read this only when the Charter includes speed, latency, throughput, scalability, memory, storage, network, CPU, GPU, or other resource behavior.

## Classify

- **Performance defect:** measured behavior violates a Charter budget, requirement, invariant, comparison basis, or supported operational expectation.
- **Performance opportunity:** measured evidence supports a likely beneficial change, but no governing expectation is violated. Admit it only as an advisory when enabled.
- **Performance evidence gap:** the required workload, environment, benchmark, profile, instrumentation, budget, or comparison baseline is unavailable or cannot be captured read-only.

**Like-for-like:** bound every claim to its workload, environment, build, method, sample count, and variance. A smell alone proves neither defect nor benefit; static evidence may locate a bottleneck, but measurement must establish impact.

## Measure

Prefer a repository-owned benchmark, profiler, production trace, or representative end-to-end proof lane. Record one reproducible run:

```text
Workload:
Environment:
Baseline:
Observed:
Budget or comparison:
Units:
Warmup and method:
Sample count and variance:
Input scale and concurrency:
Resource constraints and cache state:
Bottleneck evidence:
Supported impact:
Confidence:
Required proof:
```

Materially different environments, datasets, builds, or methods become evidence gaps. Noisy or under-sampled results support only the uncertainty they resolve.

## Bound

Run only read-only benchmarks and profilers that preserve the immutable target and authorized environment. New production instrumentation, benchmark infrastructure, tuning patches, and load-generating external mutations remain outside the audit. Route resulting gaps through the audit finding contract.
