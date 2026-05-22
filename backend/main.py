from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

import pandas as pd

import shutil
import os

from utils import clean_column_names

from charts import generate_chart

from rag import (
    build_vector_store,
    retrieve_context
)

from agent import run_business_analysis


app = FastAPI(
    title="AI-Powered Business Decision Intelligence System"
)


app.mount(
    "/charts",
    StaticFiles(directory="../charts"),
    name="charts"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


@app.get("/")
def health_check():

    return {
        "status": "running"
    }


@app.post("/analyze")
async def analyze(

    question: str = Form(...),

    csv_file: UploadFile = File(...),

    pdf_file: UploadFile = File(None)
):

    try:

        df = pd.read_csv(csv_file.file)

        df = clean_column_names(df)

        retrieved_context = ""

        if pdf_file:

            os.makedirs("uploads", exist_ok=True)

            pdf_path = f"uploads/{pdf_file.filename}"

            with open(pdf_path, "wb") as buffer:

                shutil.copyfileobj(
                    pdf_file.file,
                    buffer
                )

            vectorstore = build_vector_store(
                pdf_path
            )

            retrieved_context = retrieve_context(
                vectorstore,
                question
            )

        response = run_business_analysis(

            df=df,

            question=question,

            retrieved_context=retrieved_context
        )

        chart_path = generate_chart(
            df,
            question
        )

        chart_url = ""

        if chart_path:

            filename = chart_path.split("/")[-1]

            chart_url = f"/charts/{filename}"

        return {

            "success": True,

            "response": response,

            "chart_url": chart_url,

            "retrieved_context": retrieved_context
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }