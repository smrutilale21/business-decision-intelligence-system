import os

import requests
import streamlit as st

BACKEND_URL = os.getenv(
    "BACKEND_URL", "http://127.0.0.1:8000/analyze"
)


st.set_page_config(
    page_title="AI-Powered Business Decision Intelligence System", layout="wide"
)


st.title("📊 AI-Powered Business Decision Intelligence System")


csv_file = st.file_uploader("Upload CSV File", type=["csv"])

pdf_file = st.file_uploader("Upload PDF Report (Optional)", type=["pdf"])

question = st.text_input("Ask Business Question")


if st.button("Analyze"):

    if csv_file and question:

        with st.spinner("Analyzing business data..."):

            files = {"csv_file": csv_file}

            if pdf_file:
                files["pdf_file"] = pdf_file

            response = requests.post(
                BACKEND_URL, files=files, data={"question": question}
            )

            result = response.json()

            if result.get("success"):

                data = result["response"]

                st.success("Analysis Complete")

                st.subheader("Business Problem")
                st.write(data["business_problem"])

                st.subheader("Data Insights")

                for item in data["data_insights"]:
                    st.write(f"- {item}")

                st.subheader("Probable Causes")

                for item in data["probable_causes"]:
                    st.write(f"- {item}")

                st.subheader("Recommendations")

                for item in data["recommendations"]:
                    st.write(f"- {item}")

                st.subheader("Evidence")

                for item in data["evidence"]:
                    st.write(f"- {item}")

                st.subheader("Priority")
                st.write(data["priority"])

                st.subheader("Confidence")
                st.write(data["confidence"])

                if result.get("chart_url"):

                    st.subheader("Generated Chart")

                    full_chart_url = (
                        BACKEND_URL.replace("/analyze", "") + result["chart_url"]
                    )

                    st.image(full_chart_url, width=750)

            else:
                st.error(result.get("error", "Unknown error occurred"))
