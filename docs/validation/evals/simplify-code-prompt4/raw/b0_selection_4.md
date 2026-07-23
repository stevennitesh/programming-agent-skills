# Simplify Code decision

## Outcome

- **Mode:** one bounded read-only action decision
- **Region:** `src/request_parser.py`
- **Selected cut:** **A** — delete the unreachable v1 compatibility branch and remove `legacy_parse` as fallout.

## Why this cut is safe

The supported compatibility floor is v3+, and repository-wide callers, configuration, and runtime entries prove that no v1 path remains. The branch therefore preserves no supported behavior. Removing it needs no new commitment, interface, dependency, or ownership decision. The caller-facing fixture distinguishes parser outputs and is the observable seam that would detect a behavior change.

Candidate B is also credible because the project-owned `http_utils.normalize_headers` is an exact semantic match, but it remains residual work after this single-cut decision. Candidate C is not selected: it shortens a loop without removing a behavior family, ownership burden, or the larger proven obligations represented by A and B.

## Proof

- **Before:** the caller-facing fixture passes against the starting implementation containing the unreachable v1 branch and `legacy_parse`.
- **After:** the same fixture passes with that branch and helper removed.
- **Preserved contract:** all supported v3+ request parsing outputs remain unchanged at the caller-facing seam.
- **Reachability evidence:** repository-wide callers, configuration, and runtime entries contain no v1 use.

## Net obligations

Removed:

- one unsupported compatibility branch;
- one legacy behavior family;
- the private `legacy_parse` helper and its maintenance surface.

Introduced:

- none.

This is a strict reduction in branch families, concepts, and local implementation surface.

## State preservation

This was a read-only decision: no production path was edited and nothing was staged. The unrelated dirty `docs/notes.md` and staged `assets/logo.bin` remain untouched, so the starting and ending work-state shape is identical.

## Stop and residual

Stop after selecting and proving one coherent cut. Residual simplification opportunities are B (replace the local header normalizer with the exact project-owned implementation) and C (the loop rewrite); they are intentionally outside this one-cut result. No skipped proof or known contract risk remains within the selected decision.
