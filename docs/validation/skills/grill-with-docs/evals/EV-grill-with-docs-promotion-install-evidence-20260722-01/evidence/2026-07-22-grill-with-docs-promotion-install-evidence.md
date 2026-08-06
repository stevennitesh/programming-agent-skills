# Grill With Docs Promotion And Install Evidence

Date: 2026-07-22

Status: complete.

## Promotion Identity

Deploy Prompt 5 promoted behaviorally accepted candidate `09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7` byte-for-byte to `skills/custom/grill-with-docs`. Candidate bytes and affected claims were unchanged, so Prompt 4 evidence was reused without another behavioral wave.

The promoted skill is explicit-only and admits only direct user invocation. Wayfinder, Triage, and Improve Codebase now recommend it and stop; each caller may resume only in a later invocation with the direct-user result. Skill Router, Research, and To Questionnaire remain recommendation-only, and Audit Codebase remains suggestion-only.

## Canonical Proof

Before experimental cleanup:

```text
accepted experimental tree hash
09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7

promoted canonical tree hash
09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7

python -m scripts.validate_skills
Skill validation passed.

python -m pytest
192 passed, 4 skipped

git diff --check
passed

git diff --cached --check
passed
```

## Experimental Lifecycle

Only `skills/experimental/grill-with-docs/` and its one manifest entry were removed. Every other experimental package and manifest entry was preserved. The hash-identified pre-prune evaluation fixture remains durable validation evidence, not active experimental runtime.

After cleanup:

```text
python -m scripts.validate_skills
Skill validation passed.

python -m pytest
191 passed, 4 skipped
```

The one-test reduction is the removed experimental Grill With Docs package contract; canonical package and relationship proof now own the active surface.

## Managed Installation And Parity

The managed dry run reported exactly four changed mirrors: Grill With Docs and the three caller skills whose edges changed. The install synchronized all 25 already-managed skills without changing the global bootstrap. A second dry run reported all 25 unchanged.

| Skill | Canonical and installed tree hash |
| --- | --- |
| `grill-with-docs` | `09438242574437c91ed631a1dd59010f3c02752b51b8eb93d096259fab65def7` |
| `wayfinder` | `6b606e0669a40506abf9d99e9bc7f0f58a92cdfaa6cc521bb95f2423b947cd48` |
| `triage` | `d27fbda8a313a8c1723ecdb4b6bc640b55f8beded6c43eca362c8a2051ff2c6d` |
| `improve-codebase` | `f5ba91156eadf494b27c3caa2ff5a488bb8a69ef0ee0498c360af1932c65e0af` |

Canonical and installed hashes match for every changed mirror. No Git delivery was performed.
