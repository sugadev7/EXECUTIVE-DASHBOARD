from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import OUTPUT_DIR


def export_dataframe(df: pd.DataFrame, name: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    safe_name = "".join(char if char.isalnum() or char in "-_" else "_" for char in name.lower())
    path = OUTPUT_DIR / f"{safe_name}.csv"
    df.to_csv(path, index=False)
    return path

