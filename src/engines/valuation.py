from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import DEFAULT_TERMINAL_GROWTH, DEFAULT_WACC


def dcf_valuation(
    financials: pd.DataFrame,
    revenue_growth: float = 0.14,
    ebitda_margin_target: float = 0.24,
    wacc: float = DEFAULT_WACC,
    terminal_growth: float = DEFAULT_TERMINAL_GROWTH,
    years: int = 5,
) -> dict:
    latest = financials.sort_values("period").iloc[-1]
    revenue = latest["revenue"]
    current_margin = latest["ebitda"] / latest["revenue"]
    cash_flows = []
    forecast_rows = []
    for year in range(1, years + 1):
        revenue *= 1 + revenue_growth * (0.88 ** (year - 1))
        margin = current_margin + (ebitda_margin_target - current_margin) * year / years
        ebitda = revenue * margin
        reinvestment = revenue * 0.035
        tax = max(ebitda, 0) * 0.24
        fcf = ebitda - reinvestment - tax
        pv = fcf / ((1 + wacc) ** year)
        cash_flows.append(pv)
        forecast_rows.append({"year": year, "revenue": revenue, "ebitda": ebitda, "fcf": fcf, "pv_fcf": pv})

    terminal_fcf = forecast_rows[-1]["fcf"] * (1 + terminal_growth)
    terminal_value = terminal_fcf / max(wacc - terminal_growth, 0.01)
    pv_terminal = terminal_value / ((1 + wacc) ** years)
    enterprise_value = sum(cash_flows) + pv_terminal
    equity_value = enterprise_value + latest["cash"] - latest["debt"]

    return {
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "pv_terminal": pv_terminal,
        "pv_fcf": sum(cash_flows),
        "forecast": pd.DataFrame(forecast_rows),
    }


def comparable_valuation(financials: pd.DataFrame, competitors: pd.DataFrame) -> dict:
    latest = financials.sort_values("period").iloc[-1]
    peer_multiple = float(np.average(competitors["ev_revenue_multiple"], weights=competitors["market_share"]))
    enterprise_value = latest["revenue"] * peer_multiple
    equity_value = enterprise_value + latest["cash"] - latest["debt"]
    return {
        "peer_multiple": peer_multiple,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
    }


def blended_valuation(dcf: dict, comps: dict, dcf_weight: float = 0.60) -> dict:
    ev = dcf["enterprise_value"] * dcf_weight + comps["enterprise_value"] * (1 - dcf_weight)
    eq = dcf["equity_value"] * dcf_weight + comps["equity_value"] * (1 - dcf_weight)
    return {"enterprise_value": ev, "equity_value": eq, "dcf_weight": dcf_weight}

