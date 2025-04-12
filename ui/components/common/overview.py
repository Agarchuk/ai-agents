import streamlit as st
import pandas as pd


class OverviewComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def render(self):
        data_types = self.df.dtypes
        col1, col2 = st.columns(2)
        col1.metric("Rows", self.df.shape[0])
        col2.metric("Columns", self.df.shape[1])

        st.subheader("Data Types")
        dtypes_count = data_types.value_counts().reset_index()
        dtypes_count.columns = ['Data Type', 'Count']
        dtypes_count['Data Type'] = dtypes_count['Data Type'].apply(str)
        st.bar_chart(dtypes_count.set_index('Data Type'))