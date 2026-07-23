# Simplify Code result

**Mode and region:** One bounded, read-only simplification decision for `src/request_parser.py`.

**Selected coherent cut:** Remove the `version == "v1"` branch and the now-unreferenced `legacy_parse` helper. The authoritative compatibility floor is v3+, repository-wide callers, configuration, and entry paths contain no v1 caller, and the caller-facing fixture distinguishes the resulting output. This removes unsupported compatibility machinery without changing supported behavior or making a new product, interface, ownership, or dependency decision.

**Preserved contract and proof seam:** Parsing behavior for supported protocol versions v3+ remains unchanged. The caller-facing fixture is the observable seam capable of detecting a changed result.

**Before/after proof:**

- Before: run the caller-facing fixture against the exact starting state and require it to pass.
- After: apply only the selected deletion and its directly created fallout, then rerun the same fixture; the supplied evidence records that it passes. Follow with the nearest relevant parser tests and repository whitespace/diff checks before locking the cut.

**Net-obligation account:** Removed: one obsolete protocol branch, one legacy behavior family, and one private helper that maintainers would otherwise need to understand and preserve. Introduced: no concepts, branches, indirection, dependencies, callers, tests, configuration, operations, or ownership boundaries. The reduction is strict and is not based merely on line count.

**Work-state preservation:** This decision makes no filesystem or index change. `docs/notes.md` remains untouched, and the staged state of `assets/logo.bin` remains exactly as found. The starting ref and ending ref are identical; no invocation-created artifact exists. If executed, the production cut must remain unstaged and affect only `src/request_parser.py`.

**Stop and residual:** Stop after this single selected cut; no campaign was authorized. Candidate B remains a separate admissible residual for a future invocation because consolidating onto the project-owned normalizer is another coherent ownership cut with an exact semantic proof seam. Candidate C is rejected here: it reduces line count but leaves the same behavior branches and ownership obligations in place, so it does not establish a strict maintenance-obligation reduction. Residual ownership remains with the user for any later bounded Simplify Code invocation.
