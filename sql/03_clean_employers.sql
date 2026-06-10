CREATE OR REPLACE TABLE employers_clean AS
SELECT
    employer_id,
    TRIM(employer_name) AS employer_name,

    CASE
        WHEN industry IS NULL OR TRIM(industry) = '' THEN NULL
        WHEN LOWER(TRIM(industry)) IN (
            'healthcare',
            'manufacturing',
            'retail',
            'tech',
            'education'
        )
            THEN LOWER(TRIM(industry))
        ELSE NULL
    END AS industry,

    employer_quality
FROM employers_raw;