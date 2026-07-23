# Simplify Code result

Mode: one bounded cut in `src/request_parser.py`.

Selected cut: remove the unreachable `version == "v1"` branch and the now-unused `legacy_parse` helper.

The authoritative compatibility floor is v3+, and repository-wide caller, configuration, and entry-point evidence shows no v1 caller. The caller-facing fixture distinguishes parser outputs and therefore provides an observable seam capable of detecting a behavior change. This cut removes unsupported compatibility machinery without changing supported behavior, adding a dependency, changing an interface, or making a new ownership decision.

## Proof plan

- Before: run the caller-facing fixture against the exact starting state and require it to pass.
- Apply only the branch deletion and its directly created fallout, the unused `legacy_parse` helper.
- After: rerun the same caller-facing fixture, then the nearest focused parser tests and proportionate repository integrity checks. Require all results to match the passing baseline.
- Refresh the diff and status afterward, confirming that only `src/request_parser.py` is newly modified, the cut remains unstaged, and the pre-existing index is unchanged.

## Net-obligation account

Removed:

- one unsupported protocol-version branch;
- one legacy parsing behavior family;
- one private helper;
- the maintenance burden of reasoning about and preserving an uncallable v1 path.

Introduced: none. Supported v3+ parsing behavior, caller-visible outputs, interfaces, dependencies, configuration, and ownership remain unchanged. The result is therefore a strict net reduction in branches, concepts, and private implementation surface.

## Work-state preservation

Leave the unrelated dirty `docs/notes.md` untouched. Leave staged `assets/logo.bin` byte-for-byte unchanged and staged. Do not stage the simplification or disturb any other worktree, index, installed, tracker, or external state.

## Stop and residual

Stop after this single cut passes the before/after fixture and relevant checks and the refreshed status confirms work-state preservation. Candidate B remains a separate possible deduplication cut requiring its own baseline and proof cycle; Candidate C is residual presentation-only compression with no reduction in behavior, ownership, or maintenance obligations and is not selected. No further feature, bug, contract, interface, dependency, or ownership work is authorized.
