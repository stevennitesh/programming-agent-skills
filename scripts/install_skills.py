"""Install or update the supported custom skill pack without touching unrelated skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


MANIFEST_NAME = ".programming-agent-skills-manifest.json"
BOOTSTRAP_HEADING = "## Skill Pack Bootstrap"
LEGACY_BOOTSTRAP_HEADING = "## Skill Pack Guide"
LEGACY_BOUNDARY_HEADING = "## Boundary"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def active_skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in (root / "skills/custom").iterdir() if path.is_dir())


def tree_hash(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in directory.rglob("*") if item.is_file()):
        digest.update(path.relative_to(directory).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def read_managed_names(skills_dir: Path) -> set[str]:
    manifest = skills_dir / MANIFEST_NAME
    if not manifest.is_file():
        return set()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    names = payload.get("skills") if isinstance(payload, dict) else None
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise ValueError(f"Invalid installed manifest: {manifest}")
    return set(names)


def replace_tree(source: Path, destination: Path) -> None:
    temporary = destination.parent / f".{destination.name}.installing"
    backup = destination.parent / f".{destination.name}.previous"
    for path in (temporary, backup):
        if path.exists():
            shutil.rmtree(path)
    shutil.copytree(source, temporary)
    if destination.exists():
        destination.rename(backup)
    try:
        temporary.rename(destination)
    except Exception:
        if backup.exists() and not destination.exists():
            backup.rename(destination)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def bootstrap_section(template: Path) -> str:
    text = template.read_text(encoding="utf-8")
    start = text.find(BOOTSTRAP_HEADING)
    if start < 0:
        raise ValueError(f"Template is missing {BOOTSTRAP_HEADING}: {template}")
    return text[start:].strip() + "\n"


def preview_global_bootstrap(template: Path, target: Path) -> str:
    section = bootstrap_section(template)
    if not target.exists():
        return "created"

    text = target.read_text(encoding="utf-8")
    start = text.find(BOOTSTRAP_HEADING)
    if start >= 0:
        next_heading = re.search(
            r"(?m)^##\s+", text[start + len(BOOTSTRAP_HEADING) :]
        )
        end = len(text)
        if next_heading is not None:
            end = start + len(BOOTSTRAP_HEADING) + next_heading.start()
        current = text[start:end].strip() + "\n"
        return "present" if current == section else "updated"

    legacy_start = text.find(LEGACY_BOOTSTRAP_HEADING)
    if legacy_start >= 0:
        if text.find(LEGACY_BOUNDARY_HEADING, legacy_start) < 0:
            raise ValueError(
                f"Legacy skill-pack block has no {LEGACY_BOUNDARY_HEADING}: {target}"
            )
        return "migrated"
    return "merged"


def install_global_bootstrap(template: Path, target: Path) -> str:
    section = bootstrap_section(template)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("# Global Codex Instructions\n\n" + section, encoding="utf-8")
        return "created"
    text = target.read_text(encoding="utf-8")
    start = text.find(BOOTSTRAP_HEADING)
    if start < 0:
        legacy_start = text.find(LEGACY_BOOTSTRAP_HEADING)
        if legacy_start >= 0:
            boundary_start = text.find(LEGACY_BOUNDARY_HEADING, legacy_start)
            if boundary_start < 0:
                raise ValueError(
                    f"Legacy skill-pack block has no {LEGACY_BOUNDARY_HEADING}: {target}"
                )
            after_boundary = boundary_start + len(LEGACY_BOUNDARY_HEADING)
            next_heading = re.search(r"(?m)^##\s+", text[after_boundary:])
            legacy_end = len(text)
            if next_heading is not None:
                legacy_end = after_boundary + next_heading.start()
            updated = text[:legacy_start].rstrip() + "\n\n" + section
            if legacy_end < len(text):
                updated += "\n" + text[legacy_end:].lstrip()
            target.write_text(updated, encoding="utf-8")
            return "migrated"
        target.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")
        return "merged"
    next_heading = re.search(r"(?m)^##\s+", text[start + len(BOOTSTRAP_HEADING) :])
    end = len(text)
    if next_heading is not None:
        end = start + len(BOOTSTRAP_HEADING) + next_heading.start()
    updated = text[:start].rstrip() + "\n\n" + section
    if end < len(text):
        updated += "\n" + text[end:].lstrip()
    if updated == text:
        return "present"
    target.write_text(updated, encoding="utf-8")
    return "updated"


def install(
    root: Path,
    skills_dir: Path,
    global_agents: Path | None,
    *,
    dry_run: bool = False,
) -> dict[str, object]:
    sources = active_skill_dirs(root)
    active_names = {path.name for path in sources}
    previous_names = read_managed_names(skills_dir) if skills_dir.exists() else set()
    retired_names = sorted(previous_names - active_names)

    new_names: list[str] = []
    updated_names: list[str] = []
    unchanged_names: list[str] = []
    for source in sources:
        destination = skills_dir / source.name
        if not destination.is_dir():
            new_names.append(source.name)
        elif tree_hash(source) == tree_hash(destination):
            unchanged_names.append(source.name)
        else:
            updated_names.append(source.name)

    bootstrap_status = "skipped"
    if global_agents is not None:
        bootstrap_status = preview_global_bootstrap(
            root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
            global_agents,
        )

    if dry_run:
        return {
            "skills": sorted(active_names),
            "new": new_names,
            "updated": updated_names,
            "unchanged": unchanged_names,
            "retired": retired_names,
            "global_bootstrap": bootstrap_status,
        }

    skills_dir.mkdir(parents=True, exist_ok=True)
    for source in sources:
        replace_tree(source, skills_dir / source.name)
        if tree_hash(source) != tree_hash(skills_dir / source.name):
            raise RuntimeError(f"Installed skill failed hash verification: {source.name}")
    for name in retired_names:
        retired = skills_dir / name
        if retired.is_dir():
            shutil.rmtree(retired)

    manifest = {
        "format": 1,
        "source": "skills/custom",
        "skills": sorted(active_names),
        "hashes": {source.name: tree_hash(source) for source in sources},
    }
    (skills_dir / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if global_agents is not None:
        bootstrap_status = install_global_bootstrap(
            root / "GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md",
            global_agents,
        )

    return {
        "skills": sorted(active_names),
        "new": new_names,
        "updated": updated_names,
        "unchanged": unchanged_names,
        "retired": retired_names,
        "global_bootstrap": bootstrap_status,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path.home() / ".agents/skills",
        help="Shared Codex skills directory.",
    )
    parser.add_argument(
        "--global-agents",
        type=Path,
        default=Path.home() / ".codex/AGENTS.md",
        help="Global AGENTS.md that receives the minimal bootstrap section.",
    )
    parser.add_argument("--skip-global-agents", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    global_agents = None if args.skip_global_agents else args.global_agents.expanduser()
    try:
        result = install(
            root,
            args.skills_dir.expanduser(),
            global_agents,
            dry_run=args.dry_run,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Install failed: {error}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"Managed skills: {len(result['skills'])} in {args.skills_dir.expanduser()}")
        if result["new"]:
            print(f"New skills: {', '.join(result['new'])}")
        if result["updated"]:
            print(f"Updated skills: {', '.join(result['updated'])}")
        print(f"Unchanged skills: {len(result['unchanged'])}")
    else:
        print(f"Installed {len(result['skills'])} custom skills into {args.skills_dir.expanduser()}")
    if result["retired"]:
        print(f"Retired managed skills: {', '.join(result['retired'])}")
    print(f"Global bootstrap: {result['global_bootstrap']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
