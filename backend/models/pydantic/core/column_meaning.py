from pydantic import BaseModel

class ColumnMeaning(BaseModel):
    column_meaning: str

    class Config:
        arbitrary_types_allowed = True
    