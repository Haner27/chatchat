import streamlit as st

from server.db.repository.user_repository import get_user_by_token
from webui_pages.auth.auth import get_cookie, get_state_auth_token, set_cookie
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
from server.common.token import Token
import pdfplumber
from datetime import datetime
import urllib.parse

api = ApiRequest(base_url=api_address())

favicon = os.path.join("img", "baozi.png")
# setting the tag and favicon
st.set_page_config(
    page_title="BunAI",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)


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


def app():
    # st.session_state.auth_token = get_cookie()
    # token = get_state_auth_token()

    token = get_cookie() or get_state_auth_token()
    if token:
        user = get_user_by_token(token)
        if user:  # 验证有效后
            set_cookie(token)
        else:
            auth(api)
            return
    else:
        auth(api)
        return

    pages = {
        "对话": {
            "icon": "chat",
            "func": chat,
        }
    }
    stage = os.getenv("STAGE", "dev")
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
