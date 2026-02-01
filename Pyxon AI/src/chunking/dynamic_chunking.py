"""
Dynamic Chunking Module
Implements semantic-aware dynamic chunking
"""

from typing import List
import re
from ..parser.base_parser import Chunk


class DynamicChunking:
    """
    Dynamic chunking strategy based on semantic boundaries
    Best for documents with varying structure like books and articles
    """
    
    def __init__(self, min_chunk_size: int = 256, max_chunk_size: int = 1024):
        """
        Initialize dynamic chunking
        
        Args:
            min_chunk_size: Minimum chunk size
            max_chunk_size: Maximum chunk size
        """
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str, document_id: str) -> List[Chunk]:
        """
        Split text into semantically coherent chunks
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            
        Returns:
            List of Chunk objects
        """
        # First, try to split by paragraphs
        paragraphs = self._split_paragraphs(text)
        
        chunks = []
        current_chunk = ""
        chunk_index = 0
        start_char = 0
        current_pos = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            
            if not paragraph:
                current_pos += 1
                continue
            
            # If paragraph itself is too large, split it further
            if len(paragraph) > self.max_chunk_size:
                # Save current chunk if exists
                if current_chunk:
                    chunk = self._create_chunk(
                        current_chunk, document_id, chunk_index, start_char
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    current_chunk = ""
                
                # Split large paragraph by sentences
                sentence_chunks = self._chunk_large_paragraph(
                    paragraph, document_id, chunk_index, current_pos
                )
                chunks.extend(sentence_chunks)
                chunk_index += len(sentence_chunks)
                start_char = current_pos + len(paragraph)
            
            # If adding paragraph exceeds max size, save current chunk
            elif len(current_chunk) + len(paragraph) > self.max_chunk_size and current_chunk:
                if len(current_chunk) >= self.min_chunk_size:
                    chunk = self._create_chunk(
                        current_chunk, document_id, chunk_index, start_char
                    )
                    chunks.append(chunk)
                    chunk_index += 1
                    start_char = current_pos
                    current_chunk = paragraph
                else:
                    # Current chunk too small, add paragraph anyway
                    current_chunk += "\n\n" + paragraph
            
            # Add paragraph to current chunk
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            
            current_pos += len(paragraph) + 2  # +2 for \n\n
        
        # Add remaining chunk
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunk = self._create_chunk(
                current_chunk, document_id, chunk_index, start_char
            )
            chunks.append(chunk)
        
        return chunks
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs
        
        Args:
            text: Text to split
            
        Returns:
            List of paragraphs
        """
        # Split by double newlines or multiple spaces
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _chunk_large_paragraph(
        self, paragraph: str, document_id: str, start_index: int, start_char: int
    ) -> List[Chunk]:
        """
        Split large paragraph into sentence-based chunks
        
        Args:
            paragraph: Large paragraph text
            document_id: Document identifier
            start_index: Starting chunk index
            start_char: Starting character position
            
        Returns:
            List of chunks
        """
        # Split by sentences (Arabic and English)
        sentence_pattern = r'[.!?؟]\s+'
        sentences = re.split(sentence_pattern, paragraph)
        
        chunks = []
        current_chunk = ""
        chunk_index = start_index
        chunk_start = start_char
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            if not sentence:
                continue
            
            # If adding sentence exceeds max size
            if len(current_chunk) + len(sentence) > self.max_chunk_size and current_chunk:
                chunk = self._create_chunk(
                    current_chunk, document_id, chunk_index, chunk_start
                )
                chunks.append(chunk)
                chunk_index += 1
                chunk_start += len(current_chunk)
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add remaining chunk
        if current_chunk:
            chunk = self._create_chunk(
                current_chunk, document_id, chunk_index, chunk_start
            )
            chunks.append(chunk)
        
        return chunks
    
    def _create_chunk(
        self, content: str, document_id: str, chunk_index: int, start_char: int
    ) -> Chunk:
        """
        Create a Chunk object
        
        Args:
            content: Chunk content
            document_id: Document identifier
            chunk_index: Chunk index
            start_char: Starting character position
            
        Returns:
            Chunk object
        """
        return Chunk(
            content=content.strip(),
            chunk_id=f"{document_id}_chunk_{chunk_index}",
            document_id=document_id,
            chunk_index=chunk_index,
            start_char=start_char,
            end_char=start_char + len(content),
            metadata={
                'strategy': 'dynamic',
                'semantic_boundary': True
            }
        )
    
    def chunk_by_topics(self, text: str, document_id: str) -> List[Chunk]:
        """
        Advanced chunking based on topic segmentation
        (Simplified version - can be enhanced with ML models)
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            
        Returns:
            List of chunks
        """
        # For now, use paragraph-based chunking
        # In production, this could use topic modeling (LDA, BERT-based)
        return self.chunk(text, document_id)
