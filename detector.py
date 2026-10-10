import pandas as pd
import numpy as np

REQUIRED = ["date", "campaign_id", "spend", "clicks", "impressions", "conversions"]

def detect_anomalies(df):
    """Detect anomalies using each campaign's past observations only."""
    if df.empty:
        return pd.DataFrame(columns=[
            "date", "campaign_id", "metric", "observed", "baseline",
            "change_pct", "severity", "category", "explanation", "recommended_action",
            "ground_truth_incident"
        ])

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date", "campaign_id"]).sort_values(["campaign_id", "date"])
    results = []

    for campaign, group in data.groupby("campaign_id"):
        group = group.sort_values("date").reset_index(drop=True)
        for i in range(14, len(group)):
            row = group.iloc[i]
            history = group.iloc[max(0, i-28):i]
            if len(history) < 7:
                continue

            # Check multiple metrics with robust historical baselines.
            checks = []
            for metric in ["spend", "clicks", "conversions"]:
                hist = pd.to_numeric(history[metric], errors="coerce").dropna()
                value = pd.to_numeric(pd.Series([row[metric]]), errors="coerce").iloc[0]
                if hist.empty or pd.isna(value):
                    continue
                baseline = float(hist.median())
                mad = float((hist - baseline).abs().median())
                # MAD-based threshold with a small floor for low-variance series.
                threshold = max(3.5 * 1.4826 * mad, abs(baseline) * 0.35, 1.0)
                deviation = float(value - baseline)
                if abs(deviation) > threshold:
                    pct = ((value - baseline) / abs(baseline) * 100) if baseline != 0 else None
                    checks.append((metric, float(value), baseline, pct, deviation))

            if not checks:
                continue

            # Prefer a conversion collapse, then spend deviation, then other metrics.
            checks.sort(key=lambda x: (
                0 if x[0] == "conversions" and x[1] < x[2] * 0.25 else
                1 if x[0] == "spend" else 2
            ))
            metric, value, baseline, pct, deviation = checks[0]
            incident = bool(row.get("ground_truth_incident", False))
            if metric == "conversions" and baseline > 0 and value <= baseline * 0.25:
                category = "Possible tracking failure / conversion drop"
                severity = "Critical" if value == 0 else "Warning"
                action = "Check the conversion tag, event logs, and recent tracking changes."
            elif metric == "spend" and value > baseline * 1.5:
                category = "Unexpected spend increase"
                severity = "Critical" if value > baseline * 2 else "Warning"
                action = "Review daily budget, bid strategy, and campaign change history."
            elif metric == "spend" and value < baseline * 0.5:
                category = "Unexpected spend drop"
                severity = "Warning"
                action = "Check campaign delivery, budget limits, and ad approval status."
            else:
                category = f"Unusual {metric} movement"
                severity = "Warning"
                action = f"Compare {metric} with recent campaign settings and related metrics."

            pct_text = f"{pct:+.1f}%" if pct is not None else "not calculable from a zero baseline"
            explanation = (
                f"{campaign}: {metric} is {value:,.1f}, compared with a historical "
                f"median of {baseline:,.1f} ({pct_text}). This is unusual relative to "
                f"the campaign's recent history; the underlying cause is not confirmed."
            )
            results.append({
                "date": row["date"].date().isoformat(),
                "campaign_id": campaign,
                "metric": metric,
                "observed": round(value, 2),
                "baseline": round(baseline, 2),
                "change_pct": round(pct, 2) if pct is not None else None,
                "severity": severity,
                "category": category,
                "explanation": explanation,
                "recommended_action": action,
                "ground_truth_incident": incident
            })

    if not results:
        return pd.DataFrame(columns=[
            "date", "campaign_id", "metric", "observed", "baseline",
            "change_pct", "severity", "category", "explanation", "recommended_action",
            "ground_truth_incident"
        ])

    alerts = pd.DataFrame(results).sort_values(["date", "severity"], ascending=[False, True])
    # Group repeated alerts by campaign + category within the result set.
    # Keep the latest alert per campaign/category to reduce duplicate noise.
    alerts = alerts.drop_duplicates(subset=["campaign_id", "category"], keep="first")
    return alerts.reset_index(drop=True)

def evaluate_detection(df, alerts):
    """Evaluate only when ground-truth incident labels are present."""
    if "ground_truth_incident" not in df.columns or df["ground_truth_incident"].isna().all():
        return {"precision": None, "recall": None, "false_positive_rate": None, "tp": 0, "fp": 0, "fn": 0, "tn": 0}

    labelled = df.copy()
    labelled["ground_truth_incident"] = labelled["ground_truth_incident"].fillna(False).astype(bool)
    detected_keys = set()
    if not alerts.empty:
        for _, r in alerts.iterrows():
            detected_keys.add((str(r["campaign_id"]), str(r["date"])))
    actual = set()
    for _, r in labelled[labelled["ground_truth_incident"]].iterrows():
        actual.add((str(r["campaign_id"]), pd.to_datetime(r["date"]).date().isoformat()))
    tp = len(detected_keys & actual)
    fp = len(detected_keys - actual)
    fn = len(actual - detected_keys)
    total_non_incident = int((~labelled["ground_truth_incident"]).sum())
    tn = max(total_non_incident - fp, 0)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    fpr = fp / (fp + tn) if fp + tn else None
    return {"precision": precision, "recall": recall, "false_positive_rate": fpr, "tp": tp, "fp": fp, "fn": fn, "tn": tn}
