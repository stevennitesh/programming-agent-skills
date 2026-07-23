Mode: one bounded simplification in `src/request_parser.py`.

Selected cut: remove the `version == "v1"` branch and the now-unreferenced `legacy_parse` helper. Supported compatibility begins at v3, and repository-wide callers, configuration, and runtime entries show no v1 caller. This therefore removes obsolete implementation rather than changing an accepted interface or behavior.

Proof plan:

- Before: record the starting ref, status, relevant diff, and staged-state shape; run the caller-facing parser fixture against the untouched starting state and require it to pass.
- After: apply only the selected deletion as an unstaged change; rerun the identical fixture, then the nearest request-parser tests and repository whitespace/diff checks. Confirm all supported v3+ outputs remain identical and refresh the diff and work-state inspection.

Net-obligation account: one compatibility branch family and one private legacy parsing path disappear. No concept, dependency, interface, configuration, caller, test obligation, or ownership boundary is introduced. This is a strict reduction in branches and private implementation surface.

Work-state preservation: the proposed patch changes only `src/request_parser.py` and remains unstaged. Existing `docs/notes.md` changes remain untouched, and staged `assets/logo.bin` remains byte-for-byte staged as found. No tracker, dependency, installed state, or external state changes are authorized. For this read-only decision, no repository paths or index entries were changed.

Stop and residual: stop after this single cut passes the focused and nearest relevant proofs and the final work-state check. The duplicate header normalizer remains a separate admissible residual for a future invocation because its removal is independently bounded; the parsing-loop comprehension is left in place because it only shortens presentation without removing an additional maintenance obligation.
