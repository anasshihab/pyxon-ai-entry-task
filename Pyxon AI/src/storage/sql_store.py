"""
SQL Store Module
Manages SQLite database for structured metadata and queries
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..parser.base_parser import DocumentMetadata, Chunk


class SQLStore:
    """
    SQL database for structured data and metadata
    """
    
    def __init__(self, db_path: str = "./data/documents.db"):
        """
        Initialize SQL store
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                num_pages INTEGER,
                num_chunks INTEGER,
                language TEXT,
                encoding TEXT,
                chunking_strategy TEXT,
                total_chars INTEGER,
                total_words INTEGER,
                created_at TIMESTAMP,
                processed_at TIMESTAMP,
                metadata TEXT
            )
        """)
        
        # Chunks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                start_char INTEGER,
                end_char INTEGER,
                content_preview TEXT,
                metadata TEXT,
                FOREIGN KEY (document_id) REFERENCES documents(document_id)
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_document_id 
            ON chunks(document_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_language 
            ON documents(language)
        """)
        
        conn.commit()
        conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def add_document(self, metadata: DocumentMetadata) -> bool:
        """
        Add document metadata
        
        Args:
            metadata: DocumentMetadata object
            
        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO documents (
                    document_id, filename, file_type, file_size, num_pages,
                    num_chunks, language, encoding, chunking_strategy,
                    total_chars, total_words, created_at, processed_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                metadata.document_id,
                metadata.filename,
                metadata.file_type,
                metadata.file_size,
                metadata.num_pages,
                metadata.num_chunks,
                metadata.language,
                metadata.encoding,
                metadata.chunking_strategy,
                metadata.total_chars,
                metadata.total_words,
                metadata.created_at.isoformat(),
                metadata.processed_at.isoformat(),
                str(metadata.metadata)
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def add_chunks(self, chunks: List[Chunk]) -> Dict[str, int]:
        """
        Add chunks to database
        
        Args:
            chunks: List of Chunk objects
            
        Returns:
            Dictionary with statistics
        """
        added = 0
        failed = 0
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            for chunk in chunks:
                try:
                    # Create content preview (first 200 chars)
                    preview = chunk.content[:200] if len(chunk.content) > 200 else chunk.content
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO chunks (
                            chunk_id, document_id, chunk_index,
                            start_char, end_char, content_preview, metadata
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.start_char,
                        chunk.end_char,
                        preview,
                        str(chunk.metadata)
                    ))
                    
                    added += 1
                    
                except Exception as e:
                    print(f"Error adding chunk {chunk.chunk_id}: {e}")
                    failed += 1
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error in add_chunks: {e}")
        
        return {'added': added, 'failed': failed}
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve document metadata
        
        Args:
            document_id: Document identifier
            
        Returns:
            Document metadata or None
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM documents WHERE document_id = ?
            """, (document_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            
            return None
            
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return None
    
    def get_chunks_by_document(self, document_id: str) -> List[Dict[str, Any]]:
        """
        Get all chunks for a document
        
        Args:
            document_id: Document identifier
            
        Returns:
            List of chunks
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM chunks 
                WHERE document_id = ?
                ORDER BY chunk_index
            """, (document_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return []
    
    def list_documents(
        self, 
        language: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all documents with optional filters
        
        Args:
            language: Filter by language
            file_type: Filter by file type
            
        Returns:
            List of documents
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM documents WHERE 1=1"
            params = []
            
            if language:
                query += " AND language = ?"
                params.append(language)
            
            if file_type:
                query += " AND file_type = ?"
                params.append(file_type)
            
            query += " ORDER BY processed_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete document and all its chunks
        
        Args:
            document_id: Document identifier
            
        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete chunks first
            cursor.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
            
            # Delete document
            cursor.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Count documents
            cursor.execute("SELECT COUNT(*) FROM documents")
            num_documents = cursor.fetchone()[0]
            
            # Count chunks
            cursor.execute("SELECT COUNT(*) FROM chunks")
            num_chunks = cursor.fetchone()[0]
            
            # Count by language
            cursor.execute("""
                SELECT language, COUNT(*) as count 
                FROM documents 
                GROUP BY language
            """)
            by_language = dict(cursor.fetchall())
            
            # Count by file type
            cursor.execute("""
                SELECT file_type, COUNT(*) as count 
                FROM documents 
                GROUP BY file_type
            """)
            by_file_type = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'total_documents': num_documents,
                'total_chunks': num_chunks,
                'by_language': by_language,
                'by_file_type': by_file_type
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def search_documents(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search documents by filename
        
        Args:
            search_term: Search term
            
        Returns:
            List of matching documents
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM documents 
                WHERE filename LIKE ?
                ORDER BY processed_at DESC
            """, (f"%{search_term}%",))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def reset(self) -> bool:
        """
        Reset the SQL database - delete all documents and chunks
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete all chunks
            cursor.execute("DELETE FROM chunks")
            
            # Delete all documents
            cursor.execute("DELETE FROM documents")
            
            conn.commit()
            conn.close()
            
            print("SQL database reset successfully")
            return True
            
        except Exception as e:
            print(f"Error resetting SQL database: {e}")
            return False

