# Source-gap packet

## Evidence

- Source: `SRC-V02@1`
- Source owner: Inez, CLI owner
- Requested outcome: add JSON output to the existing `inspect` command.
- Setup: compatible.
- Publication authority: standalone Ready-for-agent items are authorized; no parent exists or may be created.
- Initial tracker state: no related parent or child items exist.

## Blocking source gap

The JSON contract is not specified. Acceptance says that `--format json`
emits “the specified keys,” but the complete source packet does not enumerate
those keys or define their value types, required/optional status, or
null/absence behavior. The proof fixture name `inspect_json` is a proof seam,
not a decision-bearing specification. Inventing those details would change C1
and could make a ticket appear Ready-for-agent without observable acceptance.

Decision required from Inez: provide the stable JSON schema for the existing
inspect result, including the exact keys, each key's value type, and how
optional or unavailable values are represented. If byte-stable serialization
is intended, also specify whether key ordering is contractual.

## Affected slices and coverage

| Source commitment or boundary | Disposition |
| --- | --- |
| C1 — serialize the existing inspect result as stable JSON | Blocked candidate slice: the missing schema prevents complete acceptance and verification evidence. |
| Acceptance — `--format json` emits the specified keys | Blocked by the same missing schema. |
| C2 — document the flag and invalid-format error | Candidate slice is otherwise bounded, but remains unpublished because the complete source design cannot pass the pre-publication readiness audit. |
| Acceptance — unknown formats exit nonzero without partial output | Accounted for in the C2 candidate slice; no source gap identified. |
| Scope — inspect output formatting | Preserved as the scope fence for both candidates. |
| Exclusions — new parent issue, YAML output, command redesign | Preserved; none would receive a ticket. |
| Category — enhancement | Authorized for eventual justified items only. |

Tentative stable order after repair:

1. JSON serialization for the existing inspect result.
2. Unknown-format rejection and documentation for `--format json`.

No blocker edge is established from the supplied evidence. Stable order and
likely overlap at the CLI/proof seam are not blocker edges. Parallel safety
and any serial constraint must be frozen with the repaired ticket bodies
before publication.

## Tracker state and mutations

Tracker state is unchanged. No `create_item`, relationship, role, state, or
read-back operation was performed. In particular, no parent was fabricated
and the fixture creation observations were not consumed.

## Exact safe continuation

Inez should amend `SRC-V02` with the missing JSON schema decision. Then rerun
To Tickets from the amended source, rebuild and audit exhaustive ticket bodies,
execution profiles, state matrices, graph, and frontier, and only then create
and read back authorized standalone Ready-for-agent items.

Next owner: Inez, CLI owner. Stop without publication or implementation.
