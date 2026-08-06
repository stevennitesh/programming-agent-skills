# Deploy Campaign Automation Separates Mechanical Evidence From Semantic Decisions

Deploy Campaigns require repeated identity, fixture-isolation, proof,
installation, and delivery checks. Leaving all of that bookkeeping in prose is
costly and error-prone, while allowing automation to interpret evidence or
advance the campaign would transfer judgment away from the campaign owner.

**Status**: accepted

The campaign owner exclusively settles skill intent, minimum viability,
research credibility and applicability, hypotheses, synthesis, evaluation
rubrics and scoring, proof sufficiency, pruning, promotion, and lifecycle
decisions. Campaign automation may write only reproducible mechanical evidence
state: campaign and lease identity, bounded artifact identities, schema and
path checks, fixture and payload isolation, deterministic proof receipts,
cache validity, parity, and invalidation of receipts whose declared inputs
changed.

The campaign manifest is a control-plane record, not a second synthesis
document. It stores exact identities and pointers to semantic owners instead
of copying their rationale. Automation may execute only owner-registered,
allowlisted deterministic proof and may reuse it only when the complete
identity tuple matches. It checks usable `.tmp` evidence before rerunning, but
temporary data is never promotion-critical and cannot satisfy explicitly fresh
behavioral sampling.

The ordinary automation surface stays narrow: start one exact campaign and
verify its declared stage from its exact manifest. Status, release, low-level
checks, and forced reruns remain recovery or debugging operations. Installation
and Git delivery retain their existing mutation owners.

## Considered Options

- Keep every check manual. Rejected because repeated hashing, fixture
  construction, cache inspection, cohort comparison, and parity bookkeeping
  consume campaign attention and have caused avoidable protocol failures.
- Automate campaign judgment and stage progression. Rejected because test
  results and evidence require semantic interpretation, and automated
  progression would blur authority and make failures look like decisions.
- Create separate automation per deploy stage. Rejected because duplicated
  command and schema rules would drift and increase ceremony.

## Consequences

- One versioned campaign-artifact owner defines stage profiles, proof profiles,
  identity algorithms, receipts, invalidation, and stable mechanical statuses.
- Verification is cost-tiered and fail-fast between tiers. Exact receipts are
  reused before deterministic proof is rerun.
- Resume, Repair, and Restart remain distinct. Changed identities stale
  dependent proof without rewriting prior receipts or choosing a semantic
  reopening route.
- Behavioral agents, source assessment, scoring, acceptance, installation,
  staging, commits, and pushes remain outside campaign-artifact automation.
- Existing automation is partial until implemented and verified against this
  boundary.
