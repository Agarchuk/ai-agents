import pandas as pd
from backend.models.pydantic.core.report import Report
import streamlit as st

from backend.models.pydantic.duplicates.duplicates_recommendations import DuplicatesRecommendations


class DuplicatesStrategies:
    def __init__(self, report: Report):
        self.report: Report = report    

    def render(self):
        st.subheader("Duplicates strategies")
        
        strategies_data = self._get_strategies_data()
        
        if strategies_data:
            strategies_df = pd.DataFrame(strategies_data)
            st.dataframe(strategies_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No duplicate value strategies have been applied.")

    def _get_strategies_data(self):
        strategies_data = []
        if self.report:
            duplicates_recommendations: DuplicatesRecommendations = self.report.duplicates_recommendations
            if duplicates_recommendations:
                for column_name, rec in duplicates_recommendations.duplicates_recommendations.items():
                    strategy_info = {
                        "Column": column_name,
                        "Action": rec['action'],
                        "Explanation": self._format_explanation(rec['explanation'])
                    }
                    strategies_data.append(strategy_info)
        return strategies_data
    
    def _format_explanation(self, explanation):
        explanation_paragraphs = explanation.split(". ")
        formatted_explanation = ""
        for i, para in enumerate(explanation_paragraphs):
            if i < len(explanation_paragraphs) - 1 and not para.endswith("."):
                para += "."
            formatted_explanation += f"- {para}\n\n"
        return formatted_explanation
