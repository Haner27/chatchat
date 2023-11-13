from sqlalchemy import Column, Integer, String, DateTime, func

from server.db.base import Base, engine


class UserModel(Base):
    """
    用户表
    """
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户 ID')
    nickname = Column(String(50), comment='nickname')
    email = Column(String(50), comment='email')
    token = Column(String(256), comment='token')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), comment='修改时间')

    def __repr__(self):
        return f"<UserModel(id='{self.id}', nickname='{self.nickname}',email='{self.email}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'email': self.email,
            'token': self.token,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
