from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.clients.ollama_client import OllamaClient
from backend.constants.system_prompts import DECIDE_DUPLICATES_SYSTEM_PROMPT
from backend.models.pydantic.duplicate_recommendations import DuplicateRecommendations
from backend.models.pydantic.duplicates_analysis import DuplicatesAnalysis
from utils.logger import log_info

class HandleDuplicateValuesNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client  

    def handle_duplicate_values(self, state: CleaningAgentState) -> CleaningAgentState:
        analysis = state['analysis']
        dataset_topic = analysis.dataset_topic
        types = analysis.types

        df = state['data']
        duplicates_analysis: DuplicatesAnalysis = state['duplicates_analysis']
        unique_identifier_column = duplicates_analysis.unique_identifier_column
        combined_key_columns = duplicates_analysis.combined_key_columns

        if unique_identifier_column:
            duplicates_count = df.duplicated(subset=[unique_identifier_column]).sum()

            user_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Dataset size: {len(df)} rows
                Key columns used for duplicate detection: {unique_identifier_column}
                Column types: {types}

                Number of duplicates found: {duplicates_count} ({duplicates_count / len(df) * 100:.1f}% of total)
                
                Should duplicates be removed or kept in this dataset? Provide your recommendation and a brief explanation.            """
            )

            duplicates_recommendations_response: DuplicateRecommendations = self.ollama_client.generate_response(
                system_prompt=DECIDE_DUPLICATES_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                formatClass=DuplicateRecommendations
            )   

            log_info(f"Duplicates recommendations response: {duplicates_recommendations_response}")
        
            if 'action' in duplicates_recommendations_response:
                log_info(f"Duplicates recommendations action: {duplicates_recommendations_response['action']}")
                if duplicates_recommendations_response['action'] == "remove":
                    log_info(f"Removing duplicates")
                    df = df.drop_duplicates(subset=[unique_identifier_column], keep="first")
                    log_info(f"Duplicates removed")
                    new_size = len(df)
                    log_info(f"New size: {new_size}")
                    duplicates_count = new_size - duplicates_count
                    log_info(f"Duplicates removed: {duplicates_count}")

        if combined_key_columns:
            duplicates_count = df.duplicated(subset=combined_key_columns).sum()

            user_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Dataset size: {len(df)} rows
                Key columns used for duplicate detection: {', '.join(combined_key_columns)}
                Column types: {types}

                Number of duplicates found: {duplicates_count} ({duplicates_count / len(df) * 100:.1f}% of total)
                
                Should duplicates be removed or kept in this dataset? Provide your recommendation and a brief explanation.            """
            )

            duplicates_recommendations_response: DuplicateRecommendations = self.ollama_client.generate_response(
                system_prompt=DECIDE_DUPLICATES_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                formatClass=DuplicateRecommendations
            )   

            log_info(f"Duplicates recommendations response: {duplicates_recommendations_response}")
        
            if 'action' in duplicates_recommendations_response:
                log_info(f"Duplicates recommendations action: {duplicates_recommendations_response['action']}")
                if duplicates_recommendations_response['action'] == "remove":
                    log_info(f"Removing duplicates")
                    df = df.drop_duplicates(subset=combined_key_columns, keep="first")
                    log_info(f"Duplicates removed")
                    new_size = len(df)
                    log_info(f"New size: {new_size}")
                    duplicates_count = new_size - duplicates_count
                    log_info(f"Duplicates removed: {duplicates_count}")

        else:
            raise ValueError("No key columns found")

        return {'data_after_duplicate_values_handling': df}
