from backend.models.pydantic.detected_issues import DetectedIssues
from utils.logger import log_info
from backend.clients.ollama_client import OllamaClient
from backend.agents.states.cleaning_agent_state import CleaningAgentState

class DataCleaningService:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
    
    def analyze_data(self, state: CleaningAgentState) -> CleaningAgentState:
        log_info(f"Analyzing data: {state}")
        if "data" not in state or state["data"] is None or state["data"].empty:
            return {"error": "No data provided"}

        df = state["data"]

        data_summary = df.describe().to_string() + "\n" + df.head().to_string()
        log_info(f"Data summary: {data_summary}")

        stats = df.describe().to_string()  # Statistics
        sample = df.head(3).to_string()  # First 3 rows
        random_sample = (df.sample(n=5).to_string())  # Random 5e rows
        dtypes = df.dtypes.to_string()  # Column types
        missing = df.isnull().sum().to_string()  # Missing values
        unique = df.nunique().to_string()  # Unique values
        
        shape = f"Rows: {df.shape[0]}, Columns: {df.shape[1]}"
        duplicates = df.duplicated().sum()
        categorical_stats = df.select_dtypes(include='object').describe().to_string()
        
        system_prompt = (
            "You are a data cleaning AI expert.\n"
            "Analyze this dataset and identify problems (e.g., missing values, duplicates, invalid data).\n"
            "Dataset context: Columns available - " + ", ".join(df.columns.tolist()) + "\n"
            "Dataset shape: " + shape + "\n\n"
            "Statistics:\n" + stats + "\n\n"
            "Sample rows (random):\n" + sample + "\n\n"  # Better representation
            "Column types:\n" + "\n".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()]) + "\n\n"
            "Missing values:\n" + missing + "\n\n"
            "Duplicate rows: " + str(duplicates) + "\n\n"
            "Unique values per column:\n" + unique + "\n\n"
            "Categorical variables summary:\n" + categorical_stats + "\n\n"
            "What data quality issues do you identify? Consider:\n"
            "- Outliers in numeric columns\n"
            "- Invalid formats (emails, dates)\n"
            "- Inconsistent categorical values\n"
            "- Values mismatching column types"
        )

        log_info(f"System prompt: {system_prompt}")

        detected_issues = self.ollama_client.generate_response(system_prompt, "", DetectedIssues)

        log_info(f"Detected issues: {detected_issues}")

        return {"issues": detected_issues}
