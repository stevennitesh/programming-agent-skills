# Report CLI

Use `scripts/update_report.py` as the only report interface. Pass absolute
paths. Every response is one JSON document on stdout; exit 2 rejects the
request, exit 3 reports an unexpected helper failure, and stderr stays empty.

Never open, parse, copy, or edit HTML. The helper reads canonical state,
validates strict JSON, and renders the complete report.

## Read Commands

```text
schema --objective map|audit
schema --objective analyze
  [--tracker-provider local-markdown]
schema --objective close
  --completion-route tracker-frontier
  [--tracker-provider local-markdown]
schema --objective close
  --completion-route local-markdown-recovery|authorized-direct-recovery
inventory --repo-root <repo>
source-identity --repo-root <repo> --path-list <paths.txt>
inspect --repo-root <repo> --report <report>
  --objective map
inspect --repo-root <repo> --report <report>
  --objective audit --subsystem-id <id>
inspect --repo-root <repo> --report <report>
  --objective analyze|close --candidate-id <id>
```

`inspect` returns the selected current projection without history and derives
the Close packet route from tracker facts. The route selects a schema;
[CANDIDATE-CONTRACT.md](CANDIDATE-CONTRACT.md) owns semantic Close admission.
Use the projection for routing, admission, work, and read-back. `schema`
returns the exact manifest template for the selected objective and Close
route; copy only its `template` object into an invocation-owned JSON file.
Unknown manifest fields are rejected.

## Publish Once

Map uses `render-report`; Audit, Analyze, and Close use `audit-subsystem`,
`analyze-candidate`, and `close-candidate` respectively. Every mutation uses
the same two calls with the same unchanged manifest:

```text
<command> --repo-root <repo> --report <report>
  --manifest <facts.json> --validate-only
<command> --repo-root <repo> --report <report>
  --manifest <same-facts.json>
  --expected-bundle-sha256 <digest-from-validation>
```

Validation writes nothing. Make at most one publication call. Do not change
the manifest between calls.

## Objective Rules

- **Map:** run `inventory` immediately before work and use its paths and
  identity. A new report expects `absent`; updating a map-only report requires
  its current digest. A report with Audit or candidate history is rejected.
- **Audit:** supply one selected subsystem's current Source Trace, six coverage
  rows, admitted records, candidates, limits, and resolved Audit, To Tickets,
  and Implement skill paths. A changed ownership or dependency boundary
  requires a separately selected Map with a new report.
- **Analyze:** supply one selected candidate's current validity, members,
  comparison, proof, tracker result, and at most one other next owner. Request
  the Local Markdown schema when that provider returned the graph; the helper
  derives and locks its contained refs and read-back digest without an HTTPS
  identity.
  The helper derives the pickup from the validated tracker result.
- **Close:** `tracker-frontier` requires the matching read-back-verified tracker
  frontier. Request its Local Markdown schema when applicable.
  `local-markdown-recovery` is restricted to an existing version-10/state-2
  recovery record caused solely by the former HTTPS-only Ready identity field;
  it revalidates one uniquely matching candidate-bound local graph and exact
  committed closeout, then records `ready-graph` without remapping.
  `authorized-direct-recovery` requires an already-landed
  `authority-required|not-applicable` candidate and direct implementation
  authority; it forbids tracker fields and retrospective ticket fabrication.
  Every route independently verifies Git commit/tree reachability, candidate
  identity, and every active member transition.

## Use The Response Literally

Successful validation returns the report, report/state/bundle digests,
`stage: validate`, `mutation_started: false`, and unchanged report state.
Successful publication returns `stage: read-back`, `mutation_started: true`,
`effect: created|replaced`, and `report_state: updated`.

On error, use `stage`, `mutation_started`, `report_unchanged`, and
`report_state` exactly as returned. Never retry or hand-edit. Remove temporary
JSON and path lists only after final read-back or a proven zero-effect failure.
