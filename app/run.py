import falcon
import json
from math import sqrt


class BaseResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = '\n I can show you the world \n \n'


class BusyResource(object):
    # A computation intense resource to demonstrate autoscaling
    def on_get(self, req, resp):
        n = 0.0001
        for i in range(1000000):
            n += sqrt(n)
        resp.body = 'busy busy...'


class PingResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = os.environ.get('MESSAGE')


app = falcon.API()

app.add_route('/app', BaseResource())
app.add_route('/app/busy', BusyResource())
app.add_route('/ping', PingResource())
