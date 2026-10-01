"""
Synthetic data generator for the Executive KPI Dashboard.
Simulates 12 months of credit card / payments business data
across 8 commercial partners in Mexico.

Author: Daniela Serrato
"""

import pandas as pd
import numpy as np
from datetime import date


# Partner configuration: name -> (base_accounts, base_revenue_mxn, base_delinquency, base_approval)
PARTNER_PROFILES = {
    "Walmart":        (45_000, 180_000_000, 0.045, 0.72),
    "Soriana":        (32_000, 120_000_000, 0.055, 0.70),
    "Liverpool":      (28_000, 150_000_000, 0.038, 0.68),
    "Coppel":         (30_000,  95_000_000, 0.085, 0.62),
    "Bodega Aurrera": (25_000,  70_000_000, 0.065, 0.66),
    "Chedraui":       (18_000,  55_000_000, 0.058, 0.69),
    "Suburbia":       (14_000,  45_000_000, 0.048, 0.74),
    "OXXO":           (10_000,  30_000_000, 0.095, 0.58),
}

# Seasonal multipliers by month index (0=Oct 2025 ... 11=Sep 2026)
# Dec(2)=spike, Jan(3)=dip, Jun-Jul(8-9) mild bump
SEASONAL_REVENUE = [1.00, 1.02, 1.25, 0.88, 0.92, 0.95, 0.98, 1.00, 1.05, 1.03, 1.00, 0.97]
SEASONAL_ACCOUNTS = [1.00, 1.01, 1.08, 0.96, 0.97, 0.98, 1.00, 1.01, 1.03, 1.02, 1.01, 1.00]
SEASONAL_DELINQUENCY = [1.00, 0.98, 0.90, 1.15, 1.12, 1.08, 1.05, 1.02, 1.00, 0.98, 0.97, 0.96]


def _month_range() -> list[date]:
    """Return first-of-month dates from Oct 2025 to Sep 2026."""
    return [date(2025, 10, 1) + pd.DateOffset(months=i) for i in range(12)]


def generate_monthly_data(seed: int = 42) -> pd.DataFrame:
    """
    Generate monthly partner-level KPI data.

    Returns a DataFrame with columns:
        month, partner, active_accounts, revenue_mxn,
        delinquency_rate, delinquency_over30, delinquency_over60, delinquency_over90,
        approval_rate, applications
    """
    rng = np.random.default_rng(seed)
    months = pd.date_range("2025-10-01", periods=12, freq="MS")
    rows = []

    for m_idx, month in enumerate(months):
        for partner, (base_acc, base_rev, base_del, base_apr) in PARTNER_PROFILES.items():
            # Apply seasonal factors + random noise
            noise_acc = rng.normal(1.0, 0.02)
            noise_rev = rng.normal(1.0, 0.03)
            noise_del = rng.normal(1.0, 0.05)
            noise_apr = rng.normal(1.0, 0.02)

            # Slight growth trend over the year (~0.5% per month)
            growth = 1.0 + m_idx * 0.005

            accounts = int(base_acc * SEASONAL_ACCOUNTS[m_idx] * noise_acc * growth)
            revenue = round(base_rev * SEASONAL_REVENUE[m_idx] * noise_rev * growth, 2)
            delinquency = np.clip(base_del * SEASONAL_DELINQUENCY[m_idx] * noise_del, 0.02, 0.15)
            approval = np.clip(base_apr * noise_apr, 0.45, 0.85)

            # Break delinquency into bands (over30 > over60 > over90)
            over30 = round(delinquency, 4)
            over60 = round(over30 * rng.uniform(0.35, 0.50), 4)
            over90 = round(over60 * rng.uniform(0.30, 0.45), 4)
            current = round(1.0 - over30, 4)

            # Applications derived from accounts and approval rate
            applications = int(accounts * rng.uniform(0.08, 0.15) / approval)

            rows.append({
                "month": month,
                "partner": partner,
                "active_accounts": accounts,
                "revenue_mxn": revenue,
                "delinquency_rate": round(over30, 4),
                "current_pct": current,
                "over_30_pct": round(over30 - over60, 4),
                "over_60_pct": round(over60 - over90, 4),
                "over_90_pct": over90,
                "approval_rate": round(approval, 4),
                "applications": applications,
            })

    df = pd.DataFrame(rows)
    df["month"] = pd.to_datetime(df["month"])
    return df


def generate_previous_year_data(seed: int = 99) -> pd.DataFrame:
    """
    Generate previous year data (Oct 2024 - Sep 2025) for YoY comparison.
    Uses a different seed and slightly lower baselines.
    """
    rng = np.random.default_rng(seed)
    months = pd.date_range("2024-10-01", periods=12, freq="MS")
    rows = []

    for m_idx, month in enumerate(months):
        for partner, (base_acc, base_rev, base_del, base_apr) in PARTNER_PROFILES.items():
            # Previous year: ~8-12% lower baselines
            py_factor = rng.uniform(0.85, 0.95)
            noise_rev = rng.normal(1.0, 0.03)

            accounts = int(base_acc * SEASONAL_ACCOUNTS[m_idx] * py_factor * rng.normal(1.0, 0.02))
            revenue = round(base_rev * SEASONAL_REVENUE[m_idx] * py_factor * noise_rev, 2)

            rows.append({
                "month": month,
                "partner": partner,
                "active_accounts": accounts,
                "revenue_mxn": revenue,
            })

    df = pd.DataFrame(rows)
    df["month"] = pd.to_datetime(df["month"])
    return df


if __name__ == "__main__":
    df = generate_monthly_data()
    print(f"Generated {len(df)} rows")
    print(df.head(16))
    print(f"\nTotal accounts range: {df.groupby('month')['active_accounts'].sum().min():,} - {df.groupby('month')['active_accounts'].sum().max():,}")
    print(f"Revenue range (MXN): ${df.groupby('month')['revenue_mxn'].sum().min():,.0f} - ${df.groupby('month')['revenue_mxn'].sum().max():,.0f}")
