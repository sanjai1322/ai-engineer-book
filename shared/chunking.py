"""
Text chunking — §6.3.

chunk_text() splits a long document into overlapping pieces so each piece
fits within a model's context and embeddings stay focused on one topic.
"""

def chunk_text(text, size=500, overlap=50):
    """
    Split text into chunks of roughly `size` words with overlap.
    """
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        chunks.append(" ".join(words[start:start + size]))
        start += size - overlap
        
    return chunks
