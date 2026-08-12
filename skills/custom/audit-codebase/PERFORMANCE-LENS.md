# Performance Lens

Read this when performance or resource behavior is governed, declared,
observed, suspected from direct current evidence, or claimed. This includes
speed, latency, throughput, scalability, memory, storage, network, CPU, GPU,
and other resource behavior. A generic smell alone does not trigger it.

## Classify

- **Performance defect:** like-for-like measured behavior violates an
  authoritative budget, requirement, invariant, or accepted operational
  threshold. A comparison baseline counts only when authority defines
  pass/fail against it.
- **Performance opportunity:** measured evidence supports a likely beneficial
  change, but no governing expectation is violated. Admit it under
  `QUALITY-LENS.md` with the measurement and proof seam preserved.
- **Performance evidence gap:** the required workload, environment, benchmark,
  profile, instrumentation, budget, or comparison baseline is unavailable
  within Audit authority.

**Like-for-like:** bind every claim to its workload, environment, build,
method, sample count, and variance. A smell alone proves neither defect nor
benefit; static evidence may locate a bottleneck, but measurement must
establish impact.

## Measure

Prefer a repository-owned benchmark, profiler, production trace, deterministic
resource count, or representative end-to-end check at the Proof Seam. Record one
reproducible evidence packet. Complete applicable fields and give a reason for
inapplicable ones; an authoritative existing trace needs provenance and
comparability, not a forced rerun.

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

Materially different environments, datasets, builds, or methods become gaps.
Noisy or under-sampled results support only the uncertainty they resolve. If
required measurement is available but unfinished, apply `QUALITY-LENS.md`'s
coverage-completion rule.

## Bound

Run only commands proven not to mutate audited paths or external systems. If a
benchmark or profiler requires workspace caches, new infrastructure,
production instrumentation, tuning patches, or load-generating external
effects, record a gap instead. Route gaps through `DEFECT-CONTRACT.md`.
