from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.config import COMPANY_NAME, OUTPUT_DIR
from src.engines.competitor_intelligence import benchmark_scores
from src.engines.financial_intelligence import financial_kpis
from src.engines.health_score import calculate_health_score
from src.engines.risk_intelligence import risk_summary
from src.engines.strategy_command import portfolio_summary
from src.utils.formatting import money, percent


def _table(data):
    table = Table(data, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a8c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d0d5dd")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def generate_board_pack(bundle) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"board_pack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=LETTER, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    kpis = financial_kpis(bundle.financials, bundle.customers)
    health = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    risks = risk_summary(bundle.risks)
    strategy = portfolio_summary(bundle.initiatives)
    peers = benchmark_scores(bundle.competitors)

    story.append(Paragraph(f"{COMPANY_NAME} Board Pack", styles["Title"]))
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), styles["Normal"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Health score is {health['overall']}/100. Revenue is {money(kpis['revenue'])} with quarterly growth of {percent(kpis['revenue_growth'])}. "
            f"Runway is {kpis['runway_months']:.1f} months and Rule of 40 is {kpis['rule_of_40']:.1f}.",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(_table([
        ["Metric", "Value"],
        ["Revenue", money(kpis["revenue"])],
        ["Gross Margin", percent(kpis["gross_margin"])],
        ["EBITDA Margin", percent(kpis["ebitda_margin"])],
        ["Cash Runway", f"{kpis['runway_months']:.1f} months"],
        ["Health Score", f"{health['overall']}/100"],
    ]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Risk and Strategy", styles["Heading2"]))
    story.append(_table([
        ["Area", "Status"],
        ["Top Risk", risks["top_risk"]],
        ["Residual Exposure", f"{risks['residual_exposure']:.1f}"],
        ["Top Initiative", strategy["top_initiative"]],
        ["Committed Investment", money(strategy["investment_required"])],
    ]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Competitive Snapshot", styles["Heading2"]))
    story.append(_table([["Company", "Market Share", "NPS", "Score"]] + [
        [row.company, percent(row.market_share), f"{row.nps:.0f}", f"{row.benchmark_score:.1f}"]
        for row in peers.head(5).itertuples()
    ]))

    doc.build(story)
    return path

