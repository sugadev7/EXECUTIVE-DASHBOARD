from __future__ import annotations

import streamlit as st
import pandas as pd

from src.config import COMPANY_NAME
from src.data_loader import load_data
from src.engines.ai_copilot import answer_question
from src.engines.board_pack import generate_board_pack
from src.engines.competitor_intelligence import benchmark_scores, competitive_narrative, segment_attractiveness
from src.engines.executive_dashboard import executive_alerts, executive_snapshot
from src.engines.financial_intelligence import financial_kpis, margin_bridge, working_capital_table
from src.engines.forecasting import build_forecast, scenario_table
from src.engines.health_score import calculate_health_score, health_recommendations
from src.engines.ma_scanner import acquisition_thesis, scan_targets
from src.engines.risk_intelligence import mitigation_actions, risk_summary, score_risks
from src.engines.strategy_command import portfolio_summary, prioritize_initiatives, strategy_memo
from src.engines.valuation import blended_valuation, comparable_valuation, dcf_valuation
from src.ui.components import dataframe, insight, page_title, section
from src.ui.sidebar import navigation
from src.ui.theme import apply_theme
from src.utils.charts import bar_chart, gauge, line_chart, priority_scatter, risk_heatmap, valuation_waterfall
from src.utils.formatting import money, percent, score_label


def executive_dashboard(bundle) -> None:
    page_title("Executive Dashboard", f"{COMPANY_NAME} operating cockpit")
    snapshot = executive_snapshot(bundle)
    kpis = financial_kpis(bundle.financials, bundle.customers)
    health = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", money(kpis["revenue"]), f"{kpis['revenue_growth'] * 100:.1f}% QoQ")
    c2.metric("Health Score", f"{health['overall']}/100", score_label(health["overall"]))
    c3.metric("EBITDA Margin", percent(kpis["ebitda_margin"]))
    c4.metric("Runway", f"{kpis['runway_months']:.1f} months")

    left, right = st.columns([1, 1])
    with left:
        st.plotly_chart(line_chart(bundle.financials, "period", "revenue", "Revenue Trend"), use_container_width=True)
    with right:
        st.plotly_chart(gauge(health["overall"], "Enterprise Health"), use_container_width=True)

    section("Board-Level Actions")
    for alert in executive_alerts(snapshot):
        insight(alert)
    for rec in health_recommendations(health):
        insight(rec)


def health_score_page(bundle) -> None:
    page_title("Health Score Engine", "Weighted operating health across finance, customer, execution, and risk")
    health = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    st.plotly_chart(gauge(health["overall"], "Overall Health Score"), use_container_width=True)
    dims = [{"dimension": k.title(), "score": v} for k, v in health["dimensions"].items()]
    st.plotly_chart(bar_chart(pd.DataFrame(dims), "dimension", "score", "Health Score Dimensions"), use_container_width=True)
    dataframe(pd.DataFrame([health["drivers"]]))


def financial_page(bundle) -> None:
    page_title("Financial Intelligence", "Margin, runway, working capital, and SaaS economics")
    kpis = financial_kpis(bundle.financials, bundle.customers)
    cols = st.columns(4)
    cols[0].metric("Gross Margin", percent(kpis["gross_margin"]))
    cols[1].metric("Rule of 40", f"{kpis['rule_of_40']:.1f}")
    cols[2].metric("CAC Payback", f"{kpis['cac_payback_months']:.1f} mo")
    cols[3].metric("Working Capital", money(kpis["working_capital"]))
    st.plotly_chart(bar_chart(margin_bridge(bundle.financials), "driver", "impact", "EBITDA Margin Bridge"), use_container_width=True)
    dataframe(working_capital_table(bundle.financials))


def risk_page(bundle) -> None:
    page_title("Risk Intelligence", "Enterprise risk exposure and mitigation priorities")
    scored = score_risks(bundle.risks)
    summary = risk_summary(bundle.risks)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Exposure", f"{summary['total_exposure']:.1f}")
    c2.metric("Residual Exposure", f"{summary['residual_exposure']:.1f}")
    c3.metric("High Priority Risks", summary["high_count"])
    st.plotly_chart(risk_heatmap(scored), use_container_width=True)
    for action in mitigation_actions(bundle.risks):
        insight(action)
    dataframe(scored)


def competitor_page(bundle) -> None:
    page_title("Competitor Intelligence", "Peer benchmarks, market share, and segment attractiveness")
    scored = benchmark_scores(bundle.competitors)
    insight(competitive_narrative(scored, COMPANY_NAME))
    st.plotly_chart(priority_scatter(scored, "market_share", "nps", "ev_revenue_multiple", "company", "Peer Positioning"), use_container_width=True)
    dataframe(scored)
    section("Segment Attractiveness")
    dataframe(segment_attractiveness(bundle.segments))


