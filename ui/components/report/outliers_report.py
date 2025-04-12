import pandas as pd
from backend.models.pydantic.core.report import Report
from backend.models.pydantic.outliers.detected_outliers import DetectedOutliers
from backend.models.pydantic.outliers.column_outliers import ColumnOutliers
import streamlit as st
from typing import Dict
import plotly.express as px

from utils.logger import log_info
from ui.components.common.preview import PreviewComponent

class OutliersReportUI:
    def __init__(self, report: Report, df: pd.DataFrame):
        self.report: Report = report
        self.df: pd.DataFrame = df

    def render(self):
        st.header("Outliers Report")

        df = self.report.handled_outliers_data

        if df is None:
            st.error("No data available for outliers analysis")
            return

        detected_outliers: DetectedOutliers = self.report.detected_outliers

        columns_names = detected_outliers.get_affected_columns()
        columns: Dict[str, ColumnOutliers] = detected_outliers.outliers_by_column
        selected_column = st.selectbox("Select column to view details:", columns_names)

        tabs = st.tabs(["Outliers Details", "Data Preview"])
        
        with tabs[0]:
            if selected_column:
                column_outliers = columns[selected_column]
                column_outliers_count = column_outliers.count
                lower_bound = column_outliers.lower_bound
                upper_bound = column_outliers.upper_bound 
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Statistics:**")
                    st.write(f"- Number of outliers: {column_outliers_count}")
                    st.write(f"- Percentage: {column_outliers_count/len(df)*100:.2f}%")
                    st.write(f"- Lower bound: {lower_bound:.5f}")
                    st.write(f"- Upper bound: {upper_bound:.5f}")
                
                with col2:
                    fig = px.box(df, y=selected_column, title=f"Box Plot for {selected_column}")
                    st.plotly_chart(fig, use_container_width=True)

                outliers = column_outliers.outliers
                st.write("**Example outlier values:**")
                st.write(outliers.tolist())

                st.write(f"**Validation:** {column_outliers.plausibility.validation}")
                st.write(f"**Plausibility explanation:** {column_outliers.plausibility.explanation}")

                if column_outliers.strategy:
                    st.write(f"**Used strategy:** {column_outliers.strategy.strategy}")
                    st.write(f"**Strategy explanation:** {column_outliers.strategy.explanation}")

        with tabs[1]:
            PreviewComponent(df, original_df=self.df, title="Preview of Handled Outliers Data").render()
