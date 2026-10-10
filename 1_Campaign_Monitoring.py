import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import validate_data
from analytics import get_analysis
from ui_theme import apply_theme

st.title("📈 Campaign Monitoring")
st.caption("Compare campaign performance with its historical behaviour.")
if "campaign_df" not in st.session_state:
    st.info("Return to Overview first to initialise the dataset.")
    st.stop()
df,_=validate_data(st.session_state["campaign_df"].copy())
campaigns=sorted(df["campaign_id"].astype(str).unique().tolist())
selected=st.selectbox("Choose a campaign",campaigns)
campaign_df=df[df["campaign_id"].astype(str)==selected].sort_values("date")
metric=st.selectbox("Metric",["spend","clicks","impressions","conversions","ctr","cpa"])
fig=px.line(campaign_df,x="date",y=metric,title=f"{selected} · {metric.title()} over time",markers=True,template="plotly_dark")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",hovermode="x unified")
st.plotly_chart(fig,use_container_width=True)
alerts,_=get_analysis(df)
campaign_alerts=alerts[alerts["campaign_id"].astype(str)==selected] if not alerts.empty else alerts
st.markdown("### 🚨 Detected anomalies")
if campaign_alerts.empty: st.success("No anomalies detected for this campaign with the current rules.")
else: st.dataframe(campaign_alerts.drop(columns=["ground_truth_incident"],errors="ignore"),use_container_width=True,hide_index=True)
st.markdown("### 🧾 Recent metrics")
st.dataframe(campaign_df.tail(20),use_container_width=True,hide_index=True)
