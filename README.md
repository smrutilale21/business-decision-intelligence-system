# Business Decision Intelligence System

An AI-powered business analytics and decision intelligence platform built using FastAPI, Streamlit, LangChain, and OpenAI.

The system allows users to upload business datasets and receive AI-generated insights, trend analysis, recommendations, and decision-support reports in a structured format.

---

## Features

- Upload CSV business datasets
- Automated data cleaning and preprocessing
- AI-generated business insights
- Trend and performance analysis
- Strategic recommendations
- FastAPI backend APIs
- Streamlit interactive frontend
- OpenAI + LangChain integration
- Structured AI responses using Pydantic

---

## Tech Stack

### Backend
- FastAPI
- Python
- LangChain
- OpenAI API
- Pandas
- Pydantic

### Frontend
- Streamlit

---

## Project Structure

```bash
business-decision-intelligence-system/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── .gitignore
├── README.md
└── .env
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/business-decision-intelligence-system.git
```

### Create Virtual Environment

```bash
python -m venv decision-ai-env
```

### Activate Virtual Environment

#### Windows

```bash
decision-ai-env\Scripts\activate
```

#### Mac/Linux

```bash
source decision-ai-env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

---

## Run Frontend

```bash
streamlit run app.py
```

---

## Future Improvements

- Authentication system
- Multi-file dataset analysis
- Dashboard visualizations
- Report export functionality
- Advanced business forecasting
- Vector database integration

---

## Author

Smruti Lale