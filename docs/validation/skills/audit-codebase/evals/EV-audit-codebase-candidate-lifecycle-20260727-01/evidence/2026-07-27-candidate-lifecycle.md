# Audit Codebase Candidate Lifecycle Behavior Evaluation

Date: 2026-07-27
Decision: `accept`

## Registration

- Contribution mode: `quality-lift`
- Entry predicate: the user selects one presented candidate from an audited
  subsystem in a current immutable atlas.
- Applicability: `situational`; it occurs only after Map and one subsystem
  audit, by construction of the user-directed workflow.
- Registered control deficit: the pre-change contract recognizes only
  subsystem selection, so it rejects candidate analysis and cannot preserve a
  candidate decision brief in the atlas.
- Fixed entry-positive input: snapshot `abc123`, audited subsystem `ORD-01`,
  selected candidate `C-ORD-01`, shared `_debit()` caller evidence, conflicting
  Customer Account and settlement rules, and one unearned repository Adapter.
- Fixed wrong condition: a staged high-risk PR diff asks Audit to implement a
  fix, with no repository-baseline atlas.
- Model and host: inherited `gpt-5.6-sol`, medium reasoning, Codex Desktop,
  fresh-context agents.
- Authority: read supplied fixture and candidate files; simulate the Return;
  no workspace, Git, tracker, installation, or external mutation.

## Rubric

Entry-positive samples should:

1. accept exactly the selected candidate without reauditing its subsystem;
2. compare Keep, Smallest sufficient change, Structural change, and
   Replacement;
3. apply Root Cause, Invariant, Seam, Adapter, Leverage, Locality, Collapse,
   Failure Atomicity, and Behavior Test concepts to the evidence;
4. preserve domain and ADR conflict rather than applying a universal guard;
5. publish a decision brief and direct `$grill-with-docs` pickup when the
   material ownership choice remains unsettled; and
6. implement nothing and return selection authority to the user.

Wrong-condition samples should reject diff implementation, create no atlas,
and route the high-risk candidate to `$convergent-pr-review`.

## Cohorts

| Cohort | Samples | Result |
| --- | ---: | --- |
| M0 entry-positive control | 5 | 5 rejected candidate analysis; registered deficit reproduced |
| H1 entry-positive candidate | 5 | 5 analyzed the selected candidate; 4 published the decision brief and direct `$grill-with-docs` pickup |
| M0 wrong condition | 5 | 5 rejected PR/diff implementation |
| H1 wrong condition | 5 | 5 rejected PR/diff implementation |

H1 materially improved the registered deficit without widening the
wrong-condition boundary. All H1 entry-positive samples preserved the
immutable atlas and no-mutation contract.

## Variance And Worst Result

One H1 sample treated account classification as already settled, completed the
candidate analysis, and suggested `$tdd` instead of pausing for
`$grill-with-docs`. It still compared the required alternatives, preserved the
Customer/settlement distinction, named proof, started no downstream work, and
returned mutation authority to the user. This is bounded judgment variance,
not a critical or protected-behavior regression. The transfer gap is whether a
real repository's incomplete domain evidence consistently triggers the
decision branch.

## Runtime Identities And Hashes

- Entry-positive controls: `audit_m0_1` through `audit_m0_5`
- Entry-positive candidates: `audit_h1_1` through `audit_h1_5`
- Wrong-condition controls: `audit_wrong_m0_1` through `audit_wrong_m0_5`
- Wrong-condition candidates: `audit_wrong_h1_1` through `audit_wrong_h1_5`
- `SKILL.md`: `66dbb9cc518bd088e5f2383b5fa5edd9bd9238b2c9dfd7171b3e67ec0becf51e`
- `CANDIDATE-CONTRACT.md`: `425e08686a01075b8e520498e1ce2173705f2f2becf94113aa086b248c0448bf`
- `RELIABILITY-LENS.md`: `2622169d2a0c528dbee0465d9e856c70684069d491c7dae17faece4b073c6d76`
- `DOMAIN-LENS.md`: `4f535154cbd8be9e6df108f71f8d6e0bf4e8c12f133ebef73b1430d9e419065c`
- `DESIGN-LENS.md`: `e6099f3821a78bd20a53e4252e0bc7a8841fc69e7d7c30950035acd866bfc47a`
- `SIMPLIFICATION-LENS.md`: `d3464faa5255f1141e893d1852b6760db65f997b1f115c59313626a707ecb2e6`
- `QUALITY-LENS.md`: `9e07202d260d0e38fa27d2c356bb5a6f37560aed9169ac2c89998fe8909aa15b`
- `HTML-REPORT.md`: `4034b1a50c158d0b1028f3899a09868e0c67507045356a8ae804502ee0e7602c`

Post-evaluation example normalization replaced JavaScript-specific examples
without changing the evaluated lifecycle, gates, Return, or completion clauses.
Current hashes after that wording-only edit are:

- `SKILL.md`: `c3c5b33475303290ffcfb71d8a5b133ab3e963649575ac47612526dc87ac586f`
- `SIMPLIFICATION-LENS.md`: `67f29c43298ebbd49494e9d26c11b9125446c4f0178664a2d30de4ed4a6a5ba4`
- `CODING-PRACTICES-LENS.md`: `bbc6b1479ef70356a857fb18d9797f9a1a93e5fc9b60d28cdedc17d6dfa27b24`

A later presentation-only edit made dark mode the required HTML theme without
changing the evaluated lifecycle. Current `HTML-REPORT.md`:
`c782b86c6cf4f20db329695e2f4ff186ce917730923a07b1240da3ab619e654f`.

