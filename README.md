@'
# Retirement Match IV SQL Pipeline

This project builds a SQL data-cleaning and panel-construction pipeline for a future instrumental variables analysis of retirement saving and household wealth.

The project uses intentionally messy synthetic data to practice common SQL data-engineering tasks, including raw CSV loading, string cleaning, type conversion, duplicate handling, joins, validation checks, and CSV export.

## Research Motivation

The motivating question is whether retirement saving increases household wealth.

The planned empirical design is:

- Treatment: retirement contribution rate
- Instrument: employer match eligibility
- Outcome: household net worth

The core IV logic is:

Employer match eligibility -> retirement contribution rate -> household net worth

## Pipeline

| Script | Purpose |
|---|---|
| `scripts/00_generate_synthetic_data.py` | Generate messy synthetic raw data |
| `scripts/run_sql.py` | Execute SQL files against DuckDB |
| `sql/01_load_raw_data.sql` | Load raw CSV files |
| `sql/02_clean_employees.sql` | Clean employee demographics |
| `sql/03_clean_employers.sql` | Clean employer data |
| `sql/04_clean_retirement_plans.sql` | Clean match eligibility and contribution rates |
| `sql/05_clean_household_finances.sql` | Clean net worth and debt |
| `sql/06_clean_earnings.sql` | Clean annual earnings |
| `sql/07_build_iv_panel.sql` | Build IV analysis panel |
| `sql/08_validation_checks.sql` | Validate row counts and IV logic |
| `sql/09_export_iv_ready.sql` | Export complete-case IV sample |

## How to Run

Generate raw synthetic data:

    python scripts\00_generate_synthetic_data.py

Run the full SQL pipeline:

    python scripts\run_sql.py sql\01_load_raw_data.sql sql\02_clean_employees.sql sql\03_clean_employers.sql sql\04_clean_retirement_plans.sql sql\05_clean_household_finances.sql sql\06_clean_earnings.sql sql\07_build_iv_panel.sql sql\08_validation_checks.sql sql\09_export_iv_ready.sql

## Output

The final exported file is:

    data/output/iv_ready_panel.csv

This file contains the complete-case sample suitable for future IV estimation.
'@ | Set-Content README.md