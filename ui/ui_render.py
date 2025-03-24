import streamlit as st

from ui.pages.login import LoginPage
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService

class App:
    def render(self):  
        session_token =  SessionStateService().get(SessionConfig.ACCESS_TOKEN, None) 

        if session_token is None:
            LoginPage().display()
        else:
            pages = [
                st.Page("ui/pages/0_home.py", title="Home", icon=":material/home:"),
                st.Page("ui/pages/1_cleaning_agent.py", title="Cleaning Agent", icon=":material/cleaning_bucket:"),
            ]
                
            pg = st.navigation(pages)
            pg.run()
