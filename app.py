
import os
from typing import Dict, TypedDict

import matplotlib.pyplot as plt
import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
import streamlit as st

# --- 1. Page & Custom Theme Setup ---
st.set_page_config(
    page_title="Paid Media AI Agent Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .metric-card {
        background: #1e222d;
        border: 1px solid #2e364f;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title {
        color: #8b92a5;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00d4b1;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- 2. Agent Logic & LangGraph Workflow ---
class AgentState(TypedDict):
    raw_data: dict
    computed_metrics: dict
    final_report: str


def compute_metrics(raw: dict) -> dict:
    google_spend = raw["google_ads"]["spend"]
    meta_spend = raw["meta_ads"]["spend"]
    total_spend = google_spend + meta_spend

    total_clicks = raw["google_ads"]["clicks"] + raw["meta_ads"]["clicks"]
    total_mqls = raw["crm_warehouse"]["mqls"]
    target_cpa = raw["business_targets"]["target_cpa"]

    actual_cpa = (
        round(total_spend / total_mqls, 2) if total_mqls > 0 else 0.0
    )
    overall_cpc = (
        round(total_spend / total_clicks, 2) if total_clicks > 0 else 0.0
    )
    cpa_variance_pct = (
        round(((actual_cpa - target_cpa) / target_cpa) * 100, 2)
        if target_cpa > 0
        else 0.0
    )

    return {
        "total_spend": total_spend,
        "total_clicks": total_clicks,
        "total_mqls": total_mqls,
        "actual_cpa": actual_cpa,
        "target_cpa": target_cpa,
        "cpa_variance_pct": cpa_variance_pct,
        "overall_cpc": overall_cpc,
        "pipeline_usd": raw["crm_warehouse"]["pipeline_usd"],
        "google_share_pct": (
            round((google_spend / total_spend) * 100, 1)
            if total_spend > 0
            else 0.0
        ),
        "meta_share_pct": (
            round((meta_spend / total_spend) * 100, 1) if total_spend > 0 else 0.0
        ),
    }


def run_agent(raw_data: dict, api_key: str) -> dict:
    computed = compute_metrics(raw_data)

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="openai/gpt-oss-120b",
        temperature=0.0,
    )

    system_prompt = """
    You are a Senior Paid Media Strategist. Your job is to analyze pre-computed marketing KPIs.

    STRICT RULES TO AVOID HALLUCINATION:
    1. Use ONLY the exact numbers provided in the input prompt.
    2. Do NOT perform any math or alter any metrics yourself.
    3. If Actual CPA > Target CPA, explicitly flag it as a performance bottleneck.

    Format your response in a clean Slack-ready markdown structure:
    - 📊 **Weekly Performance Summary**
    - 🔍 **Channel Breakdown & Root Cause Analysis**
    - 🎯 **Recommended Actions for Next Week**
    """

    user_prompt = f"""
    PRE-CALCULATED KPI DATA:
    - Total Ad Spend: ${computed['total_spend']} (Google: {computed['google_share_pct']}%, Meta: {computed['meta_share_pct']}%)
    - Total MQLs: {computed['total_mqls']}
    - Actual CPA: ${computed['actual_cpa']}
    - Target CPA: ${computed['target_cpa']} (Variance: {computed['cpa_variance_pct']}%)
    - Overall CPC: ${computed['overall_cpc']}
    - Pipeline Generated: ${computed['pipeline_usd']}

    RAW CHANNEL BREAKDOWN:
    - Google Ads: Spend ${raw_data['google_ads']['spend']}, Clicks {raw_data['google_ads']['clicks']}
    - Meta Ads: Spend ${raw_data['meta_ads']['spend']}, Clicks {raw_data['meta_ads']['clicks']}
    """

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
    )

    return {"computed": computed, "report": response.content}


# --- 3. Sidebar Inputs & Configuration ---
st.sidebar.title("⚙️ Control Panel")

# API Key Handling
default_key = os.environ.get("GROQ_API_KEY", "")
groq_api_key = st.sidebar.text_input(
    "Groq API Key", value=default_key, type="password"
)

# Data Input Source Selector
input_source = st.sidebar.radio(
    "📥 Choose Data Source",
    options=["Manual Input", "Upload CSV File", "Google Sheet URL"],
)

# Default values initialization
g_spend, g_clicks = 500.0, 800
m_spend, m_clicks = 400.0, 1200
mqls, pipeline, target_cpa = 45, 30000.0, 50.0

if input_source == "Manual Input":
    st.sidebar.subheader("🔵 Google Ads")
    g_spend = st.sidebar.number_input("Google Spend ($)", value=g_spend, step=50.0)
    g_clicks = st.sidebar.number_input("Google Clicks", value=g_clicks, step=10)

    st.sidebar.subheader("🟣 Meta Ads")
    m_spend = st.sidebar.number_input("Meta Spend ($)", value=m_spend, step=50.0)
    m_clicks = st.sidebar.number_input("Meta Clicks", value=m_clicks, step=10)

    st.sidebar.subheader("💼 CRM & Targets")
    mqls = st.sidebar.number_input("MQLs / Leads", value=mqls, step=1)
    pipeline = st.sidebar.number_input("Pipeline ($)", value=pipeline, step=1000.0)
    target_cpa = st.sidebar.number_input("Target CPA ($)", value=target_cpa, step=5.0)

