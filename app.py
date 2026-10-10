import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
from pathlib import Path
from data_utils import make_demo_data, validate_data
from analytics import get_analysis
from ui_theme import apply_theme

st.set_page_config(page_title="Campaign Sentinel", page_icon="◉", layout="wide")
apply_theme()

@st.cache_data(show_spinner=False)
def load_included_data(path, modified_time):
    return pd.read_csv(path)

st.sidebar.markdown("# ◉ Campaign Sentinel")
st.sidebar.caption("CAMPAIGN INTELLIGENCE PLATFORM")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Data source")
uploaded = st.sidebar.file_uploader("Upload campaign CSV", type=["csv"], help="Required: date, campaign identifier, spend, clicks, impressions and conversions.")

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        source_df, messages = validate_data(raw)
        # Avoid overwriting session state on every rerun when the same upload remains selected.
        signature = hashlib.sha256(uploaded.getvalue()).hexdigest()
        if st.session_state.get("upload_signature") != signature:
            st.session_state["campaign_df"] = source_df
            st.session_state["data_source"] = f"Uploaded CSV · {uploaded.name}"
            st.session_state["upload_signature"] = signature
        for message in messages:
            st.sidebar.info(message)
    except Exception as exc:
        st.sidebar.error(f"Could not read this CSV: {exc}")

if "campaign_df" not in st.session_state:
    dataset_path = Path(__file__).parent / "data" / "daily_campaign_metrics.csv"
    if dataset_path.exists():
        try:
            raw = load_included_data(str(dataset_path), dataset_path.stat().st_mtime)
            st.session_state["campaign_df"], _ = validate_data(raw)
            st.session_state["data_source"] = "Included demo dataset"
        except Exception as exc:
            st.sidebar.warning(f"Included dataset could not be loaded: {exc}")
            st.session_state["campaign_df"], _ = validate_data(make_demo_data())
            st.session_state["data_source"] = "Synthetic demo fallback"
    else:
        st.session_state["campaign_df"], _ = validate_data(make_demo_data())
        st.session_state["data_source"] = "Synthetic demo data"

# Normalise once and preserve the validated frame in session state.
df, validation_messages = validate_data(st.session_state["campaign_df"].copy())
st.session_state["campaign_df"] = df
alerts, metrics = get_analysis(df)

st.markdown("""
<div class="cs-hero">
  <div class="cs-eyebrow">PS-04 · INTELLIGENT MARKETING OPERATIONS</div>
  <h1>Campaign <span>Sentinel</span></h1>
  <div class="cs-pill">✦ Adaptive anomaly alerting · without alert fatigue</div>
  <p>See beyond the noise. Detect unusual campaign behaviour, understand what changed, and prioritise the incidents that deserve attention.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📡 Performance at a glance")
c1,c2,c3,c4 = st.columns(4)
c1.metric("📣 Campaigns", f"{df['campaign_id'].nunique():,}")
c2.metric("💰 Total spend", f"${df['spend'].sum():,.0f}")
c3.metric("🎯 Conversions", f"{int(df['conversions'].sum()):,}")
c4.metric("🚨 Unique alerts", f"{len(alerts):,}")
c5,c6,c7,c8 = st.columns(4)
c5.metric("🔴 Critical", int((alerts["severity"]=="Critical").sum()) if not alerts.empty else 0)
c6.metric("🟡 Warnings", int((alerts["severity"]=="Warning").sum()) if not alerts.empty else 0)
c7.metric("Precision", f"{metrics['precision']:.1%}" if metrics["precision"] is not None else "N/A")
c8.metric("Recall", f"{metrics['recall']:.1%}" if metrics["recall"] is not None else "N/A")

left,right = st.columns([1.55,1])
with left:
    st.markdown("### 📈 Spend & conversion trend")
    trend = df.groupby("date",as_index=False).agg(spend=("spend","sum"),conversions=("conversions","sum"))
    fig = px.line(trend,x="date",y=["spend","conversions"],color_discrete_sequence=["#38bdf8","#34d399"],labels={"value":"Daily total","date":"Date","variable":"Metric"})
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=10,r=10,t=15,b=10),legend_title_text="",hovermode="x unified")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.markdown("### 🧭 Alert severity")
    if alerts.empty:
        st.success("No anomalies detected in this dataset.")
    else:
        sev=alerts["severity"].value_counts().rename_axis("severity").reset_index(name="count")
        fig2=px.pie(sev,names="severity",values="count",hole=.62,color="severity",color_discrete_map={"Critical":"#fb7185","Warning":"#fbbf24","Informational":"#38bdf8"})
        fig2.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0,t=10,b=10),legend_title_text="")
        st.plotly_chart(fig2,use_container_width=True)

st.markdown("### 🏆 Campaign monitoring")
col_a,col_b=st.columns(2)
with col_a:
    campaign_spend=df.groupby("campaign_id",as_index=False).agg(spend=("spend","sum")).sort_values("spend",ascending=False).head(10)
    f=px.bar(campaign_spend,x="spend",y="campaign_id",orientation="h",color="spend",title="Top 10 campaigns by spend",labels={"spend":"Total spend (USD)","campaign_id":"Campaign"},color_continuous_scale=["#164e63","#22d3ee"])
    f.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",yaxis={"categoryorder":"total ascending"},coloraxis_showscale=False)
    st.plotly_chart(f,use_container_width=True)
with col_b:
    if "channel" in df.columns:
        group_col="channel"
        chart_title="Spend by channel"
    else:
        # Dataset doesn't contain channel labels; use the 8 highest-spend campaigns instead.
        group_col="campaign_id"
        chart_title="Spend distribution by campaign"
    grouped=df.groupby(group_col,as_index=False).agg(spend=("spend","sum")).sort_values("spend",ascending=False).head(8)
    f2=px.pie(grouped,names=group_col,values="spend",hole=.55,title=chart_title,color_discrete_sequence=px.colors.qualitative.Safe)
    f2.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=0,r=0,t=35,b=0),legend_title_text="")
    st.plotly_chart(f2,use_container_width=True)

st.markdown("### ⚡ Latest alerts")
if alerts.empty:
    st.info("No alerts found. Upload a campaign CSV or explore the included demo dataset.")
else:
    columns=[c for c in ["date","campaign_id","metric","observed","baseline","severity","category"] if c in alerts.columns]
    st.dataframe(alerts[columns].head(8),use_container_width=True,hide_index=True)

with st.expander("ℹ️ About this dashboard"):
    st.write(f"**Current source:** {st.session_state.get('data_source','Unknown')}")
    st.write("Alerts are rule-based investigation signals, not confirmed root causes. If you use synthetic demo data, displayed results are for demonstration only.")
    st.write("Use the sidebar pages for campaign monitoring, Smart Alerts, Incident Analysis, alert performance and settings.")
