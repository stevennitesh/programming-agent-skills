# Execution profiles

Use with the [lane helper](../scripts/lane_worktree.py) when repeated setup or
commands benefit from shared settings. The lead chooses the relevant repository
commands; a profile is optional and does not define acceptance or scheduling.

The JSON fields are:

| Field | Meaning |
| --- | --- |
| `env` | Explicit environment overrides. Inherited environment values are not copied into evidence. |
| `inputs` | Environment-variable names mapped to existing file or directory paths. Relative paths resolve from the lane checkout. |
| `outputs` | Environment-variable names mapped to disposable directories inside lane runtime. Relative paths resolve from runtime. |
| `setup` | Ordered argument arrays for explicitly selected setup commands. |
| `checks` | Ordered argument arrays for health commands. At least one is required by `ready`. |
| `timeout` | Positive per-command seconds; defaults to 300. |

Only supplied setup and checks execute. `exec` uses the environment and path
settings, but runs only its command after `--`. One-off environment/path arguments
override matching profile keys; one-off setup/check arrays append to the profile.
`--timeout` overrides the profile timeout. Do not put credentials in command
arguments or printed output; those are retained in command evidence.

Environment names follow host case rules: Windows treats case variants as the
same key, while POSIX keeps them distinct. Each profile mapping must have distinct
keys under those rules before applying one-off overrides. Keys may not overlap across `env`,
`inputs`, and `outputs`, or replace the helper's `LANE_WORKTREE` and `LANE_RUNTIME`
variables under those rules.

Arguments and profile values support the literal tokens `@worktree@`,
`@runtime_root@`, `@temp_root@`, `@cache_root@`, `@pytest_basetemp@`, and
`@pytest_cache@`. This is simple token replacement, not shell interpolation.

For example, adapt this Windows Python profile to the repository's actual setup,
data location, and smoke test. Other platforms use their own interpreter paths.

```json
{
  "inputs": {"DATA_ROOT": "../../datasets/current"},
  "outputs": {"RESULTS_DIR": "results"},
  "setup": [
    ["python", "-m", "venv", "@runtime_root@/venv"],
    ["@runtime_root@/venv/Scripts/python.exe", "-m", "pip", "install", "-r", "@worktree@/requirements-dev.txt"]
  ],
  "checks": [
    ["@runtime_root@/venv/Scripts/python.exe", "-m", "pytest", "tests/test_smoke.py", "--basetemp", "@pytest_basetemp@", "-o", "cache_dir=@pytest_cache@"]
  ],
  "timeout": 300
}
```

Use an interpreter bound to the intended environment. A successful generic Python
command alone does not prove that project imports resolve to this checkout; choose
a relevant import or application smoke check when that can fail. Package-manager
caches may be shared through explicit environment overrides when concurrent use is
supported; mutable project environments and generated data need exclusive ownership.

Temporary directories, common cache defaults, and declared outputs are routed for
each invocation. Tool-specific outputs still need the appropriate command options,
such as the pytest paths above. Shared input declarations perform a small file
read or directory enumeration; dataset validation belongs in selected checks.
They neither copy data nor prevent the invoked application from writing to it.

Readiness evidence records the observed commit and profile digest, not a complete
fingerprint of dependencies or mutable datasets. Reuse evidence only while the
relevant inputs remain valid. `--checks-only` is an explicit choice to retain setup;
it still checks declared paths and runs health commands. Changes in the worker's
permissions or environment require the affected checks in that context.
