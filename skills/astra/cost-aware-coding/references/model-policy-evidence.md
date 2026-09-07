# Evidence and limits

Snapshot: 2026-09-06. Benchmark-informed starting choices, not demonstrated
savings for a particular repository. Refresh relevant measurements before new
comparative claims. Reported API task costs are not Codex subscription usage.

Use [Model policy](model-policy.md) for execution choices. The measurements here
help assess tradeoffs and design calibration; they do not establish task-specific
winners or prove that XHigh improves review.

## Engineering

### Aggregate Pareto comparison

[Artificial Analysis Intelligence Index v4.2](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index)
provides a consistent aggregate of ten evaluations, task costs, and estimated
decode time. In the September 6 capture, 15 Luna/Terra/Sol/Astra effort settings
had all three metrics; nine other selected settings lacked a complete triple
and were omitted without imputation.

Using rounded published values, Sol Medium/High and Astra Low/Medium are on the
cost/score frontier. Above Sol Low, Astra occupies the decode-time/score frontier
among those 15 settings. Sol Medium displays score 46, USD 0.37/task and 1.3
decode minutes; Astra Low displays 49, USD 0.63 and 0.8 minutes. Luna Max displays
43, USD 0.10 and 3.9 minutes. Terra's measured settings do not reach either
frontier in this subset; that is not evidence that Terra is useless everywhere.

Time is weighted output tokens divided by generation speed, excluding first-token
latency and tool/orchestration overhead. Costs are weighted benchmark API expense.
These are not measured times to an accepted coding change. Frontiers use point
estimates, not uncertainty-adjusted dominance; small gaps and missing settings
limit conclusions. This aggregate does not establish the best effort for easy
retrieval. Keep other benchmarks as separate evidence views.

### Long-horizon engineering

[DeepSWE v1.1](https://deepswe.datacurve.ai/) uses 113 original long-horizon
engineering tasks and mini-swe-agent. All-efforts view, with Terra enabled:

| Configuration | Rounded pass@1 | USD/task | Steps |
| --- | --- | --- | --- |
| Luna Max | 67% ±4% | USD 0.61 | 102 |
| Terra XHigh | 60% ±2% | USD 1.70 | 43 |
| Terra Max | 70% ±3% | USD 3.96 | 76 |
| Sol Medium | 61% ±2% | USD 1.42 | 31 |
| Sol High | 69% ±1% | USD 2.66 | 37 |
| Astra Low | 67% ±1% | USD 2.19 | 20 |
| Astra Medium | 73% ±3% | USD 4.38 | 26 |

Astra High and Max also display 73%, at USD 5.72 and USD 12.37. Rounded scores and
overlapping uncertainty do not prove equivalence. Steps are not elapsed time.

## Scientific programming

[Artificial Analysis SciCode](https://artificialanalysis.ai/evaluations/scicode)
reports scientific subproblem accuracy: Sol High 57.8%, Medium 57.4%, XHigh/Max
57.1%; Terra Max 55.0%, XHigh 52.3%; Astra Medium 54.2%, Low 54.1%; Luna Max 53.6%.
Small differences do not establish significant superiority or cost efficiency
without task costs.

[SciCode's authors](https://scicode-bench.github.io/) describe numerical methods,
simulation, and scientific calculation; computational finance has only one main
problem. Neither benchmark establishes a winner for backtesting, leakage
detection, financial data semantics, or statistical design. Task-specific routes
in this policy are engineering hypotheses for those workloads.

## Workload and harness sensitivity

[CursorBench 3.2](https://cursor.com/cn/cursorbench) reports Terra Max at 64.9%
and USD 2.31/task versus Sol High at 63.5% and USD 2.79. That differs from DeepSWE's
tradeoff. Task distributions and harnesses can favor different choices; do not
average their scores or assume a ranking transfers to another workload.

[Superconductor's Rails evaluation](https://www.superconductor.com/blog/gpt-5-6-benchmark)
selected Sol High for daily use. Community
[execution/planning accounts](https://www.reddit.com/r/codex/comments/1vfwsug/gpt56_sol_luna_and_terra_choosing_by_cost_speed/)
include Terra XHigh users and conflicting Luna experiences. These inform
candidates, not controlled evidence of specialization.

[Artificial Analysis's Astra study](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra)
found agentic token savings could offset higher token prices. Compare accepted
changes rather than price per token. Benchmark versions and harnesses differ;
launch maxima cannot be assigned to Medium. More reasoning can cost more without
improving a particular result; measure its benefit on the relevant task.

## Interpreting time and requested calibration

Prefer measured elapsed time through acceptance. A decode estimate uses total
generated tokens divided by generation speed; sequential requests also add
first-token latency, tool duration, and orchestration overhead. Steps help explain
those costs but are not minutes. Do not multiply total task tokens by steps again.
Parallel elapsed time follows the critical path, including integration. Keep
benchmark scores, harnesses, and timing definitions separate. A cost/time frontier
ignores quality and cannot choose a model without an adequate quality requirement.
Report human switching time separately; do not convert subscription quota into
invented API charges.

When calibration is requested, compare matched tasks against direct Sol and direct
Astra baselines, including an arm without an Astra planning pass. Keep acceptance
fixed and independent of workers. Include failures and abandoned attempts in total
cost; track defects, corrections, completion rate, elapsed time and total usage.
Small pilots establish feasibility, not general superiority. Ordinary execution
does not require an evaluation or tracking artifact merely to justify a route.
