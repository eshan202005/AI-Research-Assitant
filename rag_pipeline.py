from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  
from langchain_core.runnables import RunnableParallel , RunnablePassthrough
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


def create_vector_store(chunks):#we created a function that takes the chunks of text and creates a vector store using the Chroma library. It initializes an embedding model using OpenAIEmbeddings and then adds the chunks to the vector database for later retrieval during the RAG process.

    # Create embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create empty Chroma vector store
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory="chroma_db",
        collection_name="pdf_chunks"
    )

    # Add chunks to vector database
    vector_store.add_documents(chunks)

    return vector_store



def format_docs(docs):# to join the retrieved documents into a single string that can be used as context for the language model. It takes a list of documents and concatenates their page content with double newlines in between, making it easier for the model to process the information as a coherent context when generating responses to user queries.

    return "\n\n".join(
        doc.page_content for doc in docs
    )


def create_rag_chain(vector_store):# to create a Retrieval-Augmented Generation (RAG) chain using the vector store. It initializes a language model and then sets up a retriever from the vector store. Finally, it combines the retriever and the language model into a RAG chain that can be used to generate responses based on retrieved information from the vector database.

    # Create language model
    llm = ChatOpenAI(model="gpt-5-mini")

    # Create retriever from vector store
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question using only the
        provided context.

        Context:
        {context}

        Question:
        {question}
        """
    )

    parser=StrOutputParser()


    retrieval_chain = retriever | format_docs

    generation_chain = prompt | llm | parser



    parallel_chain = RunnableParallel({
        "context": retrieval_chain,
        "question": RunnablePassthrough()
    }) 


    final_chain = parallel_chain | generation_chain


    return final_chain


