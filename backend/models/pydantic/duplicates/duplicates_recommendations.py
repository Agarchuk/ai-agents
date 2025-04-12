from typing import List
from pydantic import BaseModel
from backend.models.pydantic.duplicates.duplicate_recommendation import DuplicateRecommendation

class DuplicatesRecommendations(BaseModel):
    duplicates_recommendations: dict[str, DuplicateRecommendation]