# Campaign Sentinel — Glacier Style Dashboard

A Streamlit campaign-monitoring demo with a dark navy / cyan theme, KPI cards, interactive charts, Smart Alerts, Incident Analysis, campaign monitoring, and alert performance evaluation.

## Run on Windows

1. Extract `Campaign_Sentinel_Glacier_Style_Updated.zip`.
2. Open the extracted `Campaign_Sentinel_GlacierStyle` folder in VS Code.
3. Open **Terminal → New Terminal** in that folder.
4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

6. Open the `Local URL` printed in the terminal (usually `http://localhost:8501`).

## Included pages

- **Overview (`app.py`)** — campaign KPIs, spend/conversion trend, severity breakdown, spend ranking and latest alerts.
- **Campaign Monitoring** — choose a campaign and metric to inspect over time.
- **Smart Alerts** — filter and investigate alerts, with CSV export.
- **Incident Analysis** — review an anomaly, its historical timeline and session-only status.
- **Alert Performance** — precision, recall, false-positive rate and confusion counts when labels are present.
- **Settings** — demo settings page.

## Data format

The included `data/daily_campaign_metrics.csv` is synthetic demo data, not organiser-provided or live campaign data. You can upload a CSV using the sidebar. Required columns are `date`, `campaign_id`, `spend`, `clicks`, `impressions`, and `conversions`. A `ground_truth_incident` column is optional and is used only for demo evaluation.

Alerts are statistical, rule-based investigation signals, not proof of a confirmed root cause. Evaluation results on synthetic data are demonstration-only.

## What changed

- Refreshed dashboard theme with rounded metric cards, cyan/teal accents and consistent styling.
- Added more interactive Plotly charts and icon-labelled metrics.
- Added `analytics.py` with a shared Streamlit cache so pages reuse anomaly detection/evaluation results rather than repeatedly recalculating them for the same dataset.
- Preserved the existing page set and detector behaviour as closely as possible.
