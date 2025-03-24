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
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser

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
        log_info(f"Models: {response.json()}")
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

        log_info(f"Prompt: {prompt}")

        log_info(f"LLM model: {self.model}")

        chain = prompt | llm_with_structured_output

        try:
            response = chain.invoke({})

            st.write("response")
            st.write(response)

                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            response = {"error": str(e)}

        return response


    def send_request(self,
                    system_prompt: str, 
                    user_prompt: str, 
                    formatClass: type[BaseModel],
                    tools: List[Dict[str, Any]] = []) -> Tuple[Dict[str, Any], float]:
        try:
            log_info(f"Tools provided to send_request: {tools}")
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = ollama.chat(
                model=self.model, 
                messages=messages,
                tools=tools,
                format=formatClass.model_json_schema(), 
                stream=False
            )
            
            log_info(f"Response: {response}")

            validated_response = formatClass.model_validate_json(response.message.content)
            
            log_info(f"Validated response: {validated_response}")
            
            return validated_response.model_dump(), response.total_duration / 1e9
        except Exception as e:
            log_info(f"Error in send_request: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}, 0.0

    