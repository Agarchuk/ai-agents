from pydantic import BaseModel

class OutliersInfo(BaseModel):
    column: str
    count: int
    lower_bound: float
    upper_bound: float