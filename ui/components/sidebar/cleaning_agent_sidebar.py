from backend.clients.ollama_client import OllamaClient
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
import streamlit as st

class CleaningAgentSidebar:
    def __init__(self):
        self.ollama_client: OllamaClient = SessionStateService.get_or_create_ollama_client()

    def render(self):
        model_names = self.ollama_client.get_models()
        
        st.sidebar.title("Ollama Model")
        selected_model = st.sidebar.selectbox(
            "Select Ollama model",
            model_names
        )

        SessionStateService.set(SessionConfig.SELECTED_OLLAMA_MODEL, selected_model)
