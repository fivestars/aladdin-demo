import redis
import os

redis_conn = None
if os.environ["REDIS_CREATE"] == "true":
    redis_conn = redis.StrictRedis(
                host=os.environ["REDIS_HOST"],
                port=os.environ["REDIS_PORT"],
            )
    redis_conn.set('msg', '\n I can show you the world from Redis \n \n')