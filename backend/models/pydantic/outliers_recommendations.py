from pydantic import BaseModel
from typing import Literal

OutliersStrategy = Literal[
    'remove rows', 
    'replace with median', 
    'replace with mean', 
    'keep',
    'winsorize'
]

class OutliersRecommendations(BaseModel):
    strategy: OutliersStrategy
    explanation: str
    risks: str
    benefits: str