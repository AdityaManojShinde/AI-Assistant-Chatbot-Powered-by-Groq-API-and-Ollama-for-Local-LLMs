"""
Response Formatter for AI Assistant Chatbot.

This module handles formatting and processing of AI responses,
following the Single Responsibility Principle.
"""

import re
from typing import Dict, List
from abc import ABC, abstractmethod


class ResponseFormatterInterface(ABC):
    """Interface for response formatters following the Interface Segregation Principle."""
    
    @abstractmethod
    def format_response(self, response: str) -> Dict[str, any]:
        """Format the response according to specific requirements."""
        pass


class ThinkingResponseFormatter(ResponseFormatterInterface):
    """Formatter for responses containing thinking sections."""
    
    def format_response(self, response: str) -> Dict[str, any]:
        """Format the response to separate thinking sections from main content."""
        # Find all <think></think> blocks
        think_pattern = r'<think>(.*?)</think>'
        
        # Extract thinking content
        thinking_blocks = re.findall(think_pattern, response, flags=re.DOTALL)
        
        # Remove thinking blocks from main response
        main_response = re.sub(think_pattern, '', response, flags=re.DOTALL)
        
        # Clean up any remaining <think> or </think> tags
        main_response = re.sub(r'</?think>', '', main_response)
        
        # Clean up extra whitespace
        main_response = main_response.strip()
        
        return {
            "thinking": thinking_blocks,
            "main_response": main_response
        }


class ResponseStatistics:
    """Class to calculate response statistics."""
    
    def __init__(self, response: str):
        self.response = response
    
    def get_word_count(self) -> int:
        """Get the word count of the response."""
        return len(self.response.split())
    
    def get_character_count(self) -> int:
        """Get the character count of the response."""
        return len(self.response)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get all statistics as a dictionary."""
        return {
            "word_count": self.get_word_count(),
            "character_count": self.get_character_count()
        }


class ResponseProcessor:
    """Main class for processing AI responses."""
    
    def __init__(self, formatter: ResponseFormatterInterface = None):
        self.formatter = formatter or ThinkingResponseFormatter()
    
    def process_response(self, response: str) -> Dict[str, any]:
        """Process the response using the configured formatter."""
        formatted_response = self.formatter.format_response(response)
        
        # Add statistics
        stats = ResponseStatistics(response)
        formatted_response["statistics"] = stats.get_statistics()
        
        return formatted_response
    
    def set_formatter(self, formatter: ResponseFormatterInterface) -> None:
        """Set a new formatter following the Strategy Pattern."""
        self.formatter = formatter
