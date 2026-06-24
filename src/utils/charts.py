from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import ACCENT, DANGER, PRIMARY, SUCCESS, WARNING


def line_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title)
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str | None = None):
    fig = px.bar(df, x=x, y=y, color=color, title=title)
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def gauge(value: float, title: str):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": PRIMARY},
                "steps": [
                    {"range": [0, 50], "color": "#f8d7da"},
                    {"range": [50, 70], "color": "#fff3cd"},
                    {"range": [70, 100], "color": "#d1e7dd"},
                ],
            },
        )
    )
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def risk_heatmap(df: pd.DataFrame):
    fig = px.density_heatmap(
        df,
        x="probability",
        y="impact",
        z="exposure",
        nbinsx=5,
        nbinsy=5,
        color_continuous_scale=["#d1e7dd", "#fff3cd", "#f8d7da"],
        title="Risk Exposure Heatmap",
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
    return fig


def valuation_waterfall(values: dict[str, float]):
    labels = list(values.keys())
    amounts = list(values.values())
    fig = go.Figure(
        go.Waterfall(
            x=labels,
            y=amounts,
            measure=["relative"] * (len(labels) - 1) + ["total"],
            connector={"line": {"color": "#8792a2"}},
            increasing={"marker": {"color": SUCCESS}},
            decreasing={"marker": {"color": DANGER}},
            totals={"marker": {"color": PRIMARY}},
        )
    )
    fig.update_layout(template="plotly_white", title="Enterprise Value Bridge")
    return fig


def priority_scatter(df: pd.DataFrame, x: str, y: str, size: str, label: str, title: str):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=label,
        hover_name=label,
        color_discrete_sequence=[PRIMARY, ACCENT, SUCCESS, WARNING, DANGER],
        title=title,
    )
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
    return fig

