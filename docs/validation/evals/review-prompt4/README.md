# Review Prompt 4 Raw Evidence

This directory preserves the exact 95 disposable Prompt 4 outputs under
`raw/`. `SHA256SUMS` gives one SHA-256 identity and repository-relative pointer
for every sample.

The classification is exhaustive:

| Class | Pointer pattern | Count | Use |
| --- | --- | ---: | --- |
| Valid D0/B0 comparisons | `raw/D0-*/{control,candidate}*/sample-*.txt`, excluding `raw/D0-ROUTE/{control,candidate}/` | 70 | Seven valid five-sample control/candidate comparisons; Route uses the `control-redo` and `candidate-redo` arms |
| Separate viability lanes | `raw/{B0-SUITE,INVOCATION,REMEDIATION}/candidate/sample-*.txt` | 15 | Five samples each for the integrated B0 suite, invocation, and protocol-correct remediation |
| Superseded Route attempt | `raw/D0-ROUTE/{control,candidate}/sample-*.txt` | 10 | Retained protocol deviation; supports no judgment |

Counts, hashes, and paths are proof of artifact identity only. The audit record
owns the protocol, rubric, judgments, limitations, and accepted claims.
