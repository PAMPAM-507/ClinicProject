import redis

from abc import ABC, abstractmethod

from ..Redis import RedisClass


class SetABC(ABC):

    @abstractmethod
    def set(self, redis_client: redis.Redis, key: str, value: str):
        pass


class SetKeyValue(SetABC):

    def set(self, redis_client: redis.Redis, key: str, value: str):
        redis_client.set(key, value)
