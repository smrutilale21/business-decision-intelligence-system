import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/analyze")

st.set_page_config(
    page_title="AI-Powered Business Decision Intelligence System",
    page_icon="📊",
    layout="wide",
)

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

with st.sidebar:

    st.markdown("## 📌 Sample Questions")

    sample_questions = [
        "Which region has the highest revenue growth potential?",
        "Show monthly sales trends over time.",
        "Which product categories have low profit margins?",
        "What factors are reducing overall profitability?",
        "Which business segment requires immediate attention?",
    ]

    with st.container(border=True):
        selected_sample_question = st.radio(
            "Choose a sample business question:",
            sample_questions,
            label_visibility="collapsed",
        )

    if selected_sample_question:
        st.session_state.selected_question = selected_sample_question

    st.divider()
    st.markdown("## 📊 Analysis Summary")

    if st.session_state.analysis_data is None:
        st.markdown(
            """
            <div style="
                background-color:#111827;
                padding:0.9rem 1rem;
                border-radius:10px;
                border:1px solid #374151;
                color:#6B7280;
                font-size:0.9rem;
                text-align:center;
            ">
                📂 KPIs will appear after analysis
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        data = st.session_state.analysis_data

        kpi_card_style = """
            background-color:#111827;
            padding:0.7rem 1rem;
            border-radius:10px;
            margin-bottom:0.7rem;
            border:1px solid #374151;
        """

        st.markdown(
            f"""
            <div style="{kpi_card_style}">
                <div style="font-size:0.85rem; color:#9CA3AF;">Priority</div>
                <div style="font-size:1.4rem; font-weight:600;">{data["priority"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="{kpi_card_style}">
                <div style="font-size:0.85rem; color:#9CA3AF;">Confidence</div>
                <div style="font-size:1.4rem; font-weight:600;">{data["confidence"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="{kpi_card_style}">
                <div style="font-size:0.85rem; color:#9CA3AF;">Analysis Status</div>
                <div style="font-size:1.4rem; font-weight:600;">✅ Completed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <style>
        .main { padding-top: 1rem; }

        .block-container {
            padding-top: 1.5rem;
            max-width: 1200px;
        }

        .stButton > button {
            width: 100%;
            height: 3rem;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
        }

        .metric-card {
            background-color: #111827;
            border: 1px solid #374151;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .insight-card {
            background-color: #111827;
            border: 1px solid #374151;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .section-title {
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 AI-Powered Business Decision Intelligence System")

st.caption(
    "Analyze business datasets using AI-generated insights, "
    "recommendations, risk analysis, and strategic decision intelligence."
)

st.divider()

input_col1, input_col2 = st.columns(2)

with input_col1:
    csv_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
    )

with input_col2:
    pdf_file = st.file_uploader(
        "Upload PDF Report (Optional)",
        type=["pdf"],
    )

question = st.text_area(
    "Ask Business Question",
    value=st.session_state.selected_question,
    placeholder="Example: Which region has the highest sales growth potential?",
    height=120,
)

analyze_button = st.button("🚀 Analyze Business Data")

st.divider()

if analyze_button:

    if csv_file and question:

        with st.spinner("Analyzing business data..."):

            files = {"csv_file": csv_file}

            if pdf_file:
                files["pdf_file"] = pdf_file

            response = requests.post(
                BACKEND_URL,
                files=files,
                data={"question": question},
                timeout=180,
            )

            result = response.json()

            if result.get("success"):
                st.session_state.analysis_data = result["response"]
                st.session_state.analysis_result = result
                st.rerun()

            else:
                st.error(result.get("error", "Unknown error occurred"))

    else:
        st.warning("Please upload a CSV file and enter a business question.")

if st.session_state.analysis_data is not None:

    data = st.session_state.analysis_data
    result = st.session_state.analysis_result

    st.success("✅ Analysis Completed")

    st.markdown(
        '<h2 class="section-title">🧠 Executive Summary</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="insight-card">
            <h4>Business Problem</h4>
            <p>{data["business_problem"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns(2)

    with left_col:

        st.markdown(
            '<h3 class="section-title">📈 Data Insights</h3>',
            unsafe_allow_html=True,
        )

        for item in data["data_insights"]:
            st.markdown(
                f'<div class="insight-card"> {item}</div>',
                unsafe_allow_html=True,
            )

    with right_col:

        st.markdown(
            '<h3 class="section-title">⚠️ Probable Causes</h3>',
            unsafe_allow_html=True,
        )

        for item in data["probable_causes"]:
            st.markdown(
                f'<div class="insight-card"> {item}</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<h3 class="section-title">💡 Recommendations</h3>',
        unsafe_allow_html=True,
    )

    for item in data["recommendations"]:
        st.markdown(
            f'<div class="insight-card"> {item}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("📑 Supporting Evidence"):
        for item in data["evidence"]:
            st.markdown(
                f'<div class="insight-card"> {item}</div>',
                unsafe_allow_html=True,
            )

    if result.get("chart_url"):

        st.markdown(
            '<h3 class="section-title">📉 Business Visualization</h3>',
            unsafe_allow_html=True,
        )

        full_chart_url = BACKEND_URL.replace("/analyze", "") + result["chart_url"]
        st.image(full_chart_url, width=850)

    report_text = f"""BUSINESS DECISION INTELLIGENCE REPORT
====================================

Business Problem
----------------
{data["business_problem"]}

Data Insights
-------------
"""
    for item in data["data_insights"]:
        report_text += f"- {item}\n"

    report_text += "\nProbable Causes\n----------------\n"
    for item in data["probable_causes"]:
        report_text += f"- {item}\n"

    report_text += "\nRecommendations\n----------------\n"
    for item in data["recommendations"]:
        report_text += f"- {item}\n"

    report_text += "\nEvidence\n---------\n"
    for item in data["evidence"]:
        report_text += f"- {item}\n"

    report_text += f"""
Priority
--------
{data["priority"]}

Confidence
----------
{data["confidence"]}
"""

    st.download_button(
        label="⬇ Download Business Report",
        data=report_text,
        file_name="business_analysis_report.txt",
        mime="text/plain",
    )
