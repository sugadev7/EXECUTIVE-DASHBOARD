from __future__ import annotations

from src.engines.financial_intelligence import financial_kpis
from src.engines.health_score import calculate_health_score, health_recommendations
from src.engines.risk_intelligence import risk_summary
from src.engines.strategy_command import portfolio_summary
from src.utils.formatting import money, percent


SYSTEM_PROMPT = """You are a board-level strategy copilot. Be concise, numeric, and decision-oriented."""


def answer_question(question: str, bundle) -> str:
    q = question.lower().strip()
    kpis = financial_kpis(bundle.financials, bundle.customers)
    health = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    risks = risk_summary(bundle.risks)
    strategy = portfolio_summary(bundle.initiatives)

    if any(term in q for term in ["health", "score", "diagnose"]):
        recs = " ".join(health_recommendations(health)[:2])
        return f"Current health score is {health['overall']}/100. The weakest dimensions are {sorted(health['dimensions'], key=health['dimensions'].get)[:2]}. {recs}"
    if any(term in q for term in ["cash", "runway", "burn"]):
        return f"Cash is {money(kpis['cash'])}, runway is {kpis['runway_months']:.1f} months, and working capital is {money(kpis['working_capital'])}. Hiring and growth spend should stay tied to booked ARR milestones."
    if any(term in q for term in ["risk", "threat", "mitigation"]):
        return f"Top risk is {risks['top_risk']} owned by {risks['top_owner']}. Residual exposure is {risks['residual_exposure']:.1f}; move this into the weekly operating review until exposure declines."
    if any(term in q for term in ["strategy", "initiative", "priority"]):
        return f"Top initiative is {strategy['top_initiative']}. Active and planned initiatives require {money(strategy['investment_required'])} and create {money(strategy['revenue_upside'])} in modeled revenue upside."
    if any(term in q for term in ["margin", "profit", "ebitda"]):
        return f"Gross margin is {percent(kpis['gross_margin'])} and EBITDA margin is {percent(kpis['ebitda_margin'])}. The practical lever is discount governance plus support automation before broad cost reduction."
    return (
        f"Executive readout: revenue is {money(kpis['revenue'])}, quarterly growth is {percent(kpis['revenue_growth'])}, "
        f"health score is {health['overall']}/100, and the highest-priority initiative is {strategy['top_initiative']}."
    )

