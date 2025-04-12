from pydantic import BaseModel
from typing import List
import pandas as pd

class RemovedImpossibleOutliersInfo(BaseModel):
    columns: List[str]
    removed_rows: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class RemovedImpossibleOutliers(BaseModel):
    removed_duplicates: List[RemovedImpossibleOutliersInfo] 