# Logic Prototype

Use this branch for a **decision surface**: state transitions, data shape, interface feel, or action legality that must be driven through cases.

[SKILL.md](SKILL.md) owns the question, write boundary, command, verdict, and reconciliation. This file owns the logic artifact and smoke gate.

## Model

Model only the states, actions, and data needed by the locked question. Put them behind the smallest explicit decision interface that fits:

- **Reducer:** `(state, action) -> state` for discrete events over one state object.
- **State machine:** explicit states and transitions when action legality is the question.
- **Pure functions over plain data:** transformations without ongoing current state.
- **Class or module:** a clear interface when the concept genuinely owns internal state.

Inputs enter only through the decision surface; each call returns updated state or an observable state snapshot. Keep I/O, prompts, timing, randomness, and rendering in the disposable shell. Drive the public decision surface; treat private helpers as implementation details.

## Drive

Build a thin terminal shell that lets the judge press buttons and watch state change.

Render one stable frame showing:

1. **Current state:** pretty-printed and diff-friendly.
2. **Available actions:** short commands with enough labels to drive the model.

Keep the frame within one screen. Use native terminal formatting or an existing styling dependency only when it improves judgment.

Run this loop:

1. Initialize one state object.
2. Render the frame.
3. Read one command and translate it into an action.
4. Update state through the decision surface.
5. Re-render until quit.

Surface unavailable or illegal actions and leave state unchanged when the model defines them.

## Smoke

Run the prototype's repo-native command and verify:

- the first frame renders;
- at least one action changes visible state;
- an unavailable or illegal action is surfaced and leaves state unchanged when applicable;
- quit works.
