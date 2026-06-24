from pathlib import Path

APP_NAME = "MBA Strategy Command Center"
COMPANY_NAME = "Northstar Analytics"
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

PRIMARY = "#1f7a8c"
ACCENT = "#d1495b"
SUCCESS = "#2e8b57"
WARNING = "#f2a541"
DANGER = "#c73e1d"
INK = "#18212f"
MUTED = "#6b7280"
PAPER = "#f7f8fa"

HEALTH_WEIGHTS = {
    "growth": 0.20,
    "profitability": 0.18,
    "liquidity": 0.14,
    "customer": 0.16,
    "execution": 0.14,
    "risk": 0.18,
}

DEFAULT_WACC = 0.115
DEFAULT_TERMINAL_GROWTH = 0.035
DEFAULT_TAX_RATE = 0.24

