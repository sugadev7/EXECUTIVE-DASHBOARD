from __future__ import annotations

import pandas as pd


def financial_kpis(financials: pd.DataFrame, customers: pd.DataFrame) -> dict:
    df = financials.sort_values("period")
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    cust = customers.sort_values("period").iloc[-1]
    revenue_growth = latest["revenue"] / prev["revenue"] - 1
    gross_margin = latest["gross_profit"] / latest["revenue"]
    ebitda_margin = latest["ebitda"] / latest["revenue"]
    cac_payback = latest["sales_marketing"] / max(cust["new_arr"], 0.01) * 3
    rule_of_40 = revenue_growth * 100 + ebitda_margin * 100
    return {
        "revenue": latest["revenue"],
        "revenue_growth": revenue_growth,
        "gross_margin": gross_margin,
        "ebitda_margin": ebitda_margin,
        "cash": latest["cash"],
        "runway_months": latest["cash"] / max(latest["monthly_burn"], 0.01),
        "cac_payback_months": cac_payback,
        "rule_of_40": rule_of_40,
        "working_capital": latest["accounts_receivable"] - latest["accounts_payable"],
    }


def margin_bridge(financials: pd.DataFrame) -> pd.DataFrame:
    df = financials.sort_values("period").tail(2)
    start, end = df.iloc[0], df.iloc[1]
    rows = [
        ("Prior EBITDA", start["ebitda"]),
        ("Revenue growth", (end["revenue"] - start["revenue"]) * (start["gross_profit"] / start["revenue"])),
        ("Gross margin change", end["gross_profit"] - start["gross_profit"] - (end["revenue"] - start["revenue"]) * (start["gross_profit"] / start["revenue"])),
        ("R&D investment", -(end["rd"] - start["rd"])),
        ("Sales & marketing", -(end["sales_marketing"] - start["sales_marketing"])),
        ("G&A leverage", -(end["ga"] - start["ga"])),
        ("Current EBITDA", end["ebitda"]),
    ]
    return pd.DataFrame(rows, columns=["driver", "impact"])


def working_capital_table(financials: pd.DataFrame) -> pd.DataFrame:
    df = financials.copy()
    df["dso"] = df["accounts_receivable"] / df["revenue"] * 90
    df["dpo"] = df["accounts_payable"] / df["cost_of_revenue"] * 90
    df["net_working_capital"] = df["accounts_receivable"] - df["accounts_payable"]
    return df[["period", "dso", "dpo", "net_working_capital", "cash"]].tail(8)

