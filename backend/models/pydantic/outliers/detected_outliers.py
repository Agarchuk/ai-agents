from pydantic import BaseModel
from typing import Dict, List
from backend.models.pydantic.outliers.column_outliers import ColumnOutliers


class DetectedOutliers(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        
    outliers_by_column: Dict[str, ColumnOutliers]
    total_outliers: int
    
    def get_affected_columns(self) -> List[str]:
        return list(self.outliers_by_column.keys())
    