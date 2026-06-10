DROP TABLE IF EXISTS household_finances_clean;

CREATE TABLE household_finances_clean AS
SELECT DISTINCT
    TRY_CAST(employee_id AS BIGINT) AS employee_id,

    CASE
        WHEN net_worth IS NULL OR TRIM(CAST(net_worth AS VARCHAR)) = '' THEN NULL
        ELSE TRY_CAST(
            REPLACE(
                REPLACE(TRIM(CAST(net_worth AS VARCHAR)), '$', ''),
                ',',
                ''
            ) AS DOUBLE
        )
    END AS net_worth,

    CASE
        WHEN household_debt IS NULL OR TRIM(CAST(household_debt AS VARCHAR)) = '' THEN NULL
        ELSE TRY_CAST(
            REPLACE(
                REPLACE(TRIM(CAST(household_debt AS VARCHAR)), '$', ''),
                ',',
                ''
            ) AS DOUBLE
        )
    END AS household_debt

FROM household_finances_raw;