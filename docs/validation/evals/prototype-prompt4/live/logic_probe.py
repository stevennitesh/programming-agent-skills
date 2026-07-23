from __future__ import annotations

import json
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class QueueState:
    items: tuple[str, ...] = ()
    capacity: int = 2


def reduce_queue(state: QueueState, action: tuple[str, str | None]) -> QueueState:
    kind, value = action
    if kind == "enqueue" and value and len(state.items) < state.capacity:
        return replace(state, items=(*state.items, value))
    if kind == "dequeue" and state.items:
        return replace(state, items=state.items[1:])
    return state


def main() -> None:
    cases = (
        ("happy", QueueState(), ("enqueue", "A"), ("A",)),
        ("boundary", QueueState(("A", "B")), ("enqueue", "C"), ("A", "B")),
        ("rejected", QueueState(("A",)), ("rename", "B"), ("A",)),
    )
    report = []
    for name, before, action, expected in cases:
        after = reduce_queue(before, action)
        report.append(
            {
                "case": name,
                "input": {"items": before.items, "action": action},
                "observed": {"items": after.items},
                "criterion": after.items == expected,
            }
        )
    print(
        json.dumps(
            {
                "question": "Does an explicit reducer preserve queue invariants?",
                "cases": report,
                "invariants": ["capacity <= 2", "rejected actions preserve state"],
                "limits": ["in-memory model", "not production proof"],
                "supported_direction": "explicit reducer" if all(
                    item["criterion"] for item in report
                ) else "none",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
