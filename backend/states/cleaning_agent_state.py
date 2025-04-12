from typing import Optional
import pandas as pd
from pydantic import BaseModel
from backend.models.pydantic.core.report import Report

class CleaningAgentState(BaseModel):
    data: Optional[pd.DataFrame] = None
    report: Optional[Report] = None
    error: Optional[str] = None
    iteration: Optional[int] = 1
    continue_cleaning: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True