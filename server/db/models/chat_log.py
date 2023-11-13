from sqlalchemy import Column, Integer, DateTime, func, Text, String

from server.db.base import Base


class ChatLogModel(Base):
    """
    聊天日志
    """
    __tablename__ = 'chat_log'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='聊天记录 ID')
    uid = Column(Integer, comment='用户 ID')
    req = Column(Text, comment='用户请求')
    resp = Column(Text, comment='ai 响应')
    dialogue_mode = Column(String(50), comment='对话模式')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), comment='修改时间')

    def __repr__(self):
        return f'<ChatLogModel(id={self.id})>'
