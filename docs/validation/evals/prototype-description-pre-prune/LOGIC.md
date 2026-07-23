# Logic Prototype

Use this branch for one decision about state transitions, rules, data shape, API shape, or interface behavior. [SKILL.md](SKILL.md) owns Freeze, authority, the lifecycle, reconciliation, and Return. This file owns only Logic Probe, Smoke, and verdict-evidence mechanics.

## Model

Model only the states, actions, data, and boundaries needed by the frozen question. Put them behind the smallest explicit decision interface that fits: a reducer, explicit state machine, pure functions over plain data, or a class/module that genuinely owns internal state.

Make current state, input, action, output, and invalid behavior visible. Keep I/O, prompts, timing, randomness, and rendering in a replaceable disposable shell. Drive the public decision surface; do not judge private helpers.

## Driver

Use an interactive terminal driver when human exploration supplies the evidence. Render a stable frame with current state and available actions; surface illegal actions and preserve state when the model rejects them.

Use a deterministic one-shot report when a frozen rule decides. For every representative case, print the input, observed output, criterion result, invariants, and limits without requiring prompts.

Include happy, boundary, and rejected cases whenever each can change the decision. Keep persistence and production integrations out unless the frozen question explicitly requires an isolated substitute.

## Smoke And Evidence

Smoke passes when the driver reaches the model and exercises the representative set:

- interactive: the first frame renders, a valid action visibly changes state, relevant invalid behavior is visible and safe, and quit works;
- deterministic: every frozen case and criterion result appears, repeated runs are equivalent, and no interactive path is required.

Verdict evidence explains which frozen answer the observed behavior supports and which cases remain untested. Timing or naturally variable evidence belongs in Measure, not Logic.

Return to `Judge` in [SKILL.md](SKILL.md); this branch does not Reconcile or Return.
