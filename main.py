import tornado.web
import tornado.wsgi
import handlers
import os
import model
import tornado.options
import tornado.httpserver
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handler = [
            (r"/", handlers.IndexHandler),
            (r"/news/new", handlers.NewsHandler),
            (r"/news", handlers.ListNewsHandler),
            (r"/entry/([^/]+)", handlers.EntryHandler),
            (r"/compose", handlers.ComposeHandler),
            (r"/auth/login", handlers.AuthLoginHandler),
            (r"/auth/logout", handlers.AuthLogoutHandler),
        ]

        settings = dict(
            blog_title="Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )

        tornado.wsgi.WSGIApplication.__init__(self, handler, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = model.database


# Issue : locale.Error: local query failed
# based on this suggestion http://code.google.com/p/python-for-android/issues/detail?id=1
# and this snippet from http://code.google.com/p/python-for-android/issues/attachmentText?id=1&aid=8862727350419203445&name=monkey_locale.py&token=ABZ6GAcpG3dWuh_F9FOJ5TnNxsz3o_XeGA%3A1411486676371
def patch_locale():
    def getlocale(*args, **kwargs):
        return (None, None)
    import locale
    locale.getlocale=getlocale

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

#application = Application()

if __name__ == "__main__":
    patch_locale()
    main()