# Runtime Profiles

The owning skill selects one semantic profile. This table supplies the runtime
binding; the orchestrator passes it directly when starting the worker.

| Profile | Agent type | Model | Reasoning |
| --- | --- | --- | --- |
| `clear-worker` | `luna_max` | `gpt-5.6-luna` | `max` |
| `adaptive-worker` | `default` | `gpt-5.6-terra` | `xhigh` |
| `fast-adaptive-worker` | `default` | `gpt-5.6-sol` | `medium` |
| `demanding-worker` | `default` | `gpt-5.6-sol` | `high` |

Choose worker profiles in this order:

1. `demanding-worker` for a public interface, cross-owner invariant,
   migration or compatibility boundary, trust boundary, or broad coupling;
2. `adaptive-worker` for consequential choices contained within one owner; or
3. `clear-worker` for a settled, repeatable path with no consequential choice.

Use `fast-adaptive-worker` instead of `adaptive-worker` only under an explicit
latency preference that accepts its lower reasoning setting. Do not infer speed
or cost from the profile name.

`default` means spawn a fresh-context collaboration subagent with the row's
model and reasoning. A named agent type loads its custom TOML; its configured
model and reasoning must match the row.

`../assets/luna_max.toml` is the canonical named-agent template;
`$repo-bootstrap` owns its repo-local provisioning and reconciliation.

Enforce a row only for a spawned implementation actor. Review roles use their
owning review skill's fresh-context and separation rules without a model or
reasoning assignment from this worker table. A known mismatched implementation
binding is `transport-blocked`.
