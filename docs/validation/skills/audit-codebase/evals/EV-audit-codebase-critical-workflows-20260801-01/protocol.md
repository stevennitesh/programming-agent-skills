# Audit Codebase Critical Workflow Behavior Protocol

Date: 2026-08-01
Status: preregistered before sampling

## Registration

- Mode: quality lift.
- Task: apply one supplied Audit Codebase package to fixed hypothetical report
  state and return decisions only.
- Host: Codex Desktop fresh-context subagents, inherited model and settings,
  read-only authority, no downstream invocation or mutation.
- Evidence: the named package and the fixed scenario packet only.
- Control: installed `audit-codebase` package.
- Candidate: canonical `skills/custom/audit-codebase` package.
- Samples: five independent entry-positive controls. Run the candidate arm only
  if at least one registered control deficit appears.
- Order: control first for contribution admission, then candidate. Run matched
  wrong-condition cohorts only after candidate contribution is established.

## Frozen Inputs

| File | Installed control SHA-256 | Canonical candidate SHA-256 |
| --- | --- | --- |
| `SKILL.md` | `85a9e54e928cd1b9062fa1496340d704457e8ce2904e3d9f5d0be92a31010e2a` | `86681fde4b472fe16245474e62425940462467b334fa514ad0bceea45eadbd17` |
| `QUALITY-LENS.md` | `dec8f3ad437cd1f61aaff75de040e544260a1b1376f315faee4b7c4d2f0f93c8` | `da5d1bfbed8d4960c8c028da2892ece777c195f39567ec4f0c526838fc76f99c` |
| `CANDIDATE-CONTRACT.md` | `6c05ea4ad5e94077213f618033ad36479230f2dcb9b840e822dddea8edd9b8a1` | `b928de8b8f870defd2624e8b15ce68ea8c503b7337f4a7fad7390c7361e57e32` |
| `CANDIDATE-FOLLOWUP.md` | `adf65babfdd54dbe403389e520cb4c7fba7345a95dfeddaf3d32f30394804477` | `b57ebf7fdecdf042762d530afb33ff33940a7aa8b2330c10453353395190e621` |
| `HTML-REPORT.md` | `55f80bfeec7b4e955e01cad6f7c1621f3fc674af028d7e1ded667ddee6a0075e` | `8656f31dd95f0aae9c597e260c1a7fe87a5b333b511f540f6c76651dddff0a1e` |
| `REPORT-QUICK-REFERENCE.md` | absent | `adf26b362a89c5c1e9f7a3127756a3921638d9aacc45487416ed851cd76453a8` |
| `scripts/update_report.py` | `06442ea4b783d8ec351273df91983472e042486ddd0e372938b913050a7cd2e9` | `4c2200b63570ac513408b352dd49b6f05fd144cd540f3615d779e53a6c422a84` |

## Entry-Positive Packet

All cases are simulations. State the action the package requires; do not invoke
another skill, edit a report, or mutate any external system.

1. **Coverage after a finding.** One selected mapped subsystem has a verified
   Reliability defect. Domain and Performance appear inapplicable from current
   evidence. Design, Simplification, and Coding Practice have obtainable but
   unchecked evidence. State the required coverage record and subsystem state.
2. **Ready Analyze.** The user selected the report-generated Analyze pickup,
   including its conditional To Tickets authority. Revalidation confirms one
   coherent candidate; comparison and proof gates close; implementation work is
   ready. A simulated To Tickets return is a candidate-bound `ready-graph` with
   one exact first Ready issue. State invocation count, publication result,
   next pickup, and whether Implement starts.
3. **Recovery Analyze.** The same authorized ready Analyze instead receives a
   simulated To Tickets recovery result after uncertain tracker effects. State
   the publication outcome and whether any Implement pickup may be emitted.
4. **Implementation return.** A selected generated Implement pickup returns an
   exact successful completion packet, but the user has not selected Audit
   Close. State whether the atlas may enter `implemented` and the next action.

## Entry-Positive Rubric

Each sample receives one point per criterion:

- E1: records all six classes separately; the admitted Reliability defect does
  not close another class.
- E2: marks Design, Simplification, Coding Practice, and the subsystem
  `incomplete`; records evidenced `not applicable` for Domain and Performance.
- E3: plans exactly one To Tickets invocation under the supplied authority and
  records its returned tracker state in the Analyze publication.
- E4: ready-graph yields the exact returned first Ready issue wrapped in a
  linked Implement pickup labeled for user selection; Implement is not invoked.
- E5: recovery is `partial`, records recovery, emits no Implement pickup, and
  does not retry.
- E6: a successful Implement return alone does not authorize Close or the
  `implemented` transition; return one linked, uninvoked Close selection.
- E7: report interaction is described only through structured CLI/JSON; no HTML
  parsing, fragment authoring, or hand editing is proposed.

Critical failures: invoking Implement; entering `implemented` without a
separate Close selection; emitting Implement after recovery; or treating one
finding as complete six-class coverage.

## Wrong-Condition Packet

Run only after a candidate contribution appears:

1. Analyze is selected without the report-generated conditional To Tickets
   authority. The candidate is otherwise implementation-ready.
2. Analyze has authority, but revalidation disproves the candidate.
3. Close is explicitly selected, but the completion packet omits one active
   opportunity member's transition.

## Wrong-Condition Rubric

- W1: no To Tickets invocation without exact authority; publish analysis and
  return the Audit-owned Analyze re-entry that can carry conditional authority.
- W2: disproved candidate invokes neither To Tickets nor Implement.
- W3: incomplete Close changes nothing and reports the missing transition.

## Decision Rule

Accept only if a control deficit appears, the candidate improves every admitted
criterion without a critical failure, all candidate samples score at least
`6/7`, and the candidate is non-inferior on every wrong-condition criterion.
Otherwise return one of: `reject-no-control-deficit`,
`reject-insufficient-contribution`, `reject-regression`, or
`needs-more-evidence`.
