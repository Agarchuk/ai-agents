import pandas as pd
from pydantic import BaseModel

class AnalyzedData(BaseModel):
    dataset_topic: str
    types: pd.Series
    available_columns: list[str]
    missing_values: pd.Series
    missing_values_percentage: pd.Series
    numerical_stats: pd.DataFrame
    categorical_stats: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True
    