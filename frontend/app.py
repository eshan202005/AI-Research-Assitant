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

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None


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

    # ==========================================
    # UPLOAD TO FASTAPI
    # ==========================================

    if (
        uploaded_file
        and uploaded_file.name != st.session_state.processed_file
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:

            with st.spinner(
                "Processing PDF..."
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

                st.session_state.processed_file = (
                    uploaded_file.name
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

        st.success("✅ PDF Uploaded")

        st.success("✅ RAG Ready")

    st.markdown("---")

    # ==========================================
    # FUTURE FEATURES
    # ==========================================

    st.subheader("🚀 Future Features")

    st.markdown("""
    - Multi PDF Support
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
    "Ask a question about your document..."
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
        "Please upload a PDF first."
    )