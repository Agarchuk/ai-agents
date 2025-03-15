import streamlit as st

class App:
    def render(self):  
        pages = [
            st.Page("ui/pages/0_home.py", title="Home", icon=":material/home:"),
        ]
                
        pg = st.navigation(pages)
        pg.run()
