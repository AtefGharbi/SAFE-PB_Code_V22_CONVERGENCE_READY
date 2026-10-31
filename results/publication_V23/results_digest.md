# SAFE-PB experiment results digest

- Run status: `passed`
- Publication eligible: `False`
- Inferential unit: `training_seed`
- Independent training seeds: `10`

**Do not copy these numbers into the manuscript. This is an engineering/pilot run, not publication evidence.**

## Binding Voltage

| Method | Social loss | PAR | CVaR90 | Voltage violation min | Discomfort variance |
|---|---:|---:|---:|---:|---:|
| SAFE-PB | -4097 | 1.566 | -3507 | 583.2 | 0.1101 |
| SAFE-PB_no_CVaR | -4019 | 1.566 | -3442 | 581.4 | 0.1099 |
| SAFE-PB_no_fairness | -4103 | 1.566 | -3511 | 583.2 | 0.1099 |
| SAFE-PB_no_safety | -4176 | 1.584 | -3514 | 666 | 0.02672 |
| SAFE-PB_single_price | -605.7 | 1.566 | -492.4 | 582.6 | 0.11 |
| No-DR | 1352 | 1.539 | 1490 | 678.6 | 0.0009706 |
| TOU | -1201 | 1.531 | -1035 | 677.4 | 0.01231 |
| Tabular_Q_learning | -1.036e+04 | 1.564 | -9098 | 650.4 | 0.1004 |
| MPC | -1.039e+04 | 1.572 | -9125 | 644.4 | 0.1347 |

## Nominal

| Method | Social loss | PAR | CVaR90 | Voltage violation min | Discomfort variance |
|---|---:|---:|---:|---:|---:|
| SAFE-PB | -4178 | 1.584 | -3517 | 0 | 0.02659 |
| SAFE-PB_no_CVaR | -4100 | 1.583 | -3450 | 0 | 0.02648 |
| SAFE-PB_no_fairness | -4182 | 1.584 | -3522 | 0 | 0.02648 |
| SAFE-PB_no_safety | -4179 | 1.584 | -3515 | 0 | 0.02672 |
| SAFE-PB_single_price | -719.1 | 1.583 | -609.3 | 0 | 0.02667 |
| No-DR | 1352 | 1.539 | 1490 | 0 | 0.0009706 |
| TOU | -1201 | 1.531 | -1035 | 0 | 0.01231 |
| Tabular_Q_learning | -1.036e+04 | 1.564 | -9098 | 0 | 0.1004 |
| MPC | -1.039e+04 | 1.572 | -9125 | 0 | 0.1347 |

## Multiplicity-corrected paired results

Significant SAFE-PB contrasts among selected outcomes: 41 of 80 (Holm-adjusted p < 0.05).
