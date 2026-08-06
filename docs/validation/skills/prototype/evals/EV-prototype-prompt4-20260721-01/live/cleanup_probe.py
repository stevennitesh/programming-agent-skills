from __future__ import annotations

import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RUN_ROOT = ROOT / ".tmp/prototype-prompt4/live-cleanup"


def port_is_open(port: int) -> bool:
    with socket.socket() as probe:
        probe.settimeout(0.25)
        return probe.connect_ex(("127.0.0.1", port)) == 0


def main() -> None:
    if RUN_ROOT.exists():
        shutil.rmtree(RUN_ROOT)
    RUN_ROOT.mkdir(parents=True)
    shared = RUN_ROOT / "shared.txt"
    shared.write_text("user-before\nprototype-owned\nuser-concurrent\n", encoding="utf-8")
    disposable = RUN_ROOT / "probe.txt"
    cache = RUN_ROOT / "cache.bin"
    credential = RUN_ROOT / "credential.txt"
    durable = RUN_ROOT / "authorized-verdict.md"
    for path, text in (
        (disposable, "probe"),
        (cache, "cache"),
        (credential, "ephemeral"),
        (durable, "verdict evidence"),
    ):
        path.write_text(text, encoding="utf-8")

    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "http.server",
            str(port),
            "--bind",
            "127.0.0.1",
            "--directory",
            str(RUN_ROOT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(20):
        if port_is_open(port):
            break
        time.sleep(0.05)
    was_live = port_is_open(port)

    shared.write_text("user-before\nuser-concurrent\n", encoding="utf-8")
    disposable.unlink()
    cache.unlink()
    credential.unlink()
    server.terminate()
    server.wait(timeout=5)
    for _ in range(20):
        if not port_is_open(port):
            break
        time.sleep(0.05)
    is_live = port_is_open(port)

    before_remove = {
        "disposable_absent": not disposable.exists(),
        "cache_absent": not cache.exists(),
        "credential_absent": not credential.exists(),
        "user_work_preserved": shared.read_text(encoding="utf-8")
        == "user-before\nuser-concurrent\n",
        "authorized_evidence_present": durable.read_text(encoding="utf-8")
        == "verdict evidence",
        "process_was_live": was_live,
        "process_stopped_and_port_released": server.poll() is not None and not is_live,
    }
    shutil.rmtree(RUN_ROOT)
    print(
        json.dumps(
            {
                "dispositions": {
                    "probe.txt": "delete",
                    "cache.bin": "delete",
                    "credential.txt": "delete",
                    "shared.txt": "restore Prototype-owned line only",
                    "authorized-verdict.md": "authorized durable evidence",
                    f"process:{server.pid}/port:{port}": "stop and release",
                },
                "read_back_before_root_removal": before_remove,
                "run_root_absent": not RUN_ROOT.exists(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
