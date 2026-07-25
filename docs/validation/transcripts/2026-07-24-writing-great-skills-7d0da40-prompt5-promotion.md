# Writing Great Skills Deploy Prompt 5

Campaign epoch: `2026-07-24-writing-great-skills-7d0da40`

Authorized unit: Deploy Prompt 5 only

Operation: `writing-great-skills` Author followed by the separately owned
installation phase only after canonical proof

Starting Git `HEAD`: `7d0da40a218114aa138265557ea2454361dcd147`

## Decision

Decision: `evidence-gap`.

Prompt 4 was reread as `accepted`; the Pruning Pass was reread as `complete`
with `pruning-not-needed`; exact
`M0 = post-decision H1 = V1 = P1` was verified at
`campaign-tree-v1:175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341`.
`H1-POINTER-REPAIR-01` remained `reject-no-control-deficit` and absent from
P1.

## Canonical Proof And Rollback

Exact P1 was provisionally promoted into the canonical four-file package and
read back at its frozen tree identity. The directly affected focused proof
then failed:

`tests/test_deploy_prompt_contracts.py::test_behavior_evaluation_contract_supports_quality_lift_and_adaptive_cost`

The test uses heading-bounded normalized semantics. It requires the canonical
behavior-evaluation owner to preserve defect-correction and quality-lift
registration, entry-positive and wrong-condition cohorts, adaptive M0/H1
sample gates, conditional-efficacy judgment, and the complete terminal
disposition vocabulary. P1 removes those semantics. The failure is therefore
not a human-prose snapshot eligible for proof repair.

Prompt 5 did not modify P1 or the proof contract. Canonical was restored before
installation to exact C0 at
`campaign-tree-v1:559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032`.
The installed mirror was read-only and already matched canonical at the same
identity.

## Proof Boundary

- Focused canonical proof: `14 passed, 1 failed`.
- Skill validation: passed after the provisional promotion.
- Exact P1 tree proof: passed before focused proof.
- Exact canonical rollback tree proof: passed.
- Final preserved-state focused proof: `15 passed`.
- Full integration suite on preserved canonical state: `213 passed, 4 skipped`.
- Behavioral evidence: reused unchanged; no Prompt 5 behavior rerun.
- Installer dry-run, changed-cohort proof, synchronization, parity-after-sync,
  and post-install dry-run: not run because canonical proof is a prerequisite.
- Experimental cleanup: no `writing-great-skills` experimental package or
  manifest entry existed; every other candidate was preserved.

## Terminal Claims

Semantic contract: P1 is exact but not promotable because it omits a required
canonical compatibility contract.

Bounded behavior: the five exact M0 controls remain valid only within the
frozen Prompt 4 task, model family, host, reasoning configuration, tools,
authority, runtime, and rubric. They do not override the canonical
compatibility failure.

Runtime-load proxy: P1 is 4,872 bytes and 639 whitespace-delimited words,
equal to V1. No token or latency telemetry is available, and no installed load
claim is made.

## Frozen Decision Capsule

<!-- DEPLOY-STAGE-CAPSULE:prompt5:start -->
unit: Deploy Prompt 5
decision: evidence-gap
campaign-shape: hypothesis-candidate
runtime-identities: M0 = post-decision H1 = V1 = P1 175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341; canonical = installed = preserved C0 559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032; rejected frozen H1 95c45d53a6e853bad3a74981634b2bdf8c0e3bc7fc8a11f5a568fc3b0efad577
canonical-proof: failed heading-bounded semantic compatibility test for behavior-evaluation registration, adaptive sampling, wrong-condition, judgment, and terminal dispositions
failure-classification: frozen M0 compatibility omission; not human-prose snapshot
canonical-state: provisional P1 promotion rolled back before installation
installed-state: read-only; exact canonical C0 parity; not mutated
behavioral-evidence: exact Prompt 4 evidence reused; no rerun
experimental-cleanup: not-applicable; target package and manifest entry absent
recommended-next-unit: Deploy Prompt 1
successor-started: false
git-delivery: pending
<!-- DEPLOY-STAGE-CAPSULE:prompt5:end -->

## Shared Run Contract Return

```text
Authorized unit completed: Deploy Prompt 5: Promote And Install P1 for writing-great-skills, campaign 2026-07-24-writing-great-skills-7d0da40
Decision: evidence-gap
Campaign shape: hypothesis-candidate
Runtime identities: M0 = post-decision H1 = V1 = P1 175c70bbe0ee79fad197f44ba32f0786b9bb94250ef22da21e66ded47d9e0341; rejected frozen H1 95c45d53a6e853bad3a74981634b2bdf8c0e3bc7fc8a11f5a568fc3b0efad577; canonical = installed = preserved C0 559a03933cc1abdb91d02bf06d4f6dcf45743cd3a23144c4f9641e92ebf38032
Artifacts changed: active synthesis; candidate record; campaign manifest; compact final manifest; this Prompt 5 transcript
Evidence used or reused: exact Prompt 4 accepted capsule and five 8/8 M0 controls; exact Pruning complete/pruning-not-needed capsule; exact P1 tree proof; provisional canonical read-back; focused canonical semantic proof; skill validation; exact canonical rollback and installed read-only parity; final preserved-state focused proof; full integration suite
Residual gaps: frozen M0 omits required canonical behavior-evaluation compatibility semantics; P1 is not promotable; installer dry-run, cohort proof, synchronization, post-sync parity, and clean post-install dry-run were not reached; exact model build, sampler seed, tokens, latency, prevalence, cross-host, and broader transfer remain unavailable or unproved
Recommended next unit: Deploy Prompt 1
Git HEAD: 7d0da40a218114aa138265557ea2454361dcd147 -> 7d0da40a218114aa138265557ea2454361dcd147
Git delivery: pending
Exact stop reason: Exact P1 failed a frozen heading-bounded canonical compatibility contract, so canonical C0 was restored before installation and Prompt 5 stopped with evidence-gap; Prompt 1 is the required route.
```
