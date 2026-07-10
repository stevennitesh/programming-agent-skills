# Logic Prototype

Use this branch for a **decision surface**: state transitions, data shape, interface feel, or action legality that must be driven through cases.

[SKILL.md](SKILL.md) owns the prototype contract, write boundary, verdict, and cleanup. This file owns the logic artifact and smoke gate.

## Right Shape

Reach for a logic prototype to:

- drive a state model by hand;
- check action legality across states;
- feel out a data shape or module interface;
- expose hidden edge cases in a workflow, reducer, or state machine.

Use [UI.md](UI.md) for visual layout or information hierarchy.

## Decision Surface

Put the logic behind a small, pure interface. The terminal shell is disposable; the logic interface is the decision surface.

Build the shell under `.tmp/` and call real seams, methods, adapters, or prototype-only pure modules when possible. Use an authorized module path only when the question requires real app constraints.

A logic prototype produces **design evidence**. Examples, invariants, fixtures, and edge cases strengthen that evidence; production proof belongs to the real coding workflow.

Model only the states, actions, and data needed by the locked question.

Choose the shape that fits:

- **Reducer** - `(state, action) -> state`; best for discrete events over one state object.
- **State machine** - explicit states, transitions, and illegal actions; best when action legality is the question.
- **Pure functions over a plain data type** - best when there is no ongoing current state.
- **Class or module with a clear interface** - best when the concept genuinely owns ongoing internal state.

Keep a pure decision surface: inputs enter through the interface and updated state leaves through return values. The terminal shell owns I/O, prompts, timing, randomness, and rendering.

## Terminal Shell

Build the smallest terminal app that lets the judge press buttons and watch state change.

Stay repo-native: use the host project's language and tooling. Ask before selecting a runtime when the project has no obvious one.

Render a stable frame by clearing the screen with `console.clear()`, `print("\033[2J\033[H")`, or the local equivalent.

Each frame shows:

1. **Current state** - pretty-printed and diff-friendly; one field per line or formatted JSON is fine.
2. **Available actions** - short keyboard shortcuts or commands with enough labels to drive the model.

Use native terminal formatting when helpful. Reuse an existing styling dependency; otherwise keep formatting native. Keep the frame within one screen.

## Interaction Loop

1. Initialize one in-memory state object.
2. Render the first frame.
3. Read one key or command.
4. Translate it into an action.
5. Update state through the decision surface.
6. Re-render the frame.
7. Repeat until quit.

Handle unavailable or illegal actions enough to keep the probe running and make the state rule visible.

## One Command

Add or report one repo-native command: `pnpm run <name>`, `python <path>`, `uv run <path>`, `bun <path>`, `make <target>`, or the repo's equivalent.

When no task runner exists, put the command at the top of the prototype file or nearby note.

## Smoke Gate

Run the command once and verify:

- the first frame renders;
- at least one action changes visible state;
- an unavailable or illegal action is surfaced and leaves state unchanged when the model has one;
- quit works.

Report the command and every assumption that affects judgment.

## Logic Constraints

- Keep the shell thin and the decision surface pure.
- Use in-memory state; add persistence only when persistence is the question.
- Stop at the locked question.
- Drive the public decision surface; treat private helpers as implementation detail.
- Treat the terminal shell as disposable.
