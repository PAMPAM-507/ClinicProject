import redis
import copy


class RedisClass:

    def __init__(self, host="localhost", port=6379, db=0):
        self.__host = host
        self.__port = port
        self.__db = db

    @property
    def redis_client(self):
        return self.__redis_client

    @redis_client.setter
    def redis_client(self, value):
        self.__redis_client = value

    def __enter__(self):
        self.redis_client = redis.Redis(host=self.__host, port=self.__port, db=self.__db)
        return self.redis_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_client.close()
