from backend.states.cleaning_agent_state import CleaningAgentState
from backend.models.pydantic.duplicates.duplicates_recommendations import DuplicatesRecommendations
from backend.models.pydantic.duplicates.removed_duplicates import RemovedDuplicates, RemovedDuplicatesInfo
from utils.logger import log_info
import pandas as pd

class HandleDuplicateValuesNode:
    def handle_duplicate_values(self, state: CleaningAgentState) -> CleaningAgentState:
        report = state.report
        if report.handled_missing_values_data is None:
            df: pd.DataFrame = state.data.copy()
        else:
            df = report.handled_missing_values_data.copy()

        duplicates_recommendations: DuplicatesRecommendations = report.duplicates_recommendations
        removed_duplicates_list = []

        for key, recommendation in duplicates_recommendations.duplicates_recommendations.items():  
            if 'action' in recommendation:
                if recommendation['action'] == "remove":
                    columns = [col.strip() for col in key.split(',')]
                    
                    duplicates_mask = df.duplicated(subset=columns, keep='first')
                    removed_rows = df[duplicates_mask].copy()
                    
                    removed_info = RemovedDuplicatesInfo(
                        columns=columns,
                        removed_rows=removed_rows
                    )
                    removed_duplicates_list.append(removed_info)
                    
                    df = df.drop_duplicates(subset=columns, keep="first")

        report.handled_duplicates_data = df
        report.removed_duplicates = RemovedDuplicates(removed_duplicates=removed_duplicates_list)

        if df is not None:
            report.cleaned_data = df

        return {'report': report}
