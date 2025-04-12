import pandas as pd
import streamlit as st
from backend.models.pydantic.core.report import Report
from utils.logger import log_info

class MissingValuesComponent:
    def __init__(self, report: Report):
        self.report: Report = report
        log_info(self.report)

    def render(self):
        st.subheader("Missing Values")
        missing_data = pd.DataFrame({
            'Missing Values': self.report.missing_values,
            'Percentage': self.report.missing_values_percentage
        })
        
        missing_data = missing_data[missing_data['Missing Values'] > 0]
        st.dataframe(missing_data, use_container_width=True)

        st.subheader("Missing Values Heatmap")
        st.write("Columns with missing values:")
        cols_with_missing = missing_data.index.tolist()
        if cols_with_missing:
            st.dataframe(self.report.initial_data_preview[cols_with_missing].isna(), use_container_width=True)
        else:
            st.success("No missing values found!")