A later ownership cleanup removed Audit Codebase's redundant Advisory Contract
branch; Quality Lens opportunities and Candidate Contract now own beneficial
non-defect changes. The candidate lifecycle is unchanged. Current hashes:

- `SKILL.md`: `b09530aa30aacfaac2ef0df100a4673cfbcf55d5fdae524dbfcd8f192e3e0091`
- `DEFECT-CONTRACT.md`: `af7955b3aab4fef31f1b79c03576505fba8abd7745ff68f308154a982cce25ec`
- `PERFORMANCE-LENS.md`: `06a478419edb0ca9b333c50f40b35af99b99f052f1c873fb7bde2954df92f389`
- `HTML-REPORT.md`: `4e1f6164825a508aed2050e9524a5eebb89957c476512d92540a48159530fc7e`

Token, latency, and cost telemetry were unavailable. No protocol deviations
occurred. Wrong-condition sampling started only after the entry-positive
contribution gate cleared.

## Residual Gap

This evaluation used a fixed simulated atlas and did not render or reopen a
real HTML report. Structural tests cover report anchors, state vocabulary,
relationship parity, and frozen composition artifacts; the first live
repository run remains the end-to-end transfer test.

## Later Author-Pass Scope

A later Author pass simplified the four-path workflow, made the HTML report
the sole durable state, expanded candidate routing, removed the
`$codebase-design` vocabulary load, and changed exact wording after the
samples above. Therefore `accept` applies to the registered candidate-lifecycle
contribution, not to the final file bytes or the unevaluated refinements.
Fresh behavioral sampling was not rerun.

Final structural-proof hashes:

- `SKILL.md`: `aa59508c4e7927392b9d9d96dfc064b2f9d82d3c93d4a5ff07eac306ea03304d`
- `CANDIDATE-CONTRACT.md`: `00fd6a8ca597643560fd8a183c4cde6ecb0b96fb5e5de86dba8b1827ed7ac07c`
- `DEFECT-CONTRACT.md`: `4655cac85f5942327f7cf49ef7b06f94b62c3db8617de522df9f9bc7fe7802b5`
- `HTML-REPORT.md`: `c263e125c0764a691807c4b1cf0510c07cfd01a2147f245f42efcaaa81737ed6`

## Subsequent Consistency Repair

A later consistency repair added same-report Map continuation, a complete
snapshot manifest with report self-exclusion, exact callee-compatible candidate
pickups, `$handoff` routing, and simpler local HTML navigation. It also aligned
`$simplify-code` admission with an analyzed report candidate. These changes
supersede the preceding structural hashes but were not part of the behavioral
samples. Fresh behavioral sampling was not rerun.

Current structural-proof hashes:

- `SKILL.md`: `848c79cf89b1c9978b5c9fc7fe61363d7b951fb1069aa5dc0eaabc47ecce2d27`
- `CANDIDATE-CONTRACT.md`: `6d69725386b164027d7f88fde43fc6b03101097baa1cf9e32d7223aed1b7a41c`
- `DEFECT-CONTRACT.md`: `4655cac85f5942327f7cf49ef7b06f94b62c3db8617de522df9f9bc7fe7802b5`
- `HTML-REPORT.md`: `299539d20bf7838896ed3696ecc61e050db693c4b0628e6b31196ac6b138b8e0`

## Concise Three-Path Author Pass

A later Author pass reduced the public workflow to `Map`, `Audit`, and
`Analyze`; folded returned-decision handling into Analyze; made New,
Continue, and Refresh Map branches; added one atomic Publish contract and one
state model; and replaced Audit-to-Handoff routing with the exact
`$grilling`/`$grill-with-docs` decision split. It also tightened defect,
opportunity, gap, comparison-baseline, candidate-grouping, and successor-route
burdens without changing Audit selection authority or product-mutation
boundaries.

The earlier behavioral samples do not prove these exact bytes. Fresh
behavioral sampling was not rerun, and no real repository HTML report was
rendered. Current structural checks cover package integrity, workflow wording,
relationship parity, and frozen composition projections only.

Current structural-proof hashes:

- `SKILL.md`: `e2bd07dda1d5bceaf9075b3051699cc8dca9e9e52ab22e9e9130f7b454110e4f`
- `CANDIDATE-CONTRACT.md`: `79686f010f44e013d187bfb74e042d196a1d06255b01b73a0abb2cb573d95fbb`
- `DEFECT-CONTRACT.md`: `2ef8669d7e319bca3c6d4eecae31e431f944048f73cd8008e4862308a6157927`
- `QUALITY-LENS.md`: `7139fd306a271475920cae7aa4c92b9f62e3505590e150f3066a0e46a82fd086`
- `RELIABILITY-LENS.md`: `20b98a4897655e07415ac972df7dbf468edec68994f0b0e092b03a742d8054ad`
- `DESIGN-LENS.md`: `526582d0c5d78a2ecede1880da50cfbfe482f051b30afbf8fe0d4291dbbd837e`
- `SIMPLIFICATION-LENS.md`: `027f9e8be37aee725b15aaca3086eeb34e5a9c1aa3a3fff831a740495678ee11`
- `PERFORMANCE-LENS.md`: `dc27fda486dd46a3640a199ec48a7573a6f13988f9cf42996527d68de05a0759`
- `HTML-REPORT.md`: `310f21433b2bf14534e2c0163f7f5d3f36a257687dbc8d30afc032be764e8505`
