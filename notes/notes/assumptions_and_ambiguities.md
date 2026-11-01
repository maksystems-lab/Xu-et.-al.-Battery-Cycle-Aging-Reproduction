| Issue                       | What the paper says                                    | What we must investigate                                 |
|-----------------------------|--------------------------------------------------------|----------------------------------------------------------|
| Initial total energy $E^0$  | Defines initial energy                                 | Exact case-study value                                   |
| Terminal energy $E^{final}$ | Requires final total energy to be at least $E^{final}$ | Exact chosen value                                       |
| Initial segment allocation  | Appendix gives an ordered allocation rule              | How it relates to the annual case-study initialisation   |
| Eq. 16                      | Uses an inequality                                     | Must not replace it with equality without justification  |
| Binary variable $v_t$       | Prevents simultaneous charging and discharging         | Whether relaxation is valid for the actual price data    |
| Time indexing               | Energy state evolves across intervals                  | Resolve $t=0$, $t=1$ and terminal indexing before coding |
| Annual operation            | Daily optimisation horizons of 24 hours                | How initial and terminal states are treated between days |