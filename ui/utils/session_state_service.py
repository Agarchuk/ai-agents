import streamlit as st
from backend.clients.postgres_client import PostgresClient
from backend.clients.auth0_client import Auth0Client
from backend.mappers.user_mapper import UserMapper
from backend.services.user_service import UserService
from ui.utils.session_config import SessionConfig
from utils.logger import log_info

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
    def has(key: str) -> bool:
        """Checks if the key exists in session_state."""
        return key in st.session_state

    @staticmethod
    def get_user_sub() -> str:
        return SessionStateService.get(SessionConfig.USER_SUB)
    
    @staticmethod
    def get_or_create_component(key, constructor, *args, **kwargs):
        if not SessionStateService.has(key):
            log_info(f"Creating component: {key}")
            component_instance = constructor(*args, **kwargs) if callable(constructor) else constructor()
            SessionStateService.set(key, component_instance)
        return SessionStateService.get(key)

    @staticmethod
    def get_or_create_postgres_client():
        return SessionStateService.get_or_create_component(SessionConfig.POSTGRES_CLIENT, PostgresClient)

    @staticmethod
    def get_or_create_auth0_client():
        return SessionStateService.get_or_create_component(SessionConfig.AUTH0_CLIENT, Auth0Client)

    @staticmethod
    def get_or_create_user_service():
        return SessionStateService.get_or_create_component(SessionConfig.USER_SERVICE, UserService)

    @staticmethod
    def get_or_create_user_mapper():
        return SessionStateService.get_or_create_component(SessionConfig.USER_MAPPER, UserMapper)