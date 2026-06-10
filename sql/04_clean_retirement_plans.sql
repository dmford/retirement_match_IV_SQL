DROP TABLE IF EXISTS retirement_plans_clean;

CREATE TABLE retirement_plans_clean AS
SELECT DISTINCT
    TRY_CAST(employee_id AS BIGINT) AS employee_id,

    CASE
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'yes' THEN 1
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'y' THEN 1
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = '1' THEN 1
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'eligible' THEN 1
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'no' THEN 0
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'n' THEN 0
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = '0' THEN 0
        WHEN LOWER(TRIM(CAST(employer_match_eligible AS VARCHAR))) = 'not eligible' THEN 0
        ELSE NULL
    END AS employer_match_eligible,

    CASE
        WHEN TRIM(CAST(retirement_contribution_rate AS VARCHAR)) = '' THEN NULL
        WHEN RIGHT(TRIM(CAST(retirement_contribution_rate AS VARCHAR)), 1) = '%' THEN
            TRY_CAST(
                REPLACE(TRIM(CAST(retirement_contribution_rate AS VARCHAR)), '%', '')
                AS DOUBLE
            ) / 100
        ELSE
            TRY_CAST(TRIM(CAST(retirement_contribution_rate AS VARCHAR)) AS DOUBLE)
    END AS retirement_contribution_rate

FROM retirement_plans_raw;