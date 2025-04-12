from pydantic import BaseModel
from typing import Literal

class OutliersPlausibility(BaseModel):
    validation: Literal['plausible', 'implausible']
    explanation: str