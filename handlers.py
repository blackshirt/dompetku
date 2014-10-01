import datetime
import tornado.web
import tornado.escape
import tornado.wsgi
import json
import model
from hashlib import sha512
from form import MessageForm

from peewee import fn
import model
from form import MessageForm, TipeTransaksiForm


__all__ = ['IndexHandler', 'NewsHandler', 'EntryHandler', 'ComposeHandler', 'AuthLogoutHandler']


# from http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj



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
        self.render("base.html")


#from: http://stackoverflow.com/questions/6514783/tornado-login-examples-tutorials
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user() == None:
            self.render("login.html", errormessage="")
        else:
            self.redirect("/")

    def post(self):
        try:
            uname = self.get_argument("username", "")
            passwd = self.get_argument("password", "")
            auth = self.authenticate(uname, passwd)

            if auth:
                self.set_current_user(uname)
                self.redirect("/")
            else:
                errormessage = "wrong password or username."
                self.render("login.html", errormessage=errormessage)
        except ValueError as errreason:
            errormessage = "Something wrong"+errreason
            self.render("login.html", errormessage=errormessage)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", user)
        else:
            self.clear_cookie("user")

    def authenticate(self, uname, passwd):
        dbpasswd = model.User.select(passwd).where(model.User.name == uname)
        passwdhash = sha512(passwd.encode('utf-8')).hexdigest()
        if dbpasswd:
            if (dbpasswd == passwdhash):
                return True

        return False


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class NewsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = MessageForm(self.request.arguments)
        self.render('create_news.html', form=form)

    @tornado.web.authenticated
    def post(self):
        form = MessageForm(self.request.arguments)
        if form.validate():
            post = model.Message.create(title=form.data['title'],
                                        body=form.data['body'],
                                        author=2,
                                        created=datetime.datetime.now())
            post.save()
            return self.redirect('/news')
        self.render('create_news.html', form=form)

class EditTransHandler(BaseHandler):
    def get(self, tid):
        trans = model.TipeTransaksi.get(model.TipeTransaksi.ttid == tid)
        form = TipeTransaksiForm(obj=trans)
        self.render('transedit.html', form=form)

    def post(self, tid):
        post = model.TipeTransaksi.get(model.TipeTransaksi.ttidid == tid)
        if post:
            form = TipeTransaksiForm(self.request.arguments, obj=post)
            if form.validate():
                form.populate_obj(post)
                post.save()
                return self.redirect('/news')
        else:
            form = TipeTransaksiForm(obj=post)
        self.render('transedit.html', form=form)


class EditNewsHandler(BaseHandler):
    def get(self, msgid):
        post = model.Message.get(model.Message.mid == msgid)
        form = MessageForm(obj=post)
        self.render('newsedit.html', form=form)

    def post(self, msgid):
        post = model.Message.get(model.Message.mid == msgid)
        if post:
            form = MessageForm(self.request.arguments, obj=post)
            if form.validate():
                form.populate_obj(post)
                post.save()
                return self.redirect('/news')
        else:
            form = MessageForm(obj=post)
        self.render('newsedit.html', form=form, obj=post)


class DeleteNewsHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, mid):
        msgtodelete = self.get_argument('mid')
        msgid = model.Message.get(model.Message.mid == int(msgtodelete))
        if msgid:
            try:
                msgid.delete_instance()
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




