# Simplify Code result

**Mode and region:** One bounded, read-only simplification decision for `src/request_parser.py`.

**Selected coherent cut:** Delete the `version == "v1"` branch and the now-unused `legacy_parse` helper.

The supported compatibility floor is v3+, repository-wide callers, configuration, and runtime entries establish that no v1 caller remains, and the caller-facing fixture distinguishes parser outputs. This makes the v1 path an unsupported branch family rather than preserved behavior. Removing it needs no interface, dependency, ownership, or product commitment.

**Preserved contract and proof seam:** Parsing behavior for every supported protocol version (v3+) remains unchanged. The caller-facing fixture is the observable seam and already passes with this cut.

**Proof plan:**

- Before: from the exact starting worktree, record the ref, status, relevant diff, and staged-state shape; run the caller-facing fixture and confirm it passes while distinguishing parser outputs.
- After: apply only the selected deletion as an unstaged change; rerun the same fixture, then the nearest parser tests and proportionate repository checks; inspect the final diff and status to confirm only `src/request_parser.py` changed and the index is unchanged.

**Net-obligation account:** Removes one unsupported compatibility condition, one legacy implementation path, and one private helper. Introduces no concepts, branches, callers, tests, configuration, dependencies, coordination, or operational responsibilities. The reduction is therefore strict rather than a transfer of burden.

**Work-state preservation:** Leave the unrelated dirty `docs/notes.md` and staged `assets/logo.bin` byte-for-byte and index-for-index as found. The selected production change would remain unstaged. No tracker, installed-state, dependency, or external-state mutation is authorized.

**Stop and residual:** Stop after this single cut passes the focused and nearest relevant proof and the work-state check. The existing `http_utils.normalize_headers` replacement is a separate plausible simplification but is residual work because only one coherent cut is authorized; it remains owned by a future explicitly invoked Simplify Code task. The parsing-loop comprehension is rejected: it shortens presentation without removing an additional behavior, ownership, branch, or maintenance obligation.
