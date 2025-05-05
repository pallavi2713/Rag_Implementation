import streamlit as st
from api_utils import upload_document, list_documents, delete_document

# ========== Load Custom CSS ==========
def load_css():
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ styles.css not found. Custom styles will not be applied.")

load_css()

# ========== Sidebar UI ==========
def display_sidebar():
    st.sidebar.image("logo.png", width=120)
    st.sidebar.title("📁 Document Management")

    # Sidebar: Model Selection
    st.sidebar.subheader("AI Model")
    model_options = ["gemini-2.0-flash"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Sidebar: Upload Document
    st.sidebar.header("📤 Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html"])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(
                        f"✅ File '{uploaded_file.name}' uploaded successfully"
                    )
                    st.session_state.documents = list_documents()

    # Sidebar: Refresh List
    st.sidebar.header("📋 Uploaded Documents")
    if st.sidebar.button("🔄 Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list if not already
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents

    # Sidebar: List & Delete Documents
    if documents:
        for doc in documents:
            st.sidebar.markdown(
                f"<div class='bot-message'>📄 {doc['filename']}<br>ID: {doc['id']}<br><small>Uploaded: {doc['upload_timestamp']}</small></div>",
                unsafe_allow_html=True
            )

        selected_file_id = st.sidebar.selectbox(
            "Select a document to delete",
            options=[doc['id'] for doc in documents],
            format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x)
        )
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f" Deleted document with ID {selected_file_id}.")
                    st.session_state.documents = list_documents()
                else:
                    st.sidebar.error(f"❌ Failed to delete document with ID {selected_file_id}.")
    else:
        st.sidebar.info("No documents uploaded yet.")

# ========== Main Area ==========
def main():
    st.title("📚 Document Upload and Management")
    st.caption("Styled with custom CSS")

    display_sidebar()

if __name__ == "__main__":
    main()
