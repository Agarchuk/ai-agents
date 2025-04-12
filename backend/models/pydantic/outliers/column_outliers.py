from dataclasses import dataclass
import pandas as df
from backend.models.pydantic.outliers_plausibility import OutliersPlausibility
from backend.models.pydantic.outliers_plausibility_strategy import OutliersPlausibilityStrategy

@dataclass
class ColumnOutliers:
    count: int
    lower_bound: float
    upper_bound: float
    outliers: dict
    column_meaning: str | None = None
    plausibility: OutliersPlausibility | None = None
    strategy: OutliersPlausibilityStrategy | None = None
