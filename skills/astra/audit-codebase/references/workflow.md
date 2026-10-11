# Prepared work and verification

Use these operations when their mechanics remove repeated work. The agent still
chooses hypotheses, adequate evidence, useful improvements, and investigation
depth. A short direct audit needs no delegation, receipt collection, or gap ledger.
Commands use UTF-8 directly on Windows; callers need no Python encoding flags.

## Prepare the selected stage

```text
python <atlas.py> prepare-audit --repo-root <repo> --report <report> --subsystem <id>
python <atlas.py> prepare-analysis --repo-root <repo> --report <report> --candidate <id>
python <atlas.py> prepare-outcomes --repo-root <repo> --report <report> --target candidate:<id> --type verified
```

Repeat `--subsystem` or `--candidate` for separate packets, or `--target` for a
single outcome packet covering the selected set. `--affected-subsystem` expands
audit or analysis scope. `--path` binds additional proof inputs, including test
configuration, fixtures, or probe scripts outside the mapped owners. Use
`--output` for another JSON filename beside the report; preparation never
overwrites judgments. Blank judgment fields cannot publish.
Outcome and gap packets bind each target's source separately; additional `--path`
proof inputs are shared across the selected targets and retained for every
outcome type.

Prepare at the source state actually being investigated or verified. If source
changes during investigation, inspect the delta before preparing a replacement.
A newer fingerprint alone is not renewed evidence.

## Publish independent results once

```text
python <atlas.py> publish-batch --repo-root <repo> --report <report> --id selected-owners --packet audit-subsystem=<alpha.json> --packet audit-subsystem=<beta.json>
```

Use the same packet shape for direct and authorized delegated work. Workers
supply judgments and evidence in their assigned packets; the coordinator owns
publication. The helper validates the whole batch and makes one guarded write,
then reads it back. `--validate-only` checks without publishing.

Prepared packets retain their investigated source snapshots. Report guards may
advance only when ownership, selected records and work, assigned outcome types,
and source identities still match. Full re-audits also guard the owner's retained
work because historical IDs can be reintroduced. Source drift or a same-target
conflict rejects the batch without
partial publication. A raw
manifest has no compatibility proof and still needs the exact report revision.
After interruption, retry the same batch ID and packets. An embedded receipt
confirms prior publication; reusing that ID with changed packets is rejected.
Choose a new ID for a new decision batch. One writer lock remains authoritative.

## Append a narrow follow-up

Use `prepare-audit --append` and publish it with `append-findings`. Supply a
meaningful trace summary and new finding/candidate IDs. Existing analyses, audit
source identities, and lens coverage remain intact. New records bind to their own
inspected source. The append operation accepts no replacement lens coverage,
coverage prose, or audit recommendation. Use a full audit only when reassessing
that broader scope; it intentionally replaces the current audit and retains its
previous records in history.
Keep an ID for the same claim. Give a materially different finding or proposal
a new ID so previous work outcomes do not apply to it.

## Capture or carry a check

```text
python <atlas.py> verify --repo-root <repo> --report <report> --id regression --target candidate:<id> --environment <host-runtime> --path <proof-input> -- <command> <arguments>
python <atlas.py> verify --repo-root <repo> --report <report> --id after-commit --target candidate:<id> --environment <host-runtime> --path <proof-input> --reuse regression -- <command> <arguments>
```

`verify` runs an already-authorized command in the repository, saves its combined
output beside the report, and records the command, exit code, environment digest,
log digest, source before/after, content inputs, ownership, and source drift. It
does not choose a test strategy or mark a finding fixed. A failed command or
source-mutating check is recorded as insufficient proof; the CLI returns nonzero.

Carry-forward creates a new receipt referencing the original. It requires a
passing, drift-free receipt, unchanged candidate membership, log, command,
environment, input paths, file contents/kinds/executable bits, and implicated
ownership. Index-only or
commit-only changes can qualify while their original strict source fingerprints
remain preserved. Gitlinks retain strict identity checks. The helper refuses
automatic carry-forward when content, ownership, proof inputs, or environment
changes; inspect the delta and choose the relevant new proof. Include
every meaningful proof input; the helper cannot discover hidden dependencies,
remote state, or external toolchain changes. Do not reuse a check whose unrecorded
dependencies changed.

Use `prepare-outcomes --type verified --check <receipt-id>` to bind the receipt's
proof inputs and evidence references automatically; repeat `--check` as needed.
Supply the conclusion that the check supports. A verified outcome referencing
receipts rejects failed checks, changed proof contracts or logs, and mismatched
source. Inspection also marks verification changed when a referenced log disappears
or changes. Implementation, commit, and deployment remain separate outcomes. Direct
evidence can still establish an
outcome without using the command wrapper.
The CLI returns a compact receipt summary. Complete snapshots stay in the report
and are available through selected inspection with history or `inspect --full`.

## Record an evidence gap's disposition

```text
python <atlas.py> prepare-gaps --repo-root <repo> --report <report> --lens <subsystem>:performance
python <atlas.py> record-gaps --repo-root <repo> --report <report> --manifest <gaps.json>
python <atlas.py> status --repo-root <repo> --report <report> --gaps
```

Repeat `--lens`, or use `--finding <gap-id>`, to prepare the selected claims.
Record `closed`, `narrowed`, or `deferred`, decisive evidence, and the remaining
question and revisit condition when unresolved. The helper binds each disposition
to the original claim and the source inspected for this follow-up. It does not
rewrite historical lens coverage or turn uncertainty into a verified fix.
The compact view derives current gaps and their latest applicable dispositions;
a replaced claim does not inherit an older closure. Changed disposition inputs
remain visible for judgment. Evidence counts replace payloads in `status --gaps`;
use `inspect --gaps` with a subsystem or finding filter for the evidence.
