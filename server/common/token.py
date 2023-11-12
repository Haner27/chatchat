__EXPIRED_AT_KEY__ = '__expire_at__'
__SALT_KEY__ = '__salt__'
__SALT__ = 'chat_chat_salt_salt'

import json
from base64 import b64encode, b64decode
import time
from hashlib import md5
from configs import logger


class TokenException(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return f'<TokenException: {self.__msg}>'


class TokenPayload:
    def __init__(self, **kwargs):
        self.__payload_dict = kwargs
        for k, v in self.__payload_dict.items():
            setattr(self, k, v)

    def to_dict(self):
        return self.__payload_dict


class Token:
    def __init__(self, token: str):
        try:
            if not token or not isinstance(token, str):
                raise TokenException('token format is invalid')
            self.__token = token
            segments = self.__token.split(".")
            if len(segments) != 2:
                raise TokenException('token format is invalid')

            payload_segment, self.__sign = segments
            payload = self.extract_payload(payload_segment)
            self.__payload = TokenPayload(**payload)
        except Exception as ex:
            self.__token = ''
            self.__sign = ''
            self.__payload = None

    @classmethod
    def gen(cls, expire: int, **kwargs):
        kwargs[__EXPIRED_AT_KEY__] = int(time.time()) + expire
        kwargs.update({
            __EXPIRED_AT_KEY__: int(time.time()) + expire,
            __SALT_KEY__: __SALT__,
        })
        token = f'{cls.encode_payload(kwargs)}.{cls.get_sign(kwargs)}'
        return cls(token=token)

    def extract_payload(self, payload_encoded: str) -> dict:
        d = dict()
        for k, v in self.decode_payload(payload_encoded).items():
            d[k] = v
        return d

    @staticmethod
    def get_sign(payload: dict) -> str:
        sorted_str = '&'.join([f'{k}={v}' for k, v in sorted(payload.items(), key=lambda a: a[0])])
        s = md5()
        s.update(sorted_str.encode('utf-8'))
        return s.hexdigest()

    @staticmethod
    def encode_payload(payload: dict) -> str:
        return b64encode(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode_payload(payload_encoded: str) -> dict:
        return json.loads(b64decode(payload_encoded))

    @property
    def is_valid(self) -> bool:
        try:
            if not self.__payload:
                return False

            sign = self.get_sign(self.__payload.to_dict())
            if self.__sign != sign:
                raise TokenException('token\'s sign is invalid')

            if self.expired_at < int(time.time()):
                raise TokenException('token is expired')

        except Exception as ex:
            logger.error(ex)
            return False
        return True

    @property
    def token(self) -> str:
        return self.__token

    @property
    def expired_at(self) -> int:
        return self.__payload.to_dict().get(__EXPIRED_AT_KEY__, 0)

    @property
    def expired_at_str(self) -> str:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.expired_at))

    @property
    def ttl(self) -> int:
        ex = self.expired_at
        ts = int(time.time())
        if ex < ts:
            return -1
        return ex - ts

    @property
    def payload(self):
        return self.__payload

    def __str__(self) -> str:
        return f'<Token: {self.__token}>'


if __name__ == '__main__':
    t0 = Token.gen(2, name='hnf', age=100, gender='male')
    print(t0.expired_at, t0.ttl, t0.payload)
    print(t0.payload.name, t0.payload.age, t0.payload.gender, t0.payload.to_dict())
    t = Token(t0.token)
    print(t.is_valid)
    print(t.payload.name, t.payload.age, t.payload.gender, t.payload.to_dict())
    time.sleep(1)
    print(t.is_valid)
    time.sleep(3)
    print(t.is_valid)
