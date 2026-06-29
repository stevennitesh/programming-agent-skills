# Logic Prototype

Use this branch when the prototype question is about **business logic, state transitions, data shape, or interface feel**: the kind of thing that looks reasonable on paper but only feels wrong once the user can push it through cases.

This file defines the logic branch. Use the lifecycle in [SKILL.md](SKILL.md): write down the question, keep the artifact throwaway, run it once, capture the answer, and clean up or hand off.

## Right Shape

Reach for a logic prototype when the user needs to:

- drive a state model by hand
- check whether actions are legal in the right states
- feel out a data shape or module interface before implementation
- expose hidden edge cases in a workflow, reducer, or state machine

If the question is visual layout or information hierarchy, use [UI.md](UI.md).

## Logic Shape

Put the actual logic behind a small, pure interface. The terminal shell is throwaway; the logic module is the decision surface.

Model only the states, actions, and data needed to expose the decision surface.

Choose the shape that fits the question:

- **Reducer** - `(state, action) -> state`; best for discrete events over one state object.
- **State machine** - explicit states, transitions, and illegal actions; best when action legality is the question.
- **Pure functions over a plain data type** - best when there is no ongoing current state.
- **Class or module with a clear interface** - best when the concept genuinely owns ongoing internal state.

Keep the logic pure: no I/O, terminal code, prompts, sleeps, random behavior, or logging for control flow. The TUI imports the logic and calls it; nothing flows back from the TUI into the logic except inputs.

The validated shape can inform a real implementation pass later. Do not treat prototype code as production code.

## Terminal Shell

Build the smallest terminal app that lets the user press buttons and watch state change.

Use the host project language and tooling. Do not add a new runtime or package manager just for the prototype. If the project has no obvious runtime, ask.

Each render should replace the frame, not append to scrollback. Use `console.clear()`, `print("\033[2J\033[H")`, or the local equivalent.

Each frame should show:

1. **Current state** - pretty-printed and diff-friendly; one field per line or formatted JSON is fine.
2. **Available actions** - short keyboard shortcuts or commands, with enough labels for the user to drive the model.

Use native terminal formatting when helpful: bold for section names, dim for less important derived values. Do not add a styling dependency unless the project already uses one.

Keep the frame small enough to fit on one screen.

## Interaction Loop

The loop is deliberately simple:

1. Initialize one in-memory state object.
2. Render the first frame.
3. Read one key or one command.
4. Translate it into an action.
5. Update state through the logic interface.
6. Re-render the whole frame.
7. Repeat until quit.

Handle unavailable or illegal actions enough to keep the prototype running and make the state rule visible. Do not build broad error handling.

## One Command

Add or report one repo-native command to run the prototype: `pnpm run <name>`, `python <path>`, `uv run <path>`, `bun <path>`, `make <target>`, or the repo's equivalent.

If there is no task runner, put the command at the top of the prototype file or nearby note.

## Smoke Check

Before handing it over, run the command once and verify:

- the first frame renders
- at least one action changes visible state
- one unavailable or illegal action is handled without crashing, when the model has illegal actions
- quit works

Report the command and any assumption the prototype made.

## Anti-Patterns

- Blurring the logic and TUI together.
- Adding production persistence when persistence is not the question.
- Generalizing beyond the question.
- Testing private helpers instead of letting the user drive the model.
- Shipping the terminal shell into production.
