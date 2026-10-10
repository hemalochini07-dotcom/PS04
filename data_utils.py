import pandas as pd
import numpy as np

COLUMN_ALIASES = {
    "date": ["date", "day", "timestamp", "campaign_date"],
    "campaign_id": ["campaign_id", "campaign", "campaign_name", "id"],
    "spend": ["spend", "cost", "amount_spent", "ad_spend"],
    "clicks": ["clicks", "click"],
    "impressions": ["impressions", "impression"],
    "conversions": ["conversions", "conversion", "purchases"]
}

def validate_data(df):
    data = df.copy()
    data.columns = [str(c).strip().lower().replace(" ", "_") for c in data.columns]
    rename = {}
    for standard, aliases in COLUMN_ALIASES.items():
        for col in data.columns:
            if col in aliases:
                rename[col] = standard
                break
    data = data.rename(columns=rename)
    missing = [c for c in ["date", "campaign_id", "spend", "clicks", "impressions", "conversions"] if c not in data.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date", "campaign_id"])
    for col in ["spend", "clicks", "impressions", "conversions"]:
        data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)
    if "ground_truth_incident" in data.columns:
        data["ground_truth_incident"] = data["ground_truth_incident"].astype(str).str.lower().isin(["true", "1", "yes", "y"])
    else:
        data["ground_truth_incident"] = False
    messages = []
    duplicate_count = int(data.duplicated(["date", "campaign_id"]).sum())
    if duplicate_count:
        data = data.drop_duplicates(["date", "campaign_id"], keep="last")
        messages.append(f"Removed {duplicate_count} duplicate campaign/date row(s).")
    if data.empty:
        raise ValueError("No valid rows found after checking the date and campaign columns.")
    data["ctr"] = np.where(data["impressions"] > 0, data["clicks"] / data["impressions"] * 100, 0)
    data["cpa"] = np.where(data["conversions"] > 0, data["spend"] / data["conversions"], np.nan)
    return data.sort_values(["campaign_id", "date"]).reset_index(drop=True), messages

def make_demo_data(seed=8):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=180, freq="D")
    rows = []
    for campaign_num in range(1, 21):
        campaign = f"CMP-{campaign_num:02d}"
        spend_base = rng.uniform(700, 6500)
        clicks_base = rng.uniform(90, 650)
        conv_base = rng.uniform(8, 65)
        for i, date in enumerate(dates):
            weekday_factor = 0.88 if date.dayofweek >= 5 else 1.0
            seasonal = 1 + 0.08 * np.sin(2 * np.pi * i / 30)
            spend = max(50, spend_base * weekday_factor * seasonal * rng.normal(1, 0.08))
            clicks = max(5, clicks_base * weekday_factor * rng.normal(1, 0.09))
            impressions = max(clicks + 1, clicks * rng.uniform(12, 28))
            conversions = max(0, int(round(conv_base * weekday_factor * rng.normal(1, 0.15))))
            incident = False
            # Seed a few clear incidents, labelled for demo evaluation.
            if campaign_num == 3 and i == 125:
                conversions = 0
                incident = True
            if campaign_num == 8 and i == 150:
                spend *= 2.3
                incident = True
            if campaign_num == 14 and i == 163:
                conversions = max(0, int(conv_base * 0.1))
                incident = True
            rows.append({
                "date": date, "campaign_id": campaign, "spend": round(spend, 2),
                "clicks": int(clicks), "impressions": int(impressions),
                "conversions": conversions, "ground_truth_incident": incident
            })
    return pd.DataFrame(rows)
