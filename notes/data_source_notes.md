# Historical Market Dataset

## Source

ISO New England — Zonal Information Archive

https://www.iso-ne.com/isoexpress/web/reports/pricing/-/tree/zone-info

## Selected workbook

2015 SMD Hourly Data

## Selected worksheet

SEMASS

## Selected variable

DA_LMP — Day-Ahead Locational Marginal Price

## Unit

USD/MWh

## Coverage

2015-01-01 to 2015-12-31

## Frequency

Hourly, hour-ending convention.

## Initial data-quality findings

Observations: 8,760
Unique dates: 365
Duplicate date-hour keys: 0
Missing DA_LMP: 0
Negative prices: 5
Zero prices: 7

## Notes

Original workbook is preserved under data/raw.

The extracted dataset is generated using:

src/02_inspect_market_data.py

Negative and zero prices are retained and flagged.