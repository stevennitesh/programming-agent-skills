"""Index immutable Prompt 4 captures and validate registered sample coverage."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    results = json.loads((ROOT / "results-manifest.json").read_text(encoding="utf-8"))
    registered = {"V-01"}
    registered.update(sample["id"] for sample in results["m0_viability"]["samples"])
    for cluster in results["clusters"].values():
        registered.update(sample["id"] for sample in cluster["samples"])

    capture_root = ROOT / "captures" / "m0"
    captures = {
        path.stem: {
            "path": path.relative_to(ROOT.parents[3]).as_posix(),
            "sha256": digest(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(capture_root.glob("*.md"))
    }
    missing = sorted(registered - captures.keys())
    unexpected = sorted(captures.keys() - registered)
    if missing or unexpected:
        raise SystemExit(f"capture mismatch: missing={missing}, unexpected={unexpected}")

    index = {
        "format": 1,
        "captures": captures,
        "results_manifest_sha256": digest(ROOT / "results-manifest.json"),
        "protocol_manifest_sha256": digest(ROOT / "protocol-manifest.json"),
    }
    (ROOT / "capture-index.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
