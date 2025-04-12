import streamlit as st
from ui.components.common.overview import OverviewComponent
from ui.components.common.numerical_statistics import NumericalStatisticsComponent
from ui.components.common.preview import PreviewComponent
import pandas as pd

class DataExplorer:
    def __init__(self, df: pd.DataFrame, title: str = "Data Explorer"):
        self.df = df
        self.title = title

    def render(self):
        st.header(self.title)

        if self.df is None or self.df.empty:
            st.warning("No data available to display")
            return

        tabs = st.tabs(["Overview", "Preview", "Numerical Stats"])

        with tabs[0]:
            OverviewComponent(self.df).render()

        with tabs[1]:
            PreviewComponent(self.df).render()

        with tabs[2]:
            NumericalStatisticsComponent(self.df).render()
