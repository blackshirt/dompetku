import datetime
import tornado.web, tornado.escape
import tornado.wsgi
import os
import model
from peewee import fn
import json

__all__ = ['application', 'Application', 'IndexHandler', 'NewsHandler', 'EntryHandler', 'ComposeHandler', 'AuthLogoutHandler']

class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/news", NewsHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
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

        tornado.wsgi.WSGIApplication.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = model.database


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("blogdemo_user")

        if not user_id:
            return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))


class IndexHandler(BaseHandler):
    def get(self):
        # get random news from database
        news = model.Category.select().order_by(fn.Random()).limit(1).get()
        data = news._data
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))

    def post(self):
        _id = () + 1
        timestamp = datetime.now()
        body = urlparse.parse_qs(self.request.body)
        for key in body:
            body[key] = body[key][0]
        blog = {
            "_id": _id,
            "title": body['title'],
            "tags": body['tags'],
            "category": body['category'],
            "timestamp": timestamp
        }
        self.db.blogs.insert(blog)
        location = "/blog/" + str(_id)
        self.set_header('Content-Type', 'application/json')
        self.set_header('Location', location)
        self.set_status(201)
        self.write(dumps(blog))

    def put(self, blogid):
        # # Convert unicode to int
        _id = int(blogid)
        timestamp = datetime.now()
        body = urlparse.parse_qs(self.request.body)
        for key in body:
            body[key] = body[key][0]
        blog = {
            "title": body['title'],
            "tags": body['tags'],
            "category": body['category'],
            "timestamp": timestamp
        }
        self.db.blogs.update({"_id": _id}, {"$set": blog})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(blog))

    def delete(self, blogid):
        # # Convert unicode to int
        _id = int(blogid)
        blog = {
            "title": None,
            "tags": [],
            "category": [],
            "timestamp": None,
        }
        self.db.blogs.update({"_id": _id}, {"$set": blog})
        self.set_header('Content-Type', 'application/json')
        self.write(dumps(blog))


class NewsHandler(BaseHandler):
    pass


class EntryHandler(BaseHandler):
    pass


class ComposeHandler(BaseHandler):
    pass


class AuthLoginHandler(BaseHandler):
    pass


class AuthLogoutHandler(BaseHandler):
    pass

application = Application()


