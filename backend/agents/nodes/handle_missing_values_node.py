import pandas as pd
import streamlit as st

from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.models.pydantic.missing_value_recommendations import MissingValueRecommendations
from backend.models.pydantic.missing_value_strategy import MissingValueStrategy, StrategyType
from utils.logger import log_info


class HandleMissingValuesNode:
    def process_missing_values(self, state: CleaningAgentState) -> CleaningAgentState:
        log_info("Handling missing values")
        log_info(f"State: {state}")

        if 'missing_values_recommendations' not in state or state['missing_values_recommendations'] is None:
            st.info("No missing value recommendations found.")
            return state

        recommendations: MissingValueRecommendations = state['missing_values_recommendations']
        df = state['data']

        log_info(f"df: {df}")

        for recommendation in recommendations.recommendations:
            self._handle_missing_value(df, recommendation)

        state['data_after_missing_values_handling'] = df
        log_info(f"State after missing values handling: {state}")
        return state

    def _handle_missing_value(self, df: pd.DataFrame, recommendation: MissingValueStrategy):
        column_name = recommendation.column_name
        strategy = recommendation.strategy

        log_info(f"Handling missing values for column '{column_name}' with strategy '{strategy}'")

        if strategy == "fill with mean":
            df[column_name].fillna(df[column_name].mean(), inplace=True)
        elif strategy == "fill with median":
            df[column_name].fillna(df[column_name].median(), inplace=True)
        elif strategy == "fill with mode":
            df[column_name].fillna(df[column_name].mode()[0], inplace=True)
        elif strategy == "fill with zero":
            df[column_name].fillna(0, inplace=True)
        elif strategy == "fill with constant":
            df[column_name].fillna(recommendation.constant_value, inplace=True)
        elif strategy == "drop rows":
            df.dropna(subset=[column_name], inplace=True)
        elif strategy == "ignore":
            st.info(f"Ignoring missing values in column '{column_name}'.")
        else:
            st.error(f"Unknown missing value strategy: {strategy}") 