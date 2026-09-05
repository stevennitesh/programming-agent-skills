# Programming Agent Skills

This pack helps capable coding agents produce high-quality code through strong
judgment, simple design, and focused verification. Ordinary work stays ordinary.
Specialist procedures apply when the task needs them.

Explore imaginatively. Converge under proof. Simplify ruthlessly.

## Current direction

Build the Astra pack in `skills/astra/`. When designing or changing an Astra
skill, read [the Astra design brief](docs/astra/design-brief.md). It records the
accepted principles from [issue #94](https://github.com/stevennitesh/programming-agent-skills/issues/94),
subsequent decisions, and what remains unsettled.

Projects using this pack target the latest Astra version. Retired source remains
available as evidence; do not preserve legacy routes in current project guidance.
[Legacy pack context](docs/agents/legacy-pack-context.md) documents that historical
composition and does not govern current Astra execution.

## Sources and ownership

| Concern | Owner |
| --- | --- |
| Working commands and local constraints | `AGENTS.md` |
| Coding judgment | [Engineering contract](docs/agents/engineering-contract.md) |
| Astra skill design and migration direction | [Astra design brief](docs/astra/design-brief.md) |
| Agent-instruction authoring | [Astra writing-for-agents](skills/astra/writing-for-agents/SKILL.md) |
| Current work and conditional runbooks | [Plans index](docs/plans/README.md) |
| Domain meaning and accepted decisions | [Domain route](docs/agents/domain.md), then relevant `docs/adr/` records |
| Tracker-backed work | [Tracker guide](docs/agents/issue-tracker.md) and [label mapping](docs/agents/triage-labels.md) |
| Managed installation | `scripts/install_skills.py` and its installed manifest |
| Repository and package validation | `scripts/validate_skills.py` and focused tests |

Keep each instruction at its owning location. Use conditional pointers to load
procedures and evidence when needed. Prefer current code, configuration, and
tools for mechanical facts; retain reasons and local conventions in guidance.

## Package distinctions

- **Managed custom skills:** `skills/custom/`, selected by the current installer.
- **Astra skills:** `skills/astra/`, the new packages and their source of truth.
- **Installed skills:** copies in the target host's skill directory. Inspect
  their content before assuming which source or version is installed.
- **Legacy experiments:** `skills/experimental/`, inactive alternatives governed
  by their manifest. Optional packages live in `skills/extra/`; retired material
  lives in `skills/.archive/`.

The managed installer does not deploy Astra. It may replace a same-named manual
Astra installation with the custom version. Use the selected source for targeted
installation and verify source-to-target content. Edit source packages, not
installed copies.

The repository's engineering contract is adapted from Astra and is owned here.
It is not required to match either bootstrap seed. Existing tracker and domain
settings preserve repository meaning while their routes target current Astra;
direct coding requires no ticket.

## Evidence and durable context

Research, synthesis, transcripts, issue notes, and run logs preserve evidence.
They become current guidance only through an explicitly adopted owner. Do not
rewrite historical records to make them look current. Consult relevant ADRs for
accepted decisions, with their stated scope and supersession status.

The README explains the product and installation choices. Global templates are
separate: `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` serves the legacy installer;
`skills/astra/repo-bootstrap/templates/global-agents.md` seeds Astra guidance.
Neither template overrides personal global preferences automatically.
