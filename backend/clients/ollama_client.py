from typing import Any, Dict, Tuple
import ollama
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from backend.config.ollama_config import OLLAMA_MODEL, OLLAMA_API_URL
from utils.logger import log_info
from typing import List
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
import requests

class OllamaClient:
    def __init__(self, model: str = None):
        self.model = model or OLLAMA_MODEL
        self.llm: ChatOpenAI = ChatOpenAI(
            api_key="ollama",
            model=self.model, 
            base_url= f"{OLLAMA_API_URL}/v1"
        )

    def get_models(self) -> List[str]:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        model_names = [model['model'] for model in response.json()['models']]
        return model_names

    def generate_response(self,
                          system_prompt: str,
                          user_prompt: str,
                          formatClass: type[BaseModel]) -> Tuple[Dict[str, Any], float] :

        llm_with_structured_output = self.llm.with_structured_output(formatClass.model_json_schema())        
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])

        chain = prompt | llm_with_structured_output

        try:
            response = chain.invoke({})
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            response = {"error": str(e)}

        return response
