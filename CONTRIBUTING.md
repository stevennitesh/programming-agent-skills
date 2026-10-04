# Contributing

Contributions should improve the current Astra pack without turning ordinary
coding into a mandatory workflow.

## Start here

Start with [AGENTS.md](AGENTS.md) for repository commands and constraints.
[CONTEXT.md](CONTEXT.md) identifies source ownership and historical boundaries;
the [Astra design brief](docs/astra/design-brief.md) governs changes to skill
composition, discovery, or behavior.

The managed source is `skills/astra/`. `skills/custom/`,
`skills/experimental/`, archived records, and legacy epoch machinery are
historical or explicitly selected compatibility surfaces; do not use them as
current Astra authority.

## Development setup

Create and activate a local virtual environment, then install the development
dependencies:

```sh
python -m venv .venv
python -m pip install -r requirements-dev.txt
```

Use `python3` where your platform does not provide `python`.

## Before submitting a change

For ordinary Astra or validator changes:

```sh
python -m scripts.pytest_focused
python -m scripts.validate_skills --public
```

Run the full suite when the change affects shared helpers, installation,
transactions, legacy compatibility, or broad repository contracts:

```sh
python -m pytest -n 0
```

Installer changes should preserve unrelated skills and user instructions,
idempotence, transaction recovery, and refusal to overwrite unowned or modified
state. Use the installer tests rather than modifying an installed skill copy.

Keep local workspace configuration, scratch output, secrets, captures, and
generated evidence out of Git. The repository ignores the common local paths;
put disposable work under `.tmp/<purpose>/` as required by `AGENTS.md`.

## Change discipline

Keep project facts, accepted requirements, and workflow contracts at their
maintained owners. Retire displaced instructions and affected validator rules
together; preserve history as evidence. General coding tutorials do not need
another persistent document.

Packaging or structural checks prove only those properties. Claims that a skill
improves model behavior, quality, cost, or reliability need evidence appropriate
to that claim.
