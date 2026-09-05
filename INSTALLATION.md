# Installation and recovery

The normal installation path is in the [project README](README.md#install).
This page covers installer ownership, custom targets, and recovery.

## Managed locations

By default, the installer manages active skills in
`$HOME/.agents/skills` and the pack bootstrap in
`$HOME/.codex/AGENTS.md`.

`skills/astra/` is the only managed skill source. The installer does not
install `skills/custom/`, `skills/experimental/`, `skills/extra/`, or `skills/.archive/`.

The manifest at
`$HOME/.agents/skills/.programming-agent-skills-manifest.json` records the
skill names owned by this pack. Updates may replace or retire those managed
names. They do not touch unrelated personal skills.

Old custom manifests are accepted only to identify ownership during migration
to Astra. Preview lists replacements and retirements; modified managed files
and unmanaged same-name folders still block the transaction. Manually installed
Astra folders are not silently adopted. Preserve or relocate those copies before
installing, or use a clean target. New manifests always identify `skills/astra`.

## Preview and install

Preview the affected skills and global-bootstrap action:

```bash
python -m scripts.install_skills --dry-run
```

Apply them:

```bash
python -m scripts.install_skills
```

Use `python3` instead of `python` on systems that do not provide the shorter
command.

## Validate the installed pack

Validation checks pack structure and installed parity. It does not measure the
quality of code an agent produces. The validator has third-party dependencies,
so install them in a repository-local virtual environment.

Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m scripts.validate_skills \
  --installed-root "$HOME/.agents/skills" --require-installed
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m scripts.validate_skills `
  --installed-root "$HOME\.agents\skills" --require-installed
```

Add `--json` to the preview or install command for machine-readable evidence.

## Global instructions

When no global `AGENTS.md` exists, the installer seeds the complete
[`GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`](GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md)
template. Later installs create or update only its `## Skill Pack Bootstrap`
section. Delegation rules and other personal instructions remain untouched.

Use `--skip-global-agents` to install only the managed skills. Use
`--global-agents <path>` or `--skills-dir <path>` for nondefault targets.

## Transaction behavior

Skill additions, updates, retirements, the manifest, and the global bootstrap
commit as one transaction. The installer takes a process lock, validates the
complete managed manifest, and refuses unsafe names, modified managed trees,
or conflicting unmanaged paths before mutation.

If installation fails, it restores the previous pack and removes the temporary
snapshot. If rollback cannot finish, it preserves a named
`.programming-agent-skills-transaction-*` snapshot and refuses another install
until that transaction is recovered.

## Recover an interrupted transaction

Run the recovery command with the snapshot path reported by the installer:

```bash
python -m scripts.install_skills \
  --recover-transaction <snapshot-path>
```

For nondefault targets, repeat the original `--skills-dir` and
`--global-agents` values, or `--skip-global-agents`. Recovery binds the
snapshot to those targets and refuses live content that matches neither the
previous nor the planned identity.

| Recovery status | Meaning | Next action |
| --- | --- | --- |
| `cleared-preparation` | No managed mutation began. Preparation residue was removed. | Run the installer again. |
| `restored` | The interrupted mutation was restored and verified. | Run the installer again. |
| `cleared-commit` | The committed install was verified. Only recovery residue remained. | No reinstall is needed. |

Recovery clears transaction claims while the snapshot still exists and
removes the snapshot last.
