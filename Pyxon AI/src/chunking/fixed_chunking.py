"""
Fixed Chunking Module
Implements fixed-size chunking strategy with overlap
"""

from typing import List
from ..parser.base_parser import Chunk


class FixedChunking:
    """
    Fixed-size chunking strategy
    Best for uniform documents like reports and forms
    """
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """
        Initialize fixed chunking
        
        Args:
            chunk_size: Target size for each chunk in characters
            overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, document_id: str) -> List[Chunk]:
        """
        Split text into fixed-size chunks
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            
        Returns:
            List of Chunk objects
        """
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            # Calculate end position
            end = min(start + self.chunk_size, len(text))
            
            # Extract chunk text
            chunk_text = text[start:end]
            
            # Skip empty chunks
            if chunk_text.strip():
                # Create chunk object
                chunk = Chunk(
                    content=chunk_text,
                    chunk_id=f"{document_id}_chunk_{chunk_index}",
                    document_id=document_id,
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end,
                    metadata={
                        'strategy': 'fixed',
                        'chunk_size': self.chunk_size,
                        'overlap': self.overlap
                    }
                )
                
                chunks.append(chunk)
                chunk_index += 1
            
            # Move to next chunk with overlap
            start = end - self.overlap
            
            # Prevent infinite loop
            if start >= len(text):
                break
        
        return chunks
    
    def chunk_by_sentences(self, text: str, document_id: str) -> List[Chunk]:
        """
        Split text into chunks respecting sentence boundaries
        
        Args:
            text: Text to chunk
            document_id: Document identifier
            
        Returns:
            List of Chunk objects
        """
        import re
        
        # Split into sentences
        sentence_pattern = r'[.!?؟]\s+'
        sentences = re.split(sentence_pattern, text)
        
        chunks = []
        current_chunk = ""
        chunk_index = 0
        start_char = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            if not sentence:
                continue
            
            # Check if adding sentence exceeds chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                # Create chunk from current text
                chunk = Chunk(
                    content=current_chunk.strip(),
                    chunk_id=f"{document_id}_chunk_{chunk_index}",
                    document_id=document_id,
                    chunk_index=chunk_index,
                    start_char=start_char,
                    end_char=start_char + len(current_chunk),
                    metadata={
                        'strategy': 'fixed_sentences',
                        'chunk_size': self.chunk_size
                    }
                )
                
                chunks.append(chunk)
                chunk_index += 1
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences + " " + sentence
                start_char += len(current_chunk) - len(overlap_sentences) - len(sentence)
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add remaining chunk
        if current_chunk.strip():
            chunk = Chunk(
                content=current_chunk.strip(),
                chunk_id=f"{document_id}_chunk_{chunk_index}",
                document_id=document_id,
                chunk_index=chunk_index,
                start_char=start_char,
                end_char=start_char + len(current_chunk),
                metadata={
                    'strategy': 'fixed_sentences',
                    'chunk_size': self.chunk_size
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def _get_overlap_sentences(self, text: str) -> str:
        """
        Get last few sentences for overlap
        
        Args:
            text: Text to extract overlap from
            
        Returns:
            Overlap text
        """
        import re
        
        sentence_pattern = r'[.!?؟]\s+'
        sentences = re.split(sentence_pattern, text)
        
        # Return last 1-2 sentences for overlap
        if len(sentences) >= 2:
            return ' '.join(sentences[-2:])
        return sentences[-1] if sentences else ''
