from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from models import DecisionResponse

from prompts import SYSTEM_PROMPT

from tools import analyze_data

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


structured_llm = llm.with_structured_output(
    DecisionResponse
)


def run_business_analysis(

    df,

    question,

    retrieved_context=""

):

    dataframe_insights = analyze_data(df, question)

    prompt = f"""
    User Question:
    {question}

    Dataframe Insights:
    {dataframe_insights}

    Retrieved Business Context:
    {retrieved_context}
    """

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