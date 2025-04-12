from pydantic import BaseModel
from typing import Literal

StrategyType = Literal[
    "nullify",
    "replace_mean", 
    "replace_median"
]

class OutliersPlausibilityStrategy(BaseModel):
    strategy: StrategyType
    explanation: str