import streamlit as st
import requests


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

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 AI Research Assistant")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload your PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    # ==========================================
    # UPLOAD TO FASTAPI
    # ==========================================

    if uploaded_files:

        current_files = [
            file.name
            for file in uploaded_files
        ]

        if (
            current_files
            !=
            st.session_state.processed_files
        ):

            files = []

            for file in uploaded_files:

                files.append(
                    (
                        "files",
                        (
                            file.name,
                            file.getvalue(),
                            "application/pdf"
                        )
                    )
                )

            try:

                with st.spinner(
                    "Processing PDFs..."
                ):

                    response = requests.post(
                        "http://127.0.0.1:8000/upload",
                        files=files
                    )

                    data = response.json()

                    st.session_state.pages = (
                        data["pages"]
                    )

                    st.session_state.chunks = (
                        data["chunks"]
                    )

                    st.session_state.pdf_uploaded = True

                    st.session_state.processed_files = (
                        current_files
                    )

                    st.success(
                        data["message"]
                    )

            except Exception as e:

                st.error(
                    f"Upload Error: {str(e)}"
                )

    # ==========================================
    # CLEAR CHAT
    # ==========================================

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("---")

    # ==========================================
    # DOCUMENT STATS
    # ==========================================

    st.subheader("📊 Document Stats")

    st.write(
        f"Pages: {st.session_state.pages}"
    )

    st.write(
        f"Chunks: {st.session_state.chunks}"
    )

    if st.session_state.pdf_uploaded:

        st.success("✅ PDFs Uploaded")

        st.success("✅ RAG Ready")

    st.markdown("---")

    # ==========================================
    # FUTURE FEATURES
    # ==========================================

    st.subheader("🚀 Future Features")

    st.markdown("""
    - Metadata Tracking
    - Citations
    - MMR Retrieval
    - LangGraph Workflows
    - Multi-Agent System
    """)


# ==========================================
# MAIN PAGE
# ==========================================

st.title("📚 AI Research Assistant")

st.caption("Phase 2 • FastAPI Backend")

st.markdown("---")


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
    "Ask a question about your documents..."
)


# ==========================================
# QUESTION ANSWERING
# ==========================================

if (
    user_question
    and
    st.session_state.pdf_uploaded
):

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):

        st.write(
            user_question
        )

    try:

        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "question": user_question
                }
            )

            answer = (
                response.json()["answer"]
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message(
            "assistant"
        ):

            st.write(
                answer
            )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )


# ==========================================
# PDF NOT UPLOADED WARNING
# ==========================================

elif (
    user_question
    and
    not st.session_state.pdf_uploaded
):

    st.warning(
        "Please upload at least one PDF first."
    )