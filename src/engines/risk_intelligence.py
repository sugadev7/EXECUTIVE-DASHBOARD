from __future__ import annotations

import pandas as pd


def score_risks(risks: pd.DataFrame) -> pd.DataFrame:
    df = risks.copy()
    df["exposure"] = df["probability"] * df["impact"]
    df["residual_exposure"] = df["exposure"] * (1 - df["mitigation_effectiveness"])
    df["priority"] = pd.cut(
        df["residual_exposure"],
        bins=[-1, 4, 9, 25],
        labels=["Low", "Medium", "High"],
    )
    return df.sort_values("residual_exposure", ascending=False)


def risk_summary(risks: pd.DataFrame) -> dict:
    scored = score_risks(risks)
    return {
        "total_exposure": float(scored["exposure"].sum()),
        "residual_exposure": float(scored["residual_exposure"].sum()),
        "high_count": int((scored["priority"] == "High").sum()),
        "top_risk": str(scored.iloc[0]["risk"]),
        "top_owner": str(scored.iloc[0]["owner"]),
    }


def mitigation_actions(risks: pd.DataFrame) -> list[str]:
    top = score_risks(risks).head(3)
    return [
        f"{row.risk}: {row.mitigation} led by {row.owner}."
        for row in top.itertuples()
    ]

