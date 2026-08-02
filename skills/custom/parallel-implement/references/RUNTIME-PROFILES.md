# Runtime Profiles

The owning skill selects one semantic profile. This registry supplies its
runtime binding for every launch transport.

```text
python <skill-dir>/scripts/run_ledger.py profile --id <profile>
```

The resolver returns the exact collaboration spawn arguments.

| Profile | Agent type | Model | Reasoning |
| --- | --- | --- | --- |
| `parallel-root` | `current` | `gpt-5.6-sol` | `high` |
| `clear-worker` | `luna_max` | `gpt-5.6-luna` | `max` |
| `adaptive-worker` | `default` | `gpt-5.6-terra` | `xhigh` |
| `fast-adaptive-worker` | `default` | `gpt-5.6-sol` | `medium` |
| `demanding-worker` | `default` | `gpt-5.6-sol` | `high` |
| `serial-integrator` | `default` | `gpt-5.6-sol` | `medium` |
| `ordinary-reviewer` | `default` | `gpt-5.6-sol` | `high` |
| `assurance-coordinator` | `default` | `gpt-5.6-sol` | `high` |
| `har-spec-reviewer` | `default` | `gpt-5.6-sol` | `xhigh` |
| `har-standards-reviewer` | `default` | `gpt-5.6-sol` | `xhigh` |
| `har-specialist` | `default` | `gpt-5.6-sol` | `xhigh` |

`current` means the existing root must match the row. `default` means spawn a
fresh-context collaboration subagent with the row's model and reasoning. A
named agent type loads its custom TOML; its configured model and reasoning must
match the row.

`../assets/luna_max.toml` is the canonical named-agent template;
`$repo-bootstrap` owns its repo-local provisioning and reconciliation.

Escalate `serial-integrator` to `high` only for conflicting architectural
intent, cross-module invariants, migrations or compatibility behavior,
security-sensitive boundaries, or a repeated failed correction.

The accepted launch request proves the requested binding when resolved
telemetry is unavailable. A missing or mismatched implementation or integration
binding is `transport-blocked`; a formal-review mismatch is
`transport-invalid` and receives no review credit.
