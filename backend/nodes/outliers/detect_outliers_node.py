from backend.clients.ollama_client import OllamaClient
from backend.models.pydantic.core.column_meaning import ColumnMeaning
from backend.states.cleaning_agent_state import CleaningAgentState
import pandas as pd
from typing import Dict
from backend.models.pydantic.outliers.column_outliers import ColumnOutliers
from backend.models.pydantic.outliers.detected_outliers import DetectedOutliers
from utils.logger import log_info
from scipy.stats import skew, kurtosis
from backend.constants.system_prompts import DETECT_COLUMN_MEANING_PROMPT
import streamlit as st

class DetectOutliersNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client


    def detect_outliers(self, state: CleaningAgentState) -> CleaningAgentState:
        report = state.report
        df: pd.DataFrame = report.cleaned_data
        data_types = report.data_types

        numeric_cols = [col for col, dtype in data_types.items() if 'float' in dtype.name or 'int' in dtype.name]
        
        outliers_by_column: Dict[str, ColumnOutliers] = {}
        total_ouliers_count = 0

        if not numeric_cols:
            return {"report": report}
        
        for col in numeric_cols:
            count, lower, upper, outliers = self._detect_column_outliers(df, col)
            col_meaning = self._detect_column_meaning(report.dataset_topic, col)

            if count > 0:
                outliers_by_column[col] = ColumnOutliers(
                    count=count,
                    lower_bound=lower,
                    upper_bound=upper,
                    outliers=outliers,
                    column_meaning=col_meaning
                )
            total_ouliers_count += count

        log_info(f"total_ouliers_count: {total_ouliers_count}")
            
        report.detected_outliers = DetectedOutliers(outliers_by_column=outliers_by_column, total_outliers=total_ouliers_count)

        return {"report": report}
    
    def _detect_column_outliers(self, df: pd.DataFrame, column: str) -> tuple[int, float, float]:
        log_info(f"Detecting outliers for column: {column}")
        skewness = skew(df[column].dropna())
        kurt = kurtosis(df[column].dropna())
        is_normal = abs(skewness) < 0.5 and abs(kurt) < 1
        
        if is_normal:
            mean = df[column].mean()
            std = df[column].std()
            if std == 0:
                return 0, None, None, []
            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
        else:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            if IQR == 0:
                return 0, None, None, []

            iqr_multiplier = 1.5 + min(abs(skewness) / 2, 1.5)
            lower_bound = Q1 - iqr_multiplier * IQR
            upper_bound = Q3 + iqr_multiplier * IQR
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]

        return len(outliers), lower_bound, upper_bound, outliers

    def _detect_column_meaning(self, dataset_topic, column: str):

            col_meaning_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Column name: {column}
                """
            )
            col_meaning = self.ollama_client.generate_response(
                DETECT_COLUMN_MEANING_PROMPT,
                col_meaning_prompt,
                ColumnMeaning
            )

            return col_meaning['column_meaning']
