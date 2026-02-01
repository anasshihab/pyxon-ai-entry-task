"""
Base Document Parser Module
Provides abstract base class for all document parsers
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib


@dataclass
class Chunk:
    """Represents a document chunk with metadata"""
    content: str
    chunk_id: str
    document_id: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    def __post_init__(self):
        """Generate chunk hash if not provided"""
        if not self.chunk_id:
            self.chunk_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique chunk ID based on content and position"""
        content_hash = hashlib.sha256(
            f"{self.document_id}_{self.chunk_index}_{self.content[:100]}".encode()
        ).hexdigest()[:16]
        return f"chunk_{content_hash}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary"""
        return {
            'chunk_id': self.chunk_id,
            'document_id': self.document_id,
            'content': self.content,
            'chunk_index': self.chunk_index,
            'start_char': self.start_char,
            'end_char': self.end_char,
            'metadata': self.metadata,
            'embedding': self.embedding
        }


@dataclass
class DocumentMetadata:
    """Document metadata and statistics"""
    document_id: str
    filename: str
    file_type: str
    file_size: int
    num_pages: Optional[int] = None
    num_chunks: int = 0
    language: str = 'en'
    encoding: str = 'utf-8'
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: datetime = field(default_factory=datetime.now)
    chunking_strategy: str = 'auto'
    total_chars: int = 0
    total_words: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            'document_id': self.document_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'num_pages': self.num_pages,
            'num_chunks': self.num_chunks,
            'language': self.language,
            'encoding': self.encoding,
            'created_at': self.created_at.isoformat(),
            'processed_at': self.processed_at.isoformat(),
            'chunking_strategy': self.chunking_strategy,
            'total_chars': self.total_chars,
            'total_words': self.total_words,
            'metadata': self.metadata
        }


@dataclass
class ParseResult:
    """Result of document parsing operation"""
    document_id: str
    text: str
    chunks: List[Chunk]
    metadata: DocumentMetadata
    success: bool = True
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            'document_id': self.document_id,
            'text': self.text,
            'chunks': [chunk.to_dict() for chunk in self.chunks],
            'metadata': self.metadata.to_dict(),
            'success': self.success,
            'error': self.error
        }


class BaseParser(ABC):
    """Abstract base class for document parsers"""
    
    def __init__(self, language: str = 'en', preserve_diacritics: bool = True):
        """
        Initialize base parser
        
        Args:
            language: Document language ('en', 'ar', etc.)
            preserve_diacritics: Whether to preserve Arabic diacritics
        """
        self.language = language
        self.preserve_diacritics = preserve_diacritics
    
    @abstractmethod
    def parse(self, file_path: str) -> ParseResult:
        """
        Parse document and extract text
        
        Args:
            file_path: Path to document file
            
        Returns:
            ParseResult with extracted text and metadata
        """
        pass
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """
        Extract raw text from document
        
        Args:
            file_path: Path to document file
            
        Returns:
            Extracted text content
        """
        pass
    
    def _generate_document_id(self, file_path: str) -> str:
        """
        Generate unique document ID
        
        Args:
            file_path: Path to document file
            
        Returns:
            Unique document identifier
        """
        file_hash = hashlib.sha256(file_path.encode()).hexdigest()[:16]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"doc_{file_hash}_{timestamp}"
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove control characters except newlines and tabs
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        
        return text.strip()
    
    def _calculate_stats(self, text: str) -> Dict[str, int]:
        """
        Calculate text statistics
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics
        """
        return {
            'total_chars': len(text),
            'total_words': len(text.split()),
            'total_lines': text.count('\n') + 1
        }
    
    @staticmethod
    def is_arabic(text: str) -> bool:
        """
        Check if text contains Arabic characters
        
        Args:
            text: Text to check
            
        Returns:
            True if text contains Arabic
        """
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        return arabic_chars / max(len(text), 1) > 0.3
