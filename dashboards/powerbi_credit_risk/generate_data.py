"""
Credit Risk Portfolio Monitor — Data Generator
Generates 4 CSV files for Power BI dashboard.
Author: Daniela Serrato
"""

import numpy as np
import pandas as pd
from itertools import product

np.random.seed(42)

OUTPUT_DIR = "."

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
MONTHS = pd.date_range("2024-10-01", "2026-09-01", freq="MS")
MONTH_STRS = [m.strftime("%Y-%m") for m in MONTHS]

PARTNERS = [
    "BradesCard", "CrediMax", "FinanzaPlus", "NovaPay",
    "SolCredito", "AztecaFin", "LinkPago", "MetroBank",
]

DELINQUENCY_BANDS = [
    "Current", "1-29", "30-59", "60-89", "90-119", "120+", "Write-off",
]

# Risk profile per partner: (base_current_pct, avg_balance_per_acct, volatility)
PARTNER_PROFILES = {
    "BradesCard":  (0.78, 18_500, 0.10),
    "CrediMax":    (0.82, 22_000, 0.08),
    "FinanzaPlus": (0.74, 15_000, 0.13),
    "NovaPay":     (0.80, 20_000, 0.09),
    "SolCredito":  (0.70, 12_000, 0.15),
    "AztecaFin":   (0.76, 16_000, 0.12),
    "LinkPago":    (0.84, 25_000, 0.07),
    "MetroBank":   (0.81, 21_000, 0.08),
}


def seasonal_factor(month_idx: int) -> float:
    """Seasonal multiplier: worse in Dec-Jan (holiday spending), better mid-year."""
    month_of_year = MONTHS[month_idx].month
    seasonal = {
        1: 1.06, 2: 1.03, 3: 1.00, 4: 0.98, 5: 0.97, 6: 0.96,
        7: 0.97, 8: 0.98, 9: 1.00, 10: 1.01, 11: 1.03, 12: 1.08,
    }
    return seasonal[month_of_year]


def stress_factor(month_idx: int) -> float:
    """COVID-like stress event around months 6-8 of 2025 (indices ~8-11)."""
    # 2025-06 = index 8, 2025-07 = 9, 2025-08 = 10
    stress_center = 9
    distance = abs(month_idx - stress_center)
    if distance <= 3:
        return 1.0 + 0.18 * max(0, 1 - distance / 3.5)
    return 1.0