def strategy_page(bundle) -> None:
    page_title("Strategy Command Center", "Initiative portfolio and capital allocation")
    ranked = prioritize_initiatives(bundle.initiatives)
    summary = portfolio_summary(bundle.initiatives)
    cols = st.columns(4)
    cols[0].metric("Active", summary["active_count"])
    cols[1].metric("Planned", summary["planned_count"])
    cols[2].metric("Investment", money(summary["investment_required"]))
    cols[3].metric("Revenue Upside", money(summary["revenue_upside"]))
    st.plotly_chart(priority_scatter(ranked, "complexity", "strategic_fit", "revenue_upside", "initiative", "Initiative Priority Matrix"), use_container_width=True)
    for memo in strategy_memo(bundle.initiatives):
        insight(memo)
    dataframe(ranked)


def ma_page(bundle) -> None:
    page_title("M&A Scanner", "Acquisition target fit, valuation, and integration risk")
    scored = scan_targets(bundle.targets)
    insight(acquisition_thesis(scored))
    st.plotly_chart(priority_scatter(scored, "ev_revenue", "fit_score", "revenue", "target", "Deal Screen"), use_container_width=True)
    dataframe(scored)


def valuation_page(bundle) -> None:
    page_title("Valuation Engine", "DCF, comparable valuation, and blended equity value")
    growth = st.slider("Revenue growth assumption", 0.02, 0.30, 0.14, 0.01)
    margin = st.slider("Target EBITDA margin", 0.05, 0.35, 0.24, 0.01)
    wacc = st.slider("WACC", 0.08, 0.18, 0.115, 0.005)
    dcf = dcf_valuation(bundle.financials, growth, margin, wacc)
    comps = comparable_valuation(bundle.financials, bundle.competitors)
    blend = blended_valuation(dcf, comps)
    cols = st.columns(3)
    cols[0].metric("DCF EV", money(dcf["enterprise_value"]))
    cols[1].metric("Comps EV", money(comps["enterprise_value"]))
    cols[2].metric("Blended Equity", money(blend["equity_value"]))
    st.plotly_chart(valuation_waterfall({"PV FCF": dcf["pv_fcf"], "PV Terminal": dcf["pv_terminal"], "Enterprise Value": dcf["enterprise_value"]}), use_container_width=True)
    dataframe(dcf["forecast"])


def forecasting_page(bundle) -> None:
    page_title("Forecasting Lab", "Scenario planning for revenue and EBITDA")
    growth = st.slider("Annual revenue growth", 0.00, 0.35, 0.16, 0.01)
    margin = st.slider("Ending EBITDA margin", 0.00, 0.35, 0.22, 0.01)
    forecast = build_forecast(bundle.financials, growth, margin)
    st.plotly_chart(line_chart(forecast, "period", "revenue", "Revenue Forecast"), use_container_width=True)
    dataframe(scenario_table(bundle.financials))
    dataframe(forecast)


def board_pack_page(bundle) -> None:
    page_title("Board Pack PDF Generator", "One-click executive PDF for board meetings")
    st.write("Generate a concise PDF with KPIs, health score, risk summary, strategy priorities, and competitor snapshot.")
    if st.button("Generate Board Pack", type="primary"):
        path = generate_board_pack(bundle)
        st.success(f"Generated {path.name}")
        with open(path, "rb") as handle:
            st.download_button("Download PDF", handle, file_name=path.name, mime="application/pdf")


def copilot_page(bundle) -> None:
    page_title("AI Copilot", "Board-style analysis assistant using the project data")
    question = st.text_input("Ask a strategy question", value="What should the board focus on this quarter?")
    if question:
        insight(answer_question(question, bundle))


def main() -> None:
    apply_theme()
    bundle = load_data()
    page = navigation()
    pages = {
        "Executive Dashboard": executive_dashboard,
        "Health Score Engine": health_score_page,
        "Financial Intelligence": financial_page,
        "Risk Intelligence": risk_page,
        "Competitor Intelligence": competitor_page,
        "Strategy Command Center": strategy_page,
        "M&A Scanner": ma_page,
        "Valuation Engine": valuation_page,
        "Forecasting Lab": forecasting_page,
        "Board Pack PDF Generator": board_pack_page,
        "AI Copilot": copilot_page,
    }
    pages[page](bundle)


if __name__ == "__main__":
    main()
