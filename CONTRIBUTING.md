# Contributing

Contributions should improve the current Astra pack without turning ordinary
coding into a mandatory workflow.

## Start here

Read, in order:

1. [AGENTS.md](AGENTS.md) for repository commands and invariants.
2. [CONTEXT.md](CONTEXT.md) for source ownership and current-vs-historical
   boundaries.
3. [Astra design brief](docs/astra/design-brief.md) when changing skill
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
put disposable work under `.tmp/` or another ignored location.

## Change discipline

Keep one clear owner for each behavior. Prefer the smallest coherent change,
preserve historical evidence instead of rewriting it as current guidance, and
update callers, documentation, tests, and validation together when a contract
changes.

Packaging or structural checks prove only those properties. Claims that a skill
improves model behavior, quality, cost, or reliability need evidence appropriate
to that claim.
