import falcon
from redis_connection import redis_conn
from math import sqrt

class BaseResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ('\n I can show you the world \n \n')

class RedisResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        msg = redis_conn.get('msg')
        resp.body = (msg)

class busyResource(object):
    # A computation intense resource to demonstrate autoscaling
    def on_get(self, req, resp):
        n = 0.0001
        for i in range(1000000):
            n += sqrt(n)
        resp.body = ('busy busy...')

app = falcon.API()

if redis_conn:
    app.add_route('/redis', RedisResource())
app.add_route('/', BaseResource())
app.add_route('/busy', busyResource())
