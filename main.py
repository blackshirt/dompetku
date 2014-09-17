import tornado.web
import tornado.wsgi
import handlers



class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handlers = [
            (r"/", handlers.IndexHandler),
            (r"/news", handlers.NewsHandler),
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

        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = model.database


if __name__ : '__main__':
    application = Application()
    application.listen(8888)
    tornado.ioloop.instance(application).start()
