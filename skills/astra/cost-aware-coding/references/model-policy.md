# Model policy

The standard route uses only this pair:

| Role | Model and effort | Owns |
| --- | --- | --- |
| Lead | GPT-6 Astra Medium | Shaping, consequential decisions, review, and acceptance |
| Implementer | GPT-5.6 Sol Medium | Repository investigation, implementation, checks, debugging, and corrections |

Suggest that the user change your setting to Astra XHigh only for a particularly
difficult design decision or intensive review, with the reason it is needed. The
user decides and applies any change to your setting; you cannot change it yourself.
A changed lead effort does not change implementation ownership.

Change the implementation route only for a demonstrated capability gap or failed
recovery under [Repair allowances](repairs.md). Missing requirements, invalid
acceptance criteria, and broken environments need resolution at their source.
For an implementation-reasoning failure, propose a Sol High replacement by default,
or XHigh when deeply coupled logic or difficult debugging justifies its cost.
Native follow-ups do not change effort; follow Repair allowances for accepted
replacement, custody, and context transfer. Do not silently take over implementation.

These assignments are benchmark-informed judgments and an experimental starting
policy, not proven specializations or savings guarantees. Read
[Evidence and limits](model-policy-evidence.md) only when comparing or revising
the policy.
