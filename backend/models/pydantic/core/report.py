from typing import List, Optional
from pydantic import BaseModel
import pandas as pd

from backend.models.pydantic.duplicates.duplicates_recommendations import DuplicatesRecommendations
from backend.models.pydantic.duplicates.removed_duplicates import RemovedDuplicates
from backend.models.pydantic.missing_values.missing_value_strategy import MissingValueStrategy
from backend.models.pydantic.missing_values.missing_values_recommendations import MissingValuesRecommendations
from backend.models.pydantic.outliers.detected_outliers import DetectedOutliers
from backend.models.pydantic.outliers_explanation import OutliersPlausibilityExplanation

class Report(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    dataset_topic: str | None = None
    rows: int | None = None
    columns: int | None = None
    data_types: pd.Series | None = None
    available_columns : list[str] | None = None
    numerical_statistics: pd.DataFrame | None = None
    categorical_statistics: pd.DataFrame | None = None
    initial_data_preview: pd.DataFrame | None = None

    # missing values
    missing_values: pd.Series | None = None
    missing_values_percentage: pd.Series | None = None
    missing_values_recommendations: MissingValuesRecommendations | None = None
    handled_missing_values_data: pd.DataFrame | None = None

    # duplicates
    duplicates_recommendations: DuplicatesRecommendations | None = None
    handled_duplicates_data: pd.DataFrame | None = None
    removed_duplicates: Optional[RemovedDuplicates] = None

    # outliers
    detected_outliers: DetectedOutliers | None = None
    handled_outliers_data: pd.DataFrame | None = None

    # result
    cleaned_data: pd.DataFrame | None = None