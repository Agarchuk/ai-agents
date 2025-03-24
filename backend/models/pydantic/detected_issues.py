from pydantic import BaseModel, Field
from typing import List

class DetectedIssues(BaseModel):
    issues_detected: List[str]
