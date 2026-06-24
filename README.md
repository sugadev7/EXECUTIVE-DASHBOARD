# MBA Strategy Command Center

A production-style MBA portfolio project for executive decision support. The app combines company performance, financial intelligence, risk monitoring, competitor benchmarking, M&A screening, valuation, forecasting, board-pack PDF generation, and an AI-style strategy copilot into one Streamlit project.

## Highlights

- Executive Dashboard with KPIs, trends, and operating alerts
- Health Score Engine combining growth, profitability, liquidity, risk, customer, and execution metrics
- Financial Intelligence with margin bridge, unit economics, cash runway, and working capital views
- Risk Intelligence with heatmaps, weighted exposure, and mitigation priorities
- Competitor Intelligence with market-share and benchmark scoring
- Strategy Command Center for initiative prioritization
- M&A Scanner for target screening and strategic-fit ranking
- Valuation Engine with DCF and comparable valuation
- Forecasting Lab with configurable revenue and EBITDA scenarios
- Board Pack PDF Generator using ReportLab
- AI Copilot with deterministic business-analysis responses and optional OpenAI hook
- GitHub Actions CI for tests and syntax checks

## Repository Structure

```text
mba-strategy-command-center/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .github/workflows/ci.yml
├── assets/screenshots/
├── data/
│   ├── acquisition_targets.csv
│   ├── company_financials.csv
│   ├── competitor_benchmarks.csv
│   ├── customer_metrics.csv
│   ├── macro_assumptions.csv
│   ├── market_segments.csv
│   ├── risk_register.csv
│   └── strategy_initiatives.csv
├── docs/
│   └── deployment.md
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── engines/
│   ├── ui/
│   └── utils/
└── tests/
```

## Quick Start

```bash
cd mba-strategy-command-center
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Optional AI Setup

The included copilot works without external APIs. To connect it to a hosted model later, create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-key"
```

Then extend `src/engines/ai_copilot.py` where marked.

## Demo Data

All sample datasets live in `data/`. They represent a fictional B2B SaaS company, **Northstar Analytics**, and are safe to publish in a portfolio.

## Screenshots

Run the app and capture dashboard screenshots into `assets/screenshots/` before publishing your final GitHub README. Suggested screenshots:

- `executive-dashboard.png`
- `valuation-engine.png`
- `board-pack-generator.png`

## Testing

```bash
pytest
python -m compileall app.py src
```

## Deployment

See [docs/deployment.md](docs/deployment.md) for Streamlit Community Cloud, Render, Docker-style, and GitHub workflow guidance.

