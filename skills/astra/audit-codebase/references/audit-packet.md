# Audit packet

Use the maintained [atlas.py](../scripts/atlas.py) rather than custom manifest or
provenance assembly. Prepare before investigation:

```text
python <atlas.py> prepare-audit --repo-root <repo> --report <report.html> --subsystem <id>
```

The command writes `audit-<id>.json` beside the report and returns its path.
It supplies `version`, `expected_report_sha256`, `subsystem_id`, and
`source_identity`. Existing packets are never overwritten. Use `--output` with a
new JSON filename when preparing another packet; a bare filename resolves beside
the report. Add
`--affected-subsystem <id>` or `--path <path>` for additional implicated source
or proof inputs. Repeat either option as needed.

Keep the generated mechanics. Fill `source_trace.summary` with the meaningful
behavior traced. Add findings and candidates when supported. A minimal defect
and its candidate use:

```json
{
  "source_trace": {"summary": "Traced identity validation through both entry paths."},
  "lenses": [{"class": "reliability", "state": "complete", "finding_ids": ["unchecked-entry"]}],
  "findings": [{
    "id": "unchecked-entry", "kind": "defect", "primary_class": "reliability",
    "title": "Alternate entry bypasses identity validation",
    "expectation": "Both entries must reject invalid identities.",
    "scenario": "Invalid identity enters through the alternate caller.",
    "locations": ["src/validation.py:42"],
    "evidence": ["Focused alternate-entry probe accepted the invalid identity."],
    "impact": "Invalid state reaches the write boundary.",
    "affected_scope": ["validation", "delivery"]
  }],
  "candidates": [{
    "id": "centralize-validation", "title": "Enforce validation at the shared write boundary",
    "primary_class": "design", "strength": "strong",
    "finding_ids": ["unchecked-entry"], "direction": "Move the check to the existing write owner."
  }]
}
```

These are the judgment fields to put in the generated packet, not a separate
responses format. Candidates link to findings; no copied evidence or problem
summary is required. Scope defaults to the union of their findings. Supply a
broader explicit `affected_scope` when the proposed change reaches further. Linked
finding scopes are always included; an explicit scope cannot narrow them.

A finding needs ID, kind, class, title, locations, decisive evidence, impact,
and affected scope. A defect also needs expectation and scenario; retained
complexity needs `protected_constraint`; a gap needs `missing_evidence`.
Optional direction, causal owner, confidence, severity, proof, or revisit detail
should serve the decision. Candidate risks, benefit, required proof, additional
evidence, problem context, and before/after comparison are optional.

Record only relevant lens assessments. `complete` needs evidence or finding IDs;
`evidence gap` and `not applicable` need a reason. Finding references reuse the
evidence. Omitted dimensions render as **not inspected**, not completed.
Optional trace lists, systemic findings, recommendation, and evidence limits add
scope-specific information; coverage counts come from the helper.

Publish through the existing guarded operation:

```text
python <atlas.py> audit-subsystem --repo-root <repo> --report <report.html> --manifest <packet.json>
python <atlas.py> check-report --repo-root <repo> --report <report.html>
```

An empty draft summary cannot publish. Source or report changes reject a stale
packet. If investigation expands the bound source, prepare a fresh packet and
inspect those inputs before relying on its snapshot. Reusing judgments requires
checking that they still apply; capturing a later snapshot alone is not renewed
evidence. Never bypass guards or silently refresh a completed packet.
