from server.db.models.user_model import UserModel
from server.db.session import with_session
from server.knowledge_base.migrate import create_tables


@with_session
def create_user(session, nickname: str, email: str = '', token: str = '') -> UserModel:
    usr = UserModel(nickname=nickname, email=email, token=token)
    session.add(usr)
    return usr


@with_session
def get_user_by_id(session, uid: int) -> UserModel:
    return session.query(UserModel).filter_by(id=uid).first()


@with_session
def get_user_by_token(session, token: int) -> UserModel:
    return session.query(UserModel).filter_by(token=token).first()


@with_session
def get_current_user_count(session) -> int:
    return session.query(UserModel).count()


@with_session
def update_user_token_by_id(session, uid: int, token: str):
    u = session.query(UserModel).filter_by(id=uid).first()
    if u:
        u.token = token


if __name__ == '__main__':
    # remove_users()
    create_tables()
    # u = create_user(nickname="hnf", email="xxxx@qq.com", token="token")
    # user = get_user_by_id(uid=u.id)
    # print(user)
