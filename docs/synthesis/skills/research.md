# Research Evidence And Runtime Design Synthesis

Status: promoted in the 2026-07-23 Deploy Campaign. This synthesis records the
current decision and concise decision-changing history; it is not an executable
contract.

Runtime authority lives in `skills/custom/research/`, each target repository's
source and note conventions, caller-owned decision and transition contracts,
and `docs/synthesis/skill-context-relationships.md`.

## Promoted Identity

The canonical Research package contains only `SKILL.md` and
`agents/openai.yaml`. Its tree hash is:

`0961494db521e812540fb36052a1efdd60f22958d1e6e0ba40115ec47da9334f`

The package is byte-identical to the frozen source-derived B0 and final
behavior-complete C1. It replaced canonical tree
`ae255d2b12e88bfa8882c7c5c00116b0267df3fa88345b75819bf95112c477b2`.
The campaign shape is `pruning-only`: current differed, while `B0 = C1`.

## Runtime Decision

Research answers one bounded, source-answerable question with inspected,
claim-owning citations for one caller-owned decision or artifact. Research
owns source legwork, evidence judgment, one answer, and either one authorized
repo-local Markdown note or a no-write inline result. The caller owns the
supported decision or artifact, its state, consequences, and next transition.

The promoted minimum has six semantic units:

| Unit | Canonical behavior |
| --- | --- |
| `B0-1` | Admit and lock one question, supported use, scope, applicability, note and write authority, and return owner before source work; return typed `not-admitted` for a capability mismatch. |
| `B0-2` | Inspect the source that owns each load-bearing claim in its applicable state; non-owning secondary material is discovery only. |
| `B0-3` | Classify claims as `supported`, `conflicted`, or `unknown`; preserve applicability, counterevidence, inference, limits, and claim-driven bounded stopping. |
| `B0-4` | Create or update exactly one authorized Markdown note, or make no tracked mutation; return a blocker when publication requires a second tracked change. |
| `B0-5` | Return exactly one `answered`, `conflicted`, `blocked`, or pre-research `not-admitted` packet while preserving caller custody and standalone `Next: none`. |
| `B0-6` | Verify citation identity, entailment, authority, applicability, terminal status, output identity, mutation containment, and packet completeness before Return. |

Research remains narrowly implicitly invocable. Its description admits one
bounded primary- or governing-source question for a caller-owned use and
excludes ordinary lookup, open surveys, diagnosis, prototypes, stakeholder
gaps, and user-owned decisions.

## Relationship Surface

Relationship delta: none.

| Caller | Relationship and retained boundary |
| --- | --- |
| Skill Router, Grilling, To Questionnaire | Recommend Research and stop; they do not copy or run its procedure. |
| Wayfinder | Invokes one bounded AFK Research note and retains map or ticket state and the next transition. |
| Improve Codebase | Invokes one source gap, normally with note authority `none`, and reclassifies its candidate after Return. |
| Direct user | Invokes one admitted question or receives typed non-admission; a complete standalone answer ends `Next: none`. |

Research returns to its caller without deciding the caller's artifact, changing
caller state, or starting downstream work. No caller, relationship index, or
other skill changed in this campaign.

## Source And Candidate Decisions

The source-first checkpoint remains:

`sha256:ade1f6170d62974fcf1730a720479ce03d7d8d1aaaca635e937f2c1acf4d8ae6`

It froze the viability floor before current runtime or historical evaluation
was used as a baseline.

| Source pressure | Frozen identity | Decision |
| --- | --- | --- |
| Matt Pocock Research | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | Adapt evidence-before-claims, claim-owning source legwork, and completion pressure; its narrower note-only contract was insufficient for local B0. |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99` | No current Research baseline; qualified parallel investigation admitted only the bounded Scout hypothesis. |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` | No current Research baseline. |
| Upper-Bound Language | Prompt 2 frozen rows | Design pressure only; it did not prove local fit or behavioral efficacy. |

Prompt 3 constructed B0 without using current-minus-cuts derivation. Its only
beyond-minimum candidate was `C1-1 Compact Scout`: fresh read-only scouts for
substantial disjoint source lanes, with root Research retaining evidence
judgment, citation verification, writing, and Return.

