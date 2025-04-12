from pydantic import BaseModel
from typing import Literal, Optional
from backend.models.pydantic.missing_values.constant_value import ConstantValue

StrategyType = Literal[
    "fill with mean",
    "fill with median", 
    "fill with mode",
    "fill with zero",
    "fill with constant",
    "drop rows",
    "ignore"
]

class MissingValueStrategy(BaseModel):
    column_name: str
    strategy: StrategyType
    explanation: str
    constant_value: Optional[ConstantValue] = None
