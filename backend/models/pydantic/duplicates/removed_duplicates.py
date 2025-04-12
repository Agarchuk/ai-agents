from pydantic import BaseModel
from typing import List
import pandas as pd

class RemovedDuplicatesInfo(BaseModel):
    columns: List[str]
    removed_rows: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class RemovedDuplicates(BaseModel):
    removed_duplicates: List[RemovedDuplicatesInfo] 