from pydantic import BaseModel

class DuplicateRecommendations(BaseModel):
    action: str
    explanation: str