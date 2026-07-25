# EP-BORDER-01

- **Disposition:** `needs-more-evidence`
- **Operation and coverage:** Read-only Audit of the supplied entry-positive quality-lift record under the fixed execution configuration.
- **Decisive observations:** The control showed the registered deficit in all five fresh runs (B01-F1). Candidate-minus-control improvements were `[3, 1, 4, 0, 3]`, with minimum `0`, maximum `4`, and spread `4` (B01-F2). Three observations exceed `2`, while two do not. The fixed rule permits `accept` only when every observation exceeds `2`, and mixed results require more evidence (B01-F3). No critical failure appeared, but the observations cross the fixed boundary (B01-F4).
- **Sufficiency:** This record does not support `accept` because not every observed improvement exceeds `2`. It also does not support a regression disposition because no critical failure was observed. The fixed mixed-result branch therefore requires more evidence, and one additional matched wave is available under the same configuration (B01-F5).
- **Limits:** The judgment is limited to the supplied task, facts, and fixed execution configuration. The record provides no basis to infer behavior under other models, hosts, tasks, runtimes, or configurations, or to claim real-world prevalence.
