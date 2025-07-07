"""
Sidebar component for AI Assistant Chatbot.

This module handles the sidebar interface and configuration options,
following the Single Responsibility Principle.
"""

import streamlit as st
from typing import Tuple, Dict, Any
from abc import ABC, abstractmethod
from util.config_manager import ConfigurationManager


class SidebarInterface(ABC):
    """Interface for sidebar components following the Interface Segregation Principle."""
    
    @abstractmethod
    def render(self, server_online: bool, available_models: Dict[str, Any]) -> Tuple[str, str, str]:
        """Render the sidebar and return selected options."""
        pass


class ConfigurationSidebar(SidebarInterface):
    """Sidebar component for application configuration."""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.ui_config = config_manager.get_ui_config()
    
    def render(self, server_online: bool, available_models: Dict[str, Any]) -> Tuple[str, str, str]:
        """Render the configuration sidebar."""
        with st.sidebar:
            st.markdown("### 🔧 Configuration")
            
            # Server status
            self._render_server_status(server_online)
            st.markdown("---")
            
            # Mode and model selection
            mode, selected_model = self._render_model_selection(available_models)
            st.markdown("---")
            
            # Input method selection
            input_method = self._render_input_method_selection()
            st.markdown("---")
            
            # Quick start information
            self._render_quick_start_info()
            
            return mode, selected_model, input_method
    
    def _render_server_status(self, server_online: bool) -> None:
        """Render server status indicator."""
        st.markdown("**Server Status:**")
        if server_online:
            st.markdown(
                '<div class="server-status server-online">✅ Server is online and ready</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="server-status server-offline">❌ Server is offline</div>', 
                unsafe_allow_html=True
            )
    
    def _render_model_selection(self, available_models: Dict[str, Any]) -> Tuple[str, str]:
        """Render mode and model selection."""
        # Mode selector
        mode = st.selectbox(
            "🌐 Select AI Mode:",
            ["Cloud AI", "Local AI"],
            index=0
        )
        
        # Model selector based on mode
        if mode == "Cloud AI":
            cloud_models = available_models.get("cloud_models", [])
            selected_model = st.selectbox(
                "🤖 Select Cloud Model:",
                cloud_models,
                index=0 if cloud_models else None
            )
        else:
            local_models = available_models.get("local_models", [])
            selected_model = st.selectbox(
                "🤖 Select Local Model:",
                local_models,
                index=0 if local_models else None
            )
        
        # Refresh models button
        if st.button("🔄 Refresh Models", help="Refresh the list of available models from server"):
            st.rerun()
        
        return mode, selected_model
    
    def _render_input_method_selection(self) -> str:
        """Render input method selection."""
        return st.selectbox(
            "📝 Input Method:",
            ["Text Input", "Text Area"],
            index=0
        )
    
    def _render_quick_start_info(self) -> None:
        """Render quick start information."""
        st.markdown("**Quick Start:**")
        st.markdown("""
        1. Check server status above
        2. Select your AI mode (Cloud/Local)
        3. Choose a model
        4. Select input method
        5. Start chatting!
        """)


class SidebarFactory:
    """Factory for creating sidebar components."""
    
    @staticmethod
    def create_sidebar(sidebar_type: str = "configuration", 
                      config_manager: ConfigurationManager = None) -> SidebarInterface:
        """Create a sidebar component based on type."""
        if sidebar_type.lower() == "configuration":
            if config_manager is None:
                config_manager = ConfigurationManager()
            return ConfigurationSidebar(config_manager)
        else:
            raise ValueError(f"Unknown sidebar type: {sidebar_type}")
