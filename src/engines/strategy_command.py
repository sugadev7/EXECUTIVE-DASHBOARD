from __future__ import annotations

import pandas as pd


def prioritize_initiatives(initiatives: pd.DataFrame) -> pd.DataFrame:
    df = initiatives.copy()
    df["value_score"] = (
        df["revenue_upside"] * 0.35
        + df["margin_upside"] * 0.25
        + df["strategic_fit"] * 5
        + df["confidence"] * 4
        - df["complexity"] * 3
    )
    df["roi"] = (df["revenue_upside"] + df["margin_upside"]) / df["investment_required"]
    df["priority_rank"] = df["value_score"].rank(ascending=False, method="dense").astype(int)
    return df.sort_values("value_score", ascending=False)


def portfolio_summary(initiatives: pd.DataFrame) -> dict:
    ranked = prioritize_initiatives(initiatives)
    committed = ranked[ranked["status"].isin(["Active", "Planned"])]
    return {
        "active_count": int((ranked["status"] == "Active").sum()),
        "planned_count": int((ranked["status"] == "Planned").sum()),
        "investment_required": float(committed["investment_required"].sum()),
        "revenue_upside": float(committed["revenue_upside"].sum()),
        "top_initiative": ranked.iloc[0]["initiative"],
    }


def strategy_memo(initiatives: pd.DataFrame) -> list[str]:
    ranked = prioritize_initiatives(initiatives).head(3)
    return [
        f"Fund {row.initiative} first because it combines ${row.revenue_upside:.1f}M revenue upside with {row.confidence:.0f}/10 confidence."
        for row in ranked.itertuples()
    ]

