import streamlit as st


@st.cache_resource
def get_auth_state():
    return {"is_authorized": False}
