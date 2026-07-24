"""Build isolated Prompt 4 worker payloads from the frozen Prompt 3 manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EVAL_ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "skills" / "experimental" / "implement"
MANIFEST_PATH = PACKAGE / "evaluation-manifest.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def runtime_text(root: Path) -> str:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    metadata = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
    return (
        "----- SKILL.md -----\n"
        f"{skill}"
        "\n----- agents/openai.yaml -----\n"
        f"{metadata}"
    )


def all_fixtures(manifest: dict) -> list[dict]:
    worker = manifest["worker_visible"]
    fixtures = list(worker["viability"])
    for cluster, members in worker["quality_controls"].items():
        for fixture in members:
            fixtures.append({**fixture, "cluster": cluster})
    for fixture in fixtures:
        if fixture["id"] == "V-01":
            fixture["source_facts"] = [
                *fixture["source_facts"],
                "The settled finite Repair budget is one generation.",
            ]
            fixture["prompt4_source_repair"] = (
                "Added the required finite Repair budget; task and rubric unchanged."
            )
    return fixtures


def render_payload(manifest: dict, runtime: str, fixture: dict) -> bytes:
    config = manifest["configuration"]
    worker = manifest["worker_visible"]
    visible = {
        "shared_authority": worker["shared_authority"],
        "shared_tools": worker["shared_tools"],
        "fixture": fixture,
    }
    text = (
        f"{config['worker_template']}\n\n"
        "Treat all tracker, commit, and mutation operations as supplied simulations. "
        "Do not mutate the repository or external state. Use only the permitted "
        "operations named below. Do not read any other repository file.\n\n"
        "LOADED RUNTIME PACKAGE\n"
        "======================\n"
        f"{runtime}\n\n"
        "WORKER-VISIBLE FIXTURE\n"
        "======================\n"
        f"{json.dumps(visible, indent=2, sort_keys=True)}\n"
    )
    return text.encode("utf-8")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    runtimes = {
        "m0": runtime_text(PACKAGE / "controls" / "m0"),
        "h1": runtime_text(PACKAGE),
    }
    records = []
    payload_root = EVAL_ROOT / "payloads"
    payload_root.mkdir(parents=True, exist_ok=True)

    for fixture in all_fixtures(manifest):
        fixture_id = fixture["id"]
        arms = ["m0"] if fixture_id.startswith("V-") else ["m0", "h1"]
        rendered = {}
        for arm in arms:
            payload = render_payload(manifest, runtimes[arm], fixture)
            arm_dir = payload_root / arm
            arm_dir.mkdir(parents=True, exist_ok=True)
            path = arm_dir / f"{fixture_id}.md"
            path.write_bytes(payload)
            rendered[arm] = {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(payload),
            }

        fixture_bytes = json.dumps(
            {
                "shared_authority": manifest["worker_visible"]["shared_authority"],
                "shared_tools": manifest["worker_visible"]["shared_tools"],
                "fixture": fixture,
            },
            indent=2,
            sort_keys=True,
        ).encode("utf-8")
        record = {
            "fixture_id": fixture_id,
            "family": fixture["family"],
            "cluster": fixture.get("cluster", "m0-viability"),
            "worker_visible_fixture_sha256": sha256(fixture_bytes),
            "payloads": rendered,
        }
        if len(rendered) == 2:
            m0_payload = (ROOT / rendered["m0"]["path"]).read_bytes()
            h1_payload = (ROOT / rendered["h1"]["path"]).read_bytes()
            m0_runtime = runtimes["m0"].encode("utf-8")
            h1_runtime = runtimes["h1"].encode("utf-8")
            record["arm_delta_only_runtime"] = (
                m0_payload.replace(m0_runtime, b"<RUNTIME>", 1)
                == h1_payload.replace(h1_runtime, b"<RUNTIME>", 1)
            )
        records.append(record)

    root_only_bytes = json.dumps(
        manifest["root_only"], indent=2, sort_keys=True
    ).encode("utf-8")
    protocol = {
        "format": 1,
        "source_manifest_sha256": sha256(MANIFEST_PATH.read_bytes()),
        "runtime_packages": {
            "m0": manifest["runtimes"]["m0"]["tree_sha256"],
            "h1": manifest["runtimes"]["h1"]["tree_sha256"],
        },
        "worker_template_sha256": sha256(
            manifest["configuration"]["worker_template"].encode("utf-8")
        ),
        "root_only_evaluation_fixture_sha256": sha256(root_only_bytes),
        "records": records,
    }
    (EVAL_ROOT / "protocol-manifest.json").write_text(
        json.dumps(protocol, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
