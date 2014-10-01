import datetime
import tornado.web, tornado.escape
import tornado.wsgi
import model
from peewee import fn
import json
import os

__all__ = ['IndexHandler', 'NewsHandler', 'EntryHandler', 'ComposeHandler', 'AuthLogoutHandler']


#from http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

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
        news = model.Message.select().order_by(fn.Random()).limit(1).get()
        msg = {
            'id' : news.mid,
            'title': news.title,
            'body': news.body,
            'author': news.author.name,
            'created': news.created,
            }
        # self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(msg, default=date_handler))

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



