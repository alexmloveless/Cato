"""Vector store commands for managing conversation memory."""

import logging
from pathlib import Path

from cato.commands.base import CommandContext, CommandResult
from cato.commands.registry import command
from cato.storage.vector.base import VectorDocument
from cato.storage.vector.utils import DocumentProcessor, TextChunker

logger = logging.getLogger(__name__)


@command(
    name="vadd",
    description="Add text directly to vector store",
    usage="/vadd <text>",
)
async def vadd(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Add text directly to vector store.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Text to add.
    
    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /vadd <text>"
        )
    
    text = " ".join(args)
    
    try:
        # Create document
        import uuid
        doc_id = str(uuid.uuid4())[:8]
        doc = VectorDocument(
            id=doc_id,
            content=text,
            metadata={"type": "manual_add", "source": "user"}
        )
        
        # Add to store
        await ctx.vector_store.add([doc])
        
        return CommandResult(
            success=True,
            message=f"Added text to vector store (ID: {doc_id})"
        )
    except Exception as e:
        logger.error(f"Failed to add text to vector store: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to add text: {e}"
        )


@command(
    name="vdoc",
    description="Add document file to vector store with chunking",
    usage="/vdoc <path>",
)
async def vdoc(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Add document file to vector store with chunking.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Path to document file.
    
    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /vdoc <path>"
        )
    
    file_path = Path(args[0]).expanduser()
    
    if not file_path.exists():
        return CommandResult(
            success=False,
            message=f"File not found: {file_path}"
        )
    
    try:
        # Create chunker and processor
        chunker = TextChunker(
            chunk_size=ctx.config.vector_store.chunk_size,
            chunk_overlap=ctx.config.vector_store.chunk_overlap,
        )
        processor = DocumentProcessor(chunker, ctx.vector_store)
        
        # Add file
        chunk_ids = await processor.add_file(file_path)
        
        return CommandResult(
            success=True,
            message=f"Added document '{file_path.name}' to vector store ({len(chunk_ids)} chunks)"
        )
    except Exception as e:
        logger.error(f"Failed to add document to vector store: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to add document: {e}"
        )


@command(
    name="vquery",
    description="Query vector store for similar content",
    usage="/vquery <query> [n_results]",
)
async def vquery(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Query vector store for similar content.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Search query and optional result count.
    
    Returns
    -------
    CommandResult
        Result with success status and search results.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /vquery <query> [n_results]"
        )
    
    # Parse arguments
    n_results = 5  # Default
    if len(args) >= 2 and args[-1].isdigit():
        n_results = int(args[-1])
        query = " ".join(args[:-1])
    else:
        query = " ".join(args)
    
    try:
        # Search vector store
        results = await ctx.vector_store.search(query, n_results=n_results)
        
        if not results:
            return CommandResult(
                success=True,
                message="No results found."
            )
        
        # Format results
        output = [f"Found {len(results)} results:\n"]
        for i, result in enumerate(results, 1):
            doc = result.document
            score = result.score
            content_preview = doc.content[:100] + "..." if len(doc.content) > 100 else doc.content
            
            output.append(f"\n{i}. ID: {doc.id}")
            output.append(f"   Score: {score:.4f}")
            output.append(f"   Source: {doc.metadata.get('source', 'unknown')}")
            output.append(f"   Content: {content_preview}")
        
        return CommandResult(
            success=True,
            message="\n".join(output)
        )
    except Exception as e:
        logger.error(f"Vector store query failed: {e}")
        return CommandResult(
            success=False,
            message=f"Query failed: {e}"
        )


@command(
    name="vstats",
    description="Display vector store statistics",
    usage="/vstats",
)
async def vstats(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Display vector store statistics.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Unused.
    
    Returns
    -------
    CommandResult
        Result with success status and statistics.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    try:
        count = await ctx.vector_store.count()
        
        output = [
            "Vector Store Statistics:",
            f"  Total documents: {count}",
            f"  Collection: {ctx.config.vector_store.collection_name}",
            f"  Backend: {ctx.config.vector_store.backend}",
            f"  Embedding provider: {ctx.config.vector_store.embedding_provider}",
            f"  Embedding model: {ctx.config.vector_store.embedding_model}",
        ]
        
        return CommandResult(
            success=True,
            message="\n".join(output)
        )
    except Exception as e:
        logger.error(f"Failed to get vector store stats: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to get statistics: {e}"
        )


@command(
    name="vdelete",
    description="Delete documents from vector store by ID",
    usage="/vdelete <id>",
)
async def vdelete(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Delete documents from vector store by ID.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Document IDs to delete.
    
    Returns
    -------
    CommandResult
        Result with success status and message.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /vdelete <id>"
        )
    
    doc_id = args[0]
    
    try:
        await ctx.vector_store.delete([doc_id])
        
        return CommandResult(
            success=True,
            message=f"Deleted document {doc_id} from vector store"
        )
    except Exception as e:
        logger.error(f"Failed to delete from vector store: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to delete document: {e}"
        )


@command(
    name="vget",
    description="Retrieve documents by ID from vector store",
    usage="/vget <id>",
)
async def vget(ctx: CommandContext, *args: str) -> CommandResult:
    """
    Retrieve documents by ID from vector store.
    
    Parameters
    ----------
    ctx : CommandContext
        Command execution context.
    args : tuple[str, ...]
        Document IDs to retrieve.
    
    Returns
    -------
    CommandResult
        Result with success status and documents.
    """
    if not ctx.vector_store:
        return CommandResult(
            success=False,
            message="Vector store is not enabled. Enable it in configuration."
        )
    
    if not args:
        return CommandResult(
            success=False,
            message="Usage: /vget <id>"
        )
    
    doc_id = args[0]
    
    try:
        documents = await ctx.vector_store.get([doc_id])
        
        if not documents:
            return CommandResult(
                success=True,
                message=f"No document found with ID: {doc_id}"
            )
        
        # Format document
        doc = documents[0]
        output = [
            f"Document ID: {doc.id}",
            f"Source: {doc.metadata.get('source', 'unknown')}",
            f"Type: {doc.metadata.get('type', 'unknown')}",
            f"\nContent:\n{doc.content}",
        ]
        
        return CommandResult(
            success=True,
            message="\n".join(output)
        )
    except Exception as e:
        logger.error(f"Failed to retrieve from vector store: {e}")
        return CommandResult(
            success=False,
            message=f"Failed to retrieve document: {e}"
        )
