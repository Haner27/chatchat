import streamlit as st
from server.common.token import Token
from webui_pages.utils import *
from webui_pages.states import get_auth_state
from webui_pages.states import get_auth_state, cookie_manager
import time


def auth_page(api: ApiRequest):
    st.title("登录认证")
    st.write("请输入邀请码进行登录认证")
    token = st.text_area(
        label="秘钥", key="token", max_chars=1024, help="系统分配的秘钥", placeholder="秘钥"
    )
    clicked = st.button("开始体验")
    cookie = "chatchat_"
    result = False
    if clicked:
        if not Token(token).is_valid:
            st.toast("登录失败")
            st.error("登录失败~~")
        else:
            st.toast("登录成功")
            st.success("登录成功~~")
            result = True
            st.session_state.auth_token = token
            st.rerun()
