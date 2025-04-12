import streamlit as st
import pandas as pd

from backend.models.pydantic.core.report import Report
from ui.components.duplicates.duplicates_strategies import DuplicatesStrategies
from ui.components.common.preview import PreviewComponent

class DuplicatesReportUI:    
    def __init__(self, report: Report, df: pd.DataFrame):
        self.report: Report = report
        self.df: pd.DataFrame = df

    def render(self):
        st.header("Duplicates report")
        data = self.report.handled_duplicates_data

        if data is None or data.empty:
            st.warning("No data available to display")
            return
        
        tabs = st.tabs([
            "Preview",
            "Strategies",
            "Removed Duplicates Summary"
        ])

        with tabs[0]:
            PreviewComponent(data, original_df=self.df, title="Data after duplicate values handling").render()

        with tabs[1]:
            DuplicatesStrategies(self.report).render()

        with tabs[2]:
            self.render_removed_duplicates_summary()

    def render_removed_duplicates_summary(self):
        removed_duplicates = self.report.removed_duplicates
        if removed_duplicates and removed_duplicates.removed_duplicates:
            st.subheader("Summary of Removed Duplicates")
            for removed_info in removed_duplicates.removed_duplicates:
                st.markdown(f"**Columns:** {', '.join(removed_info.columns)}")
                st.markdown(f"**Number of Removed Rows:** {len(removed_info.removed_rows)}")
                # Optionally, display a sample of removed rows
                if not removed_info.removed_rows.empty:
                    st.dataframe(removed_info.removed_rows.head())
        else:
            st.info("No duplicates were removed.")

