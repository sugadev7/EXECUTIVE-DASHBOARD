from __future__ import annotations

import pandas as pd

from src.config import HEALTH_WEIGHTS


def _clip_score(value: float, low: float, high: float, invert: bool = False) -> float:
    if high == low:
        return 50.0
    score = (value - low) / (high - low) * 100
    if invert:
        score = 100 - score
    return float(max(0, min(100, score)))


def calculate_health_score(financials: pd.DataFrame, customers: pd.DataFrame, risks: pd.DataFrame) -> dict:
    latest = financials.sort_values("period").iloc[-1]
    previous = financials.sort_values("period").iloc[-2]
    latest_customer = customers.sort_values("period").iloc[-1]

    revenue_growth = latest["revenue"] / previous["revenue"] - 1
    gross_margin = latest["gross_profit"] / latest["revenue"]
    ebitda_margin = latest["ebitda"] / latest["revenue"]
    cash_ratio = latest["cash"] / max(latest["monthly_burn"], 1)
    net_retention = latest_customer["net_revenue_retention"]
    churn = latest_customer["logo_churn"]
    initiative_delivery = latest["initiative_delivery_rate"]
    risk_exposure = float((risks["probability"] * risks["impact"]).mean())

    dimensions = {
        "growth": _clip_score(revenue_growth, 0.00, 0.12),
        "profitability": (_clip_score(gross_margin, 0.55, 0.82) * 0.45) + (_clip_score(ebitda_margin, -0.10, 0.25) * 0.55),
        "liquidity": _clip_score(cash_ratio, 4, 18),
        "customer": (_clip_score(net_retention, 0.95, 1.25) * 0.65) + (_clip_score(churn, 0.02, 0.12, invert=True) * 0.35),
        "execution": _clip_score(initiative_delivery, 0.55, 0.95),
        "risk": _clip_score(risk_exposure, 3, 16, invert=True),
    }
    overall = sum(dimensions[k] * HEALTH_WEIGHTS[k] for k in HEALTH_WEIGHTS)

    return {
        "overall": round(overall, 1),
        "dimensions": {k: round(v, 1) for k, v in dimensions.items()},
        "drivers": {
            "revenue_growth": revenue_growth,
            "gross_margin": gross_margin,
            "ebitda_margin": ebitda_margin,
            "cash_runway_months": cash_ratio,
            "net_revenue_retention": net_retention,
            "logo_churn": churn,
            "risk_exposure": risk_exposure,
        },
    }


def health_recommendations(score: dict) -> list[str]:
    dims = score["dimensions"]
    recs: list[str] = []
    if dims["growth"] < 65:
        recs.append("Prioritize pipeline quality and conversion rate before expanding spend.")
    if dims["profitability"] < 65:
        recs.append("Run a margin sprint focused on hosting costs, services mix, and discount governance.")
    if dims["liquidity"] < 60:
        recs.append("Protect runway by sequencing hiring behind booked ARR milestones.")
    if dims["customer"] < 70:
        recs.append("Create an executive retention pod for top accounts and renewal-risk segments.")
    if dims["risk"] < 70:
        recs.append("Escalate the highest exposure risks into weekly operating reviews.")
    if not recs:
        recs.append("Maintain current operating cadence and shift attention to strategic option creation.")
    return recs

