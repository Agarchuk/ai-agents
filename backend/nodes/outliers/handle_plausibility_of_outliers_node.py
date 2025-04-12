
from typing import Dict
from backend.models.pydantic.core.column_meaning import ColumnMeaning
from backend.models.pydantic.core.report import Report
from backend.models.pydantic.outliers.column_outliers import ColumnOutliers
from backend.models.pydantic.outliers.detected_outliers import DetectedOutliers
from backend.models.pydantic.outliers_explanation import OutliersPlausibilityExplanation
from backend.models.pydantic.outliers_explanations import OutliersPlausibilityExplanations
from backend.models.pydantic.outliers_plausibility import OutliersPlausibility
from backend.models.pydantic.outliers_plausibility_strategy import OutliersPlausibilityStrategy
from backend.states.cleaning_agent_state import CleaningAgentState
import pandas as pd
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import VALIDATE_OUTLIERS_PROMPT, DETECT_IMPOSSIBLE_OUTLIER_STRATEGY_PROMPT
from utils.logger import log_info
import streamlit as st

class HandlePlausibilityOfOutliersNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def handle_plausibility_of_outliers(self, state: CleaningAgentState) -> CleaningAgentState:
        report: Report = state.report
        df: pd.DataFrame = report.cleaned_data
        dataset_topic = report.dataset_topic

        outliers_by_column: Dict[str, ColumnOutliers] = report.detected_outliers.outliers_by_column
        
        for col, column_outliers_info in outliers_by_column.items():

            validate_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Column meaning: {column_outliers_info.column_meaning}
                example_values: {df[(df[col] < column_outliers_info.lower_bound) | (df[col] > column_outliers_info.upper_bound)][col].tolist()[:3]}
                
                Are this outlier value plausible?
                """
            )

            validate_outliers = self.ollama_client.generate_response(
                VALIDATE_OUTLIERS_PROMPT,
                validate_prompt,
                OutliersPlausibility
            )

            if validate_outliers['validation'] == 'implausible':
                strategy_info = self._detect_strategy_for_impossible_outlier(
                    dataset_topic, col, column_outliers_info, df
                )
                column_outliers_info.strategy = OutliersPlausibilityStrategy(strategy=strategy_info['strategy'],
                                                                             explanation=strategy_info['explanation'])

                log_info(f"Chosen strategy for {col}: {strategy_info}")
                self._process_impossible_outlier(df, col, column_outliers_info, strategy_info["strategy"])
            
            else:
                log_info(f"Outliers in column {col} are plausible, keeping them")

            column_outliers_info.plausibility = OutliersPlausibility(validation=validate_outliers['validation'],
                                                                     explanation=validate_outliers['explanation'])

            report.handled_outliers_data = df

            if df is not None:
                report.cleaned_data = df
                state.data = df

        return {'report': report}
    
    def _detect_strategy_for_impossible_outlier(
        self, dataset_topic: str, col: str, column_outliers_info: ColumnOutliers, df: pd.DataFrame
    ) -> Dict[str, str]:
        strategy_prompt = (
            f"""
            Dataset topic: {dataset_topic}
            Column meaning: {column_outliers_info.column_meaning}
            Example implausible outliers: {df[(df[col] < column_outliers_info.lower_bound) | (df[col] > column_outliers_info.upper_bound)][col].tolist()[:3]}
            Suggest the best strategy to handle these implausible outliers.
            """
        )

        strategy_response = self.ollama_client.generate_response(
            DETECT_IMPOSSIBLE_OUTLIER_STRATEGY_PROMPT,
            strategy_prompt,
            OutliersPlausibilityStrategy
        )

        return strategy_response

    def _process_impossible_outlier(
        self, df: pd.DataFrame, col: str, column_outliers_info: ColumnOutliers, strategy: str
    ) -> None:
        outlier_mask = (df[col] < column_outliers_info.lower_bound) | (df[col] > column_outliers_info.upper_bound)

        if strategy == 'nullify':
            df.loc[outlier_mask, col] = pd.NA
            log_info(f"Nullified {outlier_mask.sum()} outlier values in column {col}")

        elif strategy == 'replace_mean':
            mean_value = df[col].mean()
            df.loc[outlier_mask, col] = mean_value
            log_info(f"Replaced {outlier_mask.sum()} outliers in column {col} with mean: {mean_value}")

        elif strategy == 'replace_median':
            median_value = df[col].median()
            df.loc[outlier_mask, col] = median_value
            log_info(f"Replaced {outlier_mask.sum()} outliers in column {col} with median: {median_value}")

        else:
            log_info(f"Unknown strategy '{strategy}' for column {col}, skipping processing")
    