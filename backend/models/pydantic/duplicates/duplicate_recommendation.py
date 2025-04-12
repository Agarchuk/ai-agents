from pydantic import BaseModel

class DuplicateRecommendation(BaseModel):
    action: str
    explanation: str