import os

from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.services.embeddings import embedding_model


class IndexNotFoundError(RuntimeError):
    """Raised when a query is made before any document has been uploaded."""


def load_retriever(index_path: str):
    index_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(index_file):
        raise IndexNotFoundError("No documents have been uploaded yet. Upload a PDF first.")

    db = FAISS.load_local(
        index_path,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    return db.as_retriever(search_kwargs={"k": settings.retrieval_k})
