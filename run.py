import redis

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("I can show you the world")

def make_app():
    # r = redis.StrictRedis(host='aladdin-demo-redis')
    # print r.dbsize()
    # r.set("message", "I can show you the world")
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(7892)
    tornado.ioloop.IOLoop.current().start()
