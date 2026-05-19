from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from models import DecisionResponse
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from tools import get_schema, get_summary, analyze_question

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(DecisionResponse)



def run_business_analysis(df, question: str):

    schema = get_schema(df)
    summary = get_summary(df)
    analysis_result = analyze_question(df, question)

    prompt = USER_PROMPT_TEMPLATE.format(
        question=question,
        schema=schema,
        summary=summary,
        analysis_result=analysis_result
    )

    try:

        response = structured_llm.invoke([
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ])

        return response.model_dump()

    except Exception as e:

        return {
            "business_problem": "LLM processing failed",
            "data_insights": [str(analysis_result)],
            "probable_causes": [str(e)],
            "recommendations": [
                "Check dataset structure",
                "Try simpler business question"
            ],
            "priority": "Medium",
            "confidence": "Low"
        }