import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
import pdfplumber


api = ApiRequest(base_url=api_address())


def pdf_chat(api):

    # Session state to manage the user's uploaded file and chat history
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = False

    # Page 1: File Upload
    if not st.session_state.uploaded_file:
        knowledge_base_page(api)
        if st.session_state.uploaded_file:
            st.rerun()
    else:
        dialogue_page(api)


# Define the Streamlit app
def app():

    pages = {
        "对话": {
            "icon": "chat",
            "func": pdf_chat,
        },
        "知识库管理": {
            "icon": "hdd-stack",
            "func": real_knowledge_base_page,
        },
    }

    with st.sidebar:
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )
    if selected_page in pages:
        pages[selected_page]["func"](api)


# Run the app
if __name__ == "__main__":
    app()
