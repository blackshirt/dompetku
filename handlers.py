import datetime
import tornado.web, tornado.escape
import tornado.wsgi
from peewee import fn
import json
import model
from form import MessageForm

__all__ = ['IndexHandler', 'NewsHandler', 'EntryHandler', 'ComposeHandler', 'AuthLogoutHandler']



#from http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else json.JSONEncoder.default(obj)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        if not self.current_user:
            self.redirect("/auth/login")
            return

    def get_current_user(self):
        user_id = self.get_secure_cookie("demo_user")
        if not user_id:
            return None
        return user_id


class IndexHandler(BaseHandler):
    def get(self):
        # get random news from database
        news = model.Message.select().order_by(fn.Random()).limit(1).get()
        # self.set_header('Content-Type', 'application/json')
        self.render("index.html", news = news)


class NewsHandler(BaseHandler):
    def get(self):
        form = MessageForm(self.request.arguments)
        self.render('create_news.html', form=form)

    def post(self):
        form = MessageForm(self.request.arguments)
        self.current_user = 1
        if form.validate():
            post = model.Message.create(title=form.data['title'],
                        body=form.data['body'],
                        author=self.current_user,
                        created = datetime.datetime.now())
            post.save()
            return self.redirect('/news')
        self.render('create_news.html', form=form)

class DeleteNewsHandler(BaseHandler):
    def get(self, msgid):
        msgtodelete = model.Message.get(model.Message.mid == int(msgid))
        if msgtodelete:
            try:
                msgtodelete.delete_instance()
            except model.Message.DoesNotExist:
                raise tornado.web.HTTPError(404)
        return self.redirect('/news')

class ListNewsHandler(BaseHandler):
     def get(self):
        news = model.Message.select()
        judul = "Informasi Terbaru"
        self.render("news.html", judul=judul, data=news)

class EntryHandler(BaseHandler):
    def get(self):
        pass


class ComposeHandler(BaseHandler):
    pass


class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class AuthLogoutHandler(BaseHandler):
     def get(self):
        self.clear_cookie("demo_user")
        self.redirect(self.get_argument("next", "/"))



