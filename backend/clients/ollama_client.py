from typing import Any, Dict, Tuple
import json

import requests
from backend.config.ollama_config import OLLAMA_API_URL
from utils.logger import log_info
from typing import List

class OllamaClient:

    def get_models(self) -> List[str]:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags")
        response.raise_for_status()
        log_info(f"Models: {response.json()}")
        return response.json()

    def send_request(self, system_prompt: str, user_prompt: str) -> Tuple[Dict[str, Any], float]:
        payload = {
            "model": "qwen2.5:0.5b",
            "system": system_prompt,
            "prompt": user_prompt,
            "format": "json",
            "stream": False
        }
        try:
            response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            response = json.loads(result.get("response", "{}"))
            log_info(f"Response: {response}")
            return response
            
        except requests.exceptions.RequestException as e:
            return {"error": f"HTTP error: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    