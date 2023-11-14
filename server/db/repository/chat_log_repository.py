from server.db.models.chat_log import ChatLogModel
from server.db.session import with_session
from server.knowledge_base.migrate import create_tables


@with_session
def create_chat_log(
    session, uid: int, req: str, resp: str, dialogue_mode: str
) -> ChatLogModel:
    chat_log = ChatLogModel(uid=uid, req=req, resp=resp, dialogue_mode=dialogue_mode)
    session.add(chat_log)
    return chat_log


@with_session
def query_chat_logs(
    session, uid: int = 0, offset: int = 0, limit: int = 10
) -> list[ChatLogModel]:
    return session.query(ChatLogModel).offset(offset).limit(limit).all()


if __name__ == "__main__":
    # create_tables()
    # u = create_chat_log(uid=1, req="你好，请说出我的名字2", resp="不知道2", dialogue_mode="happy")
    for clog in query_chat_logs():
        print(clog.id, clog.uid, clog.req, clog.resp, clog.dialogue_mode)
