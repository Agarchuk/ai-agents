from pydantic import BaseModel
from typing import List
from .missing_value_strategy import MissingValueStrategy

class MissingValuesRecommendations(BaseModel):
    recommendations: List[MissingValueStrategy]