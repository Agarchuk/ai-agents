import streamlit as st

AUTH0_CLIENT_ID = st.secrets["auth0"]["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = st.secrets["auth0"]["AUTH0_CLIENT_SECRET"]
AUTH0_DOMAIN = st.secrets["auth0"]["AUTH0_DOMAIN"]
AUTH0_AUDIENCE = f"https://{AUTH0_DOMAIN}/userinfo"
AUTH0_AUTHORIZATION_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_REVOKE_URL = f"https://{AUTH0_DOMAIN}/revoke"
AUTH0_REDIRECT_URI = st.secrets["auth0"]["AUTH0_CALLBACK_URL"]
