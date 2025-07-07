"""
PDF Generator for AI Assistant Chatbot.

This module handles PDF generation from markdown content,
following the Single Responsibility Principle.
"""

import io
import markdown
import streamlit as st
from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from abc import ABC, abstractmethod


class PDFGeneratorInterface(ABC):
    """Interface for PDF generators following the Interface Segregation Principle."""
    
    @abstractmethod
    def generate_pdf(self, content: str, question: str, model_name: str) -> bytes:
        """Generate PDF from content."""
        pass


class StyleManager:
    """Manages PDF styles following the Single Responsibility Principle."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def get_title_style(self) -> ParagraphStyle:
        """Get title style for PDF."""
        return ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            textColor=HexColor('#1f2937'),
            alignment=TA_CENTER
        )
    
    def get_heading1_style(self) -> ParagraphStyle:
        """Get heading 1 style for PDF."""
        return ParagraphStyle(
            'CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#1f2937'),
            leftIndent=0
        )
    
    def get_heading2_style(self) -> ParagraphStyle:
        """Get heading 2 style for PDF."""
        return ParagraphStyle(
            'CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=16,
            textColor=HexColor('#374151'),
            leftIndent=0
        )
    
    def get_heading3_style(self) -> ParagraphStyle:
        """Get heading 3 style for PDF."""
        return ParagraphStyle(
            'CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=HexColor('#4b5563'),
            leftIndent=0
        )
    
    def get_body_style(self) -> ParagraphStyle:
        """Get body text style for PDF."""
        return ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            textColor=HexColor('#1f2937'),
            leading=16
        )
    
    def get_code_style(self) -> ParagraphStyle:
        """Get code style for PDF."""
        return ParagraphStyle(
            'CustomCode',
            parent=self.styles['Code'],
            fontSize=10,
            spaceAfter=12,
            spaceBefore=6,
            textColor=HexColor('#dc2626'),
            backColor=HexColor('#f3f4f6'),
            borderColor=HexColor('#e5e7eb'),
            borderWidth=1,
            borderPadding=8
        )
    
    def get_quote_style(self) -> ParagraphStyle:
        """Get quote style for PDF."""
        return ParagraphStyle(
            'CustomQuote',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            leftIndent=20,
            textColor=HexColor('#6b7280'),
            fontName='Times-Italic',
            borderColor=HexColor('#e5e7eb'),
            borderWidth=0,
            leftBorderColor=HexColor('#9ca3af'),
            leftBorderWidth=4,
            borderPadding=10
        )


class MarkdownToPDFGenerator(PDFGeneratorInterface):
    """Generates PDF from markdown content."""
    
    def __init__(self):
        self.style_manager = StyleManager()
    
    def generate_pdf(self, markdown_content: str, question: str, model_name: str) -> bytes:
        """Convert markdown content to a properly formatted PDF."""
        try:
            # Create a buffer to hold the PDF
            buffer = io.BytesIO()
            
            # Create the PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build the story (content) for the PDF
            story = self._build_story(markdown_content, question, model_name)
            
            # Build the PDF
            doc.build(story)
            
            # Get the PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            return self._create_fallback_pdf(markdown_content, question, model_name)
    
    def _build_story(self, markdown_content: str, question: str, model_name: str) -> list:
        """Build the PDF story content."""
        story = []
        
        # Add title and metadata
        story.extend(self._add_header(question, model_name))
        
        # Convert markdown to HTML and process
        html_content = markdown.markdown(
            markdown_content,
            extensions=['codehilite', 'fenced_code', 'tables', 'toc']
        )
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Process each element
        story.extend(self._process_html_elements(soup))
        
        # If no structured content was found, add raw text
        if len(story) <= 5:  # Only metadata was added
            story.extend(self._process_raw_markdown(markdown_content))
        
        return story
    
    def _add_header(self, question: str, model_name: str) -> list:
        """Add header information to the PDF."""
        header_elements = []
        
        # Add title
        header_elements.append(Paragraph("AI Assistant Response", self.style_manager.get_title_style()))
        header_elements.append(Spacer(1, 20))
        
        # Add metadata
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body_style = self.style_manager.get_body_style()
        
        header_elements.append(Paragraph(f"<b>Generated:</b> {current_time}", body_style))
        header_elements.append(Paragraph(f"<b>Model:</b> {model_name}", body_style))
        header_elements.append(Paragraph(f"<b>Question:</b> {question}", body_style))
        header_elements.append(Spacer(1, 20))
        
        return header_elements

    def _process_html_elements(self, soup) -> list:
        """Process HTML elements and convert to PDF elements."""
        elements = []

        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'pre', 'code', 'blockquote', 'ul', 'ol', 'li', 'table', 'strong', 'em']):
            if element.name == 'h1':
                elements.append(Paragraph(element.get_text(), self.style_manager.get_heading1_style()))
            elif element.name == 'h2':
                elements.append(Paragraph(element.get_text(), self.style_manager.get_heading2_style()))
            elif element.name == 'h3':
                elements.append(Paragraph(element.get_text(), self.style_manager.get_heading3_style()))
            elif element.name == 'p':
                # Handle paragraphs with potential inline formatting
                text = str(element)
                text = text.replace('<p>', '').replace('</p>', '')
                text = text.replace('<strong>', '<b>').replace('</strong>', '</b>')
                text = text.replace('<em>', '<i>').replace('</em>', '</i>')
                elements.append(Paragraph(text, self.style_manager.get_body_style()))
            elif element.name == 'pre':
                # Handle code blocks
                code_text = element.get_text()
                elements.append(Preformatted(code_text, self.style_manager.get_code_style()))
            elif element.name == 'code' and element.parent.name != 'pre':
                # Handle inline code
                elements.append(Paragraph(f"<font face='Courier'>{element.get_text()}</font>", self.style_manager.get_body_style()))
            elif element.name == 'blockquote':
                elements.append(Paragraph(element.get_text(), self.style_manager.get_quote_style()))
            elif element.name in ['ul', 'ol']:
                # Handle lists
                for li in element.find_all('li'):
                    bullet = "• " if element.name == 'ul' else "1. "
                    elements.append(Paragraph(f"{bullet}{li.get_text()}", self.style_manager.get_body_style()))
                elements.append(Spacer(1, 6))

        return elements

    def _process_raw_markdown(self, markdown_content: str) -> list:
        """Process raw markdown content when structured parsing fails."""
        elements = []

        # Split content into paragraphs
        paragraphs = markdown_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Handle basic markdown formatting
                para = para.replace('**', '<b>').replace('**', '</b>')
                para = para.replace('*', '<i>').replace('*', '</i>')
                elements.append(Paragraph(para, self.style_manager.get_body_style()))

        return elements

    def _create_fallback_pdf(self, markdown_content: str, question: str, model_name: str) -> bytes:
        """Create a simple fallback PDF when main generation fails."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("AI Assistant Response", styles['Title']),
            Spacer(1, 20),
            Paragraph(f"Model: {model_name}", styles['Normal']),
            Paragraph(f"Question: {question}", styles['Normal']),
            Spacer(1, 20),
            Paragraph("Response:", styles['Heading2']),
            Paragraph(markdown_content, styles['Normal'])
        ]
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes


class PDFGeneratorFactory:
    """Factory for creating PDF generators."""

    @staticmethod
    def create_generator(generator_type: str = "markdown") -> PDFGeneratorInterface:
        """Create a PDF generator based on type."""
        if generator_type.lower() == "markdown":
            return MarkdownToPDFGenerator()
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
