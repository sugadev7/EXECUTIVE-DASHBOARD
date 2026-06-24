from __future__ import annotations


def money(value: float, suffix: str = "M") -> str:
    return f"${value:,.1f}{suffix}"


def percent(value: float) -> str:
    return f"{value * 100:,.1f}%"


def number(value: float) -> str:
    return f"{value:,.0f}"


def score_label(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Healthy"
    if score >= 50:
        return "Watch"
    return "Critical"


def delta_text(current: float, previous: float, fmt: str = "number") -> str:
    delta = current - previous
    if fmt == "percent":
        return f"{delta * 100:+.1f} pts"
    if fmt == "money":
        return f"${delta:+,.1f}M"
    return f"{delta:+,.1f}"

