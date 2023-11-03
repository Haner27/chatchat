import streamlit as st
import uuid
from webui_pages.utils import *
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from server.knowledge_base.utils import get_file_path, LOADER_DICT
from server.knowledge_base.kb_service.base import get_kb_details, get_kb_file_details
from typing import Literal, Dict, Tuple
from configs import (
    kbs_config,
    EMBEDDING_MODEL,
    DEFAULT_VS_TYPE,
    CHUNK_SIZE,
    OVERLAP_SIZE,
    ZH_TITLE_ENHANCE,
)
from server.utils import list_embed_models
import os
import time


# SENTENCE_SIZE = 100

cell_renderer = JsCode(
    """function(params) {if(params.value==true){return '✓'}else{return '×'}}"""
)


def config_aggrid(
    df: pd.DataFrame,
    columns: Dict[Tuple[str, str], Dict] = {},
    selection_mode: Literal["single", "multiple", "disabled"] = "single",
    use_checkbox: bool = False,
) -> GridOptionsBuilder:
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column("No", width=40)
    for (col, header), kw in columns.items():
        gb.configure_column(col, header, wrapHeaderText=True, **kw)
    gb.configure_selection(
        selection_mode=selection_mode,
        use_checkbox=use_checkbox,
        # pre_selected_rows=st.session_state.get("selected_rows", [0]),
    )
    return gb


def file_exists(kb: str, selected_rows: List) -> Tuple[str, str]:
    """
    check whether a doc file exists in local knowledge base folder.
    return the file's name and path if it exists.
    """
    if selected_rows:
        file_name = selected_rows[0]["file_name"]
        file_path = get_file_path(kb, file_name)
        if os.path.isfile(file_path):
            return file_name, file_path
    return "", ""


def upload_and_create_kb(api, files, kb_list):
    filename = files[0].name
    vs_type = "faiss"
    embed_model = "text-embedding-ada-002"
    kb_name = filename
    if kb_name in kb_list:
        # add a random unique hash at the end of the kb_name
        kb_name += str(uuid.uuid4())[:8]

    ret = api.create_knowledge_base(
        knowledge_base_name=kb_name,
        vector_store_type=vs_type,
        embed_model=embed_model,
    )
    st.toast(ret.get("msg", " "))

    chunk_size = 250
    chunk_overlap = 50
    zh_title_enhance = False

    ret = api.upload_kb_docs(
        files,
        knowledge_base_name=kb_name,
        override=True,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        zh_title_enhance=zh_title_enhance,
    )
    if msg := check_success_msg(ret):
        st.toast(msg, icon="✔")
        st.session_state.uploaded_file = True
        st.session_state.kb_name = kb_name
    elif msg := check_error_msg(ret):
        st.toast(msg, icon="✖")
    return kb_name


def knowledge_base_page(api: ApiRequest):
    st.session_state.uploaded_file = False
    try:
        kb_list = {x["kb_name"]: x for x in get_kb_details()}
        kb_names = list(kb_list.keys())
    except Exception as e:
        st.error(
            "获取知识库信息错误，请检查是否已按照 `README.md` 中 `4 知识库初始化与迁移` 步骤完成初始化或迁移，或是否为数据库连接错误。"
        )
        st.stop()

    if (
        "selected_kb_name" in st.session_state
        and st.session_state["selected_kb_name"] in kb_names
    ):
        selected_kb_index = kb_names.index(st.session_state["selected_kb_name"])
    else:
        selected_kb_index = 0

    selected_kb = st.selectbox(
        "请选择已有文档：",
        kb_names,
        index=selected_kb_index,
    )

    if st.button("开始chat"):
        st.session_state.kb_name = selected_kb
        return selected_kb

    # 上传文件
    files = st.file_uploader(
        "上传知识文件：",
        [i for ls in LOADER_DICT.values() for i in ls],
        accept_multiple_files=True,
    )
    if files:
        return upload_and_create_kb(api, files, kb_list)
