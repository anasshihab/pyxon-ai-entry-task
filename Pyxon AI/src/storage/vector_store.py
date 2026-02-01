"""
Vector Store Module
Manages ChromaDB for semantic search and retrieval
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from ..parser.base_parser import Chunk


class VectorStore:
    """
    Vector database for semantic search using ChromaDB
    """
    
    def __init__(
        self, 
        persist_directory: str = "./data/chroma_db",
        collection_name: str = "documents",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist database
            collection_name: Name of the collection
            embedding_model: Model for generating embeddings
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Create directory if not exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
    
    def add_chunks(
        self, 
        chunks: List[Chunk], 
        batch_size: int = 100
    ) -> Dict[str, int]:
        """
        Add chunks to vector store
        
        Args:
            chunks: List of Chunk objects
            batch_size: Batch size for processing
            
        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {'added': 0, 'failed': 0}
        
        added = 0
        failed = 0
        
        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            try:
                # Extract data from chunks
                ids = [chunk.chunk_id for chunk in batch]
                documents = [chunk.content for chunk in batch]
                metadatas = [self._prepare_metadata(chunk) for chunk in batch]
                
                # Generate embeddings
                embeddings = self._generate_embeddings(documents)
                
                # Add to collection
                self.collection.add(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                
                added += len(batch)
                
            except Exception as e:
                print(f"Error adding batch: {e}")
                failed += len(batch)
        
        return {'added': added, 'failed': failed}
    
    def search(
        self, 
        query: str, 
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Metadata filters
            
        Returns:
            List of matching chunks with scores
        """
        try:
            # Generate query embedding
            query_embedding = self._generate_embeddings([query])[0]
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter_dict
            )
            
            # Format results
            formatted_results = []
            
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'chunk_id': results['ids'][0][i],
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            return formatted_results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_by_document(
        self, 
        query: str, 
        document_id: str, 
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search within a specific document
        
        Args:
            query: Search query
            document_id: Document identifier
            k: Number of results
            
        Returns:
            List of matching chunks
        """
        return self.search(
            query=query,
            k=k,
            filter_dict={'document_id': document_id}
        )
    
    def get_chunk(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by ID
        
        Args:
            chunk_id: Chunk identifier
            
        Returns:
            Chunk data or None
        """
        try:
            results = self.collection.get(ids=[chunk_id])
            
            if results['ids']:
                return {
                    'chunk_id': results['ids'][0],
                    'content': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
            
            return None
            
        except Exception as e:
            print(f"Error retrieving chunk: {e}")
            return None
    
    def delete_document(self, document_id: str) -> int:
        """
        Delete all chunks from a document
        
        Args:
            document_id: Document identifier
            
        Returns:
            Number of chunks deleted
        """
        try:
            # Get all chunks for document
            results = self.collection.get(
                where={'document_id': document_id}
            )
            
            if results['ids']:
                # Delete chunks
                self.collection.delete(ids=results['ids'])
                return len(results['ids'])
            
            return 0
            
        except Exception as e:
            print(f"Error deleting document: {e}")
            return 0
    
    def count_chunks(self) -> int:
        """
        Get total number of chunks in store
        
        Returns:
            Number of chunks
        """
        try:
            return self.collection.count()
        except:
            return 0
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return embeddings.tolist()
    
    def _prepare_metadata(self, chunk: Chunk) -> Dict[str, Any]:
        """
        Prepare metadata for storage
        
        Args:
            chunk: Chunk object
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            'document_id': chunk.document_id,
            'chunk_index': chunk.chunk_index,
            'start_char': chunk.start_char,
            'end_char': chunk.end_char,
        }
        
        # Add custom metadata
        if chunk.metadata:
            for key, value in chunk.metadata.items():
                # ChromaDB only supports certain types
                if isinstance(value, (str, int, float, bool)):
                    metadata[key] = value
        
        return metadata
    
    def reset(self):
        """Reset the vector store (delete all data)"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error resetting store: {e}")
