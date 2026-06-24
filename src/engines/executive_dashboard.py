from __future__ import annotations

from src.engines.financial_intelligence import financial_kpis
from src.engines.health_score import calculate_health_score
from src.engines.risk_intelligence import risk_summary
from src.engines.strategy_command import portfolio_summary


def executive_snapshot(bundle) -> dict:
    kpis = financial_kpis(bundle.financials, bundle.customers)
    health = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    risk = risk_summary(bundle.risks)
    strategy = portfolio_summary(bundle.initiatives)
    return {
        "revenue": kpis["revenue"],
        "growth": kpis["revenue_growth"],
        "health_score": health["overall"],
        "runway_months": kpis["runway_months"],
        "top_risk": risk["top_risk"],
        "top_initiative": strategy["top_initiative"],
    }


def executive_alerts(snapshot: dict) -> list[str]:
    alerts = []
    if snapshot["health_score"] < 70:
        alerts.append("Enterprise health is below the target zone; focus the operating review on weakest dimensions.")
    if snapshot["runway_months"] < 12:
        alerts.append("Runway is below 12 months; stage discretionary spend behind ARR conversion.")
    if snapshot["growth"] < 0.08:
        alerts.append("Quarterly growth is below the strategic plan; inspect pipeline quality and enterprise conversion.")
    if not alerts:
        alerts.append("Operating profile is inside the target zone; use the next board cycle to create strategic options.")
    return alerts

