"""Text chunking and document processing utilities for vector store."""

import logging
import uuid
from pathlib import Path

from cato.storage.vector.base import VectorDocument, VectorStore

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Split documents into chunks for embedding.
    
    Uses recursive character splitting with overlap for better context preservation.
    
    Parameters
    ----------
    chunk_size : int, default=1000
        Target chunk size in characters.
    chunk_overlap : int, default=100
        Number of characters to overlap between chunks.
    separators : list[str] | None, optional
        List of separators to use for splitting, in priority order.
    """
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        separators: list[str] | None = None,
    ) -> None:
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._separators = separators or ["\n\n", "\n", ". ", " ", ""]
    
    def split(self, text: str) -> list[str]:
        """
        Split text into chunks.
        
        Parameters
        ----------
        text : str
            Text to split.
        
        Returns
        -------
        list[str]
            Text chunks with overlap.
        """
        return self._split_recursive(text, self._separators)
    
    def _split_recursive(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:
        """
        Recursively split using separators in order.
        
        Parameters
        ----------
        text : str
            Text to split.
        separators : list[str]
            Separators to try in order.
        
        Returns
        -------
        list[str]
            Split chunks.
        """
        if not text:
            return []
        
        # If text fits in chunk, return it
        if len(text) <= self._chunk_size:
            return [text]
        
        # Find separator to use
        separator = separators[-1]  # Default to last (empty string)
        for sep in separators:
            if sep in text:
                separator = sep
                break
        
        # Split and merge
        splits = text.split(separator) if separator else list(text)
        return self._merge_splits(splits, separator, separators)
    
    def _merge_splits(
        self,
        splits: list[str],
        separator: str,
        separators: list[str],
    ) -> list[str]:
        """
        Merge splits into chunks with overlap.
        
        Parameters
        ----------
        splits : list[str]
            Text segments after splitting.
        separator : str
            Separator used for splitting.
        separators : list[str]
            Available separators for recursive splitting.
        
        Returns
        -------
        list[str]
            Merged chunks with overlap.
        """
        chunks = []
        current_chunk = []
        current_length = 0
        
        for split in splits:
            split_length = len(split) + len(separator)
            
            if current_length + split_length > self._chunk_size and current_chunk:
                # Save current chunk
                chunk_text = separator.join(current_chunk)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap
                overlap_length = 0
                while current_chunk and overlap_length < self._chunk_overlap:
                    overlap_length += len(current_chunk[-1]) + len(separator)
                    if overlap_length > self._chunk_overlap:
                        current_chunk.pop(0)
                        break
                    current_chunk.pop(0)
                
                current_length = sum(len(s) for s in current_chunk) + len(separator) * len(current_chunk)
            
            current_chunk.append(split)
            current_length += split_length
        
        # Don't forget last chunk
        if current_chunk:
            chunks.append(separator.join(current_chunk))
        
        return chunks


class DocumentProcessor:
    """
    Process documents for vector storage.
    
    Handles text chunking and metadata management.
    
    Parameters
    ----------
    chunker : TextChunker
        Text chunker for splitting documents.
    vector_store : VectorStore
        Vector store for adding documents.
    """
    
    def __init__(
        self,
        chunker: TextChunker,
        vector_store: VectorStore,
    ) -> None:
        self._chunker = chunker
        self._store = vector_store
    
    async def add_document(
        self,
        content: str,
        source: str,
        metadata: dict | None = None,
    ) -> list[str]:
        """
        Process and add a document to the vector store.
        
        Parameters
        ----------
        content : str
            Document content.
        source : str
            Source identifier (filename, URL, etc.).
        metadata : dict | None, optional
            Additional metadata.
        
        Returns
        -------
        list[str]
            IDs of created chunks.
        """
        # Split into chunks
        chunks = self._chunker.split(content)
        
        # Create documents
        base_metadata = metadata or {}
        base_metadata["source"] = source
        base_metadata["total_chunks"] = len(chunks)
        
        # Generate unique base ID for this document
        doc_id = str(uuid.uuid4())[:8]
        
        documents = [
            VectorDocument(
                id=f"{doc_id}:{i}",
                content=chunk,
                metadata={
                    **base_metadata,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]
        
        # Add to store
        logger.info(f"Adding document '{source}' with {len(chunks)} chunks")
        return await self._store.add(documents)
    
    async def add_file(
        self,
        file_path: Path,
        metadata: dict | None = None,
    ) -> list[str]:
        """
        Read and add a file to the vector store.
        
        Parameters
        ----------
        file_path : Path
            Path to file to add.
        metadata : dict | None, optional
            Additional metadata.
        
        Returns
        -------
        list[str]
            IDs of created chunks.
        
        Raises
        ------
        FileNotFoundError
            If file does not exist.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = file_path.read_text()
        
        # Add file-specific metadata
        file_metadata = metadata or {}
        file_metadata["file_path"] = str(file_path)
        file_metadata["file_name"] = file_path.name
        
        return await self.add_document(
            content=content,
            source=str(file_path),
            metadata=file_metadata,
        )
