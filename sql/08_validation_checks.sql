-- Row counts for core cleaned tables
SELECT 'employees_clean' AS table_name, COUNT(*) AS n FROM employees_clean
UNION ALL
SELECT 'employers_clean', COUNT(*) FROM employers_clean
UNION ALL
SELECT 'retirement_plans_clean', COUNT(*) FROM retirement_plans_clean
UNION ALL
SELECT 'household_finances_clean', COUNT(*) FROM household_finances_clean
UNION ALL
SELECT 'earnings_clean', COUNT(*) FROM earnings_clean
UNION ALL
SELECT 'iv_panel', COUNT(*) FROM iv_panel;

-- Check one row per employee in iv_panel
SELECT
    employee_id,
    COUNT(*) AS n
FROM iv_panel
GROUP BY employee_id
HAVING COUNT(*) > 1;

-- Check required IV variables
SELECT
    SUM(CASE WHEN employer_match_eligible IS NULL THEN 1 ELSE 0 END) AS missing_instrument,
    SUM(CASE WHEN retirement_contribution_rate IS NULL THEN 1 ELSE 0 END) AS missing_treatment,
    SUM(CASE WHEN net_worth IS NULL THEN 1 ELSE 0 END) AS missing_outcome,
    SUM(CASE WHEN annual_earnings IS NULL THEN 1 ELSE 0 END) AS missing_earnings,
    SUM(CASE WHEN complete_iv_case = 1 THEN 1 ELSE 0 END) AS complete_iv_cases
FROM iv_panel;

-- Contribution rate bounds
SELECT
    MIN(retirement_contribution_rate) AS min_contribution_rate,
    MAX(retirement_contribution_rate) AS max_contribution_rate
FROM iv_panel;

-- First-stage sanity check
SELECT
    employer_match_eligible,
    COUNT(*) AS n,
    AVG(retirement_contribution_rate) AS avg_contribution_rate
FROM iv_panel
WHERE complete_iv_case = 1
GROUP BY employer_match_eligible
ORDER BY employer_match_eligible;

-- Reduced-form descriptive check
SELECT
    employer_match_eligible,
    COUNT(*) AS n,
    AVG(net_worth) AS avg_net_worth
FROM iv_panel
WHERE complete_iv_case = 1
GROUP BY employer_match_eligible
ORDER BY employer_match_eligible;