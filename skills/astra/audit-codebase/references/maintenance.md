# Atlas maintenance

Use when resuming a saved atlas or keeping it accurate as authorized fixes land.
The helper owns deterministic reconciliation and publication; the agent judges
ownership, changed conclusions, adequate proof, and the requested delivery scope.

## Inspect the relevant work

`status` returns counts and bounded work rows. `inspect` defaults to the same
compact view and adds relevant evidence when a subsystem, candidate, or finding
is selected. Both observe current source without writing the report.
For a copied `$audit-codebase inspect candidate ...` or `inspect finding ...`
selection, resolve its run and stable ID through filtered inspection. Report the
relevant changes and outcomes and judge what reassessment, if any, remains needed.
It does not select that record for another full audit or implementation by itself.

```text
python <atlas.py> status --repo-root <repo> --report <report.html> --outstanding
python <atlas.py> inspect --repo-root <repo> --report <report.html> --candidate <id> --history
python <atlas.py> inspect --repo-root <repo> --report <report.html> --subsystem <id>
python <atlas.py> status --repo-root <repo> --report <report.html> --changed-path <path>
```

Use `--limit` (default 20, maximum 100) and `--offset` for more rows or history.
`--outstanding` includes historical targets with unfinished work or requested
delivery pending. `--history` includes historical IDs and relevant revisions,
including reviewed ownership changes and requested delivery before and after
updates for the selected target. `inspect --full` returns the complete retained
state and cannot be combined with filters. Avoid
reading the whole HTML or state just to determine outstanding work.

Changed-path filters select records bound to that path or directory. Inspect the
returned audit, analysis, and outcome source changes to establish what changed.
Finding inspection returns its originating audit packet and current audit/scope
observations, including retained systemic findings. These remain separate from
fix-verification observations.
Applicable finding-level proof inputs also make their candidate selectable.
Outcome evidence and its observations return the latest relevant records up to
the requested limit, with totals and more-record indicators; path-filtered
observations retain matching proof inputs. Use history or full state for older detail.
Source packets include
per-path fingerprints. Map drift separately exposes added, removed, and unowned
tracked paths. An unchanged prior packet does not prove newly added code was audited.

## Reconcile reviewed ownership changes

Use `reconcile-map` for additions, deletions, moves, splits, or merges. It retains
original audits, analyses, findings, source identities, and history; it does not
reset the run or transfer an old audit's coverage to a new owner.

Every mutation uses a UTF-8 JSON manifest, `--repo-root`, `--report`, and
`--manifest`. Obtain the current `report_sha256` from inspection. Set
`version: 1` and `expected_report_sha256` to that digest. Use `--validate-only`
to check without publishing. Successful publication retains writer exclusion,
atomic replacement, and read-back; inspect state before retrying an uncertain write.

A reconciliation additionally requires `observation_identity` from current
`inventory`. Supply only reviewed structural changes:

```json
{
  "version": 1,
  "expected_report_sha256": "<current report digest>",
  "observation_identity": {
    "commit": "<inventory commit>",
    "tree": "<inventory tree>",
    "tracked_content_sha256": "<inventory digest>"
  },
  "ownership_changes": [
    {"path": "src/new.py", "owner": "validation", "reason": "New validation entry."},
    {"path": "src/removed.py", "owner": null, "reason": "Module removed."}
  ],
  "subsystems": [
    {"id": "validation", "dependencies": []}
  ]
}
```

`ownership_changes` moves each exact path to its named current owner; `null`
detaches a removed path or explicitly excludes a still-tracked path with its
reason. `subsystems` contains partial structural patches keyed by existing IDs;
a new ID needs a complete subsystem definition. Optional `systems`, `excluded`,
`title`, `coverage`, and `evidence_limits` replace those map fields. Full resulting
ownership must cover every tracked path exactly once or explicitly exclude it.
Remove or narrow a directory exclusion explicitly before assigning a path within it.

