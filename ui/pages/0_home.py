import streamlit as st

from backend.clients.ollama_client import OllamaClient

if __name__ == "__page__":
    st.title("Home")
    st.write("Welcome to the home page")    

    ollama_client = OllamaClient()
    models = ollama_client.get_models()
    st.write(models)

    if st.button("Get Models"):
        models = ollama_client.get_models()
        st.write(models)

    if st.button("Generate"):
        response = ollama_client.send_request("You are a helpful assistant.", "What is the capital of France?")
        st.write(response)

