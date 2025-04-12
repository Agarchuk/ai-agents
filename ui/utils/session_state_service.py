import streamlit as st
from backend.agents.cleaning_agent import CleaningAgent
from backend.nodes.analysis_node import AnalysisNode
from backend.nodes.dataset_topic_node import DatasetTopicNode
from backend.nodes.outliers.detect_outliers_node import DetectOutliersNode
from backend.nodes.duplicates.duplicate_values_node import DuplicateValuesNode
from backend.nodes.duplicates.handle_duplicate_values_node import HandleDuplicateValuesNode
from backend.nodes.handle_outliers_node import HandleOutliersNode
from backend.nodes.outliers.handle_plausibility_of_outliers_node import HandlePlausibilityOfOutliersNode
from backend.nodes.missing_values.missing_values_node import MissingValuesNode
from backend.nodes.missing_values.handle_missing_values_node import HandleMissingValuesNode
from backend.clients.ollama_client import OllamaClient
from backend.clients.postgres_client import PostgresClient
from backend.clients.auth0_client import Auth0Client
from backend.mappers.user_mapper import UserMapper
from backend.repositories.user_repository import UserRepository
from backend.services.user_service import UserService
from ui.utils.session_config import SessionConfig
from backend.nodes.human_confirmation_node import HumanConfirmationNode

class SessionStateService:
    """Flexible service for managing user state in Streamlit."""

    @staticmethod
    def set(key: str, value):
        """Sets the value for the specified key in session_state."""
        st.session_state[key] = value

    @staticmethod
    def get(key: str, default=None):
        """Gets the value from session_state; returns default if not found."""
        value = st.session_state.get(key, default)
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
        # print(f"get_selected_ollama_model returning: {model}") # Debug print
        return model
    
    @staticmethod
    def get_or_create_component(key, constructor, *args, **kwargs):
        if not SessionStateService.has(key):
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
        if model is None:
            model = SessionStateService.get_selected_ollama_model()
        
        client_key = f"{SessionConfig.OLLAMA_CLIENT}_{model}" if model else SessionConfig.OLLAMA_CLIENT

        return SessionStateService.get_or_create_component(client_key, OllamaClient, model)

    # Services
    @staticmethod
    def get_or_create_user_service():
        user_repository = SessionStateService.get_or_create_user_repository()
        user_mapper = SessionStateService.get_or_create_user_mapper()
        return SessionStateService.get_or_create_component(SessionConfig.USER_SERVICE, UserService, user_repository, user_mapper)
    
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
    def get_or_create_dataset_topic_node() -> DatasetTopicNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.DATASET_TOPIC_NODE}_{model}" if model else SessionConfig.DATASET_TOPIC_NODE
        return SessionStateService.get_or_create_component(node_key, DatasetTopicNode, ollama_client)
    
    @staticmethod
    def get_or_create_analysis_node() -> AnalysisNode:
        return SessionStateService.get_or_create_component(SessionConfig.ANALYSIS_NODE, AnalysisNode)
    
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
        return SessionStateService.get_or_create_component(SessionConfig.HANDLE_DUPLICATE_VALUES_NODE, HandleDuplicateValuesNode)
    
    @staticmethod
    def get_or_create_detect_outliers_node() -> DetectOutliersNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.DETECT_OUTLIERS_NODE}_{model}" if model else SessionConfig.DETECT_OUTLIERS_NODE
        return SessionStateService.get_or_create_component(node_key, DetectOutliersNode, ollama_client)

    @staticmethod
    def get_or_create_handle_plausibility_of_outliers_node() -> HandlePlausibilityOfOutliersNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.HANDLE_PLAUSIBILITY_OF_OUTLIERS_NODE}_{model}" if model else SessionConfig.HANDLE_PLAUSIBILITY_OF_OUTLIERS_NODE
        return SessionStateService.get_or_create_component(node_key, HandlePlausibilityOfOutliersNode, ollama_client)
    
    @staticmethod
    def get_or_create_handle_outliers_node() -> HandleOutliersNode:
        model = SessionStateService.get_selected_ollama_model()
        ollama_client = SessionStateService.get_or_create_ollama_client(model)
        node_key = f"{SessionConfig.HANDLE_OUTLIERS_NODE}_{model}" if model else SessionConfig.HANDLE_OUTLIERS_NODE
        return SessionStateService.get_or_create_component(node_key, HandleOutliersNode, ollama_client)

    @staticmethod
    def get_or_create_human_confirmation_node():
        return SessionStateService.get_or_create_component(
            SessionConfig.HUMAN_CONFIRMATION_NODE,
            HumanConfirmationNode
        )

    # Agents
    @staticmethod
    def get_or_create_cleaning_agent(model: str = None) -> CleaningAgent:
        if model is None:
            model = SessionStateService.get_selected_ollama_model()
        agent_key = f"{SessionConfig.CLEANING_AGENT}_{model}" if model else SessionConfig.CLEANING_AGENT
        dataset_topic_node = SessionStateService.get_or_create_dataset_topic_node()
        analysis_node = SessionStateService.get_or_create_analysis_node()
        missing_values_node = SessionStateService.get_or_create_missing_values_node()
        handle_missing_values_node = SessionStateService.get_or_create_handle_missing_values_node()
        duplicate_values_node = SessionStateService.get_or_create_duplicate_values_node()
        handle_duplicate_values_node = SessionStateService.get_or_create_handle_duplicate_values_node()
        detect_outliers_node = SessionStateService.get_or_create_detect_outliers_node()
        handle_plausibility_of_outliers_node = SessionStateService.get_or_create_handle_plausibility_of_outliers_node()
        human_confirmation_node = SessionStateService.get_or_create_human_confirmation_node()
        
        return SessionStateService.get_or_create_component(
            agent_key, 
            CleaningAgent,
            dataset_topic_node,
            analysis_node,
            missing_values_node,
            handle_missing_values_node,
            duplicate_values_node,
            handle_duplicate_values_node,
            detect_outliers_node,
            handle_plausibility_of_outliers_node,
            human_confirmation_node
        )
    