For a retired subsystem, add
`retirements: [{"id": "old", "replacement_ids": ["new"], "reason": "Reviewed boundary change."}]`.
Use multiple replacements for a split, a common replacement for a merge, or an
empty list for removed behavior. Patch current dependencies and ownership in the
same operation. Retired IDs stay reserved, original records remain inspectable,
and affected scopes resolve through their declared replacements. New owners start
mapped; retained audits whose ownership changed are marked changed until the
relevant scope is reassessed.

## Record fixes and delivery

For an authorized selected set, continue through implementation and relevant
verification and publish its outcomes together with `record-outcome`. Keep the
original diagnosis and analysis intact. Each event has a unique `id`, a `target`
of `{"kind": "candidate" | "finding", "id": "<stable id>"}`, a `type`, a
`summary`, and nonempty `evidence`. Events append; corrections use a later event.

| Type | Additional fields and meaning |
| --- | --- |
| `implemented` | Current `source_identity`; work changed, verification still needed. |
| `verified` | Current `source_identity`; evidence supports the stated fix. |
| `deferred` | Evidence and reason for leaving the work deferred; no verification claim. |
| `reopened` | Evidence for reopening work; begins a new work epoch. |
| `committed` | `reference`: full Git commit ID; records delivery, not fix verification. |
| `deployed` | `destination` and `reference`: deployed version or evidence reference. |

Obtain source packets using `source-identity --path ...`; include `paths`,
`sha256`, and the returned `fingerprints`. Implemented and verified packets must
cover current mapped ownership in the target's affected scope, plus any relevant
external proof inputs. A candidate's scope includes additions established by its
analysis and every finding bound by a group event; it resolves retired owners
through their replacements. Ownership added
after an observation marks that observation changed until new evidence covers it.
The helper checks the binding; the agent remains responsible
for what the evidence establishes. A commit or deployment event does not run those
operations or independently verify the cited evidence.

```json
{
  "version": 1,
  "expected_report_sha256": "<current report digest>",
  "events": [{
    "id": "validation-fix-verified",
    "target": {"kind": "candidate", "id": "validation-fix"},
    "type": "verified",
    "summary": "Both entry paths reject invalid identities.",
    "evidence": ["Focused caller checks passed against the recorded source."],
    "source_identity": {"paths": ["src/validation.py"], "sha256": "<source digest>", "fingerprints": {"src/validation.py": "<path digest>"}}
  }],
  "delivery_requirements": [{
    "target": {"kind": "candidate", "id": "validation-fix"},
    "commit": true,
    "deployments": ["local install"],
    "reason": "User requested commit and installation."
  }]
}
```

Include delivery requirements only for requested effects. They replace expectations
for that target while retaining the previous record in history. A requirements-only
manifest is allowed. Pending delivery remains visible alongside verified or
deferred work; neither commit nor deployment implies the fix was verified.

Candidate events bind the finding IDs present when recorded. They also apply to
those findings, including historical IDs. A later finding added to the candidate
does not inherit old verification. Record narrower finding outcomes for partial
completion; verify the candidate as a group only when the evidence covers that group.
Changed verification inputs require inspection, while an original audit changed by
its verified fix remains historical evidence. Reimplementation or reopening starts
a new epoch, including narrower work on a bound finding, so old group delivery
records cannot complete the renewed work. Group verification reflects the current
finding outcomes and must collectively cover the candidate's analyzed scope.

## Check and preview the report

`check-report` is read-only. It validates canonical state, relationships, anchors,
IDs, and copyable selection commands. It reports current ownership coverage and
freshness separately: a valid report can contain changed evidence or map drift.
It never claims to have visually inspected the report.

Open the HTML when the host supports it. Inspect navigation, filters, selection
commands, progress labels, and useful screen sizes. `record-preview` accepts the
usual guard fields plus `preview` with `environment`, `capability`, `state`,
`reason`, and nonempty `evidence`. Use `state: "unavailable"` for a host limitation;
identical records for the same environment/capability are no-ops. Reconsider when
the host or capability changes, rather than repeating the same blocked check.
Use `state: "verified"` with `report_sha256` naming the actual viewed revision.
The record names that revision before metadata publication; it does not claim
every later report was visually checked. Prior capability observations remain in
history when replaced. Repeated mentions are not attempt counts.
