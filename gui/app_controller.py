"""
Application Controller for AI Assistant Chatbot.

This module orchestrates all components and manages the application state,
following the Single Responsibility Principle and acting as the main coordinator.
"""

import streamlit as st
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from util.config_manager import ConfigurationManager
from util.api_client import APIClientFactory, APIClientInterface
from gui.styles import StyleFactory
from gui.sidebar import SidebarFactory
from gui.chat_interface import ChatInterfaceFactory


class ApplicationControllerInterface(ABC):
    """Interface for application controllers."""
    
    @abstractmethod
    def run(self) -> None:
        """Run the application."""
        pass


class SessionStateManager:
    """Manages Streamlit session state following the Single Responsibility Principle."""
    
    @staticmethod
    def initialize_session_state() -> None:
        """Initialize session state variables if they don't exist."""
        if 'current_response' not in st.session_state:
            st.session_state.current_response = None
        if 'current_question' not in st.session_state:
            st.session_state.current_question = None
        if 'current_model' not in st.session_state:
            st.session_state.current_model = None
    
    @staticmethod
    def store_response(response: str, question: str, model: str) -> None:
        """Store response data in session state."""
        st.session_state.current_response = response
        st.session_state.current_question = question
        st.session_state.current_model = model
    
    @staticmethod
    def has_current_response() -> bool:
        """Check if there's a current response in session state."""
        return (hasattr(st.session_state, 'current_response') and 
                st.session_state.current_response is not None)
    
    @staticmethod
    def get_current_response_data() -> tuple:
        """Get current response data from session state."""
        return (
            st.session_state.current_response,
            st.session_state.current_question,
            st.session_state.current_model
        )


class MainApplicationController(ApplicationControllerInterface):
    """Main application controller that orchestrates all components."""
    
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.session_manager = SessionStateManager()
        
        # Initialize components
        self._initialize_components()
        self._configure_page()
    
    def _initialize_components(self) -> None:
        """Initialize all application components."""
        # Create style manager and apply styles
        self.style_manager = StyleFactory.create_style_manager("whatsapp")
        self.style_manager.apply_styles()
        
        # Create GUI components
        self.sidebar = SidebarFactory.create_sidebar("configuration", self.config_manager)
        self.chat_interface = ChatInterfaceFactory.create_chat_interface("main", self.config_manager)
        
        # Create API clients
        self.cloud_client = APIClientFactory.create_client("cloud")
        self.local_client = APIClientFactory.create_client("local")
    
    def _configure_page(self) -> None:
        """Configure Streamlit page settings."""
        app_config = self.config_manager.get_app_config()
        st.set_page_config(
            page_title=app_config.page_title,
            layout=app_config.layout
        )
    
    def run(self) -> None:
        """Run the main application."""
        # Initialize session state
        self.session_manager.initialize_session_state()
        
        # Render header
        self.chat_interface.render_header()
        
        # Check server status and get models
        server_online = self._check_server_status()
        available_models = self._get_available_models()
        
        # Render sidebar and get configuration
        mode, selected_model, input_method = self.sidebar.render(server_online, available_models)
        
        # Main chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display current mode and model
        self.chat_interface.render_mode_indicator(mode, selected_model)
        
        # Render input section
        input_text = self.chat_interface.render_input_section(input_method)
        
        # Render action buttons
        generate_button, clear_button = self.chat_interface.render_action_buttons(server_online)
        
        # Process user request
        self._process_user_request(generate_button, input_text, mode, selected_model)
        
        # Display response if available
        self._display_current_response()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render footer
        self.chat_interface.render_footer()
    
    def _check_server_status(self) -> bool:
        """Check if the API server is running."""
        return self.cloud_client.check_server_status()
    
    def _get_available_models(self) -> Dict[str, Any]:
        """Get available models from the server."""
        return self.cloud_client.get_available_models()
    
    def _process_user_request(self, generate_button: bool, input_text: str, 
                             mode: str, selected_model: str) -> None:
        """Process user request and get AI response."""
        if generate_button:
            if input_text and input_text.strip():
                # Select appropriate API client
                client = self._get_api_client(mode)
                
                # Get response from API
                response = client.get_response(input_text, selected_model)
                
                if response:
                    # Store response in session state
                    self.session_manager.store_response(response, input_text, selected_model)
            else:
                st.warning("⚠️ Please enter a question or prompt.")
    
    def _get_api_client(self, mode: str) -> APIClientInterface:
        """Get the appropriate API client based on mode."""
        if mode == "Cloud AI":
            return self.cloud_client
        else:
            return self.local_client
    
    def _display_current_response(self) -> None:
        """Display the current response if available."""
        if self.session_manager.has_current_response():
            response, question, model = self.session_manager.get_current_response_data()
            self.chat_interface.render_response_section(response, question, model)


class ApplicationControllerFactory:
    """Factory for creating application controllers."""
    
    @staticmethod
    def create_controller(controller_type: str = "main") -> ApplicationControllerInterface:
        """Create an application controller based on type."""
        if controller_type.lower() == "main":
            return MainApplicationController()
        else:
            raise ValueError(f"Unknown controller type: {controller_type}")


def main():
    """Main entry point for the application."""
    controller = ApplicationControllerFactory.create_controller("main")
    controller.run()


if __name__ == "__main__":
    main()
