from typing import Dict
import numpy as np
from backend.models.pydantic.core.report import Report
from backend.models.pydantic.outliers.column_outliers import ColumnOutliers
from backend.models.pydantic.outliers.detected_outliers import DetectedOutliers
from backend.models.pydantic.outliers_result import OutliersResult
from backend.states.cleaning_agent_state import CleaningAgentState
import pandas as pd
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import STRATEGY_OUTLIERS_PROMPT, VALIDATE_OUTLIERS_PROMPT
from backend.models.pydantic.outliers_recommendations import OutliersRecommendations
from utils.logger import log_info
from backend.models.pydantic.outliers_explanations import OutliersPlausibilityExplanations

class HandleOutliersNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def handle_outliers(self, state: CleaningAgentState) -> CleaningAgentState:
        report: Report = state.report

        log_info(f"state: {state}")
        df: pd.DataFrame = state.data.copy()
        column_types = report.data_types
        dataset_topic = report.dataset_topic
        detected_outliers: DetectedOutliers =report.detected_outliers
        outliers_by_column: Dict[str, ColumnOutliers] = detected_outliers.outliers_by_column

        log_info(f"detected_outliers: {detected_outliers}")

        outliers_results = []
        for col, info in outliers_by_column.items():
            plausibility_explanation = info.plausibility
            lower_bound = info.lower_bound
            upper_bound = info.upper_bound

            user_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Dataset size: {len(df)} rows
                Column name: {col}
                Column type: {column_types[col]}
                Outlier details:
                - Count: {info['count']}
                - Percentage: {info['count'] / len(df) * 100:.2f}%
                - Lower bound (IQR): {lower_bound:.2f}
                - Upper bound (IQR): {upper_bound:.2f}
                - Example values: {df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].tolist()[:3]}
                
                Recommend a strategy for handling outliers in this column.
                """
            )

            log_info(f"user_prompt for outliers: {user_prompt}")

            outliers_recommendations = self.ollama_client.generate_response(
                STRATEGY_OUTLIERS_PROMPT,
                user_prompt,
                OutliersRecommendations
            )

            log_info(f"outliers_recommendations: {outliers_recommendations}")

            strategy = outliers_recommendations['strategy']
            if strategy == "remove rows":
                df = df[~((df[col] < lower_bound) | (df[col] > upper_bound))]
                print(f"Removed rows with outliers in '{col}': {outliers_recommendations['explanation']}")
            elif strategy == "replace with median":
                median = df[col].median()
                df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = median
                print(f"Replaced outliers in '{col}' with median: {outliers_recommendations['explanation']}")
            elif strategy == "replace with mean":
                mean = df[col].mean()
                df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = mean
                print(f"Replaced outliers in '{col}' with mean: {outliers_recommendations['explanation']}")
            elif strategy == "clip":
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                print(f"Clipped outliers in '{col}' to IQR bounds: {outliers_recommendations['explanation']}")
            elif strategy == "log transform":
                if (df[col] > 0).all():
                    df[col] = np.log1p(df[col])
                    print(f"Applied log transform to '{col}': {outliers_recommendations['explanation']}")
                else:
                    print(f"Skipped log transform for '{col}' due to non-positive values.")
            elif strategy == "replace with NaN":
                df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), col] = pd.NA
                print(f"Replaced outliers in '{col}' with NaN: {outliers_recommendations['explanation']}")
            elif strategy == "keep":
                print(f"Kept outliers in '{col}': {outliers_recommendations['explanation']}")
           
           

            outliers_results.append(OutliersResult(
                column=col,
                plausibility=plausibility_explanation.validation,
                plausibility_explanation=plausibility_explanation.plausibility_explanation,
                risks=outliers_recommendations['risks'],
                benefits=outliers_recommendations['benefits'],
                used_strategy=outliers_recommendations['strategy'],
                strategy_explanation=outliers_recommendations['explanation']
            ))

        return {'data_after_outliers_handling': df, 'outliers_results': outliers_results}

            


            
        
    