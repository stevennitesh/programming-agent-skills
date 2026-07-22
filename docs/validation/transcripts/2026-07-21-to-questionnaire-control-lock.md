# To Questionnaire Control Lock

Date: 2026-07-21
Decision: `ready-for-experimental-candidate`

This record is admission control for Deploy Prompt 3, not post-candidate behavioral acceptance. The current canonical skill was the sole guidance under test; no-guidance and candidate arms were not run.

## Fixed Control

| Input | Fixed value |
| --- | --- |
| Canonical skill | `skills/custom/to-questionnaire/SKILL.md` |
| Canonical skill SHA-256 | `0310b4edbed253a641c3dcd44320e8703a73234dbecc7b7f87290492ace479fb` |
| Canonical policy SHA-256 | `dc1585512a0c63a93d69421c2afae62ebc94b0eab91a792a41d2859219ce0b9a` |
| Repository commit | `c456e83c0e3976e3e1adb5bf46b2204a824cf682` with disclosed unrelated dirty work |
| To Questionnaire synthesis SHA-256 | `a5d914db6d07f71a5a83903ab2ef35f12a5b0b9b6af964cf738b2910c33a336b` |
| Wayfinder synthesis SHA-256 | `6ea3bd435f3f4803ec36201011999352f5b3be118d56520b12783dbc95afd073` |
| Relationship snapshot SHA-256 | `e1815f8f33125b8564058325f9cd92730b5169dfa32a8844bbe456d4b970b213` |
| Runtime | Five independent fresh contexts per suite; current Codex GPT-5-family runtime and inherited default reasoning |
| Tools | Read-only canonical file reads and SHA-256 verification; no candidate, synthesis, test, or relationship reads by samplers |
| Authority | Read-only; all filesystem behavior was a labeled planned-action proxy |
| Unavailable telemetry | Exact model build, reasoning tier, temperature, seed, token timing, and sampler internals |

Each sampler received the same complete case suite and rubric in a fresh context. Candidate language, conclusions, and other samples were excluded. The root inspected every result and retained the immutable control hash throughout both waves.

## Fixed Cases

| Case | Fixed pressure |
| --- | --- |
| A | Natural direct request for one risk stakeholder, plus adjacent research, live-interview, reusable-survey, and answer-analysis negatives |
| B | Explicit missing or unverified recipient authority versus a proven source-answerable mismatch |
| C | Direct request with sender, recipient, decision, gaps, source check, effort, sensitivity, durable intent, no overwrite, and no delivery; deadline, return owner, response format, and exact path omitted |
| D | Complete Wayfinder Questionnaire packet versus the same packet with retention owner omitted |
| E | Two material gaps owned by two different recipients |
| F | Three material atomic gaps under a hard three-minute budget where a catch-all exceeds the budget |
| G | Durable output with compatible `.scratch`, disposable `.tmp`, a collision, pre-existing dirty work, and concurrent unrelated drift |
| H | Returned answers offered for truth certification and downstream resolution after a Wayfinder-originated questionnaire |
| J | Explicit questionnaire artifact for recipient use during a later meeting; meeting conduct excluded |
| K | One uniquely identified role recipient versus a reusable respondent-pool instrument |
| L | Direct source, conversation-only, durable-domain, and missing-setup mismatches paired with equivalent Wayfinder mismatches |
| M | Sanitizable sensitive context versus context necessary to ask responsibly but lacking disclosure authority |
| N | Traversal escape, wrong extension, collision without overwrite, sensitivity-incompatible `.scratch`, and a legal new target |
| O | Missing ledger coverage plus an orphan question at a writable target |
| P | The direct-default case isolated from other claims |

## Rubric

`control-failure` requires the canonical guidance to cause or permit the precise violation in the fixed case. `pass` requires explicit or behaviorally sufficient control. `uncertain` admits nothing. Structural strings are supporting evidence only. Filesystem conclusions remain proxy evidence because the Control Lock prohibited mutation.

## Per-Sample Results

Wave 1 used samples `S1` through `S5`; Wave 2 used fresh samples `S6` through `S10`.

