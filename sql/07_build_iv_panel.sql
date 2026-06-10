DROP TABLE IF EXISTS iv_panel;

CREATE TABLE iv_panel AS
WITH joined AS (
    SELECT
        e.employee_id,
        e.employer_id,
        emp.employer_name,
        emp.industry,
        emp.employer_quality,

        e.age,
        e.education,
        e.education_issue,
        e.financial_literacy,

        r.employer_match_eligible,
        r.retirement_contribution_rate,

        earn.annual_earnings,

        h.net_worth,
        h.household_debt,

        CASE
            WHEN r.employee_id IS NULL THEN 1 ELSE 0
        END AS missing_retirement_record,

        CASE
            WHEN earn.employee_id IS NULL THEN 1 ELSE 0
        END AS missing_earnings_record,

        CASE
            WHEN h.employee_id IS NULL THEN 1 ELSE 0
        END AS missing_finance_record

    FROM employees_clean e

    LEFT JOIN employers_clean emp
        ON e.employer_id = emp.employer_id

    LEFT JOIN retirement_plans_clean r
        ON e.employee_id = r.employee_id

    LEFT JOIN earnings_clean earn
        ON e.employee_id = earn.employee_id

    LEFT JOIN household_finances_clean h
        ON e.employee_id = h.employee_id
),

flagged AS (
    SELECT
        *,

        CASE
            WHEN employer_match_eligible IS NOT NULL
                 AND retirement_contribution_rate IS NOT NULL
                 AND annual_earnings IS NOT NULL
                 AND net_worth IS NOT NULL
                THEN 1
            ELSE 0
        END AS complete_iv_case

    FROM joined
)

SELECT *
FROM flagged;