from backend.models.pydantic.core.report import Report
from backend.states.cleaning_agent_state import CleaningAgentState
from utils.logger import log_info
import streamlit as st

class AnalysisNode:
    def analyze_data(self, state: CleaningAgentState) -> CleaningAgentState:
        data = state.data
        report = state.report

        if report is None:
            report = Report()

        report.data_types = data.dtypes
        report.rows = data.shape[0]
        report.columns = data.shape[1]
        report.available_columns = data.columns.tolist()
        report.missing_values = data.isnull().sum()
        report.missing_values_percentage = data.isnull().mean() * 100
        report.numerical_statistics = data.describe()
        report.categorical_statistics = data.describe(include=['O'])
                
        if data is not None:
            report.initial_data_preview = data
            report.cleaned_data = data

        return {'report': report}
    