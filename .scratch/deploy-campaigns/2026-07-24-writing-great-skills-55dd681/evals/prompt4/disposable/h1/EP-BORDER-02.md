# EP-BORDER-02

**Operation:** Audit  
**Coverage:** Assigned worker-visible record only  
**Disposition:** `needs-more-evidence`

The record supports requiring more evidence, but not acceptance. The control
defect appeared in all five fresh runs (B02-F1), while the candidate corrected
it in three matched runs and reproduced it in two (B02-F2). The fixed rule
requires correction in every matched run for `accept` and directs
`needs-more-evidence` when outcomes disagree without a critical regression
(B02-F3).

The available uncertainty signal is the split candidate outcome: three
corrections and two failures. The material decision margin is two unsuccessful
runs relative to the required five-of-five correction result. Because no new
critical or protected-behavior regression appeared (B02-F4), the record does
not support `reject-regression`; because both failing candidate runs followed
protocol (B02-F5), they cannot be discarded as protocol deviations. Extending
the evidence is therefore the supported disposition.

This record is sufficient to rule out acceptance under the fixed rule and to
select `needs-more-evidence`. It is not sufficient to claim general efficacy,
real-world prevalence, transfer to another task or execution configuration, or
a terminal contribution rejection; the supplied facts define no rejection
threshold for mixed non-regressive outcomes and provide no evidence on those
broader questions.
