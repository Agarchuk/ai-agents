from typing import Optional, TypedDict, Dict
import pandas as pd
from typing import List
from backend.models.pydantic.analyzed_data import AnalyzedData
from backend.models.pydantic.duplicates_analysis import DuplicatesAnalysis
from backend.models.pydantic.missing_value_recommendations import MissingValueRecommendations

class CleaningAgentState(TypedDict):
    data: Optional[pd.DataFrame]
    analysis: Optional[AnalyzedData]
    missing_values_recommendations: MissingValueRecommendations
    data_after_missing_values_handling: Optional[pd.DataFrame]
    duplicates_analysis: Optional[DuplicatesAnalysis]
    data_after_duplicate_values_handling: Optional[pd.DataFrame]
    outliers_info: Optional[Dict[str, Dict[str, float]]]
    data_after_outliers_handling: Optional[pd.DataFrame]
    # actions: List[dict]  # Список действий (словари с issue и action)
    # history: List[dict]  # История взаимодействий
    # current_issue: Optional[str]  # Текущая проблема или None
    # current_action: Optional[str]  # Текущее действие или None
    # user_response: Optional[str]  # Ответ пользователя или None
    # cleaned_data: Optional[pd.DataFrame]
    error: Optional[str]