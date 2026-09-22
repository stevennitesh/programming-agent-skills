# Optional visual atlas

Use the atlas only when the user requests a visual system map, maintained audit
coverage, or continuation of an existing managed atlas. Focused findings do not
require it.

The helper is [atlas.py](../scripts/atlas.py). Use its current `--help` and
subcommand help for command syntax rather than relying on copied recipes.

## Ownership

The agent owns semantic judgment:

- system and subsystem boundaries;
- ownership and dependency meaning;
- evidence and counterevidence;
- finding classification, consequence, confidence, and recommendation; and
- whether audit coverage is focused, comprehensive, or incomplete.

The helper owns mechanical state such as record IDs, path expansion, overlap
checks, source fingerprints, update history, escaping, rendering, coverage
bookkeeping, and atomic publication.

Do not hand-edit generated HTML, record IDs, fingerprints, or canonical helper
state. Do not copy the entire report state into model context when targeted helper
inspection is sufficient.

A structural map does not establish audit coverage. The helper can enforce
bookkeeping; it cannot decide whether the inspected evidence is semantically
adequate.

## Use the helper as the state boundary

Inspect existing atlas state before changing it. Prepare records through the
helper, edit only the semantic judgment fields it exposes, and apply changes back
through the helper.

Directory structure or path membership does not establish semantic ownership.
Shared infrastructure needs an explicit owner and evidenced consumers.

Prepare against current source state. If the helper reports source or report
drift, re-examine the affected evidence and prepare the record again rather than
carrying old judgments onto new fingerprints.

Refreshing inventory or source fingerprints updates mechanical freshness only. It
does not revalidate a finding, clear an evidence gap, or prove that a changed
source still supports the previous judgment.

After an uncertain helper write, inspect actual atlas state before retrying. Do not
bypass helper validation or remove a writer lock without establishing that no
writer still owns it.

## Findings and coverage

Use the audit skill's semantic dispositions—`defect`, `opportunity`, `retain`,
and `gap`—and preserve the scenario, evidence, consequence, counterevidence, and
direction needed to judge each recorded finding.

Keep one causal finding rather than duplicating it under every affected subsystem.
Name additional affected owners in its evidence or direction.

A focused assessment needs only the flows, evidence, and limits relevant to its
scope.

For a claimed comprehensive atlas, account for every configured coverage lens as
examined, excluded with an evidence-based reason, or a gap. Pending or unexplained
coverage prevents a comprehensive claim. The helper's completed ledger is
necessary bookkeeping, not proof that the investigation itself was sufficient.

A map without an audit assessment remains a map, not an audited codebase.

## Retention and migration

Keep an atlas outside repository scratch only when the user or repository has
chosen a durable archival destination. Creating or updating an atlas does not
authorize commits or publication elsewhere.

Do not continue an incompatible legacy report schema in place. Preserve the
original, start a current atlas, and revalidate legacy evidence before carrying
forward current judgments.
