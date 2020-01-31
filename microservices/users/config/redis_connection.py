import os

import redis


class RedisService:
    def __init__(self, **kwargs):
        self.connection = self.connect(**kwargs)

    def connect(self, **kwargs):
        redis_con = redis.Redis(host=kwargs["host"], port=kwargs["port"])
        return redis_con



    def set(self, key, value):
        self.connection.set(key, value)

    def get(self, key):
        print(key)
        value = self.connection.get(key)
        return value

    def disconnect(self):
        self.connection.close()

con = RedisService(host='localhost',
    port=6379)