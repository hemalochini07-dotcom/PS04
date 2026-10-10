import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import get_analysis
from ui_theme import apply_theme

st.title("📊 Alert Performance")
st.caption("Review detection quality and make false positives and missed incidents visible.")
if "campaign_df" not in st.session_state:
    st.info("Return to Overview first to initialise the dataset.")
    st.stop()
df=st.session_state["campaign_df"]
alerts,result=get_analysis(df)
if "ground_truth_incident" not in df.columns or df["ground_truth_incident"].isna().all() or not df["ground_truth_incident"].astype(bool).any():
    st.warning("No positive ground-truth incident labels were found. Precision and recall may be unavailable or uninformative for this dataset.")
else:
    st.info("These metrics use the current dataset's incident labels. Synthetic demo scores are for demonstration only.")
c1,c2,c3=st.columns(3)
c1.metric("Precision",f"{result['precision']:.1%}" if result["precision"] is not None else "N/A")
c2.metric("Recall",f"{result['recall']:.1%}" if result["recall"] is not None else "N/A")
c3.metric("False-positive rate",f"{result['false_positive_rate']:.1%}" if result["false_positive_rate"] is not None else "N/A")
c4,c5,c6,c7=st.columns(4)
c4.metric("True positives",result["tp"]); c5.metric("False positives",result["fp"]); c6.metric("Missed incidents",result["fn"]); c7.metric("True negatives",result["tn"])
st.markdown("### Confusion counts")
counts=pd.DataFrame({"Outcome":["True positives","False positives","False negatives","True negatives"],"Count":[result["tp"],result["fp"],result["fn"],result["tn"]]})
fig=px.bar(counts,x="Outcome",y="Count",color="Outcome",template="plotly_dark",color_discrete_sequence=["#34d399","#fb7185","#fbbf24","#38bdf8"])
fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",showlegend=False)
st.plotly_chart(fig,use_container_width=True)
st.markdown("### How to read these metrics")
st.markdown("- **Precision:** fraction of generated alerts that match labelled incident observations.\n- **Recall:** fraction of labelled incidents detected.\n- **False-positive rate:** fraction of labelled non-incident observations incorrectly flagged.\n- Alerts are investigative signals, not proof of a confirmed root cause.")
