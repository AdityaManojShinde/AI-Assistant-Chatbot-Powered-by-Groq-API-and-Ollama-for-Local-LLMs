"""
API Client for AI Assistant Chatbot.

This module handles all API communication with the backend server,
following the Single Responsibility Principle.
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class APIClientInterface(ABC):
    """Interface for API clients following the Interface Segregation Principle."""
    
    @abstractmethod
    def check_server_status(self) -> bool:
        """Check if the API server is running."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> Dict[str, Any]:
        """Get available models from the server."""
        pass
    
    @abstractmethod
    def get_response(self, input_text: str, model_name: str) -> Optional[str]:
        """Get response from the API."""
        pass


class BaseAPIClient(APIClientInterface):
    """Base API client with common functionality."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 60
    
    def check_server_status(self) -> bool:
        """Check if the API server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> Dict[str, Any]:
        """Get available models from the server."""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return self._get_fallback_models()
        except:
            return self._get_fallback_models()
    
    def _get_fallback_models(self) -> Dict[str, Any]:
        """Return fallback models if server is not available."""
        return {
            "cloud_models": [
                "qwen/qwen3-32b",
                "qwen-qwq-32b",
                "llama3-70b-8192",
                "llama-3.1-8b-instant",
                "compound-beta",
                "gemma2-9b-it",
                "mistral-saba-24b",
            ],
            "local_models": [
                "qwen3:0.6b",
                "deepseek-r1:1.5b",
            ]
        }
    
    def _handle_api_response(self, response_data: Any) -> Optional[str]:
        """Handle API response format."""
        if isinstance(response_data, dict) and "output" in response_data:
            output = response_data["output"]
            return output if isinstance(output, str) else str(output)
        else:
            return str(response_data)
    
    def _handle_request_errors(self, e: Exception) -> None:
        """Handle common request errors."""
        if isinstance(e, requests.exceptions.ConnectionError):
            st.error("❌ Connection failed. Please ensure the API server is running on localhost:8000")
        elif isinstance(e, requests.exceptions.Timeout):
            st.error("⏱️ Request timed out. The server might be busy or the model is taking longer to respond.")
        elif isinstance(e, requests.exceptions.HTTPError):
            if e.response.status_code == 500:
                error_detail = e.response.json().get('detail', 'Unknown error')
                st.error(f"🚨 Server error: {error_detail}")
            else:
                st.error(f"❌ HTTP error: {e}")
        elif isinstance(e, requests.exceptions.RequestException):
            st.error(f"❌ Request failed: {str(e)}")
        else:
            st.error(f"❌ An unexpected error occurred: {str(e)}")


class CloudAPIClient(BaseAPIClient):
    """API client for cloud-based AI models."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.endpoint = "/chat/invoke"
    
    def get_response(self, input_text: str, model_name: str) -> Optional[str]:
        """Get response from the cloud chat API."""
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{self.base_url}{self.endpoint}",
                    json={
                        "input": {
                            'question': input_text,
                            'model': model_name
                        }       
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                return self._handle_api_response(response.json())
                
        except Exception as e:
            self._handle_request_errors(e)
            return None


class LocalAPIClient(BaseAPIClient):
    """API client for local AI models."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.endpoint = "/local_chat/invoke"
        self.timeout = 120  # Longer timeout for local models
    
    def get_response(self, input_text: str, model_name: str) -> Optional[str]:
        """Get response from the local chat API."""
        try:
            with st.spinner("Processing locally..."):
                response = requests.post(
                    f"{self.base_url}{self.endpoint}",
                    json={
                        "input": {
                            'question': input_text,
                            'model': model_name
                        }       
                    },
                    timeout=self.timeout
                )
                response.raise_for_status()
                return self._handle_api_response(response.json())
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                error_detail = e.response.json().get('detail', 'Unknown error')
                if "model" in error_detail.lower():
                    st.error(f"🚨 Model error: {error_detail}")
                    st.info(f"💡 Make sure the selected model is installed in Ollama. Run `ollama pull {model_name}` to download it.")
                else:
                    st.error(f"🚨 Server error: {error_detail}")
            else:
                st.error(f"❌ HTTP error: {e}")
            return None
        except Exception as e:
            self._handle_request_errors(e)
            return None


class APIClientFactory:
    """Factory class for creating API clients following the Factory Pattern."""
    
    @staticmethod
    def create_client(client_type: str, base_url: str = "http://localhost:8000") -> APIClientInterface:
        """Create an API client based on the specified type."""
        if client_type.lower() == "cloud":
            return CloudAPIClient(base_url)
        elif client_type.lower() == "local":
            return LocalAPIClient(base_url)
        else:
            raise ValueError(f"Unknown client type: {client_type}")
