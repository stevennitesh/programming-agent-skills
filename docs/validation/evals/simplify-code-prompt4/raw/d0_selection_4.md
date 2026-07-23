# Simplify Code result

**Mode and region:** one-cut mode, bounded to `src/request_parser.py`.

**Selected coherent cut:** remove the `version == "v1"` branch and the now-unused `legacy_parse` helper. The authoritative compatibility floor is v3+, repository-wide callers, configuration, and runtime entries show no v1 use, and the caller-facing fixture distinguishes the observable outputs. This removes an unsupported compatibility branch rather than changing a supported contract.

**Proof plan and evidence:**

- Before: run the caller-facing fixture against the exact starting state and record the starting ref, status, relevant diff, and index shape.
- After: rerun that same fixture, then the nearest request-parser tests and proportionate repository checks. The supplied result says the distinguishing fixture passes with this cut.
- Lock: refresh the diff and status; verify that only the v1 branch and its newly unused helper disappeared, supported v3+ outputs remain unchanged, and no invocation artifacts were created.

**Net-obligation account:** removed one unsupported protocol-version branch, one legacy parsing path, and one private helper. Introduced no concepts, branches, indirection, dependencies, interfaces, configuration, tests, or operational duties. The result is therefore a strict reduction in caller and maintainer obligations.

**Work-state preservation:** this is a read-only action decision, so no synthetic source was modified. During execution, the cut would remain unstaged in `src/request_parser.py`; the unrelated dirty `docs/notes.md` and staged `assets/logo.bin` would remain byte-for-byte and index-for-index as found.

**Stop and residual:** stop after this single bounded cut is proved and locked. Replacing the local header normalizer is a separate coherent simplification and is deferred to a future explicitly admitted Simplify Code task. The loop comprehension is rejected because it reduces line count without removing a behavior, ownership, or maintenance obligation. No dependency, interface, public-contract, feature, or bug work is included.
