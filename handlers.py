import datetime
import tornado.web
import tornado.escape
import tornado.wsgi
# import json
import model
from hashlib import sha512
#from form import MessageForm

from peewee import fn
from form import MessageForm, TipeTransaksiForm, TransaksiForm


__all__ = ['HomeHandler', 'NewsHandler', 'AuthLogoutHandler']


# from http://blog.codevariety.com/2012/01/06/python-serializing-dates-datetime-datetime-into-json/
def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, edit=False):
        self.edit = edit

    def get(self):
        if not self.current_user:
            self.redirect("/auth/login")
        return

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if user:
            return user
        else:
            return None

    @property
    def db(self):
        return self.application.db

    def get_common_info(self):
        commoninfo = {
            'user': self.get_current_user(),
        }
        return commoninfo


class HomeHandler(BaseHandler):
    def get(self):
        news = model.Message.select().order_by(fn.Random()).limit(1).get()
        self.render("index.html", news=news)


# from: http://stackoverflow.com/questions/6514783/tornado-login-examples-tutorials
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user() is None:
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
                self.redirect("/news")
            else:
                errormessage = "wrong password or username."
                self.render("login.html", errormessage=errormessage)
        except ValueError as errreason:
            errormessage = "Something wrong" + str(errreason)
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
            if dbpasswd == passwdhash:
                return True

        return False


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/news")


class ListNewsHandler(BaseHandler):
    def get(self):
        news = model.Message.select()
        judul = "Informasi Terbaru"
        self.render("news/list.html", judul=judul, data=news)

class NewsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = MessageForm(self.request.arguments)
        self.render('news/create.html', form=form)

    @tornado.web.authenticated
    def post(self):
        form = MessageForm(self.request.arguments)
        if form.validate():
            post = model.Message.create(title=form.data['title'],
                                        body=form.data['body'],
                                        author=4,
                                        created=form.data['created'],)
            post.save()
            return self.redirect('/news')
        self.render('news/create.html', form=form)


class EditNewsHandler(BaseHandler):
    def get(self, msgid):
        post = model.Message.get(model.Message.mid == msgid)
        form = MessageForm(obj=post)
        self.render('news/edit.html', form=form)

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
        self.render('news/edit.html', form=form, obj=post)


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


class ListTransaksiHandler(BaseHandler):

    def get(self):
        listtrans = model.Transaksi.select()
        number = listtrans.count()
        kwargs = {}
        page_number = int(self.get_argument('page', default=1))
        items_per_page = int(number / 2)
        kwargs.update(number=number, page_number=page_number, items_per_page=items_per_page)
        query = listtrans.paginate(page_number, items_per_page)
        self.render("transaksi/list.html", trans=query, kwargs=kwargs)


class TransaksiHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render('transaksi/create.html', form=form)

    @tornado.web.authenticated
    def post(self):
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = model.Transaksi.create(info=form.data['info'],
                                          user = 1,
                                          type=2,
                                          amount=form.data['amount'],
                                          transdate=datetime.datetime.now(),
                                          memo=form.data['memo'])
            post.save()
            return self.redirect('/trans')
        self.render('transaksi/create.html', form=form)

class EditTransaksiHandler(BaseHandler):
    def get(self, transid):
        post = model.Transaksi.get(model.Transaksi.tid == transid)
        form = TransaksiForm(obj=post)
        self.render('transaksi/edit.html', form=form)

    def post(self, transid):
        post = model.Transaksi.get(model.Transaksi.tid == transid)
        if post:
            form = TransaksiForm(self.request.arguments, obj=post)
            if form.validate():
                form.populate_obj(post)
                post.save()
                return self.redirect('/trans')
        else:
            form = TransaksiForm(obj=post)
        self.render('transaksi/edit.html', form=form, obj=post)

