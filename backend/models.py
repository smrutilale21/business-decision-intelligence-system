from pydantic import BaseModel
from typing import List, Optional


class DecisionResponse(BaseModel):

    business_problem: str

    data_insights: List[str]

    probable_causes: List[str]

    recommendations: List[str]

    evidence: List[str]

    priority: str

    confidence: str

    metric_column: Optional[str] = None

    dimension_column: Optional[str] = None

    aggregation: Optional[str] = None

    chart_type: Optional[str] = None

    derived_metric: Optional[str] = None