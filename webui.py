import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
from webui_pages.states import get_auth_state
from server.common.token import Token
import pdfplumber

api = ApiRequest(base_url=api_address())


def pdf_chat(api):
    # Session state to manage the user's uploaded file and chat history
    if "kb_name" not in st.session_state:
        st.session_state.kb_name = None

    # Page 1: File Upload
    if not st.session_state.kb_name:
        st.session_state.kb_name = knowledge_base_page(api)
        if st.session_state.kb_name:
            st.rerun()
    else:
        dialogue_page(api, "知识库问答", st.session_state.kb_name)


def chat(api):
    dialogue_page(api)


def auth(api):
    auth_page(api)


# Define the Streamlit app
def app():
    stage = os.getenv("STAGE", "dev")
    if not get_auth_state()["is_authorized"]:
        auth(api)
        return

    pages = {
        "对话": {
            "icon": "chat",
            "func": chat,
        }
    }
    if stage == "dev":
        pages.update(
            {
                "文档对话": {
                    "icon": "chat",
                    "func": pdf_chat,
                },
                "知识库管理": {
                    "icon": "hdd-stack",
                    "func": real_knowledge_base_page,
                },
            }
        )

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
