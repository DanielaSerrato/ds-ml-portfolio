"""
Executive KPI Dashboard — Payments / Fintech
Streamlit application for monitoring credit card portfolio health
across commercial partners.

Author: Daniela Serrato
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

from data_generator import generate_monthly_data, generate_previous_year_data, PARTNER_PROFILES

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Executive KPI Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Color palette & constants
# ---------------------------------------------------------------------------
NAVY = "#0F1E3D"
GREEN = "#28c840"
RED = "#ff5f57"
YELLOW = "#febc2e"
LIGHT_GRAY = "#E8EAF0"
CARD_BG = "#1A2744"
TEXT_WHITE = "#F0F2F6"
CHART_COLORS = [NAVY, "#1B5E96", "#2882C8", "#5AAEF2", GREEN, YELLOW, RED, "#A855F7"]
DELINQUENCY_COLORS = {"Vigente": GREEN, "+30 dias": YELLOW, "+60 dias": "#FF9F43", "+90 dias": RED}
TARGET_APPROVAL = 0.65

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
    /* Global */
    .stApp {{
        background-color: #F7F8FC;
    }}
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {NAVY};
    }}
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] span {{
        color: {TEXT_WHITE} !important;
    }}
    /* Metric cards */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG};
        padding: 16px 20px;
        border-radius: 10px;
        color: {TEXT_WHITE};
    }}
    div[data-testid="stMetric"] label {{
        color: {LIGHT_GRAY} !important;
        font-size: 0.85rem !important;
    }}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
        color: {TEXT_WHITE} !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }}
    /* Compact block spacing */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }}
    /* Header */
    .dashboard-header {{
        color: {NAVY};
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 0;
        letter-spacing: -0.02em;
    }}
    .dashboard-sub {{
        color: #5A6880;
        font-size: 0.9rem;
        margin-top: 0;
        margin-bottom: 1.2rem;
    }}
    /* Section titles */
    .section-title {{
        color: {NAVY};
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
        padding-bottom: 4px;
        border-bottom: 2px solid {NAVY};
        display: inline-block;
    }}
    /* Footer bar */
    .footer-bar {{
        background-color: {CARD_BG};
        padding: 10px 20px;
        border-radius: 8px;
        color: {LIGHT_GRAY};
        font-size: 0.82rem;
        margin-top: 1rem;
    }}
    /* Hide Streamlit default footer */
    footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Load data (cached)
# ---------------------------------------------------------------------------

@st.cache_data
def load_data():
    df = generate_monthly_data(seed=42)
    df_prev = generate_previous_year_data(seed=99)
    return df, df_prev

df_all, df_prev_all = load_data()

# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Filtros")

    all_months = sorted(df_all["month"].dt.to_period("M").unique())
    month_labels = [m.strftime("%b %Y") for m in all_months]

    start_month, end_month = st.select_slider(
        "Rango de meses",
        options=list(range(len(all_months))),
        value=(0, len(all_months) - 1),
        format_func=lambda i: month_labels[i],
    )
    selected_months = all_months[start_month : end_month + 1]

    all_partners = sorted(df_all["partner"].unique())
    selected_partners = st.multiselect(
        "Socios comerciales",
        options=all_partners,
        default=all_partners,
    )

    compare_prev = st.toggle("Comparar vs periodo anterior", value=True)

    st.markdown("---")
    st.markdown(
        f"<div style='color:{LIGHT_GRAY}; font-size:0.75rem;'>"
        "Daniela Serrato | Portfolio DS/ML<br>"
        "Executive KPI Dashboard v1.0"
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Filter data
# ---------------------------------------------------------------------------
mask = (
    df_all["month"].dt.to_period("M").isin(selected_months)
    & df_all["partner"].isin(selected_partners)
)
df = df_all[mask].copy()

# Previous period: same number of months, immediately before the selected range
n_months = len(selected_months)
prev_end = selected_months[0] - 1
prev_periods = pd.period_range(end=prev_end, periods=n_months, freq="M")
mask_prev = (
    df_all["month"].dt.to_period("M").isin(prev_periods)
    & df_all["partner"].isin(selected_partners)
)
df_prev_period = df_all[mask_prev].copy()

# ---------------------------------------------------------------------------
# Helper: compute deltas
# ---------------------------------------------------------------------------

def pct_delta(current, previous):
    """Return percentage change; None if previous is 0."""
    if previous == 0:
        return None
    return round((current - previous) / previous * 100, 1)


def abs_delta(current, previous):
    """Return absolute difference rounded to 2 decimal places."""
    return round(current - previous, 2)


# ---------------------------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------------------------
# Current period (last month in selection for rates, sum for volumes)
last_month = df["month"].max()
df_latest = df[df["month"] == last_month]

total_accounts = df_latest["active_accounts"].sum()
monthly_revenue = df_latest["revenue_mxn"].sum()
avg_delinquency = (
    (df_latest["delinquency_rate"] * df_latest["active_accounts"]).sum()
    / df_latest["active_accounts"].sum()
    if df_latest["active_accounts"].sum() > 0
    else 0
)
avg_approval = (
    (df_latest["approval_rate"] * df_latest["applications"]).sum()
    / df_latest["applications"].sum()
    if df_latest["applications"].sum() > 0
    else 0
)

# Previous period equivalents
if not df_prev_period.empty:
    prev_last = df_prev_period["month"].max()
    df_prev_latest = df_prev_period[df_prev_period["month"] == prev_last]
    prev_accounts = df_prev_latest["active_accounts"].sum()
    prev_revenue = df_prev_latest["revenue_mxn"].sum()
    prev_delinquency = (
        (df_prev_latest["delinquency_rate"] * df_prev_latest["active_accounts"]).sum()
        / df_prev_latest["active_accounts"].sum()
        if df_prev_latest["active_accounts"].sum() > 0
        else 0
    )
    prev_approval = (
        (df_prev_latest["approval_rate"] * df_prev_latest["applications"]).sum()
        / df_prev_latest["applications"].sum()
        if df_prev_latest["applications"].sum() > 0
        else 0
    )
else:
    prev_accounts = prev_revenue = prev_delinquency = prev_approval = 0

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<p class="dashboard-header">Executive KPI Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    f'<p class="dashboard-sub">Portafolio de Tarjetas de Credito  |  '
    f'{selected_months[0].strftime("%b %Y")} - {selected_months[-1].strftime("%b %Y")}  |  '
    f'{len(selected_partners)} socios seleccionados</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Row 1 — KPI Cards
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    delta_acc = f"{pct_delta(total_accounts, prev_accounts):+.1f}%" if compare_prev and prev_accounts else None
    st.metric("Cuentas Activas", f"{total_accounts:,}", delta=delta_acc)

with k2:
    delta_rev = f"{pct_delta(monthly_revenue, prev_revenue):+.1f}%" if compare_prev and prev_revenue else None
    st.metric("Ingresos Mensuales (MXN)", f"${monthly_revenue:,.0f}", delta=delta_rev)

with k3:
    delta_del = (
        f"{abs_delta(avg_delinquency * 100, prev_delinquency * 100):+.2f} pp"
        if compare_prev and prev_delinquency
        else None
    )
    st.metric(
        "Mora +30 dias",
        f"{avg_delinquency * 100:.2f}%",
        delta=delta_del,
        delta_color="inverse",
    )

with k4:
    delta_apr = (
        f"{abs_delta(avg_approval * 100, prev_approval * 100):+.2f} pp"
        if compare_prev and prev_approval
        else None
    )
    st.metric("Tasa de Aprobacion", f"{avg_approval * 100:.1f}%", delta=delta_apr)

# ---------------------------------------------------------------------------
# Chart defaults
# ---------------------------------------------------------------------------
CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#111827",
    font=dict(family="Inter, sans-serif", color=TEXT_WHITE, size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=340,
)

# ---------------------------------------------------------------------------
# Row 2 — Revenue Trend + Accounts by Partner
# ---------------------------------------------------------------------------
st.markdown('<p class="section-title">Tendencia e Ingresos</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    # Monthly revenue trend with optional previous year
    rev_monthly = (
        df.groupby("month")["revenue_mxn"]
        .sum()
        .reset_index()
        .rename(columns={"revenue_mxn": "Ingresos"})
    )
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=rev_monthly["month"],
        y=rev_monthly["Ingresos"],
        mode="lines+markers",
        name="Periodo actual",
        line=dict(color=GREEN, width=3),
        marker=dict(size=6),
    ))

    # Previous year line (shifted +12 months for overlay)
    if compare_prev:
        prev_yr = (
            df_prev_all[df_prev_all["partner"].isin(selected_partners)]
            .groupby("month")["revenue_mxn"]
            .sum()
            .reset_index()
        )
        prev_yr["month_shifted"] = prev_yr["month"] + pd.DateOffset(years=1)
        fig_rev.add_trace(go.Scatter(
            x=prev_yr["month_shifted"],
            y=prev_yr["revenue_mxn"],
            mode="lines",
            name="Ano anterior",
            line=dict(color=LIGHT_GRAY, width=2, dash="dash"),
        ))

    fig_rev.update_layout(
        **CHART_LAYOUT,
        title="Ingresos Mensuales (MXN)",
        yaxis_title="MXN",
        xaxis_title=None,
        yaxis_tickformat=",.0f",
    )
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    # Active accounts by partner (horizontal bar, last month)
    acc_partner = (
        df_latest.groupby("partner")["active_accounts"]
        .sum()
        .sort_values()
        .reset_index()
    )
    fig_acc = px.bar(
        acc_partner,
        x="active_accounts",
        y="partner",
        orientation="h",
        color_discrete_sequence=[CHART_COLORS[2]],
        text="active_accounts",
    )
    fig_acc.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig_acc.update_layout(
        **CHART_LAYOUT,
        title=f"Cuentas Activas por Socio — {last_month.strftime('%b %Y')}",
        xaxis_title="Cuentas",
        yaxis_title=None,
        showlegend=False,
    )
    st.plotly_chart(fig_acc, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 3 — Delinquency Bands + Approval Rate
# ---------------------------------------------------------------------------
st.markdown('<p class="section-title">Calidad de Cartera y Aprobacion</p>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    # Stacked bar: delinquency bands by month
    del_monthly = (
        df.groupby("month")[["current_pct", "over_30_pct", "over_60_pct", "over_90_pct"]]
        .apply(lambda g: pd.Series({
            "Vigente": (g["current_pct"] * df.loc[g.index, "active_accounts"]).sum()
                       / df.loc[g.index, "active_accounts"].sum(),
            "+30 dias": (g["over_30_pct"] * df.loc[g.index, "active_accounts"]).sum()
                        / df.loc[g.index, "active_accounts"].sum(),
            "+60 dias": (g["over_60_pct"] * df.loc[g.index, "active_accounts"]).sum()
                        / df.loc[g.index, "active_accounts"].sum(),
            "+90 dias": (g["over_90_pct"] * df.loc[g.index, "active_accounts"]).sum()
                        / df.loc[g.index, "active_accounts"].sum(),
        }))
        .reset_index()
    )
    del_melted = del_monthly.melt(id_vars="month", var_name="Banda", value_name="Porcentaje")
    del_melted["Porcentaje"] = del_melted["Porcentaje"] * 100

    fig_del = px.bar(
        del_melted,
        x="month",
        y="Porcentaje",
        color="Banda",
        color_discrete_map=DELINQUENCY_COLORS,
        barmode="stack",
    )
    fig_del.update_layout(
        **CHART_LAYOUT,
        title="Bandas de Mora por Mes (%)",
        xaxis_title=None,
        yaxis_title="%",
        yaxis_range=[0, 100],
    )
    st.plotly_chart(fig_del, use_container_width=True)

with c4:
    # Approval rate by partner with target line
    apr_partner = (
        df_latest.groupby("partner")
        .apply(lambda g: (g["approval_rate"] * g["applications"]).sum() / g["applications"].sum())
        .sort_values(ascending=False)
        .reset_index(name="approval_rate")
    )
    apr_partner["approval_pct"] = apr_partner["approval_rate"] * 100

    fig_apr = px.bar(
        apr_partner,
        x="partner",
        y="approval_pct",
        color_discrete_sequence=[CHART_COLORS[1]],
        text="approval_pct",
    )
    fig_apr.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    # Target line
    fig_apr.add_hline(
        y=TARGET_APPROVAL * 100,
        line_dash="dash",
        line_color=RED,
        annotation_text=f"Meta {TARGET_APPROVAL*100:.0f}%",
        annotation_position="top right",
        annotation_font_color=RED,
    )
    fig_apr.update_layout(
        **CHART_LAYOUT,
        title=f"Tasa de Aprobacion por Socio — {last_month.strftime('%b %Y')}",
        xaxis_title=None,
        yaxis_title="%",
        yaxis_range=[0, 100],
        showlegend=False,
    )
    st.plotly_chart(fig_apr, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 4 — Partner Summary Table
# ---------------------------------------------------------------------------
st.markdown('<p class="section-title">Resumen por Socio Comercial</p>', unsafe_allow_html=True)

# Build summary for last month
summary = (
    df_latest.groupby("partner")
    .agg(
        Cuentas=("active_accounts", "sum"),
        Ingresos_MXN=("revenue_mxn", "sum"),
        Mora_30=("delinquency_rate", "mean"),
        Aprobacion=("approval_rate", "mean"),
    )
    .reset_index()
    .rename(columns={"partner": "Socio"})
)

# MoM growth: compare last month vs second to last
months_sorted = sorted(df["month"].unique())
if len(months_sorted) >= 2:
    second_last = months_sorted[-2]
    df_second = df[df["month"] == second_last]
    rev_prev_month = df_second.groupby("partner")["revenue_mxn"].sum().rename("rev_prev")
    rev_curr_month = df_latest.groupby("partner")["revenue_mxn"].sum().rename("rev_curr")
    mom = pd.concat([rev_curr_month, rev_prev_month], axis=1)
    mom["Crecimiento_MoM"] = ((mom["rev_curr"] - mom["rev_prev"]) / mom["rev_prev"] * 100).round(1)
    summary = summary.merge(mom[["Crecimiento_MoM"]].reset_index().rename(columns={"partner": "Socio"}), on="Socio", how="left")
else:
    summary["Crecimiento_MoM"] = None

summary = summary.sort_values("Ingresos_MXN", ascending=False)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Socio": st.column_config.TextColumn("Socio Comercial", width="medium"),
        "Cuentas": st.column_config.NumberColumn("Cuentas Activas", format="%d"),
        "Ingresos_MXN": st.column_config.NumberColumn("Ingresos (MXN)", format="$%,.0f"),
        "Mora_30": st.column_config.ProgressColumn(
            "Mora +30",
            format="%.2f%%",
            min_value=0,
            max_value=0.15,
        ),
        "Aprobacion": st.column_config.ProgressColumn(
            "Aprobacion",
            format="%.1f%%",
            min_value=0,
            max_value=1.0,
        ),
        "Crecimiento_MoM": st.column_config.NumberColumn(
            "Crecimiento MoM (%)",
            format="%.1f%%",
            help="Cambio porcentual mes a mes en ingresos",
        ),
    },
)

# ---------------------------------------------------------------------------
# Footer — Monthly Close Summary
# ---------------------------------------------------------------------------
close_date = last_month.replace(day=1) + pd.offsets.MonthEnd(0)
today = pd.Timestamp.today().normalize()
next_close = (today.replace(day=1) + pd.offsets.MonthEnd(0))
days_to_close = (next_close - today).days

st.markdown(
    f'<div class="footer-bar">'
    f'<strong>Ultimo cierre:</strong> {close_date.strftime("%d %b %Y")} &nbsp; | &nbsp; '
    f'<strong>Dias para proximo cierre:</strong> {days_to_close} &nbsp; | &nbsp; '
    f'<strong>Frescura de datos:</strong> Actualizados al {close_date.strftime("%d/%m/%Y")} &nbsp; | &nbsp; '
    f'<strong>Socios activos:</strong> {len(selected_partners)} de {len(PARTNER_PROFILES)}'
    f'</div>',
    unsafe_allow_html=True,
)
