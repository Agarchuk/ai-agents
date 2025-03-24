import streamlit as st
from backend.agents.cleaning_agent import CleaningAgent
from backend.agents.nodes.analysis_node import AnalysisNode
from backend.agents.nodes.detect_outliers_node import DetectOutliersNode
from backend.agents.nodes.duplicate_values_node import DuplicateValuesNode
from backend.agents.nodes.handle_duplicate_values_node import HandleDuplicateValuesNode
from backend.agents.nodes.handle_outliners_node import HandleOutlinersNode
from backend.agents.nodes.missing_values_node import MissingValuesNode
from backend.agents.nodes.handle_missing_values_node import HandleMissingValuesNode
from backend.clients.ollama_client import OllamaClient
from backend.clients.postgres_client import PostgresClient
from backend.clients.auth0_client import Auth0Client
from backend.mappers.user_mapper import UserMapper
from backend.repositories.user_repository import UserRepository
from backend.services.data_cleaning_service import DataCleaningService
from backend.services.user_service import UserService
from ui.utils.session_config import SessionConfig
from utils.logger import log_info

class SessionStateService:
    """Flexible service for managing user state in Streamlit."""

    @staticmethod
    def set(key: str, value):
        """Sets the value for the specified key in session_state."""
        st.session_state[key] = value
        print(f"Set session state: {key} = {value}")  # Debug print

    @staticmethod
    def get(key: str, default=None):
        """Gets the value from session_state; returns default if not found."""
        value = st.session_state.get(key, default)
        print(f"Get session state: {key} = {value}")  # Debug print
        return value
    
    @staticmethod
    def has(key: str) -> bool:
        """Checks if the key exists in session_state."""
        return key in st.session_state

    @staticmethod
    def get_user_sub() -> str:
        return SessionStateService.get(SessionConfig.USER_SUB)

    @staticmethod
    def get_selected_ollama_model() -> str:
        model = SessionStateService.get(SessionConfig.SELECTED_OLLAMA_MODEL, "smollm2:135m")
        print(f"get_selected_ollama_model returning: {model}") # Debug print
        return model
    
    @staticmethod
    def get_or_create_component(key, constructor, *args, **kwargs):
        if not SessionStateService.has(key):
            log_info(f"Creating component: {key}, args: {args}, kwargs: {kwargs}")
            component_instance = constructor(*args, **kwargs) if callable(constructor) else constructor()
            SessionStateService.set(key, component_instance)
        return SessionStateService.get(key)

    # Clients
    @staticmethod
    def get_or_create_postgres_client():
        return SessionStateService.get_or_create_component(SessionConfig.POSTGRES_CLIENT, PostgresClient)

    @staticmethod
    def get_or_create_auth0_client():
        return SessionStateService.get_or_create_component(SessionConfig.AUTH0_CLIENT, Auth0Client)
    
    @staticmethod
    def get_or_create_ollama_client(model: str = None):
        log_info(f"Creating ollama client with model: {model}")
        
        if model is None:
            model = SessionStateService.get_selected_ollama_model()
        print(f"Ollama client will be created with model: {model}")
        
        # Create a model-specific key for the client
        client_key = f"{SessionConfig.OLLAMA_CLIENT}_{model}" if model else SessionConfig.OLLAMA_CLIENT

        return SessionStateService.get_or_create_component(client_key, OllamaClient, model)

    # Services
    @staticmethod
    def get_or_create_user_service():
        user_repository = SessionStateService.get_or_create_user_repository()
        user_mapper = SessionStateService.get_or_create_user_mapper()
        return SessionStateService.get_or_create_component(SessionConfig.USER_SERVICE, UserService, user_repository, user_mapper)
    
    @staticmethod
    def get_or_create_data_cleaning_service(model: str = None):
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        return SessionStateService.get_or_create_component(SessionConfig.DATA_CLEANING_SERVICE, DataCleaningService, ollama_client)

    # Repositories
    @staticmethod
    def get_or_create_user_repository():
        return SessionStateService.get_or_create_component(SessionConfig.USER_REPOSITORY, UserRepository)

    # Mappers
    @staticmethod
    def get_or_create_user_mapper():
        return SessionStateService.get_or_create_component(SessionConfig.USER_MAPPER, UserMapper)
    

    # Nodes
    @staticmethod
    def get_or_create_analysis_node() -> AnalysisNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.ANALYSIS_NODE}_{model}" if model else SessionConfig.ANALYSIS_NODE
        return SessionStateService.get_or_create_component(node_key, AnalysisNode, ollama_client)
    
    @staticmethod
    def get_or_create_missing_values_node() -> MissingValuesNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.MISSING_VALUES_NODE}_{model}" if model else SessionConfig.MISSING_VALUES_NODE
        return SessionStateService.get_or_create_component(node_key, MissingValuesNode, ollama_client)
    
    @staticmethod
    def get_or_create_handle_missing_values_node() -> HandleMissingValuesNode:
        return SessionStateService.get_or_create_component(SessionConfig.HANDLE_MISSING_VALUES_NODE, HandleMissingValuesNode)
    
    @staticmethod
    def get_or_create_duplicate_values_node() -> DuplicateValuesNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.DUPLICATE_VALUES_NODE}_{model}" if model else SessionConfig.DUPLICATE_VALUES_NODE
        return SessionStateService.get_or_create_component(node_key, DuplicateValuesNode, ollama_client)
    
    @staticmethod
    def get_or_create_handle_duplicate_values_node() -> HandleDuplicateValuesNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.HANDLE_DUPLICATE_VALUES_NODE}_{model}" if model else SessionConfig.HANDLE_DUPLICATE_VALUES_NODE
        return SessionStateService.get_or_create_component(node_key, HandleDuplicateValuesNode, ollama_client)
    
    @staticmethod
    def get_or_create_detect_outliners_node() -> DetectOutliersNode:
       return SessionStateService.get_or_create_component(SessionConfig.DETECT_OUTLINERS_NODE, DetectOutliersNode, )
    
    @staticmethod
    def get_or_create_handle_outliners_node() -> HandleOutlinersNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.HANDLE_OUTLINERS_NODE}_{model}" if model else SessionConfig.HANDLE_OUTLINERS_NODE
        return SessionStateService.get_or_create_component(node_key, HandleOutlinersNode, ollama_client)
    
    # Agents
    @staticmethod
    def get_or_create_cleaning_agent(model: str = None) -> CleaningAgent:
        if model is None:
            model = SessionStateService.get_selected_ollama_model()
        agent_key = f"{SessionConfig.CLEANING_AGENT}_{model}" if model else SessionConfig.CLEANING_AGENT
        analysis_node = SessionStateService.get_or_create_analysis_node()
        missing_values_node = SessionStateService.get_or_create_missing_values_node()
        handle_missing_values_node = SessionStateService.get_or_create_handle_missing_values_node()
        duplicate_values_node = SessionStateService.get_or_create_duplicate_values_node()
        handle_duplicate_values_node = SessionStateService.get_or_create_handle_duplicate_values_node()
        detect_outliners_node = SessionStateService.get_or_create_detect_outliners_node()
        handle_outliners_node = SessionStateService.get_or_create_handle_outliners_node()
        return SessionStateService.get_or_create_component(agent_key, CleaningAgent, analysis_node, missing_values_node, handle_missing_values_node, duplicate_values_node, handle_duplicate_values_node, detect_outliners_node, handle_outliners_node)
    