from utils.logger import log_warning
from backend.config.security_config import (
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_AUTHORIZATION_URL,
    AUTH0_TOKEN_URL,
    AUTH0_REVOKE_URL,
    AUTH0_REDIRECT_URI,
)
from streamlit_oauth import OAuth2Component

class Auth0Client:
    def __init__(self):
        self.oauth2 = OAuth2Component(
            AUTH0_CLIENT_ID,
            AUTH0_CLIENT_SECRET,
            AUTH0_AUTHORIZATION_URL,
            AUTH0_TOKEN_URL,
            AUTH0_REVOKE_URL,
        )
        self.auth_config = {
            "name": "Login with Google",
            "icon": "https://www.google.com.tw/favicon.ico",
            "redirect_uri": AUTH0_REDIRECT_URI,
            "scope": "openid email profile https://www.googleapis.com/auth/calendar.events",
            "key": "google",
            "pkce": 'S256',
        }

    def authorize(self):
        log_warning("Starting OAuth2 authorization")
        result = self.oauth2.authorize_button(**self.auth_config)
        log_warning(f"Authorization result: {result}")

        return result

