from __future__ import annotations

import json
import statistics
import time


WORKLOAD = tuple(range(20_000))
WARMUPS = 2
SAMPLES = 5


def shape_a() -> int:
    return sum(value * value for value in WORKLOAD)


def shape_b() -> int:
    return sum(map(lambda value: value * value, WORKLOAD))


def observe(fn) -> list[float]:
    for _ in range(WARMUPS):
        fn()
    samples = []
    for _ in range(SAMPLES):
        start = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - start) / 1_000_000)
    return samples


def main() -> None:
    a = observe(shape_a)
    b = observe(shape_b)
    median_a = statistics.median(a)
    median_b = statistics.median(b)
    select_b = median_b <= median_a * 0.85 and max(b) <= max(a)
    print(
        json.dumps(
            {
                "question": "Which cache-shape loop is the better design candidate?",
                "metric": "milliseconds per operation",
                "workload_size": len(WORKLOAD),
                "warmups": WARMUPS,
                "samples": {"A": a, "B": b},
                "summary": {
                    "median_A": median_a,
                    "median_B": median_b,
                    "worst_A": max(a),
                    "worst_B": max(b),
                },
                "predeclared_rule": (
                    "select B only when median_B <= 85% of median_A "
                    "and worst_B <= worst_A"
                ),
                "verdict": "B" if select_b else "A",
                "limits": [
                    "local interpreter and host only",
                    "microbenchmark is not a production baseline or SLO proof",
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
