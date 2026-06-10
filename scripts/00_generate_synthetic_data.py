from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260610
N_EMPLOYEES = 2_000
N_EMPLOYERS = 80

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def make_employers(rng):
    employer_ids = np.arange(1, N_EMPLOYERS + 1)
    employer_quality = rng.normal(0, 1, N_EMPLOYERS)

    return pd.DataFrame({
        "employer_id": employer_ids,
        "employer_name": [f"Employer {i}" for i in employer_ids],
        "industry": rng.choice(
            ["healthcare", "manufacturing", "retail", "tech", "education"],
            size=N_EMPLOYERS,
        ),
        "employer_quality": employer_quality.round(3),
    })


def make_employees(rng, employers):
    employee_ids = np.arange(1, N_EMPLOYEES + 1)

    return pd.DataFrame({
        "employee_id": employee_ids,
        "employer_id": rng.choice(employers["employer_id"], size=N_EMPLOYEES),
        "age": rng.integers(25, 61, size=N_EMPLOYEES),
        "education": rng.choice(
            ["high_school", "some_college", "college", "graduate"],
            size=N_EMPLOYEES,
            p=[0.25, 0.25, 0.35, 0.15],
        ),
        "financial_literacy": rng.normal(0, 1, size=N_EMPLOYEES).round(3),
    })


def make_retirement_plans(rng, employees, employers):
    df = employees.merge(employers[["employer_id", "employer_quality"]], on="employer_id")

    match_latent = -0.2 + 0.8 * df["employer_quality"] + rng.normal(0, 1, len(df))
    match = (match_latent > 0).astype(int)

    contribution = (
        0.03
        + 0.04 * match
        + 0.015 * df["financial_literacy"]
        + 0.0008 * (df["age"] - 25)
        + rng.normal(0, 0.03, len(df))
    )

    contribution = np.clip(contribution, 0, 0.20)

    return pd.DataFrame({
        "employee_id": df["employee_id"],
        "employer_match_eligible": match,
        "retirement_contribution_rate": contribution.round(4),
    })


def make_earnings(rng, employees, employers):
    df = employees.merge(employers[["employer_id", "employer_quality"]], on="employer_id")

    education_bonus = df["education"].map({
        "high_school": 0,
        "some_college": 8_000,
        "college": 20_000,
        "graduate": 35_000,
    })

    earnings = (
        35_000
        + 900 * (df["age"] - 25)
        + education_bonus
        + 7_500 * df["employer_quality"]
        + rng.normal(0, 12_000, len(df))
    )

    earnings = np.clip(earnings, 18_000, None)

    return pd.DataFrame({
        "employee_id": df["employee_id"],
        "annual_earnings": earnings.round(2),
    })


def make_household_finances(rng, employees, plans, earnings):
    df = employees.merge(plans, on="employee_id").merge(earnings, on="employee_id")

    education_bonus = df["education"].map({
        "high_school": 0,
        "some_college": 10_000,
        "college": 35_000,
        "graduate": 70_000,
    })

    net_worth = (
        -25_000
        + 2.2 * df["annual_earnings"]
        + 500_000 * df["retirement_contribution_rate"]
        + 2_000 * (df["age"] - 25)
        + education_bonus
        + 20_000 * df["financial_literacy"]
        + rng.normal(0, 60_000, len(df))
    )

    debt = rng.normal(35_000, 20_000, len(df))

    return pd.DataFrame({
        "employee_id": df["employee_id"],
        "net_worth": net_worth.round(2),
        "household_debt": debt.round(2),
    })


def mess_text_columns(df, rng):
    messy = df.copy()

    for col in messy.select_dtypes(include=["object", "string"]).columns:
        messy[col] = messy[col].astype(str)

        upper_mask = rng.random(len(messy)) < 0.15
        lower_mask = rng.random(len(messy)) < 0.15
        space_mask = rng.random(len(messy)) < 0.10

        messy.loc[upper_mask, col] = messy.loc[upper_mask, col].str.upper()
        messy.loc[lower_mask, col] = messy.loc[lower_mask, col].str.lower()
        messy.loc[space_mask, col] = "  " + messy.loc[space_mask, col] + "  "

    return messy


