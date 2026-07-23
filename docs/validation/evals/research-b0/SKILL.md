---
name: research
description: Research one bounded source-answerable question for a caller-owned decision or artifact. Use when primary or governing sources can support a cited repo-local Markdown note or no-write inline answer; exclude ordinary lookup, open surveys, diagnosis, prototypes, stakeholder gaps, and user-owned decisions.
---

# Research

Answer one bounded question with inspected claim-owning evidence. Research owns
source legwork, evidence judgment, one answer, and one authorized note or a
no-write result. The caller owns the supported decision or artifact, its state,
and the next transition.

## Admission And Lock

Before source work, lock:

- the question and supported caller use;
- scope and exclusions;
- applicable date, version, jurisdiction, or repository fixed point;
- note authority as one exact repo-local path, delegated repo convention
  choice, or `none`;
- write authority as `create`, `update`, or `none`; and
- the return owner.

Infer obvious fields for a direct request. A caller need only supply its owned
facts; Research chooses evidence depth and source strategy. Preserve stricter
source, access, assurance, or budget constraints.

Admit only one question whose answer can materially come from inspectable
sources under those bounds. Otherwise return `Status: not-admitted`, all failed
or missing predicates, settled fields, the actual need shape, available
evidence, `Tracked mutation: none`, and the return owner without researching or
writing. A direct return may name one existing owner only for a deterministic
match. A caller return makes no route choice.

## Evidence

Decompose the answer into load-bearing claims. For each claim, inspect the
source that owns it in the applicable state: repository source, tests,
configuration, governing documentation, or decisions; versioned official
documentation, specifications, tagged source, or release notes; an issuing
body's applicable text; original study, data, and method; or a
methodologically relevant synthesis for an aggregate claim. Secondary sources,
snippets, indexes, and summaries are discovery only unless they own the exact
synthesis claim.

For every load-bearing claim, record:

- `supported`, `conflicted`, or `unknown`;
- owning source and direct citation;
- applicable date, version, jurisdiction, fixed point, population, or method;
- material counterevidence;
- labeled inference and cited premises, when applicable; and
- answer impact and limits.

Judge authority and applicability before prestige, count, or nominal recency.
Search for evidence that could falsify or narrow the proposed answer. Reconcile
differences in scope; preserve applicable conflict and exact unknowns.

Stop only when every load-bearing claim is classified, the best known
applicable owner was inspected or its access failure recorded, material
counterevidence and limits are explicit, and another bounded lane repeats the
evidence or cannot close a named gap. A supplied time or source budget may end
search but cannot convert an unknown into support.

## Output

When one note is authorized, create or update only that Markdown file. If path
choice was delegated, use the repository convention or
`docs/research/<slug>.md`. If publication requires another tracked mutation,
return the publication blocker instead.

The note proportionally identifies the question, research status, caller use,
scope, freshness, answer with adjacent citations, conflicts, unknowns, limits,
source identities and authority, stopping basis, caller-use boundary, and
return owner. Omit empty conditional material. A `conflicted` or `blocked` note
is durable evidence, not a settled answer.

Without note authority, return the same applicable evidence inline and make no
tracked mutation.

## Verify And Return

Before Return, verify every load-bearing claim against the inspected cited
source for identity, entailment, authority, and applicability. Confirm the
research status follows the claims:

- `answered`: every load-bearing claim is supported;
- `conflicted`: applicable evidence materially conflicts and no more
  fundamental claim is unknown; or
- `blocked`: a load-bearing claim remains unknown because required evidence,
  access, freshness, applicability, or authority is insufficient.

For a note, reread the file, confirm it is the authorized path, and prove this
run changed only that note. Otherwise prove tracked mutation is `none`.
Compare starting and ending work state, preserve pre-existing work, and remove
or report disposable captures.

Return exactly one `answered`, `conflicted`, `blocked`, or pre-research
`not-admitted` packet. Include the question, answer or exact evidence boundary,
direct citations or absolute note path, freshness, material limits, stopping
basis, mutation result, caller-use boundary, and return owner. A blocker also
includes attempted lanes and an observable unblock condition.

Return to the caller without deciding its artifact, changing its state, or
starting downstream work. A complete standalone answer ends with `Next: none`.
Completion requires the locked contract, classified claims, bounded stopping,
verified citations and status, one authorized note or no tracked mutation, a
complete Return, and no caller-owned continuation.
