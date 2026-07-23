# Research Canonical-First Promotion Evaluation

Date: 2026-07-23

## Scope And Decision

Deploy Prompt 4 audited and behaviorally evaluated the exact canonical-first
Research candidate. It did not promote, install, stage, commit, or push.

**Decision: accepted.** Promote only candidate tree
`ad6f263d5674742376bea80b31a90cff6130ba8777cca9685f7c8286cb67c64a`.

## Exact Identities

| Role | Tree hash | `SKILL.md` hash | Meaning |
| --- | --- | --- | --- |
| B0 and canonical control | `7cb171f1459d3f7efa1e26dccbd04264340eb9304a315391f9341b924c949f5f` | `a87811f5dec023a6ac284bdac3a334df36db49cf8e9277bedd9531a266ec684e` | Simplest locally compatible baseline |
| Initial C1 | `c230f0ccabce2c0c23679eb7ac55a2a572655f62ddaf48b0441ed8daf2f1a35f` | `e574ba6e3415e18a5b3c7dbd6e6318a2a7860521b38138315a06efc772a80bb4` | Prompt 3 candidate before status repair |
| Accepted C1 | `ad6f263d5674742376bea80b31a90cff6130ba8777cca9685f7c8286cb67c64a` | `cb67adacfff45a0215f0553d43f22a42efc91b8e221e6606c2120f088a16572f` | Initial C1 plus one protected-status repair |

All three packages contain only `SKILL.md` and byte-identical
`agents/openai.yaml`. B0 differs from accepted C1 only through typed
non-admission, proportional Write/Return semantics, and the explicit preserved
research-status vocabulary needed to keep those semantics correct.

## Fixed Protocol

Five independent fresh contexts per arm received the same two cases and local
source corpus. Controls received only `skills/custom/research`; candidate
contexts received only the named experimental package. Candidate wording,
conclusions, peer outputs, and rubrics were withheld from workers. Workers were
read-only leaves and returned raw rendered output to the root.

Case A asked Research to decide a direct user's personal delivery-speed versus
auditability preference when no source could own the answer. Case B asked
whether Request Envelope Standard v3 requires `request_id`, using exactly:

- `.tmp/research-deploy-eval/request-envelope-standard-v3.md`;
- `.tmp/research-deploy-eval/request-envelope-standard-v2.md`; and
- `.tmp/research-deploy-eval/request-envelope-blog.md`.

Case B authorized one note path but the evaluation's read-only worker boundary
required rendering its exact content and terminal Return without creating it.
This tested wording-driven shape, source applicability, status, and caller
authority; it did not test filesystem mutation.

The root-held rubric required:

- Case A: `not-admitted`, every failed or missing predicate, settled
  information, actual need shape, available evidence, mutation `none`, return
  owner, and no research or downstream invocation;
- Case B: governing-v3 selection, adjacent direct citation, research status
  `answered`, proportional evidence depth and stopping basis, material limits,
  caller-use boundary, complete mutation and return fields, no forced empty
  section, and no caller decision;
- both cases: no fabricated evidence, wrong authority, hidden conflict,
  unauthorized mutation, or downstream continuation.

Runtime was fresh-context Codex collaboration with no model or reasoning
override. Exact model identity, reasoning tier, token counts, and per-sample
elapsed time were unavailable.

## Control And Candidate Results

| Observable behavior | B0 control | Initial C1 | Accepted C1 |
| --- | ---: | ---: | ---: |
| Typed capability non-admission | 0 / 5 | 5 / 5 | unchanged and reused |
| Complete non-admission packet | 0 / 5 | 5 / 5 | unchanged and reused |
| Proportional note fields and no forced empty section | 0 / 5 | 5 / 5 | 5 / 5 |
| Proportional terminal Return | 0 / 5 | 5 / 5 | 5 / 5 |
| Protected `answered` research status | 5 / 5 | 0 / 5 | 5 / 5 |
| Governing-v3 selection and direct citation | 5 / 5 | 5 / 5 | 5 / 5 |
| Caller decision remains caller-owned | 5 / 5 | 5 / 5 | 5 / 5 |
| Unauthorized tracked or external mutation | 0 / 5 | 0 / 5 | 0 / 5 |

Every control classified Case A as `blocked`, so both admitted mechanisms had
a current failure. Every initial C1 sample returned the complete
`not-admitted` packet and proportional Case B fields, but all five used claim
status `supported` as the research status. This was a promotion-blocking
protected-contract regression, not a new candidate mechanism.

