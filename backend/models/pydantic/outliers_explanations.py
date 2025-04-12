from pydantic import BaseModel
from typing import List
from backend.models.pydantic.outliers_explanation import OutliersPlausibilityExplanation

class OutliersPlausibilityExplanations(BaseModel):
    plausibility_explanations: List[OutliersPlausibilityExplanation]

    def get_explanation(self, column: str) -> OutliersPlausibilityExplanation:
        return next((explanation for explanation in self.plausibility_explanations if explanation.column == column), None)
