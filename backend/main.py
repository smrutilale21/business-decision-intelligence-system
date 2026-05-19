from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

from agent import run_business_analysis
from utils import clean_column_names


app = FastAPI(
    title="AI Business Decision Intelligence System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "project": "AI Business Decision Intelligence System"
    }


@app.post("/analyze")
async def analyze_business_data(
    question: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        df = pd.read_csv(file.file)

        df = clean_column_names(df)

        result = run_business_analysis(df, question)

        return {
            "success": True,
            "response": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }