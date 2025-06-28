import streamlit as st
import io
from typing import Optional
import re
import PyPDF2

class DocumentProcessor:
    """Handles document text extraction from PDF and TXT files."""
    
    def extract_text(self, uploaded_file) -> Optional[str]:
        """
        Extract text from uploaded PDF or TXT file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Extracted text as string or None if extraction fails
        """
        try:
            if uploaded_file.type == "application/pdf":
                return self._extract_pdf_text(uploaded_file)
            elif uploaded_file.type == "text/plain":
                return self._extract_txt_text(uploaded_file)
            else:
                st.error(f"Unsupported file type: {uploaded_file.type}")
                return None
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return None
    
    def _extract_pdf_text(self, pdf_file) -> str:
        """Extract text from PDF file using PyPDF2."""
        try:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_parts = []
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text.strip():  # Only add non-empty text
                    text_parts.append(text)
            
            if not text_parts:
                return "Unable to extract readable text from this PDF. The PDF might be scanned or have complex formatting. Please try uploading a TXT file instead."
            
            # Join all text parts
            full_text = '\n'.join(text_parts)
            
            # Clean up the extracted text
            cleaned_text = self.clean_text(full_text)
            
            # Validate the extracted text
            if not self.validate_document(cleaned_text):
                return "The extracted text appears to be incomplete or corrupted. Please try uploading a TXT file instead."
            
            return cleaned_text
            
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}. Please try uploading a TXT file instead.")
    
    def _extract_txt_text(self, txt_file) -> str:
        """Extract text from TXT file."""
        try:
            # Read the text file
            text = txt_file.read().decode('utf-8')
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def validate_document(self, text: str) -> bool:
        """
        Validate if the extracted text is meaningful.
        
        Args:
            text: Extracted text string
            
        Returns:
            True if text is valid, False otherwise
        """
        if not text or len(text.strip()) < 50:
            return False
        
        # Check if text contains meaningful content (not just whitespace/special chars)
        meaningful_chars = sum(1 for c in text if c.isalnum())
        return meaningful_chars > 20
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess the extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace and normalize line breaks
        text = re.sub(r'\r\n|\r|\n', '\n', text)
        
        # Split into lines and clean each line
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 1:  # Only keep non-empty lines with content
                # Remove excessive spaces within the line
                line = re.sub(r'\s+', ' ', line)
                cleaned_lines.append(line)
        
        # Join lines back together
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove any remaining multiple spaces
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        
        # Remove excessive line breaks (more than 2 consecutive)
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        return cleaned_text.strip()
