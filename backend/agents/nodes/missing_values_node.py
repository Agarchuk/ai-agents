import streamlit as st
import pandas as pd

from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import RECOMMEND_MISSING_VALUES_STRATEGIE_SYSTEM_PROMPT, RECOMMEND_CONSTANT_FOR_MISSING_VALUES_SYSTEM_PROMPT
from backend.constants.user_prompts import RECOMMEND_CONSTANT_FOR_MISSING_VALUES_USER_PROMPT
from backend.models.pydantic.missing_value_recommendations import MissingValueRecommendations
from backend.models.pydantic.missing_value_strategy import MissingValueStrategy
from backend.models.pydantic.constant_value import ConstantValue
from utils.logger import log_info

class MissingValuesNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def process_missing_values(self, state: CleaningAgentState) -> CleaningAgentState:
        log_info("Processing missing values")
        log_info(f"State: {state}")

        if 'analysis' not in state or state['analysis'] is None:
            return {"error": "No analysed data provided"}
        
        df = state['data']
        analysis = state['analysis'].copy()

        dataset_topic = analysis.dataset_topic
        missing_values = analysis.missing_values
        columns_with_missing = missing_values[missing_values > 0].index.tolist()
        
        if not columns_with_missing:
            st.info("No missing values found in the dataset.")
            return state
        
        recommendations_list = []
        
        for col in columns_with_missing:
            column_info = {}
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
                
            column_info[col] = col_stats

            log_info(f"Column info: {column_info}")

            column_info_str = str(column_info).replace('{', '{{').replace('}', '}}')

            user_prompt = (
                f"""
                The dataset topic is: {dataset_topic}.
                It has {len(df)} rows. Below is information about the column '{col}' with missing values:                
                
                {column_info_str}
                
                Recommend the best strategy for handling missing values in '{col}', considering the dataset topic and this information.                """
            )

            missing_value_strategy = self.ollama_client.generate_response(
                system_prompt=RECOMMEND_MISSING_VALUES_STRATEGIE_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                formatClass=MissingValueStrategy
            )

            log_info(f"Missing value strategy: {missing_value_strategy}")

            if missing_value_strategy and missing_value_strategy['strategy'] == "fill with constant":
                system_prompt = RECOMMEND_CONSTANT_FOR_MISSING_VALUES_SYSTEM_PROMPT
                user_prompt = RECOMMEND_CONSTANT_FOR_MISSING_VALUES_USER_PROMPT.format(
                    dataset_topic=dataset_topic,
                    column_name=col,
                    data_type=column_info[col]['dtype'],
                    missing_percentage=column_info[col]['missing_percent'],
                    statistics=column_info_str
                )

                log_info(f"User prompt: {user_prompt}")

                constant_value = self.ollama_client.generate_response(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    formatClass=ConstantValue
                )

                log_info(f"Constant value: {constant_value}")

                missing_value_strategy['constant_value'] = constant_value
            
            recommendations_list.append(missing_value_strategy)

        log_info(f"Recommendations: {recommendations_list}")
        recommendations = MissingValueRecommendations(recommendations=recommendations_list)
                            
        return {"missing_values_recommendations": recommendations}
