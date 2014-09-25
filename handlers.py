import datetime
import tornado.web, tornado.escape
import tornado.wsgi
import peewee
import model
from peewee import fn
import json

__all__ = ['IndexHandler', 'NewsHandler', 'EntryHandler', 'ComposeHandler', 'AuthLogoutHandler']



#from http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else json.JSONEncoder.default(obj)

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
        msg = news._data
        # self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(msg, default=date_handler))

    
class HomeHandler(BaseHandler):
     def get(self):
        self.render("base.html")


class NewsHandler(BaseHandler):
     def get(self):
        news = model.Message.select()
        title = "Informasi Terbaru"
        self.render("news.html", title=title, data=news)


class EntryHandler(BaseHandler):
    pass


class ComposeHandler(BaseHandler):
    pass


class AuthLoginHandler(BaseHandler):
    pass


class AuthLogoutHandler(BaseHandler):
    pass



