import streamlit as st
import pandas as pd
import pandas as pd

class NumericalStatisticsComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def render(self):
        st.subheader("Numerical Summary")
        st.dataframe(self.df.describe(), use_container_width=True)

        st.subheader("Dataset Info")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rows", self.df.shape[0])
        with col2:
            st.metric("Columns", self.df.shape[1])
        
        dtypes_count = self.df.dtypes.value_counts()
        dtype_summary = ", ".join([f"{dtype}({count})" for dtype, count in dtypes_count.items()])
        st.caption(f"Data types: {dtype_summary}")
        
        columns_info = []
        for col in self.df.columns:
            non_null = self.df[col].count()
            null_count = self.df[col].isna().sum()
            null_percent = f"{null_count / len(self.df) * 100:.1f}%"
            dtype = str(self.df[col].dtype)
            sample = str(self.df[col].iloc[0]) if len(self.df) > 0 else ""
            if len(sample) > 50:
                sample = sample[:47] + "..."
            
            columns_info.append({
                "Column": col,
                "Type": dtype,
                "Non-Null Count": f"{non_null} ({100-float(null_percent[:-1]):.1f}%)",
                "Null Count": f"{null_count} ({null_percent})",
                "Sample Value": sample
            })
        
        st.dataframe(pd.DataFrame(columns_info), use_container_width=True)

