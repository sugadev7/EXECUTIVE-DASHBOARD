# Deployment Guide

## Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Select the repository and set the main file path to `app.py`.
4. Confirm Python dependencies are installed from `requirements.txt`.
5. Deploy.

## Render

1. Create a new Web Service from your GitHub repository.
2. Build command:

```bash
pip install -r requirements.txt
```

3. Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## Local Production Smoke Test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
streamlit run app.py
```

## GitHub Actions

The included workflow runs tests and Python compilation on every push and pull request.

