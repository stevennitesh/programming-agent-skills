# EP-BORDER-03

- Status: `complete`
- Operation: Audit (read-only semantic judgment)
- Coverage: the supplied `EP-BORDER-03` record under the fixed task and execution configuration
- Disposition: `needs-more-evidence`

The control deficit appeared in all six fresh runs (`B03-F1`), so the contribution comparison is admissible. The six candidate-minus-control improvements are `[2, 3, 2, 3, 2, 3]` (`B03-F2`): minimum 2, maximum 3, and spread 1. Three observations touch the boundary and three exceed it. Because acceptance requires every improvement to be greater than 2, and the rule explicitly sends boundary-touching results to more evidence (`B03-F3`), this record does not support `accept`.

No critical failure or protocol deviation supports an early regression disposition (`B03-F4`). The uncertainty signal is the repeatable split between boundary-touching and above-boundary results; the material decision margin is zero at the worst result because the minimum equals, rather than clears, the boundary. Extending is therefore required, and a second realistic fixture family is available under the same fixed execution configuration (`B03-F5`).

The supplied facts are sufficient for `needs-more-evidence`, but not for a terminal efficacy judgment beyond this fixed task and configuration. They do not establish results for the available second family, wrong-condition behavior, applicability or prevalence, transfer to other configurations, or whether additional sampling will clear or continue to touch the boundary.
