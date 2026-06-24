from __future__ import annotations

import pandas as pd


def build_forecast(financials: pd.DataFrame, growth: float, margin_target: float, quarters: int = 8) -> pd.DataFrame:
    latest = financials.sort_values("period").iloc[-1]
    period = pd.Period(latest["period"], freq="Q")
    revenue = latest["revenue"]
    current_margin = latest["ebitda"] / latest["revenue"]
    rows = []
    for q in range(1, quarters + 1):
        revenue *= 1 + growth / 4
        margin = current_margin + (margin_target - current_margin) * q / quarters
        gross_profit = revenue * min(0.82, latest["gross_profit"] / latest["revenue"] + 0.01 * q)
        ebitda = revenue * margin
        rows.append(
            {
                "period": str(period + q),
                "revenue": revenue,
                "gross_profit": gross_profit,
                "ebitda": ebitda,
                "ebitda_margin": margin,
            }
        )
    return pd.DataFrame(rows)


def scenario_table(financials: pd.DataFrame) -> pd.DataFrame:
    scenarios = [
        ("Downside", 0.06, 0.10),
        ("Base", 0.14, 0.20),
        ("Upside", 0.22, 0.26),
    ]
    rows = []
    for name, growth, margin in scenarios:
        forecast = build_forecast(financials, growth, margin)
        final = forecast.iloc[-1]
        rows.append(
            {
                "scenario": name,
                "annual_growth": growth,
                "target_ebitda_margin": margin,
                "ending_revenue": final["revenue"],
                "ending_ebitda": final["ebitda"],
            }
        )
    return pd.DataFrame(rows)

