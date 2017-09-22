import os
import falcon
from redis_connection import redis_conn

class BaseResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ('\n I can show you the world \n \n')

class RedisResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        foo = redis_conn.get('msg')
        resp.body = (foo)

app = falcon.API()

app.add_route('/redis', RedisResource())
app.add_route('/', BaseResource())


