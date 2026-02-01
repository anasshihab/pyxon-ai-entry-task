"""
PDF Parser Module
Handles PDF document parsing and text extraction
"""

import os
from typing import Optional
import PyPDF2
from .base_parser import BaseParser, ParseResult, DocumentMetadata
from datetime import datetime


class PDFParser(BaseParser):
    """Parser for PDF documents"""
    
    def __init__(self, language: str = 'en', preserve_diacritics: bool = True):
        """
        Initialize PDF parser
        
        Args:
            language: Document language
            preserve_diacritics: Whether to preserve Arabic diacritics
        """
        super().__init__(language, preserve_diacritics)
    
    def parse(self, file_path: str) -> ParseResult:
        """
        Parse PDF document
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            ParseResult with extracted content
        """
        try:
            # Validate file
            if not os.path.exists(file_path):
                return ParseResult(
                    document_id='',
                    text='',
                    chunks=[],
                    metadata=None,
                    success=False,
                    error=f"File not found: {file_path}"
                )
            
            # Generate document ID
            document_id = self._generate_document_id(file_path)
            
            # Extract text
            text = self.extract_text(file_path)
            
            # Clean text
            text = self._clean_text(text)
            
            # Calculate statistics
            stats = self._calculate_stats(text)
            
            # Get file metadata
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            # Count pages
            num_pages = self._count_pages(file_path)
            
            # Detect language
            detected_language = 'ar' if self.is_arabic(text) else self.language
            
            # Create metadata
            metadata = DocumentMetadata(
                document_id=document_id,
                filename=filename,
                file_type='pdf',
                file_size=file_size,
                num_pages=num_pages,
                language=detected_language,
                total_chars=stats['total_chars'],
                total_words=stats['total_words'],
                metadata={'parser_version': '1.0.0'}
            )
            
            # Create result (chunks will be added by chunking engine)
            result = ParseResult(
                document_id=document_id,
                text=text,
                chunks=[],
                metadata=metadata,
                success=True
            )
            
            return result
            
        except Exception as e:
            return ParseResult(
                document_id='',
                text='',
                chunks=[],
                metadata=None,
                success=False,
                error=f"PDF parsing error: {str(e)}"
            )
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract raw text from PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text_parts = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                    continue
        
        return '\n'.join(text_parts)
    
    def _count_pages(self, file_path: str) -> int:
        """
        Count number of pages in PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Number of pages
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except:
            return 0
    
    def extract_metadata(self, file_path: str) -> dict:
        """
        Extract PDF metadata
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary with PDF metadata
        """
        metadata = {}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_metadata = pdf_reader.metadata
                
                if pdf_metadata:
                    metadata = {
                        'title': pdf_metadata.get('/Title', ''),
                        'author': pdf_metadata.get('/Author', ''),
                        'subject': pdf_metadata.get('/Subject', ''),
                        'creator': pdf_metadata.get('/Creator', ''),
                        'producer': pdf_metadata.get('/Producer', ''),
                        'creation_date': pdf_metadata.get('/CreationDate', '')
                    }
        except Exception as e:
            print(f"Warning: Could not extract PDF metadata: {e}")
        
        return metadata
