import streamlit as st
import hashlib
import uuid
import pandas as pd

from utils.logger import log_info

class PreviewComponent:
    def __init__(self, df: pd.DataFrame, title: str = "Data Preview", max_rows: int = None, original_df: pd.DataFrame = None):
        self.df = df
        self.title = title
        self.max_rows = max_rows
        self.original_df = original_df
        
        unique_seed = f"{str(df)}{title}{str(uuid.uuid4())}"
        self.component_id = hashlib.md5(unique_seed.encode()).hexdigest()

    def _highlight_imputed(self, val, col):
        if self.original_df is not None and pd.isna(self.original_df.loc[val.name, col]):
            return 'background-color: yellow'
        return ''

    def _highlight_changed(self, val, col):
        if self.original_df is not None and not pd.isna(self.original_df.loc[val.name, col]) and self.df.loc[val.name, col] != self.original_df.loc[val.name, col]:
            return 'background-color: lightblue'
        return ''

    def render(self):
        st.subheader(self.title)
        
        if self.df is None or self.df.empty:
            st.warning("No data available to display")
            return
                    
        if self.original_df is not None:
            styled_df = self.df.style.apply(
                lambda x: [self._highlight_changed(x, col) for col in self.df.columns], 
                axis=1
            ).apply(
                lambda x: [self._highlight_imputed(x, col) for col in self.df.columns], 
                axis=1
            )
            
            if self.max_rows is not None:
                styled_df = styled_df.head(self.max_rows)
            
            st.dataframe(styled_df, use_container_width=True)
        else:
            if self.max_rows is not None:
                st.dataframe(self.df.head(self.max_rows), use_container_width=True)
            else:
                st.dataframe(self.df, use_container_width=True)
