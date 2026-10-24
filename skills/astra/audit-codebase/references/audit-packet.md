# Audit packet

Use the maintained [atlas.py](../scripts/atlas.py) rather than custom manifest or
provenance assembly. Prepare before investigation:

```text
python <atlas.py> prepare-audit --repo-root <repo> --report <report.html> --subsystem <id>
```

The command writes `audit-<id>.json` beside the report and returns its path.
It supplies `version`, `expected_report_sha256`, `subsystem_id`, `source_identity`,
and a semantic publication guard. Existing packets are never overwritten. Use `--output` with a
new JSON filename when preparing another packet; a bare filename resolves beside
the report. Add
`--affected-subsystem <id>` or `--path <path>` for additional implicated source
or proof inputs. Repeat either option as needed. Include every affected mapped
owner before publication; if investigation reaches another owner, reprepare with
that owner and inspect its inputs before relying on the expanded snapshot.

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
and affected scope. Its additional fields depend on the claim:

| Kind | Required detail | Conditional detail |
| --- | --- | --- |
| `defect` | `expectation`, `scenario` | `severity` |
| `opportunity` | No additional required fields | `scenario` and `severity` are not allowed. |
| `retained complexity` | `protected_constraint` | `ceiling`, `revisit_trigger` |
| `gap` | `missing_evidence` | `boundary_reason`, `reentry` |

Text such as `impact`, `scenario`, `missing_evidence`, and `evidence_limits` is a
JSON string. `locations`, `evidence`, `affected_scope`, `proof`, `finding_ids`,
and candidate `risks` and `required_proof` are arrays of nonempty strings.
Required finding arrays and required text must be nonempty. Omit unsupported
optional detail rather than filling it with placeholder claims.
Optional direction, causal owner, confidence, severity, proof, or revisit detail
should serve the decision. Candidate risks, benefit, required proof, additional
evidence, problem context, and before/after comparison are optional.

Record only relevant lens assessments. `complete` needs evidence or finding IDs;
`evidence gap` and `not applicable` need a reason. Finding references reuse the
evidence; each referenced finding's `primary_class` must equal the lens's `class`.
Use the lens's direct
`evidence` for a cross-cutting observation classified under another lens; a
candidate may link findings of different classes. Omitted dimensions render as
**not inspected**, not completed.
Optional trace lists, systemic findings, recommendation, and evidence limits add
scope-specific information; coverage counts come from the helper.

Publish through the existing guarded operation:

```text
python <atlas.py> audit-subsystem --repo-root <repo> --report <report.html> --manifest <packet.json>
python <atlas.py> check-report --repo-root <repo> --report <report.html>
```

An empty draft summary cannot publish. Source drift, ownership changes, and
same-target publication reject a stale packet. Prepared packets can advance their
report guard across unrelated publications or display edits when their semantic
guards still match. Their investigated source snapshots remain unchanged. Raw
manifests without a prepared guard still require the exact report revision.
If investigation expands the bound source, prepare a fresh packet and
inspect those inputs before relying on its snapshot. Reusing judgments requires
checking that they still apply; capturing a later snapshot alone is not renewed
evidence. Never bypass guards or silently refresh a completed packet.

For several selected owners, repeat `--subsystem`; each gets a packet from the
same report revision. Omit `--output` for multiple selections so the helper names
each packet. Use [Prepared work and verification](workflow.md) for
coordinator publication, analysis and outcome preparation, and narrow follow-ups.
