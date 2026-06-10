CREATE OR REPLACE TABLE employees_raw AS
SELECT *
FROM read_csv_auto('data/raw/employees_raw.csv');

CREATE OR REPLACE TABLE employers_raw AS
SELECT *
FROM read_csv_auto('data/raw/employers_raw.csv');

CREATE OR REPLACE TABLE retirement_plans_raw AS
SELECT *
FROM read_csv_auto(
    'data/raw/retirement_plans_raw.csv',
    all_varchar = true
);

CREATE OR REPLACE TABLE household_finances_raw AS
SELECT *
FROM read_csv_auto('data/raw/household_finances_raw.csv');

CREATE OR REPLACE TABLE earnings_raw AS
SELECT *
FROM read_csv_auto('data/raw/earnings_raw.csv');