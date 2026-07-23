---
name: research
description: Research one source question against primary sources into a cited repo-local Markdown note. Use for durable source evidence when the user requests a note or a caller authorizes one note path.
---

# Research

**Research delegates reading, not judgment.**

**Authorized note: Admit -> Lock -> Trace -> Scout -> Classify -> Gate -> Write -> Verify -> Return.**

**Inline or blocker: Admit -> Lock -> Trace -> Scout -> Classify -> Gate -> Verify -> Return.**

## Boundary

Research owns one question, source legwork, evidence judgment, a claim ledger,
one cited note, and its pointer. The caller owns the supported decision or
artifact and all other mutations.

Write exactly one tracked note only at the user's request or a
caller-authorized repo-local path. Otherwise leave the repo unchanged and
return cited inline evidence or a blocker.

## Process

1. **Admit.** Proceed only when one bounded question can be answered from
   inspectable sources and the material `Lock` fields are known. Infer obvious
   direct-user fields. Otherwise return `Status: not-admitted`, every failed or
   missing predicate, settled information, actual need shape, available
   evidence, `Tracked mutation: none`, and return owner without researching or
   writing. A direct result may recommend one existing owner only when the
   match is deterministic; a caller result returns the classification without
   choosing or invoking its next route.
2. **Lock.** Name the question, supported decision or artifact, scope,
   freshness requirement, target repo, authorized note path, write authority,
   and return owner. The path must be publishable under the repo's convention
   without another tracked mutation.
3. **Trace.** Trace every load-bearing claim to its owning authoritative source: repo
   source, tests, config, governing docs, or ADRs; versioned official docs,
   specifications, tagged source, or release notes; the issuing standards
   body; the original paper, dataset, and method; or a methodologically relevant
   systematic review for an aggregate claim. Use non-owning secondary sources
   only for discovery.
4. **Scout.** When independent lanes materially improve breadth or speed, start
   direct fresh-context read-only scouts with `fork_turns="none"`, one complete
   research contract, and one lane each. Require claims, citations, authority,
   version or date, conflicts, and gaps. Scouts never edit files, mutate
   external state, or spawn; exclude parent conclusions and peer results. The
   main agent alone judges evidence and writes the note. When continuity matters
   more than independence, fork only the minimum necessary recent context and
   do not call the result independent.
5. **Classify.** Mark every load-bearing claim `supported`, `conflicted`, or
   `unknown`; attach its source, authority, and freshness.
6. **Gate.** Proceed to Write only when every load-bearing claim is classified,
   the best authority and version or date are recorded, conflicts and gaps are
   explicit, and further search repeats evidence or cannot close a documented
   gap. A blocked note records attempted lanes and missing evidence.
7. **Write.** Use the repo's research-note convention or
   `docs/research/<slug>.md`. If publication requires another tracked mutation,
   return a blocker to the caller rather than exceeding one-note authority.
   Preserve the contract and render only the applicable semantic fields:

   - question, research status `answered`, `conflicted`, or `blocked`,
     supported caller use, scope, and freshness;
   - concise answer with adjacent claim-level citations;
   - evidence depth and stopping basis;
   - material conflicts, unknowns, and limits;
   - source identity, authority, version or date, and supported claim; and
   - caller-use boundary and return owner.

   Omit empty conditional sections. A conflicted or blocked note is durable
   evidence, not a settled answer.
8. **Verify.** Verify every returned claim has a citation and compare work state
   so the run preserved pre-existing work. For a written note, also reread it,
   verify every ledger claim has a citation, confirm the authorized path exists,
   and require that this run changed only that note.
9. **Return.** For a written note, return its path, one-paragraph answer, status,
   applicable evidence depth and stopping basis, material limits, caller-use
   boundary, mutation result, and return owner. For a no-write result, return
   cited inline evidence or the blocker with the same applicable fields and
   `Tracked mutation: none`. When caller-invoked, return to that caller; it owns
   the supported decision and next route. For an admitted standalone result,
   return `Next: none` when the answer is complete; otherwise recommend at most
   one next route.