elif input_source == "Upload CSV File":
    st.sidebar.subheader("📁 CSV Upload")
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("CSV Uploaded!")
            # Assuming CSV has aggregated sums or single row values
            g_spend = float(df["google_spend"].sum()) if "google_spend" in df else g_spend
            g_clicks = int(df["google_clicks"].sum()) if "google_clicks" in df else g_clicks
            m_spend = float(df["meta_spend"].sum()) if "meta_spend" in df else m_spend
            m_clicks = int(df["meta_clicks"].sum()) if "meta_clicks" in df else m_clicks
            mqls = int(df["mqls"].sum()) if "mqls" in df else mqls
            pipeline = float(df["pipeline"].sum()) if "pipeline" in df else pipeline
            target_cpa = float(df["target_cpa"].iloc[0]) if "target_cpa" in df else target_cpa
        except Exception as e:
            st.sidebar.error(f"CSV read error: {e}")
    else:
        st.sidebar.info("CSV Structure Expected Columns: `google_spend`, `google_clicks`, `meta_spend`, `meta_clicks`, `mqls`, `pipeline`, `target_cpa`")

elif input_source == "Google Sheet URL":
    st.sidebar.subheader("🔗 Google Sheet")
    sheet_url = st.sidebar.text_input("Public Google Sheet URL")
    target_cpa = st.sidebar.number_input("Target CPA ($)", value=target_cpa, step=5.0)

    if sheet_url:
        try:
            # Convert normal share link to export CSV link
            if "/edit" in sheet_url:
                csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
            else:
                csv_url = sheet_url

            df = pd.read_csv(csv_url)
            st.sidebar.success("Google Sheet Connected!")
            
            g_spend = float(df["google_spend"].sum()) if "google_spend" in df else g_spend
            g_clicks = int(df["google_clicks"].sum()) if "google_clicks" in df else g_clicks
            m_spend = float(df["meta_spend"].sum()) if "meta_spend" in df else m_spend
            m_clicks = int(df["meta_clicks"].sum()) if "meta_clicks" in df else m_clicks
            mqls = int(df["mqls"].sum()) if "mqls" in df else mqls
            pipeline = float(df["pipeline"].sum()) if "pipeline" in df else pipeline
            if "target_cpa" in df:
                target_cpa = float(df["target_cpa"].iloc[0])
        except Exception as e:
            st.sidebar.error("Public Sheet URL check karein (Anyone with link view access needed).")

# Raw Payload Assembly
raw_payload = {
    "google_ads": {"spend": g_spend, "clicks": g_clicks},
    "meta_ads": {"spend": m_spend, "clicks": m_clicks},
    "crm_warehouse": {"mqls": mqls, "pipeline_usd": pipeline},
    "business_targets": {"target_cpa": target_cpa},
}

computed_live = compute_metrics(raw_payload)

# --- 4. Main Dashboard Header ---
st.title("🎯 Paid Media AI Agent Dashboard")
st.caption(
    "LangGraph Orchestration • Deterministic Math Engine • Multi-Source Data Support"
)
st.divider()

# Top Metric Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""<div class="metric-card">
        <div class="metric-title">Total Spend</div>
        <div class="metric-value">${computed_live['total_spend']:,.2f}</div>
    </div>""",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""<div class="metric-card">
        <div class="metric-title">Total MQLs</div>
        <div class="metric-value">{computed_live['total_mqls']}</div>
    </div>""",
        unsafe_allow_html=True,
    )

with c3:
    cpa_color = (
        "#00d4b1"
        if computed_live["actual_cpa"] <= computed_live["target_cpa"]
        else "#ff4b4b"
    )
    st.markdown(
        f"""<div class="metric-card">
        <div class="metric-title">Actual CPA</div>
        <div class="metric-value" style="color: {cpa_color};">${computed_live['actual_cpa']:.2f}</div>
    </div>""",
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""<div class="metric-card">
        <div class="metric-title">Target CPA</div>
        <div class="metric-value">${computed_live['target_cpa']:.2f}</div>
    </div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# --- 5. Visual Charts Section ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Spend Share by Channel")
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    fig1.patch.set_facecolor("#0e1117")
    ax1.set_facecolor("#0e1117")

    labels = ["Google Ads", "Meta Ads"]
    spends = [g_spend, m_spend]
    colors = ["#4285F4", "#0081FB"]

    if sum(spends) > 0:
        ax1.pie(
            spends,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            textprops={"color": "white"},
            startangle=90,
        )
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.info("Spend zero hai, chart display nahi ho sakta.")

with col_right:
    st.subheader("🎯 CPA Comparison")
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    fig2.patch.set_facecolor("#0e1117")
    ax2.set_facecolor("#0e1117")

    categories = ["Actual CPA", "Target CPA"]
    values = [computed_live["actual_cpa"], target_cpa]
    bar_colors = ["#ff4b4b" if values[0] > values[1] else "#00d4b1", "#8b92a5"]

    ax2.bar(categories, values, color=bar_colors, width=0.5)
    ax2.tick_params(colors="white")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("white")
    ax2.spines["bottom"].set_color("white")

    st.pyplot(fig2)

st.divider()

# --- 6. Execution Button & Agent Report Output ---
if st.button("🚀 Agent Se Strategic Report Generate Karein", type="primary"):
    if not groq_api_key:
        st.error(
            "⚠️ Groq API Key required hai. Sidebar mein apni key enter karein."
        )
    else:
        with st.spinner("LangGraph Agent reasoning running..."):
            try:
                res = run_agent(raw_payload, groq_api_key)
                st.subheader("📝 Agent Generated Insights")
                st.markdown(res["report"])
            except Exception as e:
                st.error(f"Error: {str(e)}")