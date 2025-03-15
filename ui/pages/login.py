import os
import streamlit as st
from utils.logger import log_warning, log_success
from backend.clients.auth0_client import Auth0Client
from backend.services.auth0_service import Auth0Service
from backend.services.user_service import UserService
from backend.mappers.user_mapper import UserMapper
from ui.utils.session_state_service import SessionStateService
from ui.utils.session_config import SessionConfig
    
class LoginPage:
    def __init__(self):
        self.auth0_client = SessionStateService.get_or_create_auth0_client()
        self.user_service = SessionStateService.get_or_create_user_service()
        self.user_mapper = SessionStateService.get_or_create_user_mapper()
        self.auth_service = Auth0Service(self.auth0_client, self.user_service, self.user_mapper)

    def display(self):
        st.title("Login")
        st.write("Please log in to continue..") 
        user_dto = self.auth_service.authorize_user()

        if user_dto:
            log_success(f"User {user_dto.sub} logged in")
            SessionStateService.set(SessionConfig.USER_SUB, user_dto.sub)
            SessionStateService.set(SessionConfig.TOKEN_KEY, user_dto.token)
            st.rerun()
