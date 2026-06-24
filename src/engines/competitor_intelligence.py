from __future__ import annotations

import pandas as pd


def benchmark_scores(competitors: pd.DataFrame) -> pd.DataFrame:
    df = competitors.copy()
    max_share = df["market_share"].max()
    max_nps = df["nps"].max()
    min_price = df["average_contract_value"].min()
    df["benchmark_score"] = (
        (df["market_share"] / max_share) * 30
        + (df["nps"] / max_nps) * 25
        + (df["product_breadth"] / 10) * 20
        + (min_price / df["average_contract_value"]) * 10
        + (df["channel_strength"] / 10) * 15
    )
    return df.sort_values("benchmark_score", ascending=False)


def competitive_narrative(scored: pd.DataFrame, company_name: str) -> str:
    ours = scored[scored["company"] == company_name].iloc[0]
    leader = scored.iloc[0]
    if leader["company"] == company_name:
        return "The company leads the peer set on combined market share, product breadth, NPS, and channel strength."
    gap = leader["benchmark_score"] - ours["benchmark_score"]
    return f"{leader['company']} leads the benchmark by {gap:.1f} points; the largest opportunity is improving channel reach and enterprise product depth."


def segment_attractiveness(segments: pd.DataFrame) -> pd.DataFrame:
    df = segments.copy()
    df["attractiveness"] = (
        df["tam_billion"] * 0.25
        + df["growth_rate"] * 100 * 0.25
        + df["gross_margin_potential"] * 100 * 0.20
        - df["competitive_intensity"] * 6
        + df["strategic_fit"] * 4
    )
    return df.sort_values("attractiveness", ascending=False)

