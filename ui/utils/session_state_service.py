import streamlit as st
from ui.utils.session_config import SessionConfig

class SessionStateService:
    """Flexible service for managing user state in Streamlit."""

    @staticmethod
    def set(key: str, value):
        """Sets the value for the specified key in session_state."""
        st.session_state[key] = value

    @staticmethod
    def get(key: str, default=None):
        """Gets the value from session_state; returns default if not found."""
        return st.session_state.get(key, default)

    @staticmethod
    def get_user_sub() -> str:
        return SessionStateService.get(SessionConfig.USER_SUB)

