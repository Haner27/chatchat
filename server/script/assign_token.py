from server.db.repository.user_repository import create_user, get_user_by_id
from server.common.token import Token

# 授权脚本
DAYS = 86400

users = [
    dict(nickname="hnf", email="369685930@qq.com"),
    dict(nickname="haner27", email="haner27@126.com"),
]

if __name__ == '__main__':
    # for user in users:
    #     user.update(token=Token.gen(DAYS * 7, **user).token)
    #     u = create_user(**user)
    #     print(u)

    u1 = get_user_by_id(18)
    print(u1, u1.token)
    token1 = Token(u1.token)
    print(token1.payload.nickname, token1.payload.email)