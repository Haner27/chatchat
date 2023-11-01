import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
import pdfplumber


api = ApiRequest(base_url=api_address())

# Define the Streamlit app
def app():
    # Session state to manage the user's uploaded file and chat history
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    # Page 1: File Upload
    if st.session_state.uploaded_file is None:
        with st.container():
            uploaded_file = st.file_uploader("Please upload a PDF file", type=["pdf"])
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.rerun()  # Rerun the app to move to the chat page

    # Page 2: Chat
    if st.session_state.uploaded_file is not None:
        dialogue_page(api)


# Run the app
if __name__ == "__main__":
    app()
