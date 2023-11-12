from server.db.models.user_model import UserModel
from server.db.session import with_session
from server.knowledge_base.migrate import create_tables


@with_session
def create_user(session, nickname: str, email: str, token: str) -> UserModel:
    usr = UserModel(nickname=nickname, email=email, token=token)
    session.add(usr)
    return usr


@with_session
def get_user_by_id(session, uid: int) -> UserModel:
    return session.query(UserModel).filter_by(id=uid).first()


if __name__ == '__main__':
    create_tables()
    u = create_user(nickname="hnf", email="xxxx@qq.com", token="token")
    user = get_user_by_id(uid=u.id)
    print(user)