| Claim | S1 | S2 | S3 | S4 | S5 | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Narrow implicit positive plus adjacent negatives | failure | failure | failure | failure | failure | admit |
| Typed `Incomplete` versus `Not admitted` | failure | failure | failure | failure | failure | admit |
| Visible safe Direct defaults | failure evidence in case | failure | failure | failure evidence in case | failure evidence in case | admit |
| At-most-one compact Direct intake | pass | pass | pass | pass | pass | `reject-no-control-failure` |
| Complete and incomplete Wayfinder packet handling | failure | failure | failure | failure | failure | admit |
| One recipient and multi-owner split | pass | pass | pass | pass | uncertain | `reject-no-control-failure` |
| Stable structured ledger and bidirectional mapping | failure | failure | failure | failure | failure | admit |
| Existing atomic, neutral, answerable question discipline | pass | pass | pass | pass | pass | `reject-no-control-failure` |
| Optional catch-all under effort pressure | failure | failure | failure | failure | failure | admit |
| Durable storage, collision, overwrite, and attributable drift | failure | failure | failure | failure | failure | admit |
| Typed matched Direct and Wayfinder Returns | failure | failure | failure | failure | failure | admit |
| Existing no-delivery and no-downstream-synthesis boundary | pass | pass | pass | compound failure only for absent Wayfinder ownership | pass | `reject-no-control-failure`; caller ownership admitted with matched Return |

| Claim | S6 | S7 | S8 | S9 | S10 | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Later-meeting artifact without meeting conduct | pass | pass | pass | pass | pass | `reject-no-control-failure` |
| Uniquely identified role versus respondent pool | pass | pass | pass | pass | pass | `reject-no-control-failure` |
| Direct route distinctions and Wayfinder next-route authority | failure | failure | failure | failure | failure | admit |
| Sensitive-context authorization before write | failure | failure | failure | failure | failure | admit |
| Resolved path, containment, extension, collision, overwrite, and storage preflight | failure | failure | failure | failure | failure | admit |
| Semantic and effort checks before Save | failure | failure | failure | failure | pass | admit; one sample misread post-Save effort verification |
| Exact visible Direct defaults | failure | failure | failure | failure | failure | admit |
| Conditional durable Wayfinder identity, lifetime, and retention | failure | failure | failure | failure | failure | admit |

## Aggregate And Variance

Thirteen additions were admitted. Six proposed restatements were rejected because the control already supplied the behavior: compact Direct intake, one-recipient splitting, core question quality, later-meeting artifact use, singular role recipients, and the substantive no-delivery/no-synthesis boundary.

All admitted claims showed control failure in at least four of five independent samples; twelve showed failure in all five. The sole variance was the pre-Save effort claim: four samples correctly observed that effort fit is verified only after Save, while one treated the general completion criterion as a pre-Save gate. The ordered canonical procedure and worst result support admission.

Critical control failures included missed natural invocation, missing typed outcomes, writing despite an incomplete durable caller packet, mandatory catch-all pressure, disposable storage for durable intent, unguarded traversal or overwrite, sensitive-context discovery after Save, and incomplete Wayfinder identity and ownership evidence.

## Dependency Notes

- Preserve the passing canonical one-recipient, compact-intake, question-quality, and stop boundaries as baseline behavior; do not present them as candidate additions.
- Compose typed status, Wayfinder entry, durable identity, and matched Return as one coherent adapter boundary.
- Compose safe defaults, path preflight, sensitivity, pre-Save semantic proof, and attributable mutation as one artifact transaction.
- Do not activate the Wayfinder invocation edge. The leaf candidate remains incomplete as a coordinated release until Wayfinder supplies and consumes the matching packet and external-wait state under separate extraction and integrated proof.

## Residual Gap

This record contains control-only behavioral evidence. Planned filesystem actions were not executed, candidate improvement and regression are unmeasured, and invocation precision has no candidate arm. Deploy Prompt 4 must run at least five independent fresh candidate samples per admitted claim, inspect produced artifacts and filesystem state, and decide acceptance before promotion.
