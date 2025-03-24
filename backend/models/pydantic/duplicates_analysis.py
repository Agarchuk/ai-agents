from pydantic import BaseModel, model_validator

class DuplicatesAnalysis(BaseModel):
    unique_identifier_column: str | None = None
    combined_key_columns: list[str] | None = None



        
