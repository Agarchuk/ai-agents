import pandas as pd

from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.models.pydantic.analyzed_data import AnalyzedData
from backend.models.pydantic.dataset_topic import DatasetTopic
from backend.clients.ollama_client import OllamaClient

class AnalysisNode:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def analyze_data(self, state: CleaningAgentState) -> CleaningAgentState:
        data = state['data']

        types = data.dtypes
        available_columns = data.columns.tolist()
        missing_values = data.isnull().sum()
        missing_values_percentage = data.isnull().mean() * 100

        numerical_stats = data.describe()
        categorical_stats = data.describe(include=['O'])

        dataset_topic = self.get_topic_from_llm(data)

        analyzed_data = AnalyzedData(
            types=types,
            available_columns=available_columns,
            missing_values=missing_values,
            missing_values_percentage=missing_values_percentage,
            numerical_stats=numerical_stats,
            categorical_stats=categorical_stats,
            dataset_topic=dataset_topic
        )

        return {"analysis": analyzed_data}
    
    def get_topic_from_llm(self, data: pd.DataFrame) -> str:

        system_prompt = """
        You are a data analysis expert tasked with identifying the topic of a dataset. 
        Based on the provided data, including column names and sample values, provide a concise description of the dataset's topic in 1-2 sentences.
        """

        user_prompt = f"""
        Analyze the following dataset to determine its topic. 
        Use the column names and sample data below:

        Column names: {', '.join(data.columns)}
        Sample data (first 5 rows):
        {data.head().to_string()}

        Provide a concise topic description based on this information.
        """

        response = self.ollama_client.generate_response(system_prompt, user_prompt, DatasetTopic)

        return response['dataset_topic']
