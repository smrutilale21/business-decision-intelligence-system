import streamlit as st
import requests


st.set_page_config(
    page_title="AI Business Decision Intelligence System",
    page_icon="📊",
    layout="wide"
)


st.title("📊 AI Business Decision Intelligence System")

st.markdown(
    """
Upload business dataset and ask intelligent business questions.
"""
)


uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


question = st.text_input(
    "Ask business question",
    placeholder="Which product has the highest sales?"
)


if st.button("Analyze"):

    if uploaded_file is None:
        st.warning("Please upload CSV file")

    elif not question.strip():
        st.warning("Please enter question")

    else:

        with st.spinner("Analyzing business data..."):

            response = requests.post(
                "https://business-decision-intelligence-system.onrender.com/analyze",
                files={
                    "file": uploaded_file
                },
                data={
                    "question": question
                }
            )
            result = response.json()

            if result["success"]:

                data = result["response"]

                st.success("Analysis completed")

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

                st.subheader("Priority")
                st.write(data["priority"])

                st.subheader("Confidence")
                st.write(data["confidence"])

                with st.expander("Raw JSON Output"):
                    st.json(result)

            else:
                st.error(result["error"])