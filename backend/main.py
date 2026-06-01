from fastapi import FastAPI, UploadFile, File
from typing import List

from backend.models import (  #import structural models for request and response
    ChatRequest,
    ChatResponse,
    UploadResponse
)

from backend.services.rag_service import (
    create_vector_store,    #import langchain models
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
    return {  #testing
        "message": "AI Research Assistant Backend Running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):   # creates a empty  chatrequest object 

    global rag_chain            

    if rag_chain is None:
        return ChatResponse(
            answer="Please upload a PDF first."
        )
    answer = rag_chain.invoke(request.question)  #invoke the chain with request  question 
    return ChatResponse(
        answer=answer
    )


@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_pdf(files: List[UploadFile] = File(...)): #means expecta file request files: List[UploadFile]: means hinting fast api that  file should contain list of files   
#File(...) means this parameter is required and should be treated as file upload
    global rag_chain

    # Save uploaded PDF
    all_documents = []  # create empty list to store all documents from all uploaded pdfs

    for file in files:

        file_path = f"uploads/{file.filename}" #create file path to save the uploaded file in uploads folder

        with open(file_path, "wb") as f:#open the file in write binary mode and save the uploaded file to the specified path
            f.write(await file.read())

        documents = load_pdf(file_path)#load the pdf and split it into documents using the load_pdf function from ingest.py and all documents are loaded in form of document objects page by page which contains page content and metadata like page number and source file name.

        # metadata for future citations
        for doc in documents:
            doc.metadata["source"] = file.filename #add source file name to the metadata of each document object for future reference and citation

        all_documents.extend(documents) #extend the all_documents list with the documents from the current pdf so that we have a combined list of document objects from all uploaded pdfs

    chunks = split_documents(all_documents) #split the combined list of document objects into smaller chunks using the split_documents function from ingest.py which uses langchain text splitter to create smaller chunks of text for better retrieval and processing by the RAG chain

    vector_store = create_vector_store(chunks) #create a vector store from the chunks using the create_vector_store function from rag_service.py which uses langchain embeddings and vector store to create a retrievable vector database of the document chunks

    rag_chain = create_rag_chain(vector_store) #create the RAG chain using the create_rag_chain function from rag_service.py which sets up the retriever and language model for the RAG chain based on the created vector store

    return UploadResponse(
        message=f"{len(files)} PDF(s) processed successfully",
        pages=len(all_documents),
        chunks=len(chunks))