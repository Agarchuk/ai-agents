from typing import Any, Dict, Tuple
import ollama
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from backend.config.ollama_config import OLLAMA_MODEL
from utils.logger import log_info
from typing import List
import streamlit as st
from langchain.agents import create_tool_calling_agent, AgentExecutor

class OllamaClient:
    def __init__(self):
        self.llm: ChatOllama = ChatOllama(model=OLLAMA_MODEL)

    def generate_response(self,
                          system_prompt: str,
                          user_prompt: str,
                          formatClass: type[BaseModel],
                          tools: List[Dict[str, Any]] = []) -> Tuple[Dict[str, Any], float]:

        parser = PydanticOutputParser(pydantic_object=formatClass)
        
        log_info(f"Tools provided to generate_response: {tools}")
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("placeholder", "{agent_scratchpad}"),
                ("user", user_prompt)
            ]
        ) 

        agent = create_tool_calling_agent(self.llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        
        try:
            st.write("executor")
            st.write(executor)
            response = executor.invoke({})

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
                model=OLLAMA_MODEL, 
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

    