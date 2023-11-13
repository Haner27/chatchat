import streamlit as st
import extra_streamlit_components as stx


@st.cache_resource
def get_auth_state():
    return {"is_authorized": False}


@st.cache_resource(experimental_allow_widgets=True)
def cookie_manager():
    return stx.CookieManager()