# ─────────────────────────────────────────────
# 1. portfolio_monthly.csv
# ─────────────────────────────────────────────
def generate_portfolio_monthly() -> pd.DataFrame:
    rows = []
    for mi, month in enumerate(MONTH_STRS):
        sf = seasonal_factor(mi)
        stf = stress_factor(mi)

        for partner in PARTNERS:
            base_current, avg_bal, vol = PARTNER_PROFILES[partner]

            # Total accounts for this partner (grows ~1% monthly)
            total_accounts = int(12_000 * (1 + 0.01 * mi) + np.random.normal(0, 200))

            # Delinquency distribution (shifted by stress + seasonal)
            delinq_shift = (sf - 1) * 0.5 + (stf - 1) * 1.2
            noise = np.random.normal(0, vol * 0.3)

            current_pct = max(0.55, min(0.92, base_current - delinq_shift + noise))
            remaining = 1 - current_pct

            # Split remaining across bands with decay
            band_weights = np.array([0.35, 0.25, 0.15, 0.10, 0.08, 0.07])
            band_weights = band_weights / band_weights.sum() * remaining

            pcts = np.concatenate([[current_pct], band_weights])
            pcts = np.clip(pcts, 0.005, None)
            pcts = pcts / pcts.sum()

            for bi, band in enumerate(DELINQUENCY_BANDS):
                accts = max(1, int(total_accounts * pcts[bi]))
                # Balance per account varies by band (delinquent = higher avg)
                bal_mult = 1.0 + bi * 0.12
                balance = round(accts * avg_bal * bal_mult * (1 + np.random.normal(0, 0.05)), 2)
                rows.append({
                    "month": month,
                    "partner": partner,
                    "delinquency_band": band,
                    "accounts": accts,
                    "balance": balance,
                })

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUTPUT_DIR}/portfolio_monthly.csv", index=False)
    print(f"portfolio_monthly.csv: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 2. vintage_curves.csv
# ─────────────────────────────────────────────
def generate_vintage_curves() -> pd.DataFrame:
    cohorts = pd.date_range("2024-10-01", "2026-03-01", freq="MS")  # 18 cohorts
    rows = []
    for cohort in cohorts:
        cohort_str = cohort.strftime("%Y-%m")
        # Base default rate varies by cohort (stress cohorts are worse)
        cohort_idx = (cohort.year - 2024) * 12 + cohort.month - 10
        base_terminal = 0.045 + 0.008 * np.random.randn()

        # Stress cohorts (originated mid-2025) have higher defaults
        if 8 <= cohort_idx <= 12:
            base_terminal += 0.02

        max_mob = min(12, len(MONTHS) - cohort_idx)
        for mob in range(1, max_mob + 1):
            # S-curve: fast rise months 1-6, plateau 8-12
            t = mob / 12.0
            cum_rate = base_terminal * (1 - np.exp(-4 * t)) / (1 - np.exp(-4))
            cum_rate += np.random.normal(0, 0.002)
            cum_rate = round(max(0.001, cum_rate) * 100, 3)

            rows.append({
                "origination_month": cohort_str,
                "months_on_books": mob,
                "cumulative_default_rate": cum_rate,
            })

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUTPUT_DIR}/vintage_curves.csv", index=False)
    print(f"vintage_curves.csv: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 3. roll_rates.csv
# ─────────────────────────────────────────────
def generate_roll_rates() -> pd.DataFrame:
    from_bands = ["Current", "1-29", "30-59", "60-89", "90-119", "120+"]
    to_bands = ["Current", "1-29", "30-59", "60-89", "90-119", "120+", "Write-off"]

    # Base transition matrix (from_band -> to_band probabilities)
    # Rows: from_bands, Cols: to_bands
    base_matrix = {
        "Current": {"Current": 0.92, "1-29": 0.06, "30-59": 0.015, "60-89": 0.003, "90-119": 0.001, "120+": 0.0005, "Write-off": 0.0005},
        "1-29":    {"Current": 0.35, "1-29": 0.30, "30-59": 0.25, "60-89": 0.06, "90-119": 0.02, "120+": 0.01, "Write-off": 0.01},
        "30-59":   {"Current": 0.10, "1-29": 0.12, "30-59": 0.28, "60-89": 0.35, "90-119": 0.08, "120+": 0.04, "Write-off": 0.03},
        "60-89":   {"Current": 0.05, "1-29": 0.05, "30-59": 0.08, "60-89": 0.22, "90-119": 0.40, "120+": 0.12, "Write-off": 0.08},
        "90-119":  {"Current": 0.02, "1-29": 0.02, "30-59": 0.03, "60-89": 0.05, "90-119": 0.18, "120+": 0.45, "Write-off": 0.25},
        "120+":    {"Current": 0.01, "1-29": 0.01, "30-59": 0.01, "60-89": 0.02, "90-119": 0.03, "120+": 0.32, "Write-off": 0.60},
    }

    rows = []
    for mi, month in enumerate(MONTH_STRS):
        sf = seasonal_factor(mi)
        stf = stress_factor(mi)
        stress_shift = (stf - 1) * 0.5 + (sf - 1) * 0.3

        for fb in from_bands:
            for tb in to_bands:
                base_rate = base_matrix[fb][tb]

                # During stress: increase forward rolls, decrease cures
                if tb > fb:  # rolling forward
                    rate = base_rate * (1 + stress_shift)
                elif tb < fb:  # curing
                    rate = base_rate * (1 - stress_shift * 0.5)
                else:  # staying same
                    rate = base_rate

                rate += np.random.normal(0, base_rate * 0.08)
                rate = round(max(0.001, min(0.99, rate)) * 100, 2)

                rows.append({
                    "month": month,
                    "from_band": fb,
                    "to_band": tb,
                    "roll_rate": rate,
                })

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUTPUT_DIR}/roll_rates.csv", index=False)
    print(f"roll_rates.csv: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# 4. kpi_summary.csv
# ─────────────────────────────────────────────
def generate_kpi_summary(portfolio_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mi, month in enumerate(MONTH_STRS):
        mdf = portfolio_df[portfolio_df["month"] == month]

        total_accounts = mdf["accounts"].sum()
        total_balance = round(mdf["balance"].sum(), 2)

        wo_balance = mdf[mdf["delinquency_band"] == "Write-off"]["balance"].sum()
        ncl_rate = round(wo_balance / total_balance * 100, 3) if total_balance > 0 else 0

        over_30_bands = ["30-59", "60-89", "90-119", "120+", "Write-off"]
        over_30_bal = mdf[mdf["delinquency_band"].isin(over_30_bands)]["balance"].sum()
        over_30_rate = round(over_30_bal / total_balance * 100, 3) if total_balance > 0 else 0

        over_90_bands = ["90-119", "120+", "Write-off"]
        over_90_bal = mdf[mdf["delinquency_band"].isin(over_90_bands)]["balance"].sum()
        over_90_rate = round(over_90_bal / total_balance * 100, 3) if total_balance > 0 else 0

        sf = seasonal_factor(mi)
        stf = stress_factor(mi)
        approval_rate = round(max(40, min(78, 72 - (stf - 1) * 80 - (sf - 1) * 30 + np.random.normal(0, 1.5))), 1)

        avg_credit_limit = round(35_000 * (1 + 0.005 * mi) + np.random.normal(0, 500), 0)

        rows.append({
            "month": month,
            "total_accounts": total_accounts,
            "total_balance": total_balance,
            "ncl_rate": ncl_rate,
            "over_30_rate": over_30_rate,
            "over_90_rate": over_90_rate,
            "approval_rate": approval_rate,
            "avg_credit_limit": avg_credit_limit,
        })

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUTPUT_DIR}/kpi_summary.csv", index=False)
    print(f"kpi_summary.csv: {len(df)} rows")
    return df


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating Credit Risk Portfolio data...\n")
    portfolio_df = generate_portfolio_monthly()
    generate_vintage_curves()
    generate_roll_rates()
    generate_kpi_summary(portfolio_df)
    print("\nDone! All CSVs generated.")
