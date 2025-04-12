import pandas as pd
import streamlit as st

from backend.models.pydantic.core.report import Report

class CategoricalStatisticsComponent:
    def __init__(self, report: Report):
        self.report: Report = report

    def render(self):
        st.header("Categorical Statistics")
        if not self.report.categorical_statistics.empty:
            st.dataframe(self.report.categorical_statistics)
        else:
            st.write("No categorical statistics available.")