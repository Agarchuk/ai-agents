import base64
import json
from backend.clients.auth0_client import Auth0Client
from backend.mappers.user_mapper import UserMapper
from backend.services.user_service import UserService
from utils.logger import log_info, log_warning

class Auth0Service:
    def __init__(self, auth0_client: Auth0Client, user_service: UserService, user_mapper: UserMapper):
        self.auth0_client = auth0_client
        self.user_service = user_service
        self.user_mapper = user_mapper

    def authorize_user(self):
        result = self.auth0_client.authorize()
        if not result:
            log_warning("Authorization failed: No result from auth0_client")
            return None

        id_token = result.get("token", {}).get("id_token")
        if not id_token:
            log_warning("Authorization failed: No id_token in result")
            return None

        payload = self._decode_id_token(id_token)
        if not payload:
            log_warning("Authorization failed: Could not decode id_token")
            return None
        
        user = self.user_mapper.map_payload_to_user(payload)
        if not user:
            log_warning("Authorization failed: Could not map payload to user")
            return None
        
        log_info(f"User: {user}")

        db_user = self.user_service.get_or_save_user_to_db(user)
        
        if db_user and hasattr(db_user, 'sub'):
            log_info(f"User {db_user.sub} authenticated successfully")
            return self.user_mapper.map_user_model_to_dto(db_user, id_token)
        else:
            log_warning("Authorization failed: Could not get or save user to database")
            return None
    

    def _decode_id_token(self, id_token: str) -> dict:
        """Decode the ID token and return the payload."""
        try:
            payload = id_token.split(".")[1]
            payload += "=" * (-len(payload) % 4)
            return json.loads(base64.b64decode(payload))
        except Exception as e:
            log_warning(f"Error decoding id_token: {e}")
            return None