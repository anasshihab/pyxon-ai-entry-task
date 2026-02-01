"""
Unit tests for document parser
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import DocumentParser, PDFParser, DOCXParser, TXTParser
from src.parser.base_parser import Chunk, DocumentMetadata


class TestParsers:
    """Test document parsers"""
    
    def test_txt_parser_basic(self):
        """Test basic TXT parsing"""
        # Create test file
        test_file = "./data/test_basic.txt"
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("This is a test document.\nIt has multiple lines.\nFor testing purposes.")
        
        # Parse
        parser = TXTParser()
        result = parser.parse(test_file)
        
        # Assert
        assert result.success
        assert len(result.text) > 0
        assert "test document" in result.text
        
        # Cleanup
        os.remove(test_file)
    
    def test_arabic_detection(self):
        """Test Arabic language detection"""
        # Create Arabic test file
        test_file = "./data/test_arabic.txt"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("هذا نص عربي للاختبار")
        
        # Parse
        parser = TXTParser()
        result = parser.parse(test_file)
        
        # Assert
        assert result.success
        assert result.metadata.language == 'ar'
        
        # Cleanup
        os.remove(test_file)
    
    def test_chunk_creation(self):
        """Test chunk object creation"""
        chunk = Chunk(
            content="Test content",
            chunk_id="test_123",
            document_id="doc_456",
            chunk_index=0,
            start_char=0,
            end_char=12
        )
        
        assert chunk.content == "Test content"
        assert chunk.chunk_id == "test_123"
        assert chunk.document_id == "doc_456"
    
    def test_document_parser_factory(self):
        """Test DocumentParser factory selection"""
        parser = DocumentParser()
        
        # Test supported formats
        formats = parser.supported_formats()
        assert '.pdf' in formats
        assert '.docx' in formats
        assert '.txt' in formats
    
    def test_parse_with_chunking(self):
        """Test parsing with automatic chunking"""
        # Create test file
        test_file = "./data/test_chunking.txt"
        
        content = "This is a test. " * 100  # Create longer content
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Parse with chunking
        parser = DocumentParser(strategy='fixed')
        result = parser.parse_with_chunking(test_file, chunk_size=100)
        
        # Assert
        assert result.success
        assert len(result.chunks) > 0
        assert all(isinstance(chunk, Chunk) for chunk in result.chunks)
        
        # Cleanup
        os.remove(test_file)


class TestArabicSupport:
    """Test Arabic language support"""
    
    def test_diacritics_preservation(self):
        """Test diacritics preservation"""
        from src.arabic import ArabicHandler
        
        handler = ArabicHandler(preserve_diacritics=True)
        text = "بِسْمِ اللَّهِ"
        
        assert handler.has_diacritics(text)
        assert handler.count_diacritics(text) > 0
    
    def test_diacritics_removal(self):
        """Test diacritics removal"""
        from src.arabic import ArabicHandler
        
        handler = ArabicHandler()
        text = "بِسْمِ اللَّهِ"
        removed = handler.remove_diacritics(text)
        
        assert len(removed) < len(text)
        assert not handler.has_diacritics(removed)


class TestChunking:
    """Test chunking strategies"""
    
    def test_fixed_chunking(self):
        """Test fixed-size chunking"""
        from src.chunking import FixedChunking
        
        chunker = FixedChunking(chunk_size=50, overlap=10)
        text = "This is a test sentence. " * 10
        chunks = chunker.chunk(text, "doc_123")
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, Chunk) for chunk in chunks)
        assert all(len(chunk.content) <= 60 for chunk in chunks)  # chunk_size + some margin
    
    def test_dynamic_chunking(self):
        """Test dynamic chunking"""
        from src.chunking import DynamicChunking
        
        chunker = DynamicChunking(min_chunk_size=50, max_chunk_size=200)
        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        chunks = chunker.chunk(text, "doc_123")
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, Chunk) for chunk in chunks)
    
    def test_strategy_selection(self):
        """Test automatic strategy selection"""
        from src.chunking import StrategySelector
        
        selector = StrategySelector()
        
        # Uniform text
        uniform_text = "Test sentence. " * 50
        strategy1 = selector.select_strategy(uniform_text)
        
        # Variable text
        variable_text = "Short.\n\n" + ("Long sentence with lots of words. " * 10) + "\n\nShort again."
        strategy2 = selector.select_strategy(variable_text)
        
        assert strategy1 in ['fixed', 'dynamic']
        assert strategy2 in ['fixed', 'dynamic']


class TestStorage:
    """Test storage systems"""
    
    def test_vector_store_initialization(self):
        """Test vector store initialization"""
        from src.storage import VectorStore
        
        store = VectorStore(persist_directory="./data/test_vector")
        assert store is not None
    
    def test_sql_store_initialization(self):
        """Test SQL store initialization"""
        from src.storage import SQLStore
        
        store = SQLStore(db_path="./data/test.db")
        assert store is not None
        
        # Test statistics
        stats = store.get_statistics()
        assert 'total_documents' in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