Prompt 4 rejected Scout as `rejected-no-control-failure`. Five exact serial B0
samples found all seeded counterevidence, preserved correct semantics, and had
zero critical failures. Elapsed-time and token telemetry were unavailable, so
no efficiency benefit could be inferred and no C1 arm ran. The provisional C1
tree `74253beba2ef648fbfb67fcebf001281720b964d54d4f0a967b1183b0a731288`
was reduced to exact B0.

The D0 claim-ownership and judgment/stopping controls also passed 5/5 without
the tested steering. Those results deny behavioral-efficacy credit but do not
remove independently required source-authority, conflict, unknown, status, and
completion obligations.

The Pruning Pass classified all 18 instruction-bearing passages `keep`.
Disposition: `pruning-not-needed`. No collapse, disclosure, or deletion lowered
a named runtime load without risking a protected authority, evidence, mutation,
Return, or completion obligation. Final C1 remained byte-identical to B0.

## Proof And Evidence Disposition

| Evidence | Disposition |
| --- | --- |
| Prompt 4 B0, D0, invocation, terminal, containment-decision, and Scout-control samples | `exact-reusable` for the exact promoted bytes, fixed packets, worker class, runtime, tools, authority, evidence, and rubrics recorded in the behavior evaluation. |
| Prompt 4 V5 and V9 note-action decisions | Exact for the recorded action decisions; not live host filesystem proof. |
| Structural and relationship checks | `lane-limited` to their machine contracts and owner continuity. |
| Earlier Research candidates and evaluations | `historical-admission-only`; they do not prove the promoted package. |
| Live network/provider behavior, actual host note write/reread, elapsed/token/backend telemetry, and host automatic-selection instrumentation | `missing` or unavailable as named below; no inference was made. |

Current-epoch proof records:

- [B0/C1 construction evidence](../../validation/transcripts/2026-07-23-research-b0-c1-construction-evidence.md)
- [Prompt 4 behavior evaluation](../../validation/transcripts/2026-07-23-research-behavior-eval.md)
- [Pruning Pass](../../validation/transcripts/2026-07-23-research-pruning.md)
- [Promotion and installation](../../validation/transcripts/2026-07-23-research-promotion-install.md)
- [Frozen B0 package](../../validation/evals/research-b0/)

## Deliberate Non-Changes

- No Scout, fixed agent width, consensus, summary schema, or parallel-economics
  instruction was promoted.
- No assurance taxonomy, fixed source count, numeric confidence, complete
  search log, source catalog, citation helper, cache, database, sidecar,
  auto-refresh, or provider-specific procedure was added.
- No support file, helper, note template, index, caller packet migration, or
  relationship change was needed.
- Claim statuses remain distinct from terminal research statuses.
- Exactly one tracked note remains the maximum durable mutation; note authority
  `none` remains a no-write branch.
- The root remains the evidence judge and note author; callers retain decisions,
  artifacts, tracker state, consequences, and transitions.
- Frozen B0 and campaign transcripts remain durable evidence rather than
  runtime instructions.

## Residual Gaps

Residual evidence limits are:

- live network and provider behavior;
- actual host note create/update, reread, dirty-work containment, and
  second-file recovery;
- exact backend model build, reasoning setting, elapsed agent-controlled time,
  and token telemetry;
- host-level automatic invocation instrumentation beyond fresh-context
  classification; and
- generalization beyond the fixed packets, worker class, and recorded runtime.

These limits do not contradict the exact accepted candidate. They bound the
claims: fixed-packet behavioral evidence proves only its recorded lanes, while
canonical tests, validation, installation parity, and hashes prove package and
machine-contract integration.

## Concise History

An earlier 2026-07-21 campaign explored a broader runtime with assurance tiers,
expanded source roles, optional scouts, and supporting machinery. Its behavior
records remain useful for fixture discovery but are not authority for this
source-first epoch. The 2026-07-23 campaign rebuilt the minimum from the frozen
source checkpoint, admitted only Compact Scout beyond B0, rejected it when the
serial control did not fail, found no safe pruning delta, and promoted the
resulting exact minimum.
