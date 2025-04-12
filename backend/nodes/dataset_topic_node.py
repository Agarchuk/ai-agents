from backend.constants.system_prompts import DATASET_TOPIC_SYSTEM_PROMPT
from backend.models.pydantic.core.dataset_topic import DatasetTopic
from backend.clients.ollama_client import OllamaClient
from backend.states.cleaning_agent_state import CleaningAgentState

class DatasetTopicNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def get_topic_from_llm(self, state: CleaningAgentState) -> str:
        data = state.data
        report = state.report

        user_prompt = f"""
        Analyze the following dataset to determine its topic. 
        Use the column names and sample data below:

        Column names: {', '.join(data.columns)}
        Sample data (first 5 rows):
        {data.head().to_string()}

        Provide a concise topic description based on this information.
        """

        dataset_topic = self.ollama_client.generate_response(DATASET_TOPIC_SYSTEM_PROMPT, 
                                                        user_prompt, 
                                                        DatasetTopic)['dataset_topic']

        report.dataset_topic = dataset_topic
        return {'report': report}
