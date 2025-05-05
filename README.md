# Rag_Implementation
![image](https://github.com/user-attachments/assets/4842d56b-2773-4e7c-a79b-08bf6eb04254)

# Tech stack
Frontend	- Streamlit
Backend	- FastAPI
LLM Interface - 	Langchain + Google Gemini (or OpenAI)
Embedding - Langchain EmbeddingModels
Vector - DB	Chroma
Environment	- Python, dotenv, Uvicorn

Features
✅ Upload & index documents

✅ Ask questions about your data

✅ Multi-user sessions using session IDs

✅ Real-time responses from LLMs

✅ Beautiful UI with Streamlit + custom CSS

✅ REST API endpoints with FastAPI

✅ Document management (list, delete, re-index)

![image](https://github.com/user-attachments/assets/bc978f48-493f-4028-9e40-0f96bfdaf9d7)


# 2. RAG Fundamentals
Understand RAG as a combination of retrieving documents using a vector database and generating responses using an LLM.

It enhances LLMs with custom, non-public data.

![image](https://github.com/user-attachments/assets/eaf20e3e-9794-4594-bef4-5b114816a8d5)

# 3. Langchain Basics & LCEL
Use Langchain Expression Language (LCEL) to create modular, chainable components:

Loaders → Text Splitters → Embeddings → Vectorstore

ConversationalRetrievalChain to connect retriever with LLM

# 4. Document Upload & Indexing (FastAPI)
Upload endpoint accepts files, parses them, and stores metadata.

Documents are embedded and stored in Chroma DB.

Each document gets a unique ID to support deletion and indexing.

# 5. Create Backend API (FastAPI)
/chat: Accepts user input and returns LLM response.

/upload-doc: Accepts and indexes documents.

/list-docs: Lists all indexed documents.

/delete-doc: Deletes document from Chroma and DB.

# 6. Chat Interface (Streamlit)
Users can chat using st.chat_input and see both questions and LLM answers styled with custom CSS.

Multi-user handling using session_id.

Detailed response with expandable sections showing model used and session info.

# 7. Session Management
Each session is tracked via UUID.

Chat history is stored in memory (or DB) for conversational continuity.

# 8. Add Custom Styling
## Use styles.css to define themes for:

. Chat bubbles

. Background

. Sidebar

. Input boxes

# 9. Run the App
Backend:

uvicorn app.main:app --reload

Frontend

streamlit run app_interface/app.py
