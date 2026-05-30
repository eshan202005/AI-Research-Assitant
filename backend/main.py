from fastapi import FastAPI, UploadFile, File

from backend.models import (
    ChatRequest,
    ChatResponse,
    UploadResponse
)

from backend.services.rag_service import (
    create_vector_store,
    create_rag_chain
)

from ingest import (
    load_pdf,
    split_documents
)

app = FastAPI()

# Global RAG chain
rag_chain = None


@app.get("/")
def home():
    return {
        "message": "AI Research Assistant Backend Running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    global rag_chain

    if rag_chain is None:
        return ChatResponse(
            answer="Please upload a PDF first."
        )
    answer = rag_chain.invoke(request.question)
    return ChatResponse(
        answer=answer
    )


@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_pdf(file: UploadFile = File(...)):

    global rag_chain

    # Save uploaded PDF
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load PDF
    documents = load_pdf(file_path)

    # Split into chunks
    chunks = split_documents(documents)

    # Create vector store
    vector_store = create_vector_store(chunks)

    # Create RAG chain
    rag_chain = create_rag_chain(vector_store)

    return UploadResponse(
    message="PDF processed successfully",
    pages=len(documents),
    chunks=len(chunks)
    )