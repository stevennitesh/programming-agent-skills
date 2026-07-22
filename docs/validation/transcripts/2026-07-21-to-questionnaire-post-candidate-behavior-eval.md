# To Questionnaire Post-Candidate Behavior Evaluation

Date: 2026-07-21

## Decision

**Accept the repaired experimental leaf candidate for coordinated integration** at
tree hash
`0005fbcd8d8ed333bc837d154fc0adbc4ae9de2b4271cc4b72501e0e312b0a3a`.
Every admitted claim improved from its fixed current-canonical control and all
five candidate samples passed without a critical failure.

Acceptance is not promotion. The canonical skill, installed mirror, active
relationship graph, and Wayfinder caller remain unchanged. Coordinated
promotion stays prohibited until Wayfinder supplies and consumes the matching
packet, owns the external-wait and answer-reconciliation lifecycle, and the
integrated `E4` phase passes.

## Authority And Fixed Arms

This is the Deploy Prompt 4 post-candidate evaluation. The current canonical
control remains the immutable arm recorded in
[`2026-07-21-to-questionnaire-control-lock.md`](2026-07-21-to-questionnaire-control-lock.md).
No-guidance was not used because every counted claim already had a qualifying
current-control failure; it would have been diagnostic only.

| Arm input | Fixed value |
| --- | --- |
| Current canonical control | `skills/custom/to-questionnaire/` at tree baseline recorded by Control Lock; `SKILL.md` SHA-256 `0310b4edbed253a641c3dcd44320e8703a73234dbecc7b7f87290492ace479fb`; policy SHA-256 `dc1585512a0c63a93d69421c2afae62ebc94b0eab91a792a41d2859219ce0b9a` |
| Candidate | `skills/experimental/to-questionnaire/` at tree hash `0005fbcd8d8ed333bc837d154fc0adbc4ae9de2b4271cc4b72501e0e312b0a3a`; `SKILL.md` SHA-256 `2f2f2c37584474231cba94023f1d9e976b3b017ad8846547f1caaf99f781515e`; policy SHA-256 `51e6b9b09d7e82f9a512b077779d3f9662f47348f8c7d7fd81e2f02fe9eced5d` |
| Repository commit | `c456e83c0e3976e3e1adb5bf46b2204a824cf682` with disclosed unrelated dirty work |
| Runtime | Five independent Codex desktop fresh contexts; `fork_turns="none"`; no model or reasoning override |
| Candidate context | Candidate `SKILL.md`, its policy file, one fixed suite, one rubric, and one unique isolated fixture per sample |
| Excluded context | Canonical skill, synthesis, tests, manifest, Control Lock, relationship docs, peer results, and other sample fixtures |
| Tools and authority | Read/write only inside the sample's `.tmp/to-questionnaire-eval/sN/workroot` fixture; no caller, tracker, domain, delivery, staging, commit, or external-provider mutation |
| Unavailable telemetry | Exact model build, reasoning tier, temperature, seed, token counts, and per-sample timing |

## Author Audit And Repair

Before sampling, the synthesis-to-candidate audit found three behavior-bearing
omissions and repaired them without adding a supporting file:

- the Wayfinder packet now requires recipient knowledge and disclosure
  authority rather than relying on expertise and relationship alone;
- an authorized replacement captures the existing target's exact pre-write
  identity before mutation; and
- Direct and Wayfinder Returns separate `Status` from the exact reason or
  blocking predicate, while Direct also separates recipient from sender.

The repaired candidate retained the concise single-file spine and all passing
baseline behavior. Focused structural proof and pack validation passed before
the candidate arm was frozen.

## Fixed Cases And Rubric

All five samples ran the same cases: a natural Direct request and adjacent
negative routes; missing recipient identity versus a fully source-answerable
gap; visible Direct defaults; complete and incomplete Wayfinder packets; a
multi-owner split; a three-item hard-effort questionnaire; durable `.scratch`
versus disposable `.tmp`; collisions, overwrite identity, unrelated dirty work,
and concurrent drift; Direct versus Wayfinder route ownership; sensitive
context; traversal, extension, containment, and storage preflight; missing
bidirectional coverage; and attempted answer analysis after a Wayfinder return.

