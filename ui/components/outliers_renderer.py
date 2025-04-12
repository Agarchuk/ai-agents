import streamlit as st
import pandas as pd
import plotly.express as px
from backend.states.cleaning_agent_state import CleaningAgentState
from backend.models.pydantic.outliers_result import OutliersResult
from utils.logger import log_info
from typing import List

class OutliersRenderer: 
    def __init__(self, state: CleaningAgentState):
        self.state = state

    def render(self):
        """
        Renders the outliers analysis information using Streamlit.
        
        Args:
            state (CleaningAgentState): The current state containing outliers information
        """
        if 'outliers_info' not in self.state or not self.state['outliers_info']:
            st.info("No outliers were detected in the dataset.")
            return

        df: pd.DataFrame = self.state['data']
        outliers_info = self.state['outliers_info']
        outliers_results: List[OutliersResult] = self.state['outliers_results']
        log_info(f"outliers_results: {outliers_results}")
            
        st.header("Outliers Analysis")
        
        # Display summary statistics
        st.subheader("Summary")
        total_outliers = sum(info['count'] for info in outliers_info.values())
        total_rows = len(df)
        st.write(f"Total outliers detected: {total_outliers} ({total_outliers/total_rows*100:.2f}% of total rows)")
        
        # Display detailed information for each column
        st.subheader("Detailed Analysis")
        
        columns = list(outliers_info.keys())
        selected_column = st.selectbox("Select column to view details:", columns)
        
        if selected_column:
            info = outliers_info[selected_column]
            outliers_result: OutliersResult = next((result for result in outliers_results if result.column == selected_column), None)
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Statistics:")
                st.write(f"- Number of outliers: {info['count']}")
                st.write(f"- Percentage: {info['count']/len(df)*100:.2f}%")
                st.write(f"- Lower bound: {info['lower_bound']:.2f}")
                st.write(f"- Upper bound: {info['upper_bound']:.2f}")
            
            with col2:
                # Create box plot
                fig = px.box(df, y=selected_column, title=f"Box Plot for {selected_column}")
                st.plotly_chart(fig, use_container_width=True)
            
            # Display example outliers
            outliers = df[(df[selected_column] < info['lower_bound']) | (df[selected_column] > info['upper_bound'])][selected_column]
            st.write("Example outlier values:")
            st.write(outliers.tolist())

            st.write(f"Validation: {outliers_result.plausibility}")
            st.write(f"Plausibility explanation: {outliers_result.plausibility_explanation}")
            st.write(f"Used strategy: {outliers_result.used_strategy}")
            st.write(f"Strategy explanation: {outliers_result.strategy_explanation}")
            st.write(f"Risks: {outliers_result.risks}")
            st.write(f"Benefits: {outliers_result.benefits}")
        
        # If outliers were handled, show the results
        if 'data_after_outliers_handling' in self.state:
            st.subheader("Results After Handling Outliers")
            handled_df = self.state['data_after_outliers_handling']
            st.write(f"Rows after handling: {len(handled_df)}")
            st.write(f"Rows removed: {len(df) - len(handled_df)}") 