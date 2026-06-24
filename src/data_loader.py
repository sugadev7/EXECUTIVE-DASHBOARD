from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import pandas as pd

from src.config import DATA_DIR


@dataclass(frozen=True)
class DataBundle:
    financials: pd.DataFrame
    competitors: pd.DataFrame
    risks: pd.DataFrame
    targets: pd.DataFrame
    initiatives: pd.DataFrame
    macro: pd.DataFrame
    segments: pd.DataFrame
    customers: pd.DataFrame


def _read_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    return pd.read_csv(path)


@lru_cache(maxsize=1)
def load_data() -> DataBundle:
    financials = _read_csv("company_financials.csv")
    financials["period"] = pd.PeriodIndex(financials["period"], freq="Q").to_timestamp()

    customers = _read_csv("customer_metrics.csv")
    customers["period"] = pd.PeriodIndex(customers["period"], freq="Q").to_timestamp()

    return DataBundle(
        financials=financials,
        competitors=_read_csv("competitor_benchmarks.csv"),
        risks=_read_csv("risk_register.csv"),
        targets=_read_csv("acquisition_targets.csv"),
        initiatives=_read_csv("strategy_initiatives.csv"),
        macro=_read_csv("macro_assumptions.csv"),
        segments=_read_csv("market_segments.csv"),
        customers=customers,
    )


def latest_row(df: pd.DataFrame) -> pd.Series:
    return df.sort_values("period").iloc[-1]