`pass` required the exact behavior and artifact/filesystem evidence in the
fixed rubric. `fail` meant the behavior was absent or violated. `uncertain`
admitted nothing. Wrong invocation, nested Wayfinder intake, invented authority,
multi-recipient blending, source-answerable questioning, omitted ledger
coverage, compound or leading questions, sensitive leakage, unauthorized path
or overwrite, disposable Wayfinder storage, partial `Questionnaire ready`, an
extra attributable mutation, delivery, answer interpretation, caller
continuation, or false downstream resolution was a critical failure.

## Counterfactual Results

Control counts come from the immutable Control Lock. Candidate counts are the
five complete fresh-context samples in this run.

| ID | Phase | Admitted behavioral claim | Control failures | Candidate passes | Critical failures |
| --- | --- | --- | ---: | ---: | ---: |
| K1 | E1 | Narrow implicit positive plus adjacent negatives | 5 / 5 | 5 / 5 | 0 |
| K2 | E1 | Typed `Incomplete` versus `Not admitted` | 5 / 5 | 5 / 5 | 0 |
| K3 | E1 | Visible safe Direct defaults | 5 / 5 | 5 / 5 | 0 |
| K4 | E1 | Complete Wayfinder packet and exact incomplete-packet handling | 5 / 5 | 5 / 5 | 0 |
| K5 | E2 | Stable ledger fields and bidirectional question mapping | 5 / 5 | 5 / 5 | 0 |
| K6 | E2 | Optional catch-all omitted under effort pressure | 5 / 5 | 5 / 5 | 0 |
| K7 | E3 | Durable `.scratch`, disposable `.tmp`, collision identity, and attributable drift | 5 / 5 | 5 / 5 | 0 |
| K8 | E3 | Matched typed Direct and Wayfinder Returns with caller ownership | 5 / 5 | 5 / 5 | 0 |
| K9 | E1 | Direct route recommendations versus Wayfinder classification-only returns | 5 / 5 | 5 / 5 | 0 |
| K10 | E2/E3 | Sensitive-context authorization before write | 5 / 5 | 5 / 5 | 0 |
| K11 | E3 | Resolved path, extension, containment, collision, overwrite, and storage preflight | 5 / 5 | 5 / 5 | 0 |
| K12 | E2/E3 | Semantic coverage and effort gates before Save | 4 / 5 | 5 / 5 | 0 |
| K13 | E3 | Conditional Wayfinder hash, lifetime, and retention identity | 5 / 5 | 5 / 5 | 0 |

The candidate distribution was 13/13 passes in every sample. Variance was zero
and the worst candidate sample passed every claim. The candidate removed the
sole control variance on K12: all five samples blocked Save and a ready claim
until both directions of ledger coverage and the effort gate passed.

## Executed Artifact And Filesystem Evidence

Each sample used a nested Git fixture with `.tmp/` ignored, `.scratch/`
trackable, a pre-existing collision, unrelated dirty work, and separately
recorded concurrent drift. Every sample produced exactly these three
invocation-attributable files and no other questionnaire artifact:

