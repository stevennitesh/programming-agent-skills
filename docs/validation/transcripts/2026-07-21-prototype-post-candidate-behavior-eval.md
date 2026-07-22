# Prototype Post-Candidate Behavior Evaluation

Date: 2026-07-21

## Decision

**Accept the repaired experimental candidate** at tree hash
`eb6d161906b02c0e8d8a63eabde589bf47d261d46471d52c912a48df281af171`.
The final sampled behavior had no critical failure. Acceptance is not promotion;
the canonical skill, installed mirror, and active callers remain unchanged.

## Authority And Prior Control

This run is the Deploy Prompt 4 post-candidate evaluation. It did not repeat
Control Lock. The admitted control failures remain recorded in
[`2026-07-21-prototype-candidate-behavior-eval.md`](2026-07-21-prototype-candidate-behavior-eval.md):
the active control at tree hash
`ecba1e84f0e0df9a0b32b2febdac4e1d7f096dcbf468f9c054c0d5bf7d95a3ef`
scored 1/25 across admission and Freeze, branch evidence, judgment and custody,
reconciliation and Resume, and caller return. The earlier candidate accepted by
that counterfactual was superseded by confirmed vocabulary and leaf-return
decisions.

## Fixed Runtime And Sampling

- Runtime: Codex desktop fresh-context direct collaboration agents.
- Context: `fork_turns="none"`; no model or reasoning override.
- Authority: read-only; no sample could edit files, execute a probe, invoke a
  downstream skill, or spawn another agent.
- Candidate package: only `skills/experimental/prototype/` and the files named
  by each wave.
- Exclusions: canonical skill, synthesis, tests, manifest, prior evaluations,
  and peer results.
- Telemetry unavailable: exact model identifier, reasoning mode, token counts,
  and per-sample wall-clock time.
- Judgment: the root inspected every output against the frozen behavior rubric.

Five independent contexts ran in every counted wave. Multi-case samples were
explicitly independent within one context. When sequential-case interference
appeared, the affected behavior was repaired and rerun with literal identities
and subjects.

## Invocation Precision Wave

Each of five metadata-only contexts read the candidate frontmatter and
`allow_implicit_invocation` policy, not the procedure body. Each judged three
positive requests and six adjacent negatives without an explicit skill handle.

| Request family | Result |
| --- | ---: |
| Logic bounded runnable comparison | 5 / 5 invoke |
| UI structurally different bets | 5 / 5 invoke |
| Predeclared comparative Measure | 5 / 5 invoke |
| Production implementation | 5 / 5 reject |
| Uncertain defect diagnosis | 5 / 5 reject |
| Source research | 5 / 5 reject |
| Multi-decision design | 5 / 5 reject |
| Ordinary one-number measurement | 5 / 5 reject |
| Incidental `Prototype` naming | 5 / 5 reject |
| **Total** | **45 / 45** |

Variance was zero; every sample scored 9/9. The closest boundary was ordinary
measurement, which every sample rejected because it lacked a comparative
design question and predeclared rule. The evaluated metadata and policy bytes
were unchanged by the later body repairs.

This is a fresh-context metadata routing simulation, not proof that the host
platform will auto-discover an inactive experimental package. Platform-level
implicit invocation remains promotion-time integration evidence.

## Audit And Repair Generations

### Generation 0: extracted candidate

Tree hash:
`6769619415116126a007d96811558b9d456520de77d38eb7c8470a8f92eeef3b`

Five full-package contexts exercised direct and caller non-admission, invalid
claim/judgment pairing, Measure, human custody, blocked Resume, answered caller
return, and diagnosis rejection. The wave preserved non-admission, branch,
Measure, production-proof, and leaf-return behavior. It also exposed two
omissions:

- all 5/5 rejected blocked-Resume cases returned `blocked` packets padded with
  absent or placeholder admitted-only question fields;
- one sample inferred the human judge as `decision_owner`, while the other
  samples proceeded without a named decision owner.

The candidate was repaired to make invalid Resume return `not-admitted` without
artifact inspection and to make decision owner, human judge, and artifact
custodian independent required roles.

### Generation 1: Resume and owner repair

