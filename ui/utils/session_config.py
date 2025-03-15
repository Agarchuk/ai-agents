class SessionConfig:
    """Class to store key names for session state management."""
    
    # Authentication keys
    TOKEN_KEY = "auth_token"
    USER_ID = "user_id"
    USER_SUB = "user_sub"

    # clients
    POSTGRES_CLIENT = "postgres_client"
    AUTH0_CLIENT = "auth0_client"

    # services
    USER_SERVICE = "user_service"

    # mappers
    USER_MAPPER = "user_mapper"
