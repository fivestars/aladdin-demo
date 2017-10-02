import falcon
from redis_utils.redis_connection import redis_conn

class BaseResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ('\n I can show you the world \n \n')

class RedisResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        msg = redis_conn.get('msg')
        resp.body = (msg)

app = falcon.API()

if redis_conn:
    app.add_route('/app/redis', RedisResource())
app.add_route('/app', BaseResource())
