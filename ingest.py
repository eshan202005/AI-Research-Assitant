from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(pdf_path):#created a fuction that when a file  is uploaded it will load the pdf and extract the pages as documents
    # Load PDF
    loader = PyPDFLoader(pdf_path)

    # Extract pages as documents
    documents = loader.load()

    return documents


def split_documents(documents):#created a function that takes the extracted documents and splits them into smaller chunks using the RecursiveCharacterTextSplitter
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    return chunks