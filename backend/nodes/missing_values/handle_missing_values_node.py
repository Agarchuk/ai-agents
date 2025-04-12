import pandas as pd
import streamlit as st

from backend.states.cleaning_agent_state import CleaningAgentState
from backend.models.pydantic.missing_values.missing_values_recommendations import MissingValuesRecommendations
from backend.models.pydantic.missing_values.missing_value_strategy import MissingValueStrategy
from utils.logger import log_info


class HandleMissingValuesNode:
    def process_missing_values(self, state: CleaningAgentState) -> CleaningAgentState:        
        report = state.report
        df = report.cleaned_data
        missing_values = report.missing_values

        columns_with_missing = missing_values[missing_values > 0].index.tolist()

        missing_values_recommendations: MissingValuesRecommendations = report.missing_values_recommendations

        if missing_values_recommendations is None:
            st.info("No missing value recommendations found.")
            return {'report': report}
        
        for recommendation in missing_values_recommendations.recommendations:
            column_name = recommendation.column_name
            if column_name in columns_with_missing:
                self._handle_missing_value(df, recommendation)

        report.handled_missing_values_data = df

        if df is not None:
            report.cleaned_data = df

        return {'report': report}

    def _handle_missing_value(self, df: pd.DataFrame, recommendation: MissingValueStrategy):
        column_name = recommendation.column_name
        log_info(f"_handle_missing_value column_name: {column_name}")
        strategy = recommendation.strategy

        log_info(f"Handling missing values for column '{column_name}' with strategy '{strategy}'")

        if strategy == "fill with mean":
            df[column_name].fillna(df[column_name].mean(), inplace=True)
            log_info(f"Filled missing values in column '{column_name}' with mean")
        elif strategy == "fill with median":
            df[column_name].fillna(df[column_name].median(), inplace=True)
            log_info(f"Filled missing values in column '{column_name}' with median")
        elif strategy == "fill with mode":
            df[column_name].fillna(df[column_name].mode()[0], inplace=True)
            log_info(f"Filled missing values in column '{column_name}' with mode")
        elif strategy == "fill with zero":
            df[column_name].fillna(0, inplace=True)
            log_info(f"Filled missing values in column '{column_name}' with zero")
        elif strategy == "fill with constant":
            df[column_name].fillna(recommendation.constant_value.constant_value, inplace=True)
            log_info(f"Filled missing values in column '{column_name}' with constant value")
        elif strategy == "drop rows":
            df.dropna(subset=[column_name], inplace=True)
            log_info(f"Dropped rows with missing values in column '{column_name}'")
        elif strategy == "ignore":
            st.info(f"Ignoring missing values in column '{column_name}'.")
        else:
            st.error(f"Unknown missing value strategy: {strategy}") 