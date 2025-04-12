from pydantic import BaseModel

class ConstantValue(BaseModel):
    constant_value: str
