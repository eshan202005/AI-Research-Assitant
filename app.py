import streamlit as st

from ingest import (
    load_pdf,
    split_documents
)

from rag_pipeline import (
    create_vector_store,
    create_rag_chain
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 AI Research Assistant")

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    # Clear Chat Button
    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    st.subheader("📊 Document Stats")

    st.write(
        f"Pages: {st.session_state.pages}"
    )

    st.write(
        f"Chunks: {st.session_state.chunks}"
    )

    if st.session_state.rag_chain:
        st.success("RAG Ready")

    st.markdown("---")

    st.subheader("🚀 Future Features")

    st.markdown("""
    - Multi PDF Support
    - Citations
    - FastAPI Backend
    - LangGraph Workflows
    - Multi-Agent System
    """)


# ==========================================
# MAIN PAGE
# ==========================================

st.title("📚 AI Research Assistant")

st.caption("Phase 1 • RAG System")

st.markdown("---")


# ==========================================
# PROCESS PDF ONLY ONCE
# ==========================================

if (
    uploaded_file
    and
    uploaded_file.name
    != st.session_state.processed_file
):

    pdf_path = f"data/{uploaded_file.name}"

    with open(pdf_path, "wb") as f:

        f.write(
            uploaded_file.getbuffer()
        )

    documents = load_pdf(
        pdf_path
    )

    chunks = split_documents(
        documents
    )

    vector_store = create_vector_store(
        chunks
    )

    rag_chain = create_rag_chain(
        vector_store
    )

    st.session_state.rag_chain = (
        rag_chain
    )

    st.session_state.processed_file = (
        uploaded_file.name
    )

    st.session_state.pages = (
        len(documents)
    )

    st.session_state.chunks = (
        len(chunks)
    )


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ==========================================
# CHAT INPUT
# ==========================================

user_question = st.chat_input(
    "Ask a question about your document..."
)


# ==========================================
# QUESTION ANSWERING
# ==========================================

if (
    st.session_state.rag_chain
    and
    user_question
):

    # Store User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):

        st.write(
            user_question
        )

    try:

        # Generate Response
        with st.spinner(
            "Thinking..."
        ):

            response = (
                st.session_state.rag_chain
                .invoke(user_question)
            )

        # Store Assistant Response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message(
            "assistant"
        ):

            st.write(
                response
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )