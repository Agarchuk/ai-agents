import pandas as pd
import streamlit as st

from backend.models.pydantic.core.report import Report
from backend.services.file_service import FileService
from ui.components.common.preview import PreviewComponent
from ui.components.report.duplicates_report import DuplicatesReportUI
from ui.components.report.missing_values_report import MissingValuesReportUI
from ui.components.data_explorer import DataExplorer
from ui.components.sidebar.cleaning_agent_sidebar import CleaningAgentSidebar
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig
from ui.components.report.outliers_report import OutliersReportUI
from utils.logger import log_info

if __name__ == "__page__":
    st.title("Cleaning Agent")
    st.write("This agent cleans your data")

    CleaningAgentSidebar().render()  
    
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"]) 

    if uploaded_file:
        df: pd.DataFrame = FileService.read_dataframe(uploaded_file)
        
        DataExplorer(df).render()

        selected_model = SessionStateService.get_selected_ollama_model() # Get selected model

        if st.button("Clean Dataset"):
            with st.spinner("Starting cleaning process..."):
                agent = SessionStateService.get_or_create_cleaning_agent(selected_model)
                initial_state = {
                    "data": df, 
                    "report": Report(), 
                    "error": None,
                    "iteration": 1
                }
                agent_result = agent.invoke(initial_state)

                SessionStateService.set(SessionConfig.CLEANING_RESULT, agent_result)


        if SessionStateService.has(SessionConfig.CLEANING_RESULT):
            agent_result = SessionStateService.get(SessionConfig.CLEANING_RESULT)
            report: Report = agent_result["report"]
            
            st.title("Data Quality Report")
            
            # Display reports
            MissingValuesReportUI(report).render()
            DuplicatesReportUI(report).render()
            OutliersReportUI(report).render()

            st.header("Cleaned Dataset:")
            PreviewComponent(report.cleaned_data, title="Cleaned Dataset", original_df=df).render()
            
            csv = report.cleaned_data.to_csv(index=False)
            st.download_button("Download CSV", csv, file_name="cleaned_dataset.csv")

