# Optional visual atlas

Use the atlas when the user requests a visual map, maintained audit coverage, or
continuation of an existing Astra report. Focused findings do not require it.
The helper is `scripts/atlas.py` relative to the skill directory; run it with
Python 3.11 or later. It uses Git inventory and the standard library.

## Ownership

The agent decides system boundaries, evidence, consequences, and recommendations.
The helper owns IDs, path expansion, overlap checks, source fingerprints, update
history, coverage counts, escaping, navigation, rendering, and atomic publication.
Do not author HTML, hashes, or record IDs. Do not copy the full state into context.

An atlas is one offline HTML file with embedded canonical data. No server, browser
script, CDN, or sidecar database is needed. The page groups systems and subsystems,
links dependencies, and expands findings and coverage records. Its freshness is
a dated snapshot; `inspect` checks current files and `refresh` republishes those
observations without changing judgments.

## Commands

Use absolute paths. Every invocation begins with:

```text
python <skill>/scripts/atlas.py --repo <repository> --report <repository>/.tmp/audit-codebase/<run>/report.html
```

Append one command:

| Command | Result |
| --- | --- |
| `init --title "Architecture atlas"` | Create an empty partial map; refuse an existing report. |
| `inventory` | List tracked and nonignored untracked paths. |
| `inspect` | Compact record index and mapping counts with current freshness. |
| `inspect --id <id>` | One record, its child records, and changed source paths. |
| `prepare --kind subsystem --path src/orders --out <new-draft.json>` | Generate a subsystem ID, ownership snapshot, and content fields. Repeat `--path` for additional files or directories. |
| `prepare --kind finding --subsystem <id> --path <additional-evidence> --out <new-draft.json>` | Prepare a finding bound to the subsystem's files and any additional evidence. Extra paths are optional. |
| `prepare --kind assessment --subsystem <id> --out <new-draft.json>` | Prepare coverage and limits separately from findings. |
| `prepare --kind assessment --subsystem <id> --coverage comprehensive --out <new-draft.json>` | Generate the six-lens coverage ledger. Also works with `--id` to expand an existing assessment. |
| `prepare --kind <kind> --id <existing-id> --out <new-draft.json>` | Populate an existing record for revision. |
| `apply --draft <draft.json>` | Validate and publish that record, preserving all others. |
| `refresh` | Recompute inventory and freshness and regenerate the HTML. |

Drafts belong under repository `.tmp/audit-codebase/`. Preparation refuses to
overwrite a draft. Edit only `content`, or set `remove` to true for explicit
deletion. To change source selections, prepare again with the desired `--path`
arguments. Paths are exact files or directory prefixes, not glob expressions.

Create subsystem records first, then add evidenced dependencies using returned
IDs. Dependencies contain `id` and `evidence`. Shared infrastructure has its own
owner and named consumers; overlapping ownership is rejected. Directory selections
expand mechanically, but directory structure does not establish semantic ownership.
Unmapped and untracked paths stay visible; neither counts as audited or excluded.

Prepare immediately before recording evidence and include additional decisive
files outside the selected owner. Source or report drift rejects publication.
Inspect the change, re-examine affected evidence, and prepare again; do not paste
a new hash into an old draft. A refresh does not confirm a finding or clear its
changed-source flag. When deleting a subsystem, explicitly remove or reassign its
dependent records and relationships first.

## Judgment fields

Subsystems contain name, system, purpose, ownership, and evidenced dependencies.
Findings contain kind (`defect`, `opportunity`, `retain`, `gap`), scenario, evidence,
consequence, cause, counterevidence, direction, preservation checks, priority
(`high`, `medium`, `low`) and its rationale, confidence/limits, and status. A defect
also requires its accepted expectation. The helper sorts findings by priority.
Use `resolved`, `disproved`, or `blocked`
only with current supporting evidence; missing records do not imply resolution.
Keep cross-system findings at one origin and name other affected owners in the
evidence and direction, without duplicating the same cause under each subsystem.

An assessment names examined flows, relevant dimensions, limits, and recommendation.
Its coverage is `focused`, `comprehensive`, or `incomplete`. These are explicit
agent judgments; the script cannot infer completeness from path counts or findings.
For comprehensive coverage, the helper generates Design, Domain, Reliability,
Simplification, Coding Practice, and Performance entries. Mark each `examined`
with the flows and evidence inspected, `excluded` with an evidence-based reason,
or `gap` with the missing evidence and its consequence for the audit. Pending or
unexplained entries prevent a comprehensive claim. Gaps remain prominently labeled
in HTML; comprehensive scope does not mean complete evidence. Use `incomplete`
to save a ledger with pending work. Focused assessments need no ledger.
The helper enforces accounting, not the truth or adequacy of supplied evidence.
Reuse the assessment record when updating the same audit scope. To reassign a
child record, prepare its ID with `--subsystem <new-owner>` and appropriate paths.
A map without an
assessment is displayed as not audited. Historical versions remain in the report.

Publish after a coherent update, then open the report for the user when useful.
The helper reads back its output; no manual JSON/HTML synchronization is required.
Exit 2 reports a rejected or failed operation. Inspect state after an uncertain
publication; never bypass the helper or remove a writer lock without establishing
that its writer is no longer active.

Legacy custom reports use a different schema and remain unchanged. This helper
does not silently migrate them. Start an Astra atlas and revalidate selected
legacy evidence if migrating is requested. Retain an atlas outside scratch only
through an explicitly chosen archival workflow; this skill does not commit it.
