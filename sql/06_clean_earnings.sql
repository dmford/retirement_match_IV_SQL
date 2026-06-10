DROP TABLE IF EXISTS earnings_clean;

CREATE TABLE earnings_clean AS
SELECT
    employee_id,

    CASE
        WHEN annual_earnings IS NULL
             OR TRIM(CAST(annual_earnings AS VARCHAR)) = ''
            THEN NULL

        ELSE TRY_CAST(
            REPLACE(
                REPLACE(
                    TRIM(CAST(annual_earnings AS VARCHAR)),
                    '$',
                    ''
                ),
                ',',
                ''
            ) AS DOUBLE
        )
    END AS annual_earnings

FROM earnings_raw;