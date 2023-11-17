import hashlib
import time
import urllib

from server.common.token import Token
from server.db.repository.user_repository import get_user_by_token, create_user, get_current_user_count
from webui_pages.utils import *
from uuid import uuid4
from streamlit.runtime.scriptrunner import get_script_run_ctx
from webui_pages.states import cookie_manager
import urllib.parse

MAX_INVITED_COUNT = 100


# Define the Streamlit app
def get_state_auth_token():
    if not hasattr(st.session_state, "auth_token"):
        return None
    return st.session_state.auth_token


def get_cookie():
    cookie = "chatchat_"
    ctx = get_script_run_ctx()
    server = st.runtime.get_instance().get_client(ctx.session_id)
    print(server.cookies, 222222222)
    if cookie in server.cookies:
        value = urllib.parse.unquote(server.cookies[cookie].value)
        st.session_state.auth_token = value
        return
    else:
        return None


def del_cookie():
    cookie = "chatchat_"
    cookie_manager().delete(cookie)


def set_cookie(token):
    cookie = "chatchat_"
    cookie_manager().set(cookie, token, expires_at=datetime.now() + timedelta(days=7))
    st.session_state.auth_token = token
    time.sleep(0.5)


def gen_token():
    uid = uuid4().hex
    return uid[:6]


def get_token_info():
    num = 1 + get_current_user_count()
    if num > MAX_INVITED_COUNT:
        return "", 0

    ctx = get_script_run_ctx()
    session_id = ctx.session_id
    return hashlib.md5(session_id.encode()).hexdigest()[:6], num


def create_auth_user(token):
    user = get_user_by_token(token)
    if not user:
        try:
            create_user(nickname=f"invited_{token}", token=token)
        except Exception as ex:
            # token 冲突
            st.warning("请稍后重试")


def auth_page(api: ApiRequest):
    token, num = get_token_info()
    if not token:
        st.title("（T w T）很遗憾,邀请码已发送完毕")
        return

    st.title("登录认证")
    st.write(f"您是第({num}/{MAX_INVITED_COUNT})位幸运用户，系统已经为您分配邀请码，请妥善保存~~~完成后续认证开始体验吧!")
    st.subheader(f"邀请码: {token}")
    t1 = st.text_area(
        label="输入邀请码", key="token", max_chars=1024, help="复制邀请码到输入框中进行验证", placeholder="邀请码"
    )
    clicked = st.button("开始体验")
    if clicked:
        if t1 != token:
            st.toast("登录失败")
            st.error("登录失败~~")
            # st.rerun()
        else:
            st.toast("登录成功")
            st.success("登录成功~~")
            # 查找并创建用户
            create_auth_user(t1)
            set_cookie(t1)
            st.rerun()
