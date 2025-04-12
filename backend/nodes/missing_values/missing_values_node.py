import streamlit as st
import pandas as pd

from backend.states.cleaning_agent_state import CleaningAgentState
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import RECOMMEND_MISSING_VALUES_STRATEGIE_SYSTEM_PROMPT, RECOMMEND_CONSTANT_FOR_MISSING_VALUES_SYSTEM_PROMPT
from backend.constants.user_prompts import RECOMMEND_CONSTANT_FOR_MISSING_VALUES_USER_PROMPT
from backend.models.pydantic.missing_values.missing_values_recommendations import MissingValuesRecommendations
from backend.models.pydantic.missing_values.missing_value_strategy import MissingValueStrategy
from backend.models.pydantic.missing_values.constant_value import ConstantValue
from utils.logger import log_info

class MissingValuesNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def process_missing_values(self, state: CleaningAgentState) -> CleaningAgentState:
        if state.report is None or state.report.missing_values is None:
            return {"error": "No analysed data provided"}
        
        df = state.data
        report = state.report
        dataset_topic = report.dataset_topic
        missing_values = report.missing_values

        columns_with_missing = missing_values[missing_values > 0].index.tolist()
        
        if not columns_with_missing:
            st.info("No missing values found in the dataset.")
            return state
        
        recommendations_list = self.generate_missing_value_recommendations(df, columns_with_missing, dataset_topic)
        
        report.missing_values_recommendations = MissingValuesRecommendations(recommendations=recommendations_list)                            
        return {"report": report}

    def generate_missing_value_recommendations(self, df: pd.DataFrame, columns_with_missing, dataset_topic):
        recommendations_list = []
        log_info(f"columns_with_missing: {columns_with_missing}")
        for col in columns_with_missing:
            column_info = self.collect_column_stats(df, col)

            column_info_str = str(column_info).replace('{', '{{').replace('}', '}}')
            user_prompt = self.format_user_prompt(dataset_topic, df, col, column_info_str)
            strategy_response = self.ollama_client.generate_response(
                system_prompt=RECOMMEND_MISSING_VALUES_STRATEGIE_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                formatClass=MissingValueStrategy
            )

            if strategy_response:
                strategy = MissingValueStrategy(
                    column_name=col,
                    strategy=strategy_response['strategy'],
                    explanation=strategy_response['explanation']
                )

                if strategy.strategy == "fill with constant":
                    constant_value = self.determine_constant_value(dataset_topic, col, column_info, column_info_str)
                    strategy.constant_value = constant_value

                recommendations_list.append(strategy)

        return recommendations_list

    def collect_column_stats(self, df: pd.DataFrame, col):
        missing_count = df[col].isnull().sum()
        missing_percent = missing_count / len(df) * 100
        col_stats = {
            "missing_count": missing_count,
            "missing_percent": f"{missing_percent:.2f}%",
            "dtype": str(df[col].dtype)
        }

        if pd.api.types.is_numeric_dtype(df[col]):
            col_stats.update({
                "mean": df[col].mean(),
                "median": df[col].median(),
                "std": df[col].std(),
                "min": df[col].min(),
                "max": df[col].max()
            })
        else:
            value_counts = df[col].value_counts().head(3)
            col_stats["top_values"] = value_counts.to_dict() if not value_counts.empty else {}
        
        return {col: col_stats}

    def format_user_prompt(self, dataset_topic, df, col, column_info_str):
        return (
            f"""
            The dataset topic is: {dataset_topic}.
            It has {len(df)} rows. Below is information about the column '{col}' with missing values:                
            
            {column_info_str}
            
            Recommend the best strategy for handling missing values in '{col}', considering the dataset topic and this information.                """
        )

    def determine_constant_value(self, dataset_topic, col, column_info, column_info_str):
        system_prompt = RECOMMEND_CONSTANT_FOR_MISSING_VALUES_SYSTEM_PROMPT
        user_prompt = RECOMMEND_CONSTANT_FOR_MISSING_VALUES_USER_PROMPT.format(
            dataset_topic=dataset_topic,
            column_name=col,
            data_type=column_info[col]['dtype'],
            missing_percentage=column_info[col]['missing_percent'],
            statistics=column_info_str
        )

        return self.ollama_client.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            formatClass=ConstantValue
        )
