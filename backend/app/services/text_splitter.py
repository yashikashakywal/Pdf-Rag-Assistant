from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings

# Overlap prevents important context from being lost at chunk boundaries.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
    separators=["\n\n", "\n", ".", " ", ""],
)


def split_text(text: str) -> list[str]:
    return text_splitter.split_text(text)
