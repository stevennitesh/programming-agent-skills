# Fresh Composition Epoch migration control

Status: active control; 241 migration row(s) verified.

This durable `.scratch/` control implements issue #41 and remains temporary
cross-ticket execution state. It is not research, synthesis, validation, or
runtime authority. The complete private inventory remains only in the ignored
sidecar at `.tmp/fresh-composition-epoch/migration-ledger-private.json`; this tracked closeout deliberately
publishes no private source locators.

## Fixed point

- Source Git HEAD: `2397586d4bbb0774d9b479ccff9f8a5640df705e`
- Public inventory fingerprint: `sha256-v1:142696879766074cb49dd023ed738d20887fe0b8b6fef3e74a20c06c71d3e122`
- Private inventory fingerprint: `sha256-v1:ea2a555b40dfca4e3690c56b14975029425a6e71d7edec314eec8e3cb997ce5e`
- Public rows: 479
- Private/local rows: 70
- Public migration dispositions: `move` 158, `owner-gap` 6, `preserve-in-place` 315
- Private/local source states: `local-residue` 44, `private-ignored` 26
- Private/local terminal statuses: `blocked` 44, `verified` 26

## Verified migrations

- `MIG-0072` -> `docs/research/skills/to-spec/RP-to-spec-20260724-01.md`
- `MIG-0073` -> `None`
- `MIG-0074` -> `None`
- `MIG-0075` -> `None`
- `MIG-0076` -> `None`
- `MIG-0077` -> `docs/research/skills/convergent-pr-review/RP-convergent-pr-review-20260724-01.md`
- `MIG-0078` -> `docs/research/skills/implement/RP-implement-20260724-02.md`
- `MIG-0079` -> `docs/research/skills/implement/RP-implement-20260724-01.md`
- `MIG-0080` -> `None`
- `MIG-0081` -> `None`
- `MIG-0082` -> `None`
- `MIG-0083` -> `None`
- `MIG-0084` -> `None`
- `MIG-0085` -> `None`
- `MIG-0086` -> `docs/research/skill-pack-composition/sources/SRC-0002.md`
- `MIG-0087` -> `docs/research/skill-pack-composition/sources/SRC-0003.md`
- `MIG-0088` -> `docs/research/skill-pack-composition/sources/SRC-0004.md`
- `MIG-0089` -> `docs/research/skill-pack-composition/sources/SRC-0005.md`
- `MIG-0090` -> `docs/research/skill-pack-composition/sources/SRC-0006.md`
- `MIG-0091` -> `docs/research/skill-pack-composition/sources/SRC-0007.md`
- `MIG-0092` -> `None`
- `MIG-0093` -> `None`
- `MIG-0094` -> `None`
- `MIG-0095` -> `None`
- `MIG-0096` -> `None`
- `MIG-0097` -> `docs/research/skills/parallel-implement/RP-parallel-implement-20260724-02.md`
- `MIG-0098` -> `docs/research/skills/parallel-implement/RP-parallel-implement-20260724-01.md`
- `MIG-0099` -> `docs/research/skills/review/RP-review-20260724-01.md`
- `MIG-0100` -> `None`
- `MIG-0101` -> `docs/research/skills/implement/RP-implement-20260726-01.md`
- `MIG-0102` -> `docs/research/skills/implement/RP-implement-20260726-02.md`
- `MIG-0103` -> `docs/research/skills/to-spec/RP-to-spec-20260725-01.md`
- `MIG-0104` -> `docs/research/skills/to-tickets/RP-to-tickets-20260723-01.md`
- `MIG-0105` -> `None`
- `MIG-0106` -> `None`
- `MIG-0107` -> `docs/research/skill-pack-composition/sources/SRC-0001.md`
- `MIG-0108` -> `None`
- `MIG-0109` -> `None`
- `MIG-0110` -> `None`
- `MIG-0111` -> `docs/research/skills/to-tickets/RP-to-tickets-20260725-01.md`
- `MIG-0112` -> `docs/research/skills/writing-great-skills/RP-writing-great-skills-20260724-01.md`
- `MIG-0113` -> `None`
- `MIG-0114` -> `None`
- `MIG-0115` -> `None`
- `MIG-0116` -> `None`
- `MIG-0117` -> `None`
- `MIG-0118` -> `None`
- `MIG-0119` -> `None`
- `MIG-0120` -> `None`
- `MIG-0121` -> `None`
- `MIG-0122` -> `None`
- `MIG-0123` -> `None`
- `MIG-0124` -> `None`
- `MIG-0125` -> `None`
- `MIG-0126` -> `None`
- `MIG-0127` -> `None`
- `MIG-0128` -> `None`
- `MIG-0129` -> `None`
- `MIG-0130` -> `None`
- `MIG-0131` -> `None`
- `MIG-0132` -> `None`
- `MIG-0133` -> `None`
- `MIG-0134` -> `None`
- `MIG-0135` -> `None`
- `MIG-0136` -> `None`
- `MIG-0137` -> `None`
- `MIG-0138` -> `None`
- `MIG-0139` -> `None`
- `MIG-0140` -> `None`
- `MIG-0141` -> `None`
- `MIG-0142` -> `None`
- `MIG-0143` -> `None`
- `MIG-0144` -> `None`
- `MIG-0145` -> `None`
- `MIG-0146` -> `None`
- `MIG-0147` -> `None`
- `MIG-0148` -> `None`
- `MIG-0149` -> `None`
- `MIG-0150` -> `None`
- `MIG-0151` -> `None`
- `MIG-0152` -> `None`
- `MIG-0153` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/candidate.md`
- `MIG-0154` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/manifest.json`
- `MIG-0155` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/prompt1-m0.md`
- `MIG-0156` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/prompt2-h1.md`
- `MIG-0157` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/prompt3-build.md`
- `MIG-0158` -> `docs/validation/skills/to-spec/campaigns/to-spec-2026-07-25/prompt4-decision.md`
- `MIG-0159` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/candidate.md`
- `MIG-0160` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/manifest.json`
- `MIG-0161` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt1-m0.md`
- `MIG-0162` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt2-h1.md`
- `MIG-0163` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt3-build.md`
- `MIG-0164` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt4-decision.md`
- `MIG-0165` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt5-final.md`
- `MIG-0166` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/pruning.md`
- `MIG-0167` -> `docs/validation/skills/writing-great-skills/evals/EV-writing-great-skills-incumbent-reconciliation-20260724-01/results.md`
- `MIG-0168` -> `None`
- `MIG-0169` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/campaign-decision.json`
- `MIG-0170` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/fixtures/root-only-evaluation.json`
- `MIG-0171` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/fixtures/worker-visible.json`
- `MIG-0172` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/decision.md`
- `MIG-0173` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/fixtures/h1-03-root-only.json`
- `MIG-0174` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/fixtures/h1-03-worker-visible.json`
- `MIG-0175` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/fixtures/h1-05-root-only.json`
- `MIG-0176` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/fixtures/h1-05-worker-visible.json`
- `MIG-0177` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt4-20260724-01/reconciliation-entry-predicate/preregistration.md`
- `MIG-0179` -> `docs/validation/skills/implement/evals/EV-implement-prompt4-20260724-01/protocol-manifest.json`
- `MIG-0180` -> `docs/validation/skills/implement/evals/EV-implement-prompt4-20260724-01/results-manifest.json`
- `MIG-0181` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/evaluator-fixture.json`
- `MIG-0182` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/protocol-manifest.json`
- `MIG-0183` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/results-manifest.json`
- `MIG-0184` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/results.md`
- `MIG-0185` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/worker-fixtures.json`
- `MIG-0186` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/behavior-output.schema.json`
- `MIG-0187` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/behavior-protocol.md`
- `MIG-0188` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/live/cleanup_probe.py`
- `MIG-0189` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/live/logic_probe.py`
- `MIG-0190` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/live/measure_probe.py`
- `MIG-0191` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/live/ui/index.html`
- `MIG-0192` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/measure-contribution-protocol.md`
- `MIG-0193` -> `docs/validation/skills/prototype/evals/EV-prototype-prompt4-20260721-01/resume-role-protocol.md`
- `MIG-0194` -> `docs/validation/skills/review/evals/EV-review-prompt4-20260724-01/campaign-decision.json`
- `MIG-0195` -> `docs/validation/skills/review/evals/EV-review-prompt4-20260724-01/fixtures/root-only-evaluation.json`
- `MIG-0196` -> `docs/validation/skills/review/evals/EV-review-prompt4-20260724-01/fixtures/worker-visible.json`
- `MIG-0197` -> `docs/validation/skills/simplify-code/evals/EV-simplify-code-b0-d0-20260723-01/PROTOCOL.md`
- `MIG-0198` -> `docs/validation/skills/simplify-code/evals/EV-simplify-code-prompt4-20260723-01/FIXED-PACKETS.md`
- `MIG-0199` -> `docs/validation/skills/tdd/evals/EV-tdd-pruning-20260722-01/decision.md`
- `MIG-0200` -> `docs/validation/skills/tdd/evals/EV-tdd-pruning-20260722-01/protocol.md`
- `MIG-0201` -> `docs/validation/skills/tdd/evals/EV-tdd-pruning-20260722-01/response.schema.json`
- `MIG-0202` -> `docs/validation/skills/tdd/evals/EV-tdd-pruning-20260722-01/rubric.md`
- `MIG-0203` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260724-01/campaign-decision.json`
- `MIG-0204` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260724-01/fixtures/root-only-evaluation.json`
- `MIG-0205` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260724-01/fixtures/worker-visible.json`
- `MIG-0206` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260725-01/dispatch-plan.json`
- `MIG-0207` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260725-01/fixture-lint-map.json`
- `MIG-0208` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260725-01/prompt4-results.json`
- `MIG-0209` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260725-01/root-registration.json`
- `MIG-0210` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt4-20260725-01/worker-fixture.json`
- `MIG-0211` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/README.md`
- `MIG-0212` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/fixtures/h1.json`
- `MIG-0213` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/fixtures/m0.json`
- `MIG-0214` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/fixtures/runtime.json`
- `MIG-0215` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/fixtures/tracker-contract.md`
- `MIG-0216` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/isolation-v2/README.md`
- `MIG-0217` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/isolation-v2/results.md`
- `MIG-0218` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/protocol.md`
- `MIG-0219` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/pruning-v2/README.md`
- `MIG-0220` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260723-01/results.md`
- `MIG-0221` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260725-01/prompt4-results.json`
- `MIG-0222` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260725-01/root-registration.json`
- `MIG-0223` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-20260725-01/worker-fixture.json`
- `MIG-0224` -> `docs/validation/skills/writing-great-skills/evals/EV-writing-great-skills-prompt5-r2-20260724-01/final-manifest.json`
- `MIG-0225` -> `None`
- `MIG-0226` -> `None`
- `MIG-0227` -> `None`
- `MIG-0228` -> `None`
- `MIG-0229` -> `None`
- `MIG-0230` -> `None`
- `MIG-0232` -> `None`
- `MIG-0233` -> `None`
- `MIG-0234` -> `None`
- `MIG-0235` -> `None`
- `MIG-0236` -> `None`
- `MIG-0237` -> `None`
- `MIG-0238` -> `None`
- `MIG-0239` -> `None`
- `MIG-0240` -> `None`
- `MIG-0241` -> `None`
- `MIG-0242` -> `None`
- `MIG-0243` -> `None`
- `MIG-0244` -> `None`
- `MIG-0245` -> `None`
- `MIG-0249` -> `docs/validation/skills/audit-codebase/evals/EV-audit-codebase-v2-behavior-eval-20260718-01/evidence/2026-07-18-audit-codebase-v2-behavior-eval.md`
- `MIG-0250` -> `docs/validation/skills/audit-codebase/evals/EV-audit-codebase-audit-implement-handoff-eval-20260718-01/evidence/2026-07-18-audit-implement-handoff-eval.md`
- `MIG-0251` -> `docs/validation/skills/audit-codebase/evals/EV-audit-codebase-audit-pruning-equivalence-eval-20260718-01/evidence/2026-07-18-audit-pruning-equivalence-eval.md`
- `MIG-0252` -> `docs/validation/skills/audit-codebase/evals/EV-audit-codebase-coordinated-v2-behavior-eval-20260718-01/evidence/2026-07-18-coordinated-v2-behavior-eval.md`
- `MIG-0253` -> `docs/validation/skills/improve-codebase/evals/EV-improve-codebase-pruning-equivalence-eval-20260718-01/evidence/2026-07-18-improve-codebase-pruning-equivalence-eval.md`
- `MIG-0254` -> `docs/validation/skills/improve-codebase/evals/EV-improve-codebase-rewrite-eval-20260718-01/evidence/2026-07-18-improve-codebase-rewrite-eval.md`
- `MIG-0255` -> `docs/validation/skills/improve-codebase/evals/EV-improve-codebase-routing-eval-20260718-01/evidence/2026-07-18-improve-codebase-routing-eval.md`
- `MIG-0256` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-parallel-checkpoint-correction-eval-20260718-01/evidence/2026-07-18-parallel-checkpoint-correction-eval.md`
- `MIG-0257` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-root-only-orchestration-eval-20260718-01/evidence/2026-07-18-root-only-orchestration-eval.md`
- `MIG-0259` -> `docs/validation/skills/domain-modeling/evals/EV-domain-modeling-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-domain-modeling-extraction-pruning-evidence.md`
- `MIG-0260` -> `docs/validation/skills/domain-modeling/evals/EV-domain-modeling-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-domain-modeling-post-candidate-behavior-eval.md`
- `MIG-0261` -> `docs/validation/skills/grilling/evals/EV-grilling-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-grilling-extraction-pruning-evidence.md`
- `MIG-0262` -> `docs/validation/skills/grilling/evals/EV-grilling-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-grilling-post-candidate-behavior-eval.md`
- `MIG-0263` -> `docs/validation/skills/prototype/evals/EV-prototype-candidate-behavior-eval-20260721-01/evidence/2026-07-21-prototype-candidate-behavior-eval.md`
- `MIG-0264` -> `docs/validation/skills/prototype/evals/EV-prototype-description-pruning-eval-20260721-01/evidence/2026-07-21-prototype-description-pruning-eval.md`
- `MIG-0265` -> `docs/validation/skills/prototype/evals/EV-prototype-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-prototype-extraction-pruning-evidence.md`
- `MIG-0266` -> `docs/validation/skills/prototype/evals/EV-prototype-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-prototype-post-candidate-behavior-eval.md`
- `MIG-0267` -> `docs/validation/skills/prototype/evals/EV-prototype-post-prune-behavior-eval-20260721-01/evidence/2026-07-21-prototype-post-prune-behavior-eval.md`
- `MIG-0268` -> `docs/validation/skills/research/evals/EV-research-canonical-first-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-research-canonical-first-extraction-pruning-evidence.md`
- `MIG-0269` -> `docs/validation/skills/research/evals/EV-research-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-research-extraction-pruning-evidence.md`
- `MIG-0270` -> `docs/validation/skills/research/evals/EV-research-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-research-post-candidate-behavior-eval.md`
- `MIG-0271` -> `docs/validation/skills/to-questionnaire/evals/EV-to-questionnaire-control-lock-20260721-01/evidence/2026-07-21-to-questionnaire-control-lock.md`
- `MIG-0272` -> `docs/validation/skills/to-questionnaire/evals/EV-to-questionnaire-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-to-questionnaire-post-candidate-behavior-eval.md`
- `MIG-0273` -> `docs/validation/skills/to-questionnaire/evals/EV-to-questionnaire-pruning-equivalence-eval-20260721-01/evidence/2026-07-21-to-questionnaire-pruning-equivalence-eval.md`
- `MIG-0274` -> `docs/validation/skills/writing-great-skills/evals/EV-writing-great-skills-authoring-boundary-eval-20260721-01/evidence/2026-07-21-writing-great-skills-authoring-boundary-eval.md`
- `MIG-0275` -> `docs/validation/skills/writing-great-skills/evals/EV-writing-great-skills-extraction-pruning-evidence-20260721-01/evidence/2026-07-21-writing-great-skills-extraction-pruning-evidence.md`
- `MIG-0276` -> `docs/validation/skills/writing-great-skills/evals/EV-writing-great-skills-post-candidate-behavior-eval-20260721-01/evidence/2026-07-21-writing-great-skills-post-candidate-behavior-eval.md`
- `MIG-0277` -> `docs/validation/skills/domain-modeling/evals/EV-domain-modeling-promotion-install-evidence-20260722-01/evidence/2026-07-22-domain-modeling-promotion-install-evidence.md`
- `MIG-0278` -> `docs/validation/skills/grill-with-docs/evals/EV-grill-with-docs-extraction-pruning-evidence-20260722-01/evidence/2026-07-22-grill-with-docs-extraction-pruning-evidence.md`
- `MIG-0279` -> `docs/validation/skills/grill-with-docs/evals/EV-grill-with-docs-implicit-invocation-eval-20260722-01/evidence/2026-07-22-grill-with-docs-implicit-invocation-eval.md`
- `MIG-0280` -> `docs/validation/skills/grill-with-docs/evals/EV-grill-with-docs-post-candidate-behavior-eval-20260722-01/evidence/2026-07-22-grill-with-docs-post-candidate-behavior-eval.md`
- `MIG-0281` -> `docs/validation/skills/grill-with-docs/evals/EV-grill-with-docs-promotion-install-evidence-20260722-01/evidence/2026-07-22-grill-with-docs-promotion-install-evidence.md`
- `MIG-0283` -> `docs/validation/skills/prototype/evals/EV-prototype-b0-first-acceptance-20260722-01/evidence/2026-07-22-prototype-b0-first-acceptance.md`
- `MIG-0284` -> `docs/validation/skills/tdd/evals/EV-tdd-candidate-evidence-20260722-01/evidence/2026-07-22-tdd-candidate-evidence.md`
- `MIG-0285` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-i3-promotion-eval-20260722-01/evidence/2026-07-22-to-tickets-i3-promotion-eval.md`
- `MIG-0286` -> `docs/validation/skills/implement/evals/EV-implement-b0-c1-construction-evidence-20260723-01/evidence/2026-07-23-implement-b0-c1-construction-evidence.md`
- `MIG-0287` -> `docs/validation/skills/implement/evals/EV-implement-post-candidate-behavior-eval-20260723-01/evidence/2026-07-23-implement-post-candidate-behavior-eval.md`
- `MIG-0288` -> `docs/validation/skills/prototype/evals/EV-prototype-runtime-no-change-behavior-eval-20260723-01/evidence/2026-07-23-prototype-runtime-no-change-behavior-eval.md`
- `MIG-0289` -> `docs/validation/skills/prototype/evals/EV-prototype-runtime-no-change-construction-evidence-20260723-01/evidence/2026-07-23-prototype-runtime-no-change-construction-evidence.md`
- `MIG-0290` -> `docs/validation/skills/prototype/evals/EV-prototype-runtime-no-change-pruning-20260723-01/evidence/2026-07-23-prototype-runtime-no-change-pruning.md`
- `MIG-0291` -> `docs/validation/skills/research/evals/EV-research-b0-c1-construction-evidence-20260723-01/evidence/2026-07-23-research-b0-c1-construction-evidence.md`
- `MIG-0292` -> `docs/validation/skills/research/evals/EV-research-behavior-eval-20260723-01/evidence/2026-07-23-research-behavior-eval.md`
- `MIG-0293` -> `docs/validation/skills/research/evals/EV-research-canonical-first-promotion-eval-20260723-01/evidence/2026-07-23-research-canonical-first-promotion-eval.md`
- `MIG-0294` -> `docs/validation/skills/research/evals/EV-research-promotion-install-20260723-01/evidence/2026-07-23-research-promotion-install.md`
- `MIG-0295` -> `docs/validation/skills/research/evals/EV-research-pruning-20260723-01/evidence/2026-07-23-research-pruning.md`
- `MIG-0296` -> `docs/validation/skills/research/evals/EV-research-source-and-terminal-alignment-eval-20260723-01/evidence/2026-07-23-research-source-and-terminal-alignment-eval.md`
- `MIG-0297` -> `docs/validation/skills/simplify-code/evals/EV-simplify-code-behavior-eval-20260723-01/evidence/2026-07-23-simplify-code-behavior-eval.md`
- `MIG-0298` -> `docs/validation/skills/simplify-code/evals/EV-simplify-code-promotion-install-20260723-01/evidence/2026-07-23-simplify-code-promotion-install.md`
- `MIG-0299` -> `docs/validation/skills/simplify-code/evals/EV-simplify-code-pruning-20260723-01/evidence/2026-07-23-simplify-code-pruning.md`
- `MIG-0300` -> `docs/validation/skills/to-questionnaire/evals/EV-to-questionnaire-behavior-eval-20260723-01/evidence/2026-07-23-to-questionnaire-behavior-eval.md`
- `MIG-0301` -> `docs/validation/skills/to-questionnaire/evals/EV-to-questionnaire-promotion-install-20260723-01/evidence/2026-07-23-to-questionnaire-promotion-install.md`
- `MIG-0302` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-b0-c1-construction-20260723-01/evidence/2026-07-23-to-tickets-b0-c1-construction.md`
- `MIG-0303` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-promotion-install-20260723-01/evidence/2026-07-23-to-tickets-promotion-install.md`
- `MIG-0304` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt1-m0-20260723-01/evidence/2026-07-23-to-tickets-prompt1-m0.md`
- `MIG-0305` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-continuation-20260723-01/evidence/2026-07-23-to-tickets-prompt4-continuation.md`
- `MIG-0306` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-eval-20260723-01/evidence/2026-07-23-to-tickets-prompt4-eval.md`
- `MIG-0307` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt4-reconciliation-20260723-01/evidence/2026-07-23-to-tickets-prompt4-reconciliation.md`
- `MIG-0308` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-prompt5-20260723-01/evidence/2026-07-23-to-tickets-prompt5.md`
- `MIG-0309` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-pruning-v2-20260723-01/evidence/2026-07-23-to-tickets-pruning-v2.md`
- `MIG-0310` -> `docs/validation/skills/to-tickets/evals/EV-to-tickets-pruning-20260723-01/evidence/2026-07-23-to-tickets-pruning.md`
- `MIG-0311` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt1-m0-20260724-01/evidence/2026-07-24-convergent-pr-review-prompt1-m0.md`
- `MIG-0312` -> `docs/validation/skills/convergent-pr-review/evals/EV-convergent-pr-review-prompt2-synthesis-20260724-01/evidence/2026-07-24-convergent-pr-review-prompt2-synthesis.md`
- `MIG-0313` -> `docs/validation/skills/implement/evals/EV-implement-prompt5-20260724-01/evidence/2026-07-24-implement-prompt5.md`
- `MIG-0314` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt1-m0-r2-20260724-01/evidence/2026-07-24-parallel-implement-prompt1-m0-r2.md`
- `MIG-0315` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt4-r2-20260724-01/evidence/2026-07-24-parallel-implement-prompt4-r2.md`
- `MIG-0316` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-prompt5-r2-20260724-01/evidence/2026-07-24-parallel-implement-prompt5-r2.md`
- `MIG-0317` -> `docs/validation/skills/parallel-implement/evals/EV-parallel-implement-pruning-r2-20260724-01/evidence/2026-07-24-parallel-implement-pruning-r2.md`
- `MIG-0318` -> `docs/validation/skills/to-spec/evals/EV-to-spec-prompt1-m0-20260724-01/evidence/2026-07-24-to-spec-prompt1-m0.md`
- `MIG-0319` -> `None`

## Contract

Each inventoried artifact has one `MIG-NNNN` row across the tracked ledger and
ignored sidecar. Epoch, Catalog-query, proof-reuse, and migration dispositions
are separate fields. A move or removal requires a recovery pointer and Lock.
Only the listed public rows are `verified`; every other public row remains pending. Private rows retain terminal status only in the ignored sidecar, without publishing their source locators. Hash/access failure is `blocked` and never receives
an inferred identity.

Run:

```text
python -m scripts.migration_ledger check
```

The check re-enumerates tracked, untracked, ignored, private, and empty local
residue; verifies unchanged public content and each applied target; and fails
on unexplained path/content drift, missing/duplicate/stale rows, privacy
leakage, or premature proof.

Source: issues #32, #34, #38, #39, #41, and #46; ADR-0008 and ADR-0009.
