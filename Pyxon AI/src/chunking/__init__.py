"""
Chunking Package
Main interface for text chunking
"""

from .fixed_chunking import FixedChunking
from .dynamic_chunking import DynamicChunking
from .strategy_selector import StrategySelector
from typing import List
from ..parser.base_parser import Chunk


class ChunkingEngine:
    """
    Main chunking engine that manages different strategies
    """
    
    def __init__(self, strategy: str = 'auto', chunk_size: int = 512, overlap: int = 50):
        """
        Initialize chunking engine
        
        Args:
            strategy: Chunking strategy ('auto', 'fixed', 'dynamic')
            chunk_size: Target chunk size (for fixed strategy)
            overlap: Overlap between chunks (for fixed strategy)
        """
        self.strategy = strategy
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        # Initialize chunking strategies
        self.fixed_chunker = FixedChunking(chunk_size, overlap)
        self.dynamic_chunker = DynamicChunking(
            min_chunk_size=chunk_size // 2,
            max_chunk_size=chunk_size * 2
        )
        self.strategy_selector = StrategySelector()
    
    def chunk_text(
        self, 
        text: str, 
        document_id: str, 
        chunk_size: int = None,
        overlap: int = None
    ) -> List[Chunk]:
        """
        Chunk text using selected strategy
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            chunk_size: Override default chunk size
            overlap: Override default overlap
            
        Returns:
            List of Chunk objects
        """
        # Use provided parameters or defaults
        chunk_size = chunk_size or self.chunk_size
        overlap = overlap or self.overlap
        
        # Determine strategy
        if self.strategy == 'auto':
            selected_strategy = self.strategy_selector.select_strategy(text)
        else:
            selected_strategy = self.strategy
        
        # Apply chunking
        if selected_strategy == 'fixed':
            return self.fixed_chunker.chunk_by_sentences(text, document_id)
        else:
            return self.dynamic_chunker.chunk(text, document_id)
    
    def chunk_with_analysis(self, text: str, document_id: str) -> dict:
        """
        Chunk text and return analysis
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            
        Returns:
            Dictionary with chunks and analysis
        """
        # Analyze document
        analysis = self.strategy_selector.analyze_document(text)
        
        # Select strategy
        selected_strategy = self.strategy_selector.select_strategy(text)
        
        # Chunk text
        chunks = self.chunk_text(text, document_id)
        
        return {
            'chunks': chunks,
            'strategy_used': selected_strategy,
            'analysis': analysis,
            'num_chunks': len(chunks)
        }


__all__ = [
    'ChunkingEngine',
    'FixedChunking',
    'DynamicChunking',
    'StrategySelector'
]
