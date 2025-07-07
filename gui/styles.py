"""
Styling components for AI Assistant Chatbot.

This module contains all CSS styles and styling-related functionality,
following the Single Responsibility Principle.
"""

import streamlit as st
from abc import ABC, abstractmethod


class StyleManagerInterface(ABC):
    """Interface for style managers following the Interface Segregation Principle."""
    
    @abstractmethod
    def apply_styles(self) -> None:
        """Apply styles to the application."""
        pass


class WhatsAppStyleManager(StyleManagerInterface):
    """Style manager for WhatsApp-style interface with blue color scheme."""
    
    def __init__(self):
        self.css_styles = self._get_css_styles()
    
    def apply_styles(self) -> None:
        """Apply WhatsApp-style CSS to the Streamlit application."""
        st.markdown(self.css_styles, unsafe_allow_html=True)
    
    def _get_css_styles(self) -> str:
        """Get the complete CSS styles for the application."""
        return """
<style>
.main-header {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 2rem;
    color: #1f2937;
}

.stButton > button {
    border-radius: 8px;
    border: none;
    padding: 0.75rem 2rem;
    font-weight: 500;
    font-size: 1rem;
    width: 100%;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.mode-indicator {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.cloud-mode {
    background-color: #dbeafe;
    color: #1e40af;
}

.local-mode {
    background-color: #fef3c7;
    color: #b45309;
}

.stSpinner > div {
    border-top-color: #3b82f6 !important;
}

.footer {
    text-align: center;
    color: #6b7280;
    font-size: 0.875rem;
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
}

.response-container {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.thinking-container {
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #6b7280;
}

.thinking-text {
    color: #6b7280;
    font-style: italic;
    font-size: 0.95rem;
}

.main-response {
    color: #1f2937;
    line-height: 1.6;
}

.server-status {
    padding: 0.5rem 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    text-align: center;
}

.server-online {
    background-color: #d1fae5;
    color: #065f46;
    border: 1px solid #a7f3d0;
}

.server-offline {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
}

.model-refresh {
    font-size: 0.875rem;
    color: #6b7280;
    margin-top: 0.5rem;
}

/* Improve markdown rendering */
.main-response h1, .main-response h2, .main-response h3 {
    color: #1f2937;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

.main-response h1 {
    font-size: 1.5rem;
    font-weight: 600;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5rem;
}

.main-response h2 {
    font-size: 1.25rem;
    font-weight: 600;
}

.main-response h3 {
    font-size: 1.125rem;
    font-weight: 600;
}

.main-response ul, .main-response ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}

.main-response li {
    margin-bottom: 0.25rem;
}

.main-response p {
    margin-bottom: 1rem;
}

.main-response blockquote {
    border-left: 4px solid #e5e7eb;
    margin-left: 0;
    padding-left: 1rem;
    color: #6b7280;
    font-style: italic;
}

.main-response code {
    background-color: #f3f4f6;
    color: #dc2626;
    padding: 0.125rem 0.25rem;
    border-radius: 0.25rem;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875rem;
}

.main-response pre {
    background-color: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1rem 0;
}

.main-response pre code {
    background-color: transparent;
    color: #f9fafb;
    padding: 0;
}

.main-response table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.main-response th, .main-response td {
    border: 1px solid #e5e7eb;
    padding: 0.5rem;
    text-align: left;
}

.main-response th {
    background-color: #f9fafb;
    font-weight: 600;
}

.main-response strong {
    font-weight: 600;
    color: #1f2937;
}

.main-response em {
    font-style: italic;
    color: #4b5563;
}

.chat-container {
    max-width: 800px;
    margin: 0 auto;
}
</style>
"""


class StyleFactory:
    """Factory for creating style managers."""
    
    @staticmethod
    def create_style_manager(style_type: str = "whatsapp") -> StyleManagerInterface:
        """Create a style manager based on type."""
        if style_type.lower() == "whatsapp":
            return WhatsAppStyleManager()
        else:
            raise ValueError(f"Unknown style type: {style_type}")
