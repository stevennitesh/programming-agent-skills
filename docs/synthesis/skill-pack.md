# Pack Composition Contract

This is the sole composition-decision owner for one Fresh Composition Epoch.
It records the five-part contract that an epoch owner has decided; research
packets, per-skill campaigns, validators, and schedulers may supply evidence or
enforce structure but cannot select skills, assign semantic authority, decide
admission or H1, or accept the integrated result.

The canonical record begins as an inactive draft. Freezing requires a named
epoch, complete fixed point, bounded research record, acceptance scenarios,
load budget, one primary capability owner, one role per selected skill, exact
relationship rows, resolved essential gaps and collisions, and an acyclic
campaign proof graph. A frozen revision yields fingerprinted immutable
skill-local slices. Any semantic amendment increments the revision exactly
once, returns a `behavior-decision-gap`, and stales proof only for affected
skills and their downstream dependents.

<!-- pack-composition-contract:v1:begin -->
```json
{
  "capabilities": [],
  "epoch_header": {
    "acceptance_scenarios": [],
    "campaign_proof_graph": [],
    "composition_epoch_id": null,
    "contract_revision": 0,
    "epoch_lock": null,
    "exclusions": [],
    "fixed_point": {
      "environment": null,
      "repository_tree": null,
      "timestamp": null
    },
    "integration_result": {
      "decision": null,
      "evidence_pointer": null
    },
    "intended_pack_outcome": null,
    "load_budget_policy": {
      "ceiling_or_class": null,
      "metric": null,
      "status": "gap"
    },
    "research_bound": {
      "catalog_reconciliation_passes": 1,
      "independent_passes": 1,
      "named_gap_passes": 1
    },
    "schema_version": 1,
    "scope": [],
    "source_pointers": [],
    "status": "draft"
  },
  "exclusions_collisions_gaps": [],
  "relationships": [],
  "selected_skills": []
}
```
<!-- pack-composition-contract:v1:end -->

The draft selects nothing and authorizes no campaign. Integration results are
limited to `integration-accepted`, `needs-more-evidence`, or `blocked`, each
with an evidence pointer recorded by the epoch owner. Compatibility retirement,
installation, automated scheduling or acceptance, and Git delivery remain
outside this owner.
