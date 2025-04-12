import streamlit as st
import pandas as pd

from backend.models.pydantic.missing_values.missing_value_strategy import MissingValueStrategy
from backend.models.pydantic.core.report import Report
from backend.models.pydantic.missing_values.missing_values_recommendations import MissingValuesRecommendations
from utils.logger import log_info

class MissingValuesStrategiesUI:    
    def __init__(self, report: Report):
        self.report: Report = report

    def render(self):
        st.subheader("Used Strategies for Missing Values")
        
        strategies_data = self._get_strategies_data()
        
        if strategies_data:
            strategies_df = pd.DataFrame(strategies_data)
            st.dataframe(strategies_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No missing value strategies have been applied.")

    def _get_strategies_data(self):
        strategies_data = []
        missing_values_recommendations: MissingValuesRecommendations = self.report.missing_values_recommendations.recommendations
        if missing_values_recommendations:
            for rec in missing_values_recommendations:
                strategy_info = {
                    "Column": rec.column_name,
                    "Strategy": rec.strategy,
                    "Details": self._format_explanation(rec.explanation)
                }
                strategies_data.append(strategy_info)
        return strategies_data
    
    def _format_explanation(self, explanation: str) -> str:
        explanation_paragraphs: list[str] = explanation.split(". ")
        formatted_explanation: str = ""
        for i, para in enumerate(explanation_paragraphs):
            if i < len(explanation_paragraphs) - 1 and not para.endswith("."):
                para += "."
            formatted_explanation += f"- {para}\n\n"
        return formatted_explanation

    def _show_constant_value_if_applicable(self, rec: MissingValueStrategy):
        if rec.strategy == "fill with constant" and rec.constant_value:
            st.info(f"**Constant Value:** {rec.constant_value}")