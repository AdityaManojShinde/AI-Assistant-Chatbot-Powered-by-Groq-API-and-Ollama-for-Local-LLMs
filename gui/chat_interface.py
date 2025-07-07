"""
Chat interface component for AI Assistant Chatbot.

This module handles the main chat interface and user interactions,
following the Single Responsibility Principle.
"""

import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod
from util.config_manager import ConfigurationManager
from util.response_formatter import ResponseProcessor
from util.pdf_generator import PDFGeneratorFactory


class ChatInterfaceInterface(ABC):
    """Interface for chat interface components."""
    
    @abstractmethod
    def render_input_section(self, input_method: str) -> Optional[str]:
        """Render the input section and return user input."""
        pass
    
    @abstractmethod
    def render_response_section(self, response: str, question: str, model_name: str) -> None:
        """Render the response section."""
        pass


class MainChatInterface(ChatInterfaceInterface):
    """Main chat interface component."""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.ui_config = config_manager.get_ui_config()
        self.response_processor = ResponseProcessor()
        self.pdf_generator = PDFGeneratorFactory.create_generator("markdown")
    
    def render_header(self) -> None:
        """Render the main header."""
        st.markdown(
            f'<h1 class="main-header">{self.ui_config.main_header_text}</h1>', 
            unsafe_allow_html=True
        )
    
    def render_mode_indicator(self, mode: str, selected_model: str) -> None:
        """Render the current mode and model indicator."""
        if mode == "Cloud AI":
            st.markdown(
                f'<div class="mode-indicator cloud-mode">🌐 Cloud AI Mode - {selected_model}</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="mode-indicator local-mode">💻 Local AI Mode - {selected_model}</div>', 
                unsafe_allow_html=True
            )
    
    def render_input_section(self, input_method: str) -> Optional[str]:
        """Render the input section based on the selected method."""
        if input_method == "Text Input":
            return st.text_input(
                "Ask me anything:",
                placeholder=self.ui_config.default_input_placeholder,
                key="chat_input"
            )
        else:
            return st.text_area(
                "Ask me anything:",
                placeholder=self.ui_config.textarea_placeholder,
                key="chat_textarea",
                height=self.ui_config.textarea_height
            )
    
    def render_action_buttons(self, server_online: bool) -> tuple:
        """Render the action buttons and return their states."""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            generate_button = st.button("Ask Assistant", type="primary", disabled=not server_online)
        
        with col2:
            clear_button = st.button("🗑️ Clear")
            if clear_button:
                self._clear_session_state()
                st.rerun()
        
        return generate_button, clear_button
    
    def render_response_section(self, response: str, question: str, model_name: str) -> None:
        """Render the response section with thinking and main content."""
        # Process the response
        formatted_response = self.response_processor.process_response(response)
        
        # Display thinking sections if they exist
        self._render_thinking_sections(formatted_response.get("thinking", []))
        
        # Display main response
        self._render_main_response(formatted_response["main_response"], model_name)
        
        # Action buttons for response
        self._render_response_actions(formatted_response["main_response"], question, model_name, response)
        
        # Response statistics
        self._render_response_statistics(formatted_response.get("statistics", {}), model_name)
    
    def render_footer(self) -> None:
        """Render the footer."""
        st.markdown(
            f'<div class="footer">{self.ui_config.footer_text}</div>',
            unsafe_allow_html=True
        )
    
    def _render_thinking_sections(self, thinking_blocks: list) -> None:
        """Render thinking sections if they exist."""
        if thinking_blocks:
            for i, thinking in enumerate(thinking_blocks):
                st.markdown('<div class="thinking-container">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="thinking-text">💭 <strong>Thinking {i+1}:</strong><br>{thinking.strip()}</div>', 
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_main_response(self, main_response: str, model_name: str) -> None:
        """Render the main response content."""
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown(f"**🤖 Assistant ({model_name}):**")
        st.markdown(main_response)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_response_actions(self, main_response: str, question: str, model_name: str, full_response: str) -> None:
        """Render action buttons for the response."""
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_pdf_download_button(main_response, question, model_name, full_response)
        
        with col2:
            self._render_copy_button(full_response)
    
    def _render_pdf_download_button(self, main_response: str, question: str, model_name: str, full_response: str) -> None:
        """Render PDF download button."""
        try:
            pdf_bytes = self.pdf_generator.generate_pdf(main_response, question, model_name)
            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name=f"AI_Response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key=f"pdf_download_{hash(full_response)}"
            )
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            # Fallback to text download
            st.download_button(
                label="📥 Download Text",
                data=full_response,
                file_name=f"response_{model_name}_{question[:15].replace(' ', '_')}.txt",
                mime="text/plain",
                key=f"text_download_{hash(full_response)}"
            )
    
    def _render_copy_button(self, response: str) -> None:
        """Render copy to clipboard button."""
        if st.button("📋 Copy Response", key=f"copy_button_{hash(response)}"):
            st.session_state.copied_text = response
            st.success("Response copied to session!")
    
    def _render_response_statistics(self, statistics: Dict[str, Any], model_name: str) -> None:
        """Render response statistics in an expander."""
        with st.expander("📊 Response Statistics"):
            if statistics:
                st.metric("Word Count", statistics.get("word_count", 0))
                st.metric("Character Count", statistics.get("character_count", 0))
            st.metric("Model Used", model_name)
    
    def _clear_session_state(self) -> None:
        """Clear session state for responses."""
        for key in list(st.session_state.keys()):
            if key.startswith(('current_response', 'current_question', 'current_model', 'copied_text')):
                del st.session_state[key]


class ChatInterfaceFactory:
    """Factory for creating chat interface components."""
    
    @staticmethod
    def create_chat_interface(interface_type: str = "main", 
                             config_manager: ConfigurationManager = None) -> ChatInterfaceInterface:
        """Create a chat interface component based on type."""
        if interface_type.lower() == "main":
            if config_manager is None:
                config_manager = ConfigurationManager()
            return MainChatInterface(config_manager)
        else:
            raise ValueError(f"Unknown interface type: {interface_type}")
