from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260610
N_EMPLOYEES = 2_000
N_EMPLOYERS = 80

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def make_employers(rng: np.random.Generator) -> pd.DataFrame:
    employer_ids = np.arange(1, N_EMPLOYERS + 1)

    employer_quality = rng.normal(0, 1, N_EMPLOYERS)

    df = pd.DataFrame(
        {
            "employer_id": employer_ids,
            "employer_name": [f"Employer {i}" for i in employer_ids],
            "industry": rng.choice(
                ["healthcare", "manufacturing", "retail", "tech", "education"],
                size=N_EMPLOYERS,
            ),
            "employer_quality": employer_quality.round(3),
        }
    )

    return df


def make_employees(rng: np.random.Generator, employers: pd.DataFrame) -> pd.DataFrame:
    employee_ids = np.arange(1, N_EMPLOYEES + 1)

    employer_id = rng.choice(employers["employer_id"], size=N_EMPLOYEES)

    age = rng.integers(25, 61, size=N_EMPLOYEES)
    education = rng.choice(
        ["high_school", "some_college", "college", "graduate"],
        size=N_EMPLOYEES,
        p=[0.25, 0.25, 0.35, 0.15],
    )

    financial_literacy = rng.normal(0, 1, size=N_EMPLOYEES)

    df = pd.DataFrame(
        {
            "employee_id": employee_ids,
            "employer_id": employer_id,
            "age": age,
            "education": education,
            "financial_literacy": financial_literacy.round(3),
        }
    )

    return df


def make_retirement_plans(
    rng: np.random.Generator,
    employees: pd.DataFrame,
    employers: pd.DataFrame,
) -> pd.DataFrame:
    df = employees.merge(employers[["employer_id", "employer_quality"]], on="employer_id")

    match_latent = -0.2 + 0.8 * df["employer_quality"] + rng.normal(0, 1, len(df))
    employer_match_eligible = (match_latent > 0).astype(int)

    contribution_latent = (
        0.03
        + 0.04 * employer_match_eligible
        + 0.015 * df["financial_literacy"]
        + 0.0008 * (df["age"] - 25)
        + rng.normal(0, 0.03, len(df))
    )

    retirement_contribution_rate = np.clip(contribution_latent, 0, 0.20)

    plan = pd.DataFrame(
        {
            "employee_id": df["employee_id"],
            "employer_match_eligible": employer_match_eligible,
            "retirement_contribution_rate": retirement_contribution_rate.round(4),
        }
    )

    return plan


def make_earnings(
    rng: np.random.Generator,
    employees: pd.DataFrame,
    employers: pd.DataFrame,
) -> pd.DataFrame:
    df = employees.merge(employers[["employer_id", "employer_quality"]], on="employer_id")

    education_income_bonus = df["education"].map(
        {
            "high_school": 0,
            "some_college": 8_000,
            "college": 20_000,
            "graduate": 35_000,
        }
    )

    annual_earnings = (
        35_000
        + 900 * (df["age"] - 25)
        + education_income_bonus
        + 7_500 * df["employer_quality"]
        + rng.normal(0, 12_000, len(df))
    )

    annual_earnings = np.clip(annual_earnings, 18_000, None)

    earnings = pd.DataFrame(
        {
            "employee_id": df["employee_id"],
            "annual_earnings": annual_earnings.round(2),
        }
    )

    return earnings


def make_household_finances(
    rng: np.random.Generator,
    employees: pd.DataFrame,
    plans: pd.DataFrame,
    earnings: pd.DataFrame,
) -> pd.DataFrame:
    df = (
        employees.merge(plans, on="employee_id")
        .merge(earnings, on="employee_id")
    )

    education_wealth_bonus = df["education"].map(
        {
            "high_school": 0,
            "some_college": 10_000,
            "college": 35_000,
            "graduate": 70_000,
        }
    )

    net_worth = (
        -25_000
        + 2.2 * df["annual_earnings"]
        + 500_000 * df["retirement_contribution_rate"]
        + 2_000 * (df["age"] - 25)
        + education_wealth_bonus
        + 20_000 * df["financial_literacy"]
        + rng.normal(0, 60_000, len(df))
    )

    finances = pd.DataFrame(
        {
            "employee_id": df["employee_id"],
            "net_worth": net_worth.round(2),
            "household_debt": rng.normal(35_000, 20_000, len(df)).round(2),
        }
    )

    return finances


def add_raw_messiness(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    messy = df.copy()

    for col in messy.select_dtypes(include="object").columns:
        messy[col] = messy[col].astype(str)

        upper_mask = rng.random(len(messy)) < 0.15
        lower_mask = rng.random(len(messy)) < 0.15
        space_mask = rng.random(len(messy)) < 0.10

        messy.loc[upper_mask, col] = messy.loc[upper_mask, col].str.upper()
        messy.loc[lower_mask, col] = messy.loc[lower_mask, col].str.lower()
        messy.loc[space_mask, col] = "  " + messy.loc[space_mask, col] + "  "

    if len(messy) > 20:
        duplicate_rows = messy.sample(10, random_state=SEED)
        messy = pd.concat([messy, duplicate_rows], ignore_index=True)

    return messy


def main() -> None:
    rng = np.random.default_rng(SEED)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    employers = make_employers(rng)
    employees = make_employees(rng, employers)
    plans = make_retirement_plans(rng, employees, employers)
    earnings = make_earnings(rng, employees, employers)
    finances = make_household_finances(rng, employees, plans, earnings)

    tables = {
        "employers_raw.csv": employers,
        "employees_raw.csv": employees,
        "retirement_plans_raw.csv": plans,
        "earnings_raw.csv": earnings,
        "household_finances_raw.csv": finances,
    }

    for filename, df in tables.items():
        messy_df = add_raw_messiness(df, rng)
        messy_df.to_csv(RAW_DIR / filename, index=False)

    print(f"Wrote {len(tables)} raw CSV files to {RAW_DIR}")


if __name__ == "__main__":
    main()