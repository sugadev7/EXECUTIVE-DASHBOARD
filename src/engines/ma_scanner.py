from __future__ import annotations

import pandas as pd


def scan_targets(targets: pd.DataFrame) -> pd.DataFrame:
    df = targets.copy()
    df["ev_revenue"] = df["estimated_ev"] / df["revenue"]
    df["fit_score"] = (
        df["strategic_fit"] * 0.30
        + df["technology_fit"] * 0.20
        + df["customer_overlap"] * 0.15
        + df["growth_rate"] * 10 * 0.15
        + df["gross_margin"] * 10 * 0.10
        - df["integration_risk"] * 0.10
    )
    df["deal_recommendation"] = pd.cut(
        df["fit_score"],
        bins=[-100, 5.5, 7.0, 10],
        labels=["Pass", "Watchlist", "Prioritize"],
    )
    return df.sort_values("fit_score", ascending=False)


def acquisition_thesis(scored: pd.DataFrame) -> str:
    top = scored.iloc[0]
    return (
        f"{top['target']} is the leading acquisition candidate with a {top['fit_score']:.1f}/10 fit score, "
        f"{top['growth_rate'] * 100:.0f}% growth, and {top['gross_margin'] * 100:.0f}% gross margin."
    )

