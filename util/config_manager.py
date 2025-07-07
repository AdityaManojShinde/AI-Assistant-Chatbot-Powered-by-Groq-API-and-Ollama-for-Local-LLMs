"""
Configuration Manager for AI Assistant Chatbot.

This module handles application configuration and settings,
following the Single Responsibility Principle.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AppConfig:
    """Configuration data class for the application."""
    page_title: str = "AI Assistant Chatbot"
    layout: str = "centered"
    base_url: str = "http://localhost:8000"
    default_timeout: int = 60
    local_timeout: int = 120
    health_check_timeout: int = 5
    models_timeout: int = 10


@dataclass
class UIConfig:
    """Configuration for UI elements."""
    main_header_text: str = "🤖 AI Assistant Chatbot"
    footer_text: str = "AI Assistant Chatbot • Created by AdityaManojShinde"
    default_input_placeholder: str = "e.g., How does machine learning work?"
    textarea_placeholder: str = "e.g., Write a detailed explanation about quantum computing..."
    textarea_height: int = 100


class ConfigManagerInterface(ABC):
    """Interface for configuration managers."""
    
    @abstractmethod
    def get_app_config(self) -> AppConfig:
        """Get application configuration."""
        pass
    
    @abstractmethod
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration."""
        pass


class DefaultConfigManager(ConfigManagerInterface):
    """Default configuration manager implementation."""
    
    def __init__(self):
        self._app_config = AppConfig()
        self._ui_config = UIConfig()
    
    def get_app_config(self) -> AppConfig:
        """Get application configuration."""
        return self._app_config
    
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration."""
        return self._ui_config
    
    def update_app_config(self, **kwargs) -> None:
        """Update application configuration."""
        for key, value in kwargs.items():
            if hasattr(self._app_config, key):
                setattr(self._app_config, key, value)
    
    def update_ui_config(self, **kwargs) -> None:
        """Update UI configuration."""
        for key, value in kwargs.items():
            if hasattr(self._ui_config, key):
                setattr(self._ui_config, key, value)


class ModelConfig:
    """Configuration for AI models."""
    
    def __init__(self):
        self._cloud_models = [
            "qwen/qwen3-32b",
            "qwen-qwq-32b",
            "llama3-70b-8192",
            "llama-3.1-8b-instant",
            "compound-beta",
            "gemma2-9b-it",
            "mistral-saba-24b",
        ]
        
        self._local_models = [
            "qwen3:0.6b",
            "deepseek-r1:1.5b",
        ]
    
    def get_cloud_models(self) -> List[str]:
        """Get list of cloud models."""
        return self._cloud_models.copy()
    
    def get_local_models(self) -> List[str]:
        """Get list of local models."""
        return self._local_models.copy()
    
    def get_all_models(self) -> Dict[str, List[str]]:
        """Get all models organized by type."""
        return {
            "cloud_models": self.get_cloud_models(),
            "local_models": self.get_local_models()
        }
    
    def add_cloud_model(self, model_name: str) -> None:
        """Add a cloud model to the configuration."""
        if model_name not in self._cloud_models:
            self._cloud_models.append(model_name)
    
    def add_local_model(self, model_name: str) -> None:
        """Add a local model to the configuration."""
        if model_name not in self._local_models:
            self._local_models.append(model_name)
    
    def remove_cloud_model(self, model_name: str) -> None:
        """Remove a cloud model from the configuration."""
        if model_name in self._cloud_models:
            self._cloud_models.remove(model_name)
    
    def remove_local_model(self, model_name: str) -> None:
        """Remove a local model from the configuration."""
        if model_name in self._local_models:
            self._local_models.remove(model_name)


class ConfigurationManager:
    """Main configuration manager that coordinates all config components."""
    
    def __init__(self, config_manager: ConfigManagerInterface = None):
        self._config_manager = config_manager or DefaultConfigManager()
        self._model_config = ModelConfig()
    
    def get_app_config(self) -> AppConfig:
        """Get application configuration."""
        return self._config_manager.get_app_config()
    
    def get_ui_config(self) -> UIConfig:
        """Get UI configuration."""
        return self._config_manager.get_ui_config()
    
    def get_model_config(self) -> ModelConfig:
        """Get model configuration."""
        return self._model_config
    
    def update_app_config(self, **kwargs) -> None:
        """Update application configuration."""
        if hasattr(self._config_manager, 'update_app_config'):
            self._config_manager.update_app_config(**kwargs)
    
    def update_ui_config(self, **kwargs) -> None:
        """Update UI configuration."""
        if hasattr(self._config_manager, 'update_ui_config'):
            self._config_manager.update_ui_config(**kwargs)
