# Locked Launch Record

## Frozen Inputs

- Shared tasks: [`paired-tasks.md`](../fixtures/paired-tasks.md), SHA-256
  `8cd56461091acdf74279c04b85da1b9e7cbca93455641894e0289b8f87f302fe`.
- Control context: [`control-context.md`](../fixtures/control-context.md),
  SHA-256
  `4cd28fde16d8d2c3176030caf486d4eaf9cca91f0c1e5b8b2d0b0cd8e8cc6ea0`.
- Candidate context: [`candidate-context.md`](../fixtures/candidate-context.md),
  SHA-256
  `5fbf367ce94869ca31e1e57fbbfaf7acb17c5d6603f145a527a2f87a4f82919d`.

## Runtime Binding

Every sample used a fresh-context `default` worker with requested model
`gpt-5.6-sol` and reasoning `high`. Observed backend model-build and reasoning
telemetry were unavailable. Each launch allowed only the two applicable frozen
fixture files and the exact skill files or line-bounded MAP sections named by
that arm context. Memory, web, mutation, installation, tracker authority, Git
delivery, unrelated reads, peer outputs, and delegation were prohibited.

## Launch Template

```text
Locked <CONTROL | CANDIDATE> <sample-id>/<fixture-id>. Skip memory. Read only
the frozen shared task and applicable arm-context file, then exactly the skill
files or line-bounded sections authorized for <fixture-id>. No other read,
probe, search, or discovery. Evaluate only <fixture-id> against the frozen
Shared Task and protected-obligation rubric. Do not invent fixture values.
Return a complete packet containing residency, selected behavior and order,
ownership, exclusions, semantic/critical failures, deviations, and unavailable
runtime telemetry.
```

Control workers read historical skill content only through `git show` at
`84aac67b9a1a156bf5abd0c0e6526aac2c825324`. Candidate workers read the frozen
live packages identified by `candidate-context.md`.

## Formal Task IDs

| Cohort | Fixture | Control task | Candidate task |
| --- | --- | --- | --- |
| Entry-positive | P1 | `issue88_locked_control_1` | `issue88_locked_candidate_1` |
| Entry-positive | P2 | `issue88_locked_control_2` | `issue88_locked_candidate_2` |
| Entry-positive | P3 | `issue88_locked_control_3` | `issue88_locked_candidate_3` |
| Entry-positive | P4 | `issue88_locked_control_4` | `issue88_locked_candidate_4` |
| Entry-positive | P5 | `issue88_locked_control_5` | `issue88_locked_candidate_5` |
| Wrong condition | W1 sample 1 | `issue88_clean_wrong_control_1` | `issue88_clean_wrong_candidate_1` |
| Wrong condition | W1 sample 2 | `issue88_clean_wrong_control_2` | `issue88_clean_wrong_candidate_2` |

Candidate sampling followed the five locked controls after they reproduced the
registered deficit. Wrong-condition pairs followed the five locked candidates
after all cleared the entry-positive gate.
