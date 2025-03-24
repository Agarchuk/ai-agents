from backend.agents.states.cleaning_agent_state import CleaningAgentState
import pandas as pd
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import RECOMMEND_OUTLIERS_STRATEGY_SYSTEM_PROMPT
from backend.models.pydantic.outliers_recommendations import OutliersRecommendations
from utils.logger import log_info

class HandleOutlinersNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def handle_outliners(self, state: CleaningAgentState) -> CleaningAgentState:
        df: pd.DataFrame = state['data']
        analysis_data = state['analysis']
        column_types = analysis_data.types
        dataset_topic = analysis_data.dataset_topic
        outliers_info = state['outliers_info']

        for col, info in outliers_info.items():
        
            user_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Dataset size: {len(df)} rows
                Column types: {column_types}
                Numeric columns with outliers:
               
                'count': {info['count']},
                'percentage': {info['count'] / len(df) * 100},
                'lower_bound': {info['lower_bound']},
                'upper_bound': {info['upper_bound']},
                'example_values': {df[(df[col] < info['lower_bound']) | (df[col] > info['upper_bound'])][col].tolist()[:3]}
        
                
                Recommend a strategy for handling these outliers: 'remove rows', 'replace with median', 'replace with mean', 'keep'.
                """
            )

            outliers_recomendations = self.ollama_client.generate_response(
                RECOMMEND_OUTLIERS_STRATEGY_SYSTEM_PROMPT,
                user_prompt,
                OutliersRecommendations
            )

            log_info(f"outliers_recomendations: {outliers_recomendations}") 

        return {'data_after_outliers_handling': df}

            


            
        
    