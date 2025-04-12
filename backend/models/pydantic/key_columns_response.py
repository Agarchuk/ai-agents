from pydantic import BaseModel
from typing import TypeVar, Optional, List, Generic
from enum import Enum

T = TypeVar('T', bound=Enum)

class KeyColumnsResponse(BaseModel, Generic[T]):
    unique_identifier_column: Optional[T] = None
    combined_key_columns: Optional[List[T]] = None
    explanation: str