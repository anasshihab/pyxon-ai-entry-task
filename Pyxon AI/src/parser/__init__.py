"""
Document Parser Package
Main interface for document parsing
"""

from .base_parser import BaseParser, ParseResult, DocumentMetadata, Chunk
from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser
from typing import Optional
import os


class DocumentParser:
    """
    Main document parser interface
    Automatically selects appropriate parser based on file type
    """
    
    def __init__(self, language: str = 'en', preserve_diacritics: bool = True, strategy: str = 'auto'):
        """
        Initialize document parser
        
        Args:
            language: Default document language
            preserve_diacritics: Whether to preserve Arabic diacritics
            strategy: Chunking strategy ('auto', 'fixed', 'dynamic')
        """
        self.language = language
        self.preserve_diacritics = preserve_diacritics
        self.strategy = strategy
        
        # Initialize parsers
        self.parsers = {
            '.pdf': PDFParser(language, preserve_diacritics),
            '.docx': DOCXParser(language, preserve_diacritics),
            '.doc': DOCXParser(language, preserve_diacritics),
            '.txt': TXTParser(language, preserve_diacritics)
        }
    
    def parse(self, file_path: str) -> ParseResult:
        """
        Parse document using appropriate parser
        
        Args:
            file_path: Path to document file
            
        Returns:
            ParseResult with extracted content
        """
        # Get file extension
        _, ext = os.path.splitext(file_path.lower())
        
        # Select parser
        parser = self.parsers.get(ext)
        
        if not parser:
            return ParseResult(
                document_id='',
                text='',
                chunks=[],
                metadata=None,
                success=False,
                error=f"Unsupported file type: {ext}"
            )
        
        # Parse document
        return parser.parse(file_path)
    
    def parse_with_chunking(self, file_path: str, chunk_size: int = 512, overlap: int = 50):
        """
        Parse document and apply chunking
        
        Args:
            file_path: Path to document file
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            ParseResult with chunks
        """
        # Parse document first
        result = self.parse(file_path)
        
        if not result.success:
            return result
        
        # Import chunking modules
        from ..chunking import ChunkingEngine
        
        # Create chunking engine
        chunker = ChunkingEngine(strategy=self.strategy)
        
        # Apply chunking
        chunks = chunker.chunk_text(
            text=result.text,
            document_id=result.document_id,
            chunk_size=chunk_size,
            overlap=overlap
        )
        
        # Update result
        result.chunks = chunks
        result.metadata.num_chunks = len(chunks)
        result.metadata.chunking_strategy = self.strategy
        
        return result
    
    @staticmethod
    def supported_formats() -> list:
        """
        Get list of supported file formats
        
        Returns:
            List of file extensions
        """
        return ['.pdf', '.docx', '.doc', '.txt']


__all__ = [
    'DocumentParser',
    'BaseParser',
    'ParseResult',
    'DocumentMetadata',
    'Chunk',
    'PDFParser',
    'DOCXParser',
    'TXTParser'
]
