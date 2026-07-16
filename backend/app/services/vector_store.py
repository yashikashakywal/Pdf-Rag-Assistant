import os

from langchain_community.vectorstores import FAISS

from app.services.embeddings import embedding_model


def _index_exists(index_path: str) -> bool:
    return os.path.exists(os.path.join(index_path, "index.faiss"))


def create_vector_store(chunks: list[str], metadatas: list[dict], index_path: str) -> FAISS:
    """
    Add chunks to the FAISS index at `index_path`, creating it if it doesn't
    exist yet and merging into it (rather than overwriting) if it does. This
    lets a user upload multiple documents and query across all of them.

    `index_path` is expected to be a per-user directory so accounts never see
    each other's documents.
    """
    if _index_exists(index_path):
        db = FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
        db.add_texts(texts=chunks, metadatas=metadatas)
    else:
        db = FAISS.from_texts(texts=chunks, embedding=embedding_model, metadatas=metadatas)

    os.makedirs(index_path, exist_ok=True)
    db.save_local(index_path)
    return db


def reset_vector_store(index_path: str) -> None:
    """Delete the persisted index at `index_path` so the user can start fresh."""
    for fname in ("index.faiss", "index.pkl"):
        fpath = os.path.join(index_path, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
