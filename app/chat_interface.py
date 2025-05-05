import streamlit as st
from api_utils import get_api_response

# ========== Load Custom CSS ==========
def load_css():
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ styles.css not found. Custom styles will not be applied.")

load_css()

# ========== Chat Interface ==========
def display_chat_interface():
    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            css_class = "user-message" if message["role"] == "user" else "bot-message"
            st.markdown(f"<div class='{css_class}'>{message['content']}</div>", unsafe_allow_html=True)

    # User input
    if prompt := st.chat_input("Query:"):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

        # Get assistant response
        with st.spinner("Generating response..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)

            if response:
                # Update session and store assistant message
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})

                with st.chat_message("assistant"):
                    st.markdown(f"<div class='bot-message'>{response['answer']}</div>", unsafe_allow_html=True)

                    # Additional details
                    with st.expander("🔍 Details"):
                        st.markdown("**Generated Answer:**")
                        st.code(response['answer'], language="text")

                        st.markdown("**Model Used:**")
                        st.code(response['model'], language="text")

                        st.markdown("**Session ID:**")
                        st.code(response['session_id'], language="text")
            else:
                st.error("❌ Failed to get a response from the API. Please try again.")