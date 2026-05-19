from pydantic import BaseModel, Field
from typing import List


class DecisionResponse(BaseModel):
    business_problem: str = Field(description="Detected business problem")
    data_insights: List[str] = Field(description="Important insights from data")
    probable_causes: List[str] = Field(description="Possible causes behind the issue")
    recommendations: List[str] = Field(description="Recommended business actions")
    priority: str = Field(description="Priority level")
    confidence: str = Field(description="Confidence level")