import streamlit as st
from backend.models.pydantic.core.report import Report
from ui.components.missing_values.missing_values import MissingValuesComponent
from ui.components.common.numerical_statistics import NumericalStatisticsComponent
from ui.components.common.preview import PreviewComponent
from ui.components.missing_values.missing_values_strategies import MissingValuesStrategiesUI
from ui.components.common.categorical_statistics import CategoricalStatisticsComponent
from utils.logger import log_info
import pandas as pd

class MissingValuesReportUI:
    def __init__(self, report: Report, df: pd.DataFrame):
        self.report: Report = report
        self.df: pd.DataFrame = df

    def render(self):
        st.header("Missing Values")

        if self.report.handled_missing_values_data is None or self.report.handled_missing_values_data.empty:
            st.warning("No data available to display")
            return
        
        tabs = st.tabs([
            "Overview",
            "Preview",
            "Missing Values", 
            "Numerical Stats", 
            "Categorical Stats",
            "Strategies for Missing Values" 
        ])

        data_after_missing_values_handling = self.report.handled_missing_values_data
        original_data = self.report.initial_data_preview
        
        with tabs[0]:
            OverviewMissingValuesComponent(self.report).render() 

        with tabs[1]:
            PreviewComponent(
                data_after_missing_values_handling, 
                original_df=self.df,
                title="First 10 Rows"
            ).render()

        with tabs[2]:
            MissingValuesComponent(self.report).render()

        with tabs[3]:
            NumericalStatisticsComponent(self.report.cleaned_data).render()

        with tabs[4]:
            CategoricalStatisticsComponent(self.report).render()

        with tabs[5]:
            MissingValuesStrategiesUI(self.report).render()


class OverviewMissingValuesComponent:
    def __init__(self, report: Report):
        self.report: Report = report
        log_info(self.report)

    def render(self):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", self.report.rows)
            st.metric("Columns", self.report.columns)
        with col2:
            st.metric("Missing Values", self.report.missing_values.sum())
            total_cells = self.report.rows * self.report.columns
            overall_missing_percentage = (self.report.missing_values.sum() / total_cells) * 100
            st.metric("Missing Values Percentage", f"{overall_missing_percentage:.2f}%")

        st.subheader("Data Types")
        dtypes_count = self.report.data_types.value_counts().reset_index()
        dtypes_count.columns = ['Data Type', 'Count']
        dtypes_count['Data Type'] = dtypes_count['Data Type'].apply(str)
        st.bar_chart(dtypes_count.set_index('Data Type'))


class NumericalStatsComponent:
    def __init__(self, report: Report):
        self.report: Report = report
        log_info(self.report)

    def render(self):
        st.header("Numerical Statistics")
        if not self.report.numerical_statistics.empty:
            st.dataframe(self.report.numerical_statistics)
        else:
            st.write("No numerical statistics available.")
