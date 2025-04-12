from typing import Literal
from pydantic import BaseModel


class OutliersPlausibilityExplanation(BaseModel):
    column: str
    validation: Literal['plausible', 'implausible']
    plausibility_explanation: str