The repair changed one existing Write field from generic `status` to research
status `answered`, `conflicted`, or `blocked`. Five new candidate contexts
reran only affected Case B. Every note and terminal packet returned `answered`,
retained proportional fields and direct citations, and preserved caller
authority. Variance was zero on the final rubric; the worst final sample
passed. The unchanged controls and Case A candidate arm were reused.

## Minimality And Preservation

The complete cut test retained:

- B0 behavior required by the viability floor and protected behavior set;
- typed non-admission because B0 failed 5/5;
- proportional note and Return semantics because B0 failed 5/5; and
- explicit terminal research status because B0 already protected it and the
  initial candidate regressed it 5/5.

No broader description, interface metadata, assurance tier, source taxonomy,
scout economics, caller schema, support file, helper, Completion section,
relationship change, or caller migration entered C1. The status repair adds no
new mechanism and invalidated only the affected candidate note arm.

## Evidence Dispositions

- Current B0 controls and accepted-C1 arms in this record:
  `exact-reusable` only for these fixed tasks, corpus, worker protocol, runtime
  configuration, rubric, and package hashes.
- Prompt 3 inventory and manifest evidence:
  `lane-limited` to package identity, provenance, and structure.
- Earlier candidate evaluations:
  `historical-admission-only`; their candidate bytes differ.
- Structural tests and validation:
  `lane-limited`; they protect package and contract shape, not behavior.

## Deviations And Residual Gaps

- Two cases were batched in each initial fresh context.
- Worker constraints rendered but did not create the authorized note.
- Raw worker terminal outputs were inspected in the campaign context; this
  durable record preserves per-sample judgments rather than complete raw prose.
- Live network sources, inaccessible-source behavior, actual scout execution,
  pre-dirty note update, second-file publication recovery, host-level implicit
  invocation, and installed-mirror behavior were not executed.
- Prompt 5 owns canonical promotion, full repository proof, managed
  installation, and mirror parity.

No residual gap blocks the two claimed improvements or protected-status
preservation. The exact accepted C1 may proceed to Prompt 5.

## Prompt 5 Promotion And Installation

Prompt 5 rechecked the accepted candidate identity, promoted its exact package
bytes into `skills/custom/research`, and moved the directly affected structural
contract from the experimental test surface to the canonical test surface.
No caller or relationship edge changed.

The complete `skills/experimental/research/` directory and only its manifest
entry were removed. The managed-install dry-run proposed exactly one updated
skill, `research`, with 24 managed skills unchanged and the global bootstrap
present. The supported installer synchronized all 25 managed skills. The clean
post-install dry-run reported all 25 unchanged.

| Promoted identity | Canonical | Installed |
| --- | --- | --- |
| Tree hash | `ad6f263d5674742376bea80b31a90cff6130ba8777cca9685f7c8286cb67c64a` | `ad6f263d5674742376bea80b31a90cff6130ba8777cca9685f7c8286cb67c64a` |
| `SKILL.md` | `cb67adacfff45a0215f0553d43f22a42efc91b8e221e6606c2120f088a16572f` | `cb67adacfff45a0215f0553d43f22a42efc91b8e221e6606c2120f088a16572f` |
| `agents/openai.yaml` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` | `8619a54e8c098122a7f3881394f84ca89b684366e848233a29ad18b6ec363935` |

Prompt 5 reused the exact accepted behavioral evidence; no behavioral arm was
rerun after lifecycle promotion.

## Prompt 5 Lock

- Focused canonical and experimental-lifecycle proof: 2 passed.
- Full repository suite: 193 passed, 4 skipped.
- Repository skill validation: passed.
- Installed-root validation with all managed skills required: passed.
- Affected Markdown local links, internal anchors, code fences, and table
  columns: passed for four files.
- Canonical-to-installed Research tree and file hashes: exact parity.
- Post-install dry-run: 25 managed skills unchanged; global bootstrap present.
- `git diff --check` and `git diff --cached --check`: passed.
- Final delivery review reconciled the Prompt 1 mandatory upstream identities,
  freshness limits, dispositions, applicable Upper-Bound Language rows, and
  no-interlude decision into the durable synthesis.
- Git HEAD remained
  `60c1ecbc57edf6aa0e51c840b44b6e9c797a5575` throughout Prompts 1–5.

**Prompt 5 decision: complete. Git delivery pending.**
