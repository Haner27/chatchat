import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages import *
import os
from configs import VERSION
from server.utils import api_address
from webui_pages.states import get_auth_state, cookie_manager
from server.common.token import Token
import pdfplumber
from datetime import datetime
from streamlit.runtime.scriptrunner import get_script_run_ctx
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


# Define the Streamlit app
def get_state_auth_token():
    if not hasattr(st.session_state, "auth_token"):
        return None
    return st.session_state.auth_token


def get_cookie():
    cookie = "chatchat_"
    ctx = get_script_run_ctx()
    server = st.runtime.get_instance().get_client(ctx.session_id)
    if cookie in server.cookies:
        return urllib.parse.unquote(server.cookies[cookie].value)
    else:
        return None


def set_cookie(token):
    cookie = "chatchat_"
    cookie_manager().set(cookie, token, expires_at=datetime.now() + timedelta(days=7))


def app():

    print(f"state token: {get_state_auth_token()}")
    print(f"cookie token: {get_cookie()}")
    ck = get_cookie()

    if ck:
        st.session_state.auth_token = ck

    if not ck and get_state_auth_token():
        set_cookie(get_state_auth_token())

    stage = os.getenv("STAGE", "dev")
    if not ck and not get_state_auth_token():
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
