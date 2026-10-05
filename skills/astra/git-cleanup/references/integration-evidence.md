# Integration evidence

Read when ancestry is inconclusive after squash, rebase, or cherry-pick, or when
distinct branch work needs a disposition. Choose enough evidence to distinguish
integrated content from work that would otherwise be lost.

## Match the work to the destination

Identify the source tip, relevant common base, and destination revision. When a
PR supplies integration evidence, confirm its repository, base, reviewed head,
merge state, and resulting commit. A merged PR does not cover commits added to
its source branch afterward. Compare the current candidate with what was actually
accepted, not only its branch name.

Use ancestry as a useful first check. Rewritten history may require patch
equivalence, comparisons of the relevant trees or paths, and inspection of the
combined result. A squash can combine several source commits into one patch;
per-commit patch matching alone can miss that integration.

Exact tree equality establishes matching file content at those revisions, but
is not required when the destination also contains unrelated work. Explain the
remaining differences and whether they contain unique work. Conversely, a familiar
commit message or a small diff does not establish equivalence. Preserve explicit
requirements to retain commit history or experimental alternatives even when
their final content matches elsewhere.

Distinguish historical integration from current behavior. A later intentional
revert or replacement can make an old branch's content absent from the current
target without making it a missing feature to restore. Follow the accepted current
direction and preserve evidence needed to explain a superseded candidate.

## Resolve unique or uncertain work

For distinct changes, assess their purpose, current applicability, dependencies,
and verification against the user's requested scope. Retain useful portions through
the appropriate integration method when authorized; verify their behavior on the
current target. Existing tests on the old branch do not prove the composed result.

If intent or equivalence cannot be established, retain the candidate and identify
the specific missing evidence or decision. Continue with independent candidates
whose disposition is supported. Do not turn a general cleanup request into
permission to discard unexplained differences.

Carry the exact assessed source and destination identities into integration or
deletion. A moving ref invalidates conclusions about its new work until reassessed.
