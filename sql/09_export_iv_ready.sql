COPY (
    SELECT
        employee_id,
        employer_id,
        employer_name,
        industry,
        employer_quality,

        age,
        education,
        education_issue,
        financial_literacy,

        employer_match_eligible,
        retirement_contribution_rate,

        annual_earnings,
        net_worth,
        household_debt,

        complete_iv_case
    FROM iv_panel
    WHERE complete_iv_case = 1
) TO 'data/output/iv_ready_panel.csv'
WITH (HEADER, DELIMITER ',');