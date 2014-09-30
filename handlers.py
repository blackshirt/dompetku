import datetime
import tornado.web, tornado.escape
import tornado.wsgi
#from peewee import fn
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
        user_json = self.get_secure_cookie("user")
        if user_json:
            return user_json
        else:
            return None

    def get_common_info(self):
        commoninfo = {
            'user' : self.get_current_user(),
        }
        return commoninfo


class HomeHandler(BaseHandler):
    def get(self):
        self.render("base.html", commoninfo = self.get_common_info())


#from: http://stackoverflow.com/questions/6514783/tornado-login-examples-tutorials
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user() == None:
            self.render("login.html", errormessage="", commoninfo=self.get_common_info())
        else:
            self.redirect("/")

    def post(self):
        try:
            uname = self.get_argument("username", "")
            passwd = self.get_argument("password", "")
            auth = self.authenticate(uname, passwd)

            if auth:
                self.set_current_user(uname)
                self.redirect("/", commoninfo=self.get_common_info())
            else:
                errormessage = "wrong password or username."
                self.render("login.html", errormessage=errormessage, commoninfo=self.get_common_info())
        except ValueError as errreason:
            errormessage = "Something wrong"+errreason
            self.render("login.html", errormessage=errormessage, commoninfo=self.get_common_info())

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", user)
        else:
            self.clear_cookie("user")

    def authenticate(self, uname, passwd):
        if (uname == 'a') and (passwd == 'a'):
            return True
        else:
            return False


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")





#__________________________________________________________________________________________________________#_#
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
                                        created=datetime.datetime.now())
            post.save()
            return self.redirect('/news')
        self.render('create_news.html', form=form)


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



