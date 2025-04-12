from enum import Enum
from backend.states.cleaning_agent_state import CleaningAgentState
from backend.constants.system_prompts import IDENTIFY_KEY_COLUMNS_SYSTEM_PROMPT
from backend.models.pydantic.key_columns_response import KeyColumnsResponse
from utils.logger import log_info
from backend.clients.ollama_client import OllamaClient

from backend.constants.system_prompts import DECIDE_DUPLICATES_SYSTEM_PROMPT
from backend.models.pydantic.duplicates.duplicate_recommendation import DuplicateRecommendation
from backend.models.pydantic.duplicates.duplicates_recommendations import DuplicatesRecommendations

class DuplicateValuesNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def detect_duplicate_values(self, state: CleaningAgentState) -> CleaningAgentState:
        report = state.report
        dataset_topic = report.dataset_topic
        available_columns = report.available_columns
        data_types = report.data_types

        if report.handled_missing_values_data is None:
            df = state.data.copy()
        else:   
            df = report.handled_missing_values_data

        user_prompt = (
            f"""
            Dataset topic: {dataset_topic}
            Available columns: {', '.join(available_columns)}

            Recommend the key columns to use for identifying duplicates in this dataset.
            """
        )
        log_info(f"User prompt: {user_prompt}")

        ColumnNames = Enum("ColumnNames", {col: col for col in available_columns})

        key_columns_response: KeyColumnsResponse = self.ollama_client.generate_response(
            system_prompt=IDENTIFY_KEY_COLUMNS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            formatClass=KeyColumnsResponse[ColumnNames]
            )

        log_info(f"Key columns response: {key_columns_response}")

        if 'unique_identifier_column' in key_columns_response:
            unique_identifier_column = key_columns_response['unique_identifier_column']
        else:
            unique_identifier_column = None

        if 'combined_key_columns' in key_columns_response:
            combined_key_columns = key_columns_response['combined_key_columns']
        else:
            combined_key_columns = None

        log_info(f"Unique key identifier: {unique_identifier_column}")
        log_info(f"Combined key columns: {combined_key_columns}")

        duplicates_recommendations = DuplicatesRecommendations(duplicates_recommendations={})
        if unique_identifier_column:
            duplicates_count = df.duplicated(subset=[unique_identifier_column]).sum()

            user_prompt = (
                f"""
                Dataset topic: {dataset_topic}
                Dataset size: {len(df)} rows
                Key columns used for duplicate detection: {unique_identifier_column}
                Column types: {data_types}

                Number of duplicates found: {duplicates_count} ({duplicates_count / len(df) * 100:.1f}% of total)
                
                Should duplicates be removed or kept in this dataset? Provide your recommendation and a brief explanation.            """
            )

            duplicates_recommendations_response: DuplicateRecommendation = self.ollama_client.generate_response(
                system_prompt=DECIDE_DUPLICATES_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                formatClass=DuplicateRecommendation
            )   

            duplicates_recommendations.duplicates_recommendations[unique_identifier_column] = duplicates_recommendations_response

        if combined_key_columns:
            duplicates_count = df.duplicated(subset=combined_key_columns).sum()

            if duplicates_count > 0:

                user_prompt = (
                    f"""
                    Dataset topic: {dataset_topic}
                    Dataset size: {len(df)} rows
                    Key columns used for duplicate detection: {', '.join(combined_key_columns)}
                    Column types: {data_types}

                    Number of duplicates found: {duplicates_count} ({duplicates_count / len(df) * 100:.1f}% of total)
                    
                    Should duplicates be removed or kept in this dataset? Provide your recommendation and a brief explanation.            """
                )

                duplicates_recommendations_response: DuplicateRecommendation = self.ollama_client.generate_response(
                    system_prompt=DECIDE_DUPLICATES_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    formatClass=DuplicateRecommendation
                )   
                
                duplicates_recommendations.duplicates_recommendations[', '.join(combined_key_columns)] = duplicates_recommendations_response

                log_info(f"Duplicates recommendations response: {duplicates_recommendations_response}")
            
        report.duplicates_recommendations =duplicates_recommendations
        return {'report': report}

    def create_column_enum(available_columns: list[str]):
        return Enum("ColumnNames", {col: col for col in available_columns})
    
