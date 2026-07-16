import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.prompts import RAG_PROMPT
from app.db.models import User
from app.models.schemas import AnswerResponse, QuestionRequest, Source, UploadResponse
from app.services.llm import LLMConfigError, generate_answer
from app.services.pdf_loader import extract_text
from app.services.retriever import IndexNotFoundError, load_retriever
from app.services.text_splitter import split_text
from app.services.vector_store import create_vector_store, reset_vector_store

router = APIRouter()


def _user_upload_dir(user: User) -> Path:
    """Every user gets their own uploads subfolder so accounts stay isolated."""
    path = Path(settings.upload_dir) / user.id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _user_index_dir(user: User) -> str:
    """Every user gets their own FAISS index subfolder."""
    return str(Path(settings.faiss_index_dir) / user.id)


@router.get("/health")
def health_check():
    """Simple liveness probe used by the frontend to show a connection indicator."""
    return {"status": "ok"}


@router.get("/documents")
def list_documents(current_user: User = Depends(get_current_user)):
    """List PDFs that this user has already ingested into their index."""
    upload_dir = _user_upload_dir(current_user)
    files = sorted(p.name for p in upload_dir.glob("*.pdf"))
    return {"documents": files}


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type != "application/pdf" and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    upload_dir = _user_upload_dir(current_user)
    file_path = upload_dir / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    try:
        pages = extract_text(file_path)
    except Exception as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=f"Couldn't read '{file.filename}': {exc}") from exc

    if not pages:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail="No extractable text found in this PDF (it may be a scanned image).",
        )

    all_chunks = []
    all_metadata = []

    for page in pages:
        chunks = split_text(page["text"])
        all_chunks.extend(chunks)
        all_metadata.extend({"source": file.filename, "page": page["page"]} for _ in chunks)

    create_vector_store(all_chunks, all_metadata, index_path=_user_index_dir(current_user))

    return UploadResponse(
        message="Upload successful",
        filename=file.filename,
        pages=len(pages),
        chunks=len(all_chunks),
    )


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    payload: QuestionRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        retriever = load_retriever(_user_index_dir(current_user))
    except IndexNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    docs = retriever.invoke(payload.question)

    if not docs:
        return AnswerResponse(
            answer="I couldn't find that information in the uploaded document.",
            sources=[],
        )

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = RAG_PROMPT.format(context=context, question=payload.question)

    try:
        answer = generate_answer(prompt)
    except LLMConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"The language model provider returned an error: {exc}"
        ) from exc

    return AnswerResponse(
        answer=answer,
        sources=[Source(file=doc.metadata["source"], page=doc.metadata["page"]) for doc in docs],
    )


@router.delete("/reset")
def reset(current_user: User = Depends(get_current_user)):
    """Clear this user's vector index and uploaded files so they can start fresh."""
    reset_vector_store(_user_index_dir(current_user))
    upload_dir = _user_upload_dir(current_user)
    for pdf in upload_dir.glob("*.pdf"):
        pdf.unlink(missing_ok=True)
    return {"message": "Index and uploads cleared."}
