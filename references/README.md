# Research References

## Primary paper

Xu, B. et al. (2018).

Factoring the Cycle Aging Cost of Batteries
Participating in Electricity Markets.

arXiv:1707.04567

https://arxiv.org/abs/1707.04567

Used as the primary reference for the battery
cycle-aging-aware dispatch reproduction.

## Current progress

### 1. Mathematical implementation

Implemented:
- Battery cycle-depth stress function.
- Piecewise-linear marginal aging-cost calculation.
- Numerical verification against published parameters.

### 2. Historical market data analysis

Dataset:
ISO-NE 2015 SMD Hourly Data.

Region:
Southeast Massachusetts (SEMASS).

Market:
Day-Ahead.

Variable:
DA_LMP.

Unit:
USD/MWh.

Implemented:
- Workbook inspection.
- Historical price extraction.
- Price distribution analysis.
- Annual price visualisation.
- Negative-price investigation.
- Monthly statistical summaries.

### 3. Remaining work

- Resolve market timestamp conventions.
- Develop the baseline battery dispatch optimisation.
- Integrate piecewise-linear aging costs.
- Reproduce published results.
- Implement Rainflow validation.
- Investigate an original extension.