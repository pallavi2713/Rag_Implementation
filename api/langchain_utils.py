from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
import os
from typing import List
from pydantic import BaseModel, Field
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from chroma_utils import vectorstore
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv('.env')  # Loads from .env file

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

output_parser = StrOutputParser()

# Set up prompts and chains
contextualize_q_system_prompt = (
    "if document has no information about question then say context is not provided "
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as it is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])



qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


def get_rag_chain(model="gemini-2.0-flash"):  # Updated default model
    # Initialize Gemini with safety settings
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain