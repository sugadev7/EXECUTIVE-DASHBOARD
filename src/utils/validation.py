from __future__ import annotations

import pandas as pd


def require_columns(df: pd.DataFrame, columns: list[str], dataset_name: str) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"{dataset_name} is missing required columns: {joined}")


def assert_non_empty(df: pd.DataFrame, dataset_name: str) -> None:
    if df.empty:
        raise ValueError(f"{dataset_name} is empty")

