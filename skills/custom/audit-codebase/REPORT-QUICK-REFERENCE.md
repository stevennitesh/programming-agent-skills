# Report CLI

Use `scripts/update_report.py` as the only report interface. Pass absolute
repository, report, and manifest paths. The report path must be
`.tmp/audit-codebase/<run-id>/report.html` inside the audited repository.

Every command returns one JSON document. Exit `2` means the request was
rejected before a trustworthy update completed.

## Read

```text
inventory --repo-root <repo>
source-identity --repo-root <repo> --path <path> [--path <path> ...]
inspect --repo-root <repo> --report <report>
```

`inventory` returns the tracked paths and current repository identity.
`source-identity` binds a selected path set to its current contents. `inspect`
validates canonical report bytes and returns the complete state, including all
currently selectable subsystems and candidates. Use that state directly.
Never scrape or hand-edit the HTML.

## Publish

```text
render-report --repo-root <repo> --report <new-report>
  --manifest <map.json> [--validate-only]

audit-subsystem --repo-root <repo> --report <report>
  --manifest <audit.json> [--validate-only]

analyze-candidate --repo-root <repo> --report <report>
  --manifest <analysis.json> [--validate-only]
```

Publish with the chosen command. Use `--validate-only` when a no-write preview
is useful; publication performs the same validation. Map requires a new absent
report. Audit and Analyze require the current report SHA returned by `inspect`;
stale identities fail without falling back or selecting another item.

The helper writes through an invocation-owned sibling, replaces the report
atomically, and reads back the final canonical bytes. On failure, return the
reported stage and inspect current state when safe. Do not retry with a changed
manifest or another write mechanism.

## Manifest ownership

- **Map** supplies current repository identity, systems, subsystems, complete
  path ownership or exclusions, coverage, and evidence limits.
- **Audit** supplies one user-selected subsystem, its current Source Trace,
  exactly six coverage classes, findings, systemic findings, candidates,
  coverage, evidence limits, and any suggested audit order.
- **Analyze** supplies one user-selected candidate, current source identity,
  terminal state, affected scope, material options, recommendation, proof, and
  evidence limits. A blocked result includes the exact unresolved question.

For Audit and Analyze, copy only `paths` and `sha256` from the applicable
`source-identity` response. Audit binds at least the selected subsystem's owned
paths plus every shared source used as evidence; Analyze binds at least the
mapped paths in the candidate's affected scope plus any additional decisive
source. Disproved or blocked analysis may omit options and leave recommendation
empty.

Use the helper's current manifest version. Unknown fields and incomplete
ownership or coverage are rejected.
