# Programming Agent Skills

The managed source is `skills/astra/`, built primarily for GPT 6 Astra.
[The design brief](docs/astra/design-brief.md) owns accepted pack-design decisions;
each skill owns its execution rules. Ordinary coding needs no skill pipeline or
general engineering-contract document.

## Sources and ownership

| Concern | Owner |
| --- | --- |
| Working commands and repository constraints | [AGENTS.md](AGENTS.md) |
| Skill design, composition, and migration direction | [Astra design brief](docs/astra/design-brief.md) |
| Initial guidance and requested setup migrations | [Repo bootstrap](skills/astra/repo-bootstrap/SKILL.md) |
| Ongoing repository context, durable memory, and requested agent-session retrospectives | [Context hygiene](skills/astra/context-hygiene/SKILL.md) |
| Selected agent-instruction artifacts | [Writing for agents](skills/astra/writing-for-agents/SKILL.md) |
| Current work and conditional runbooks | [Plans index](docs/plans/README.md) |
| Domain meaning and decision history | [Domain route](docs/agents/domain.md), then relevant ADRs |
| Tracker-backed work | [Tracker guide](docs/agents/issue-tracker.md) and [label mapping](docs/agents/triage-labels.md) |
| Managed installation | `scripts/install_skills.py` and its installed manifest |
| Repository and package validation | `scripts/validate_skills.py` and tests |

## Package boundaries

- **Managed Astra skills:** immediate subdirectories of `skills/astra/` containing
  `SKILL.md` define the managed set. Derive inventory from that source.
- **Historical custom skills:** `skills/custom/`, retained evidence and explicitly
  selected legacy work; not deployed by the current installer.
- **Installed skills:** copies at the selected host target. Edit source packages;
  inspect installed content before assuming its version or parity.
- **Legacy experiments and optional packages:** `skills/experimental/` is governed
  by its manifest; `skills/extra/` contains optional packages. Retired material
  lives in `skills/.archive/` and `.archive/`.

The installer verifies ownership before replacement or retirement. Old custom
manifests establish migration ownership only; modified managed copies and
unmanaged name collisions stop installation. [Installation and recovery](INSTALLATION.md)
owns preview, deployment, and recovery instructions.

## Current guidance and history

Keep actual project requirements at their maintained owners. General coding
advice does not need a separate document. Research, synthesis, transcripts,
validation records, and retired guidance remain evidence; an explicit adopted
decision is needed to make them current policy. The [ADR index](docs/adr/README.md)
records applicability. [Legacy pack context](docs/agents/legacy-pack-context.md)
supplies vocabulary only for selected legacy work.

Global templates have separate consumers:
`GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` supplies the installer's managed bootstrap
section; `skills/astra/repo-bootstrap/templates/global-agents.md` is an optional
setup seed. Neither overrides personal preferences automatically. Source cleanup
does not update installed skills, global instructions, or other repositories.
