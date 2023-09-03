from abc import ABC, abstractmethod

from ..Redis import RedisClass

import redis


class GetABC(ABC):

    @abstractmethod
    def get(self, redis_client: redis.Redis, key: str):
        pass


class GetByKey(GetABC):

    def get(self, redis_client: redis.Redis, key: str):
        return redis_client.get(key)