Tree hash:
`52b9016f5dd3bada1d17b130e727c865423a5f00e7e06ea58f4a729f674156e1`

Five fresh contexts exercised six cases.

| Case | Result |
| --- | ---: |
| Blocked Resume returns `not-admitted` without artifact inspection | 5 / 5 |
| Missing decision owner blocks before mutation | 5 / 5 |
| Distinct Alex decision owner and Priya human judge reach awaiting verdict | 5 / 5 |
| Measure applies the frozen rule and limits its claim | 5 / 5 |
| TDD diagnosis returns locally without mutation | 5 / 5 |
| Improve Codebase answered packet retains current caller identity | 3 / 5 |

Two samples carried the immediately preceding TDD invoker and return owner into
the Improve Codebase packet. Two samples also described the rejected packet's
subject where the current Resume request subject was not literal in the
fixture. The repair added a Return-time current-invocation identity read-back
and made the Resume subject distinction explicit.

### Generation 2: final identity repair

Tree hash:
`eb6d161906b02c0e8d8a63eabde589bf47d261d46471d52c912a48df281af171`

Five fresh contexts received three sequential cases with deliberately distinct
literal identities and subjects:

1. current direct request `Resume blocked packet R7`, while the rejected packet
   carried old subject `Compare cache A/B`;
2. TDD request `Find cause of intermittent timeout T9`;
3. immediately following Improve Codebase request
   `Choose API shape for Candidate 12`, with decision owner Casey.

| Behavior | Result |
| --- | ---: |
| Current Resume subject preserved; old packet subject excluded | 5 / 5 |
| Invalid Resume returns `not-admitted`; artifact untouched | 5 / 5 |
| TDD diagnosis returns `not-admitted` to TDD | 5 / 5 |
| Improve Codebase packet retains Improve Codebase identity | 5 / 5 |
| Casey remains decision owner; verdict X remains design evidence | 5 / 5 |
| **Terminal packets** | **15 / 15** |
| **Critical failures** | **0 / 5 samples** |

Variance was zero and the worst final sample scored 3/3 terminal packets. No
sample selected or started a downstream route, claimed production correctness,
inspected a blocked artifact, or substituted human and decision authority.

## Acceptance Basis

The final identity generation changed only Return and rejected-Resume identity
wording. Deterministic diff and hash checks establish that the invocation
metadata, branch files, artifact procedure, judgment matrix, and Measure rules
tested in earlier waves were unchanged. The combined current evidence therefore
supports:

- narrow metadata invocation recall and adjacent-negative precision;
- direct and caller-owned non-admission without Router delegation;
- separate claim level, judgment mode, decision owner, human judge, and custody;
- truthful invalid-Resume status and packet shape;
- Measure verdict and production-proof limits;
- distinct sequential caller identity at Return.

## Structural Proof

- Experimental and validator tests: 27 passed, 1 skipped.
- Focused pack contracts: 60 passed.
- Full repository suite: 191 passed, 4 skipped.
- `python -m scripts.validate_skills`: passed after concurrent unrelated
  experimental work completed its manifest entry.
- Prototype candidate hash matches the experimental manifest:
  `eb6d161906b02c0e8d8a63eabde589bf47d261d46471d52c912a48df281af171`.
- Directly affected Wayfinder candidate hash matches the manifest:
  `00d52ec91fc001837eed728e21d7bdad5a8729fc847507c908ade168a6e0bedb`.
- `git diff --check` and `git diff --cached --check`: clean.

## Deviations And Residual Gaps

- Samples were read-only behavioral simulations, not live Logic, UI, or Measure
  probes.
- Filesystem restore, process termination, port release, browser isolation,
  measurement validity, and dirty-work preservation were not executed.
- Metadata routing was simulated because an inactive experimental package is
  not a host-discoverable installed skill.
- Canonical caller migration, full canonical proof, installer behavior, and
  installed parity belong to coordinated promotion and were not run.
- Exact model, reasoning, token, and timing telemetry was unavailable.

These gaps do not reject the experimental wording. They remain explicit
promotion proof and prevent this record from claiming canonical or installed
acceptance.