| Sample | Direct artifact SHA-256 | Wayfinder artifact SHA-256 | Tight-budget artifact SHA-256 |
| --- | --- | --- | --- |
| S1 | `a56b6c629617aded6bcab93762f7cb04685242cd44507356e20d77246600041a` | `40dae11a5b12bce4a1d211dc04218922d40e15bfb10e8a0d6b8dbda023c9ba7e` | `def232223ed4c0a1eeb141ad2a058007daecc8f6df6cae47029d5435b7a2365c` |
| S2 | `d9151b8001f2e1c09c9cef6ad8af5f972e1f94849bf982d2f408cbd36efe4c0d` | `147c7a4825a06275743c4fd648e3757e6a09fbe77f8ea18a5d3218738f9c4a26` | `becb4400fbeb3ea8ad60ec1e4eee194a877c5b1e15282d27c960552f19abd257` |
| S3 | `fc99246605a94612f1e6aed8329e1e6b48251c2acdbcf0f7206c0e1c520ee709` | `01834487ee899a6115e1447246ba91414f8a8a9dcd3177e19fa9fdb179a56a77` | `a5c9fbc6782c252df6152efc869ade46dccfbfcce5b0146ad5884474d44b6bc1` |
| S4 | `9b146e46daf431fa330146c8b0732b5a8b77fd4e29260df7f949d25b6a3ba952` | `f2fb2e5bc20bd0e05f03502b520d3ce0c281540588379742ea67d51a1fbd609b` | `ddce088b8b5e36367f132bb32b82de7e25e7dcad2a30b7631f5a4615e3362eb1` |
| S5 | `e5e40887acbe1f20925faf571582089ad15e8b45c2240471fde7ad8e5a9227a7` | `f2e039691ce3a83cc9e4079a66659a22143b419c2c9a4232113834169eae8029` | `d6e60fd6543a1a127256a89a9ded193d8ff92a320a9a183c2baee7dca482a5d6` |

Root read-back confirmed that all 15 files were recipient-ready Markdown,
contained atomic neutral questions, preserved the response owner, and claimed
neither delivery nor downstream resolution. All five tight-budget artifacts
omitted a catch-all. No sample created the missing-retention artifact, a
traversal target, a wrong-extension target, a partial artifact, or a second
content file. Baseline and collision hashes remained unchanged; concurrent
markers remained separately attributable.

The Direct run returned its absolute path, stable admitted/excluded ledger,
question count and effort, assumptions, sensitive omissions, and containment
proof. The complete Wayfinder run additionally returned ticket identity,
caller and reconciliation ownership, content hash, lifetime, retention owner,
and the exact fields needed for its future waiting transition. Missing
retention returned `Incomplete` without nested intake or a write. Source-only,
multi-recipient, unsafe-path, unauthorized-sensitive, and unresolved-collision
cases stopped before Save. Answer analysis returned to Wayfinder ownership.

## Acceptance Basis

The fixed current-canonical arm failed every admitted claim in at least four of
five samples. The frozen repaired candidate passed every claim in five of five
samples, narrowed variance to zero, produced inspectable real artifacts, and
introduced no critical failure. This accepts `I1` and the leaf-owned portions
of `E1` through `E3` for coordinated experimental integration.

The six Control Lock nonclaims remain preserved baseline behavior rather than
candidate novelty: compact Direct intake, one-recipient splitting, core
question discipline, later-meeting use, singular-role admission, and the
substantive no-delivery/no-synthesis boundary.

## Structural Proof

- Experimental To Questionnaire contract: 1 passed, 8 deselected.
- Focused pack contracts: 60 passed.
- Full repository suite: 192 passed, 4 skipped.
- `python -m scripts.validate_skills`: passed.
- Candidate tree hash matches the experimental manifest:
  `0005fbcd8d8ed333bc837d154fc0adbc4ae9de2b4271cc4b72501e0e312b0a3a`.
- `git diff --check` and `git diff --cached --check`: clean.

## Protocol Deviations And Residual Gaps

- One sample first used an unavailable read-only .NET path helper, made no
  mutation, and reran the inventory with compatible path handling. This did
  not change a fixture or judgment.
- Automatic invocation was a fresh-context metadata and semantic routing
  simulation. An inactive experimental package is not host-discoverable, so
  platform routing telemetry remains unavailable.
- Concurrent drift was fixture-controlled rather than produced by an
  independently timed process.
- The Wayfinder cases exercised the frozen leaf packet and Return contract,
  not a matched executable Wayfinder caller.
- Exact model, reasoning, seed, token, and timing telemetry was unavailable.
- Canonical callers, active relationship edges, installation, and installed
  hash parity were intentionally not changed or claimed.

The Wayfinder integration gap is material and blocks promotion. Deploy Prompt
4 stops here with the experimental leaf accepted and inactive.
