"""
TXT Parser Module
Handles plain text document parsing
"""

import os
import chardet
from typing import Optional
from .base_parser import BaseParser, ParseResult, DocumentMetadata


class TXTParser(BaseParser):
    """Parser for plain text documents"""
    
    def __init__(self, language: str = 'en', preserve_diacritics: bool = True):
        """
        Initialize TXT parser
        
        Args:
            language: Document language
            preserve_diacritics: Whether to preserve Arabic diacritics
        """
        super().__init__(language, preserve_diacritics)
    
    def parse(self, file_path: str) -> ParseResult:
        """
        Parse TXT document
        
        Args:
            file_path: Path to TXT file
            
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
            
            # Detect encoding
            encoding = self._detect_encoding(file_path)
            
            # Extract text
            text = self.extract_text(file_path, encoding)
            
            # Clean text
            text = self._clean_text(text)
            
            # Calculate statistics
            stats = self._calculate_stats(text)
            
            # Get file metadata
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            # Estimate pages
            num_pages = self._estimate_pages(text)
            
            # Detect language
            detected_language = 'ar' if self.is_arabic(text) else self.language
            
            # Create metadata
            metadata = DocumentMetadata(
                document_id=document_id,
                filename=filename,
                file_type='txt',
                file_size=file_size,
                num_pages=num_pages,
                language=detected_language,
                encoding=encoding,
                total_chars=stats['total_chars'],
                total_words=stats['total_words'],
                metadata={'parser_version': '1.0.0'}
            )
            
            # Create result
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
                error=f"TXT parsing error: {str(e)}"
            )
    
    def extract_text(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Extract raw text from TXT file
        
        Args:
            file_path: Path to TXT file
            encoding: File encoding
            
        Returns:
            Extracted text
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            # Fallback to detected encoding
            encoding = self._detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                return file.read()
    
    def _detect_encoding(self, file_path: str) -> str:
        """
        Detect file encoding
        
        Args:
            file_path: Path to file
            
        Returns:
            Detected encoding
        """
        with open(file_path, 'rb') as file:
            raw_data = file.read(10000)  # Read first 10KB
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # Default to utf-8 if detection fails
            if not encoding or result['confidence'] < 0.7:
                encoding = 'utf-8'
            
            return encoding
    
    def _estimate_pages(self, text: str, lines_per_page: int = 50) -> int:
        """
        Estimate number of pages based on line count
        
        Args:
            text: Document text
            lines_per_page: Average lines per page
            
        Returns:
            Estimated page count
        """
        line_count = text.count('\n') + 1
        return max(1, line_count // lines_per_page)
