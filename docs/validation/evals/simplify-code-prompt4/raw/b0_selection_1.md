# Simplify Code result

- **Mode and region:** One bounded, read-only action decision for `src/request_parser.py`.
- **Selected cut:** A — delete the unreachable v1 branch and remove `legacy_parse`.
- **Reasoning:** Compatibility begins at v3, and repository-wide caller, configuration, and runtime-entry evidence proves that no v1 path remains. The caller-facing fixture distinguishes the supported outputs and passes with the branch and helper removed. This cut therefore preserves the stated contract while eliminating an obsolete branch family and its private helper. It requires no new dependency, interface, ownership decision, or behavioral commitment.
- **Before proof:** The caller-facing fixture passes on the fixed starting state and distinguishes the observable parser outputs.
- **After proof:** The same fixture passes for A after removal of the v1 branch and `legacy_parse`; supported v3+ outputs remain unchanged.
- **Net obligations:** Removes one unreachable compatibility branch, one legacy parsing concept, and one helper maintenance surface. Introduces no replacement abstraction, dependency, configuration, caller, or test obligation.
- **State preservation:** This is a read-only decision, so no paths, index entries, or external state were changed. In an implementation, the cut should remain unstaged; unrelated dirty `docs/notes.md` and staged `assets/logo.bin` must retain their exact starting state.
- **Stop and residual:** Stop after A because the requested mode permits one coherent cut. B remains a separate safe-looking ownership consolidation candidate for a future invocation. C is deferred because it only shortens presentation while leaving the stronger branch and ownership obligations intact. Residual ownership stays with Simplify Code if either candidate is later admitted as its own bounded cut.
