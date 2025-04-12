from pydantic import BaseModel
from typing import Literal

class OutliersResult(BaseModel):
    column: str
    plausibility: Literal['plausible', 'implausible']
    plausibility_explanation: str
    used_strategy: str
    strategy_explanation: str
    risks: str
    benefits: str
