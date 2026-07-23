# Simplify Code result

**Mode and region:** One bounded, read-only action decision for `src/request_parser.py`.

**Selected cut:** A — delete the unreachable v1 branch and `legacy_parse`.

The compatibility floor is v3+, and repository-wide callers, configuration, and runtime entries establish that no v1 path remains. The caller-facing fixture distinguishes the observable outputs and passes with the deletion. This removes an obsolete branch family and its dedicated helper without changing supported behavior or creating a new commitment.

**Before proof:** The supplied caller-facing fixture passes on the fixed starting state and distinguishes parser outputs. Repository-wide evidence shows no v1 caller, configuration, or entry path.

**After proof:** The same caller-facing fixture passes after A. Supported v3+ output behavior is preserved.

**Net obligations:** Removes one unreachable compatibility branch, one legacy helper, and the associated v1 reasoning surface. Introduces no concept, dependency, interface, configuration, test obligation, or ownership transfer.

**State preservation:** This is a read-only decision; no production path, index entry, dependency state, or external state was changed. The unrelated dirty `docs/notes.md` and staged `assets/logo.bin` remain untouched.

**Deferred candidates:** B also has matching fixture evidence, but it would introduce a new module dependency and shift normalization ownership, which is outside this simplification cut. C shortens a loop but leaves the substantive obsolete compatibility and duplication burdens intact; line-count reduction alone is not the strongest maintenance reduction.

**Stop and residual:** Stop after A because the requested mode permits one cut. The remaining normalization duplication belongs to a separate ownership/dependency decision; the loop rewrite is a lower-value residual simplification. No proof was skipped within the supplied fixed packet.