def add_duplicates(df, rng, n=10):
    duplicate_rows = df.sample(n, random_state=SEED)
    return pd.concat([df, duplicate_rows], ignore_index=True)


def mess_employees(df, rng):
    messy = mess_text_columns(df, rng)

    missing_education = rng.random(len(messy)) < 0.02
    invalid_education = rng.random(len(messy)) < 0.01
    invalid_age = rng.random(len(messy)) < 0.01

    messy.loc[missing_education, "education"] = ""
    messy.loc[invalid_education, "education"] = "unknown"
    messy.loc[invalid_age, "age"] = rng.choice([17, 99], size=invalid_age.sum())

    return add_duplicates(messy, rng)


def mess_employers(df, rng):
    messy = mess_text_columns(df, rng)

    missing_industry = rng.random(len(messy)) < 0.03
    messy.loc[missing_industry, "industry"] = ""

    return messy


def mess_retirement_plans(df, rng):
    messy = df.copy()

    match_map = {
        1: rng.choice(["yes", "Yes", "Y", "1", " eligible "], size=len(messy)),
        0: rng.choice(["no", "No", "N", "0", " not eligible "], size=len(messy)),
    }

    messy["employer_match_eligible"] = [
        match_map[value][i] for i, value in enumerate(messy["employer_match_eligible"])
    ]

    messy["retirement_contribution_rate"] = messy[
        "retirement_contribution_rate"
    ].astype(str)

    percent_mask = rng.random(len(messy)) < 0.30
    messy.loc[percent_mask, "retirement_contribution_rate"] = (
        (
            messy.loc[percent_mask, "retirement_contribution_rate"].astype(float)
            * 100
        )
        .round(2)
        .astype(str)
        + "%"
    )

    missing_contribution = rng.random(len(messy)) < 0.02
    messy.loc[missing_contribution, "retirement_contribution_rate"] = ""

    return add_duplicates(messy, rng)


def mess_money_column(series, rng):
    messy = series.astype(str)

    dollar_mask = rng.random(len(messy)) < 0.35
    comma_mask = rng.random(len(messy)) < 0.35

    messy.loc[comma_mask] = messy.loc[comma_mask].astype(float).map(lambda x: f"{x:,.2f}")
    messy.loc[dollar_mask] = "$" + messy.loc[dollar_mask]

    return messy


def mess_earnings(df, rng):
    messy = df.copy()
    messy["annual_earnings"] = mess_money_column(messy["annual_earnings"], rng)

    missing_earnings = rng.random(len(messy)) < 0.01
    messy.loc[missing_earnings, "annual_earnings"] = ""

    return add_duplicates(messy, rng)


def mess_household_finances(df, rng):
    messy = df.copy()

    messy["net_worth"] = mess_money_column(messy["net_worth"], rng)
    messy["household_debt"] = mess_money_column(messy["household_debt"], rng)

    missing_debt = rng.random(len(messy)) < 0.03
    messy.loc[missing_debt, "household_debt"] = ""

    return add_duplicates(messy, rng)


def main():
    rng = np.random.default_rng(SEED)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    employers = make_employers(rng)
    employees = make_employees(rng, employers)
    plans = make_retirement_plans(rng, employees, employers)
    earnings = make_earnings(rng, employees, employers)
    finances = make_household_finances(rng, employees, plans, earnings)

    tables = {
        "employers_raw.csv": mess_employers(employers, rng),
        "employees_raw.csv": mess_employees(employees, rng),
        "retirement_plans_raw.csv": mess_retirement_plans(plans, rng),
        "earnings_raw.csv": mess_earnings(earnings, rng),
        "household_finances_raw.csv": mess_household_finances(finances, rng),
    }

    for filename, df in tables.items():
        df.to_csv(RAW_DIR / filename, index=False)

    print(f"Wrote {len(tables)} raw CSV files to {RAW_DIR}")


if __name__ == "__main__":
    main()