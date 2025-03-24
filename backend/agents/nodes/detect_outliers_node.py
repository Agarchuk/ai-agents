from backend.agents.states.cleaning_agent_state import CleaningAgentState
import pandas as pd

class DetectOutliersNode:
    def detect_outliners(self, state: CleaningAgentState) -> CleaningAgentState:
        df: pd.DataFrame = state['data']
        analysis = state["analysis"]
        types = analysis.types
        numeric_cols = [col for col, dtype in types.items() if 'float' in dtype.name or 'int' in dtype.name]
        outliers_info = {}

        if len(numeric_cols) == 0:
            return state
        
        for col in numeric_cols:
                count, lower, upper = self.detect_outliers(df, col)
                if count > 0:
                    outliers_info[col] = {"count": count, "lower_bound": lower, "upper_bound": upper}
        
        return {
            "outliers_info": outliers_info
        }
    
    def detect_outliers(self, df: pd.DataFrame, column: str) -> tuple[int, float, float]:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
        return len(outliers), lower_bound, upper_bound
