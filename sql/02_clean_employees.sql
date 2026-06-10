CREATE OR REPLACE TABLE employees_clean AS
WITH standardized AS (
    SELECT
        employee_id,
        employer_id,

        CASE
            WHEN age BETWEEN 18 AND 80 THEN age
            ELSE NULL
        END AS age,

        CASE
            WHEN LOWER(TRIM(education)) IN (
                'high_school',
                'some_college',
                'college',
                'graduate'
            )
                THEN LOWER(TRIM(education))
            ELSE NULL
        END AS education,

        CASE
            WHEN education IS NULL OR TRIM(education) = '' THEN 'blank'
            WHEN LOWER(TRIM(education)) = 'unknown' THEN 'unknown'
            WHEN LOWER(TRIM(education)) NOT IN (
                'high_school',
                'some_college',
                'college',
                'graduate'
            )
                THEN 'invalid'
            ELSE NULL
        END AS education_issue,

        financial_literacy
    FROM employees_raw
),

deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY employee_id
            ORDER BY employee_id
        ) AS row_num
    FROM standardized
)

SELECT
    employee_id,
    employer_id,
    age,
    education,
    education_issue,
    financial_literacy
FROM deduplicated
WHERE row_num = 1;