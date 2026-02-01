"""
Source Package
Main package initialization
"""

__version__ = '1.0.0'
__author__ = 'Anas Mohammad'
__email__ = 'anas.mohammad6673332@gmail.com'

from .parser import DocumentParser
from .chunking import ChunkingEngine
from .storage import VectorStore, SQLStore
from .rag import RAGSystem
from .arabic import ArabicHandler

__all__ = [
    'DocumentParser',
    'ChunkingEngine',
    'VectorStore',
    'SQLStore',
    'RAGSystem',
    'ArabicHandler'
]
