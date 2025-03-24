class SessionConfig:
    """Class to store key names for session state management."""
    
    # Authentication keys
    ACCESS_TOKEN = "access_token"
    USER_ID = "user_id"
    USER_SUB = "user_sub"

    # clients
    POSTGRES_CLIENT = "postgres_client"
    AUTH0_CLIENT = "auth0_client"
    OLLAMA_CLIENT = "ollama_client"

    # services
    USER_SERVICE = "user_service"
    DATA_CLEANING_SERVICE = "data_cleaning_service"

    # repositories
    USER_REPOSITORY = "user_repository"

    # mappers
    USER_MAPPER = "user_mapper"

    # nodes
    ANALYSIS_NODE = "analysis_node"
    MISSING_VALUES_NODE = "missing_values_node"
    HANDLE_MISSING_VALUES_NODE = "handle_missing_values_node"
    DUPLICATE_VALUES_NODE = "duplicate_values_node"
    HANDLE_DUPLICATE_VALUES_NODE = "handle_duplicate_values_node"
    DETECT_OUTLINERS_NODE = "detect_outliners_node"
    HANDLE_OUTLINERS_NODE = "handle_outliners_node"

    # agents
    CLEANING_AGENT = "cleaning_agent"
    
    # tools
    GET_CURRENT_DATE_TIME_TOOL = "get_current_date_time_tool"

    # sidebar
    SELECTED_OLLAMA_MODEL = "selected_ollama_model"

    # cleaning result
    CLEANING_RESULT = "cleaning_result"