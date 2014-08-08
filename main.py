import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello  from second Tornado")

application = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
])