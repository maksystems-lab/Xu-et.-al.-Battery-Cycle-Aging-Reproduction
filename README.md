# Battery Cycle-Aging-Aware Dispatch Optimisation

## Research objective

Independently reproduce the piecewise-linear
battery cycle-aging optimisation method proposed
by Xu et al. (2018).

## Reference paper

Factoring the Cycle Aging Cost of Batteries
Participating in Electricity Markets.

## Market scenario

ISO New England 2015
Southeast Massachusetts
Day-Ahead Market

## Programming environment

Python
Pyomo
HiGHS
pandas
NumPy
Matplotlib

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