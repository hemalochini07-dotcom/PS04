import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import get_analysis
from ui_theme import apply_theme

st.title("🧭 Incident Analysis")
st.caption("Investigate unusual behaviour and review the evidence behind detected anomalies.")
if "campaign_df" not in st.session_state:
    st.info("Return to Overview first to initialise the dataset.")
    st.stop()
df=st.session_state["campaign_df"].copy()
df["date"]=pd.to_datetime(df["date"],errors="coerce")
alerts,_=get_analysis(st.session_state["campaign_df"])
if alerts.empty:
    st.success("No incidents to investigate in the current dataset.")
    st.stop()

campaigns=sorted(df["campaign_id"].astype(str).unique().tolist())
selected_campaign=st.selectbox("Campaign",["All campaigns"]+campaigns)
view=alerts if selected_campaign=="All campaigns" else alerts[alerts["campaign_id"].astype(str)==selected_campaign]
if view.empty:
    st.info("No alerts for this campaign.")
    st.stop()
selected_idx=st.selectbox("Choose incident",view.index.tolist(),format_func=lambda i:f"{view.loc[i,'date']} · {view.loc[i,'campaign_id']} · {view.loc[i,'category']}")
a=view.loc[selected_idx]
st.markdown(f"### {a['campaign_id']} · {a['category']}")
c1,c2,c3=st.columns(3)
c1.metric("📍 Observed",f"{a['observed']:,.2f}")
c2.metric("📏 Historical baseline",f"{a['baseline']:,.2f}")
c3.metric("↕️ Change",f"{a['change_pct']:+.1f}%" if pd.notna(a["change_pct"]) else "N/A")
st.write(a["explanation"])
st.info("Suggested diagnostic step: "+a["recommended_action"])

campaign=df[df["campaign_id"].astype(str)==str(a["campaign_id"])].sort_values("date")
metric=a["metric"]
fig=px.line(campaign,x="date",y=metric,title=f"{a['campaign_id']} · {metric.title()} timeline",markers=True,template="plotly_dark",labels={metric:metric.title(),"date":"Date"})
alert_date=pd.to_datetime(a["date"],errors="coerce")
point=campaign[campaign["date"].dt.date==alert_date.date()] if pd.notna(alert_date) else campaign.iloc[0:0]
if not point.empty:
    fig.add_scatter(x=point["date"],y=point[metric],mode="markers",marker=dict(size=13,color="#fb7185",symbol="x",line=dict(width=2)),name="Detected anomaly")
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",hovermode="x unified")
st.plotly_chart(fig,use_container_width=True)

if "incident_status" not in st.session_state: st.session_state["incident_status"]={}
key=f"{a['campaign_id']}_{a['date']}_{a['category']}"
status_options=["Open","Investigating","Resolved"]
status=st.selectbox("Incident status",status_options,index=status_options.index(st.session_state["incident_status"].get(key,"Open")))
if st.button("💾 Save incident status"):
    st.session_state["incident_status"][key]=status
    st.success(f"Status saved for this session: {status}")
