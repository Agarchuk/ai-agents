import streamlit as st

POSTGRES_HOST = st.secrets["postgres"]["POSTGRES_HOST"]
POSTGRES_PORT = st.secrets["postgres"]["POSTGRES_PORT"]
POSTGRES_USER = st.secrets["postgres"]["POSTGRES_USER"]
POSTGRES_PASSWORD = st.secrets["postgres"]["POSTGRES_PASSWORD"]
POSTGRES_DB = st.secrets["postgres"]["POSTGRES_DB"]
DB_URL = st.secrets["postgres"]["DB_URL"]
