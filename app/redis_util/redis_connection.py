import redis
import os

redis_conn = None
# TODO: Remove once external (aws) redis script is in place
if os.environ["REDIS_CREATE"] == "true":
    redis_conn = redis.StrictRedis(
                host=os.environ["REDIS_HOST"],
                port=os.environ["REDIS_PORT"],
            )
