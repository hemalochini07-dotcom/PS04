import streamlit as st
import plotly.express as px
from analytics import get_analysis
from ui_theme import apply_theme

st.title("🔔 Smart Alerts")
st.caption("Prioritised anomaly alerts with explanations and recommended diagnostic steps.")
if "campaign_df" not in st.session_state:
    st.info("Return to Overview first to initialise the dataset.")
    st.stop()

df = st.session_state["campaign_df"]
alerts, _ = get_analysis(df)
if alerts.empty:
    st.success("No anomalies detected in the current dataset.")
    st.stop()

c1,c2,c3=st.columns(3)
c1.metric("🚨 Total unique alerts",len(alerts))
c2.metric("🔴 Critical",int((alerts["severity"]=="Critical").sum()))
c3.metric("🟡 Warnings",int((alerts["severity"]=="Warning").sum()))
st.markdown("### 🎛️ Filter alerts")
f1,f2=st.columns(2)
with f1:
    severity=st.multiselect("Severity",["Critical","Warning","Informational"],default=["Critical","Warning"])
with f2:
    category=st.selectbox("Category",["All"]+sorted(alerts["category"].dropna().unique().tolist()))
view=alerts[alerts["severity"].isin(severity)]
if category!="All": view=view[view["category"]==category]
if not view.empty:
    chart=view["severity"].value_counts().rename_axis("severity").reset_index(name="count")
    fig=px.bar(chart,x="severity",y="count",color="severity",title="Filtered alerts by severity",color_discrete_map={"Critical":"#fb7185","Warning":"#fbbf24","Informational":"#38bdf8"},template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(view.drop(columns=["ground_truth_incident"],errors="ignore"),use_container_width=True,hide_index=True)
    st.markdown("### 🧩 Alert investigation")
    selected=st.selectbox("Choose an alert",view.index.tolist(),format_func=lambda i:f"{view.loc[i,'date']} · {view.loc[i,'campaign_id']} · {view.loc[i,'category']}")
    alert=view.loc[selected]
    st.markdown(f"#### {alert['severity']} · {alert['category']}")
    st.write(alert["explanation"])
    st.info("Recommended first step: "+alert["recommended_action"])
    st.caption("This category is a rule-based hypothesis, not a confirmed root cause.")
else:
    st.info("No alerts match the selected filters.")
csv=alerts.drop(columns=["ground_truth_incident"],errors="ignore").to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download alerts as CSV",csv,"campaign_alerts.csv","text/csv")
