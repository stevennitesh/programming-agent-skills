# Finding Contract

Use this contract to turn review observations into actionable findings. A
finding must have all five:

- **Anchor:** an accepted requirement, repository rule, or supported behavior;
- **Reach:** a concrete scenario inside the selected change;
- **Evidence:** direct evidence from the reviewed candidate or safe verification;
- **Impact:** a correctness, contract, data, operability, proof, or maintainability
  failure; and
- **Proportion:** the smallest required correction or proof fits that impact.

Reject disproved, speculative, preference-only, optional-hardening, and
unrelated pre-existing concerns. A smell, unfamiliar technique, test count, or
reviewer agreement does not establish a finding. An empty review is valid.

Record one finding per violated obligation with a stable ID when a later formal
remediation review may occur. Include severity, location, anchor and supported
scenario, decisive evidence, impact, and required correction or proof. Use:

- `P0` for catastrophic production, security, privacy, or data failure;
- `P1` for a blocking supported correctness or contract failure;
- `P2` for a significant supported edge, validation, release, or operator risk;
  and
- `P3` for a lower-impact actionable correctness or maintainability problem.

Missing evidence needed to decide required behavior makes the review
`incomplete`; unavailable optional verification becomes a stated limit. A
candidate's omission of required proof may itself be a finding when the five
conditions above hold.
