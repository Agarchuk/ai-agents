from enum import Enum
from typing import List, Literal
from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.constants.system_prompts import IDENTIFY_KEY_COLUMNS_SYSTEM_PROMPT
from backend.models.pydantic.duplicates_analysis import DuplicatesAnalysis
from backend.models.pydantic.key_columns_response import KeyColumnsResponse
from utils.logger import log_info
from backend.clients.ollama_client import OllamaClient

class DuplicateValuesNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def detect_duplicate_values(self, state: CleaningAgentState) -> CleaningAgentState:
        analysis = state['analysis']
        dataset_topic = analysis.dataset_topic
        available_columns = analysis.available_columns


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

        duplicates_analysis = DuplicatesAnalysis(
            unique_identifier_column=unique_identifier_column,
            combined_key_columns=combined_key_columns,
        )
        return {'duplicates_analysis': duplicates_analysis}

    def create_column_enum(available_columns: list[str]):
        return Enum("ColumnNames", {col: col for col in available_columns})
    
