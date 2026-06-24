from __future__ import annotations

import pandas as pd

from src.engines.forecasting import build_forecast
from src.engines.valuation import dcf_valuation


def strategic_scenarios(financials: pd.DataFrame) -> pd.DataFrame:
    assumptions = [
        ("Capital Efficient", 0.10, 0.26, 0.118),
        ("Base Plan", 0.16, 0.22, 0.115),
        ("Growth Offensive", 0.24, 0.16, 0.125),
    ]
    rows = []
    for name, growth, margin, wacc in assumptions:
        forecast = build_forecast(financials, growth, margin, quarters=8)
        valuation = dcf_valuation(financials, revenue_growth=growth, ebitda_margin_target=margin, wacc=wacc)
        rows.append(
            {
                "scenario": name,
                "growth": growth,
                "ending_revenue": forecast.iloc[-1]["revenue"],
                "ending_ebitda_margin": forecast.iloc[-1]["ebitda_margin"],
                "enterprise_value": valuation["enterprise_value"],
            }
        )
    return pd.DataFrame(rows)

