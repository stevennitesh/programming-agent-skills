# Installation and recovery

The normal installation path is in the [project README](README.md#install).
This page covers installer ownership, custom targets, optional Codex tuning, and recovery.

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

Add `--json` to preview, install, or recovery commands for machine-readable
evidence.

## Global instructions

When no global `AGENTS.md` exists, the installer seeds the complete
[`GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`](GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md)
template. Later installs create or update only its `## Skill Pack Bootstrap`
section. Delegation rules and other personal instructions remain untouched.

Use `--skip-global-agents` to install only the managed skills. Use
`--global-agents <path>` or `--skills-dir <path>` for nondefault targets.

## Optional Codex quiet waiting

If your cost-aware lead keeps narrating or monitoring while Sol works because of
host-level progress instructions, this opt-in policy makes delegated waiting an
explicit exception. It applies across repositories using this Codex configuration,
only while a delegated agent holds exclusive custody and an event-driven wait is
available. Normal reporting resumes when custody returns or local work resumes.

The installer and repo-bootstrap do not apply this personal setting. Edit it
yourself, or explicitly authorize an agent to inspect and update the configuration.
Invoking cost-aware-coding alone does not grant that access. For assisted setup:

> Apply the optional Codex quiet-waiting setup from INSTALLATION.md. You may inspect
> and update my active Codex configuration for this setting. Preserve everything
> else, back up the file locally, validate TOML, and report only the relevant change
> without exposing unrelated configuration or secrets.

### Apply the policy

1. Locate the active configuration: `$CODEX_HOME/config.toml` when `CODEX_HOME`
   is set; otherwise `~/.codex/config.toml` (`%USERPROFILE%\.codex\config.toml`
   on Windows). If you use a selected profile, account for its overrides before
   editing; do not assume the default file supplies the effective value.
2. Keep a local backup. Merge the policy below into the existing root-level
   `developer_instructions` string, preserving its other text. If the key is
   absent, add the whole block **before the first TOML table header**. Do not add
   a duplicate key or a second copy of the policy.

```toml
developer_instructions = """
## Delegated-agent waiting
While a delegated agent has exclusive custody and an event-driven agent wait is available:
- Treat the pending wait as delegation progress rather than active local work. A general 60-second commentary cadence or limit on blocking waits does not apply to this event-driven wait.
- Use the longest practical event-driven interval allowed by the active workflow and runtime. Agent events and new user input can wake the wait early.
- Do not send commentary solely because time elapsed or a wait returned without a meaningful state change. Wait again without commentary. Report only a consequential question, blocker, error, custody transfer, completed candidate, meaningful state change, or user-requested status.
This exception ends when custody returns or useful local work resumes.
"""
```

3. Validate the edited file with a TOML parser. For Python 3.11+, replace the
   example path below with the actual file (use `python3` if needed):

   ```text
   python -c "import pathlib,tomllib; tomllib.loads(pathlib.Path('PATH/TO/config.toml').read_text(encoding='utf-8')); print('TOML valid')"
   ```

4. Restart Codex and check in a new session that the policy is active. Valid TOML
   alone does not establish that instructions loaded. On the next delegated run,
   verify quiet event-driven waiting and normal responses to consequential events.
   If it did not load, check the selected configuration/profile with permission;
   continue using the skill's host-instruction fallback meanwhile.

To undo, remove only this policy from `developer_instructions` (remove the key if
it was created solely for this policy), validate, and restart.

OpenAI documents `developer_instructions` as additional developer instructions
injected into the session in its [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
This policy does not override system instructions or tool limits. Instruction
loading has been verified in our Codex environment; lower token costs and behavior
across other environments remain unverified.

## Transaction behavior

Skill additions, updates, retirements, the manifest, and the global bootstrap
commit as one transaction. The installer takes a process lock, validates the
managed source and manifest, and refuses an empty/incomplete source pack, unsafe
redirects or names, modified managed trees, conflicting unmanaged paths, and
live target changes observed after planning.

The transaction commits the exact skill and global-bootstrap content captured by
its plan. If repository source changes during an install, that newer source is
left for the next run rather than being mixed into the in-flight transaction.
Runtime cache artifacts remain excluded from managed skill identity.

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
removes the snapshot last. Add `--json` when recovery evidence is consumed by
another tool.
