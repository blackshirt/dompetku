import datetime
import tornado.web
import tornado.escape
import tornado.wsgi
import model
import json
import urllib

from peewee import fn
from form import MessageForm, TipeTransaksiForm, TransaksiForm
from utils import jsonify

__all__ = ['HomeHandler', 'NewsHandler', 'AuthLogoutHandler']

class BaseHandler(tornado.web.RequestHandler):

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
        listtrans = model.Transaksi.select()
        form = TransaksiForm(self.request.arguments)
        self.render("account.html", form = form, trans = listtrans)


# from: http://stackoverflow.com/questions/6514783/tornado-login-examples-tutorials
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))  # Change this line
            return
        errormessage = "please login"
        self.render('login.html', errormessage=errormessage)

    def post(self):
        try:
            uname = self.get_argument("username", "")
            passwd = self.get_argument("password", "")
            auth = self._authenticate(uname, passwd)

            if auth:
                self.set_current_user(uname)
                self.redirect(self.get_argument('next', '/'))
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

    def _authenticate(self, uname, passwd):
        try:
            user = model.User.get(model.User.name == uname)
        except model.User.DoesNotExist:
            raise tornado.web.HTTPError(500)

        if user:
            if user.password == model.gen_hash(passwd):
                return True

        return False

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument('next', '/'))

class ListNewsHandler(BaseHandler):
    def get(self):
        news = model.Message.select()
        judul = "Informasi Terbaru"
        self.render("news/list.html", judul=judul, data=news)

    @tornado.web.authenticated
    def post(self):
        form = MessageForm(self.request.arguments)
        if form.validate():
            post = model.Message.create(title=form.data['title'],
                                        body=form.data['body'],
                                        author=1,
                                        created=form.data['created'], )
            post.save()
            return self.redirect('/news')

class NewsHandler(BaseHandler):
    def get(self):
        judul = "Informasi Terbaru"
        form = MessageForm(self.request.arguments)
        self.render('news/create.html', judul=judul, form=form)

    @tornado.web.authenticated
    def post(self):
        form = MessageForm(self.request.arguments)
        if form.validate():
            post = model.Message.create(title=form.data['title'],
                                        body=form.data['body'],
                                        author=1,
                                        created=form.data['created'], )
            post.save()
            return self.redirect('/news')

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

class ListTransaksiHandler(BaseHandler):
    def get(self):
        pass

class TransaksiBaseHandler(BaseHandler):
    def initialize(self):
        self.container =  model.Transaksi

class TransaksiByIdHandler(TransaksiBaseHandler):

    def get(self, tid):
        data = self.container.get(self.container.tid==int(tid))
        results = data._data
        self.set_header('Content-Type', 'application/json')
        self.write(jsonify(results))

class TransaksiHandler(TransaksiBaseHandler):

    def get(self, transid=None):
        transid = self.get_argument('transid', None)
        if transid:
            try:
                item = self.container.get(self.container.tid==int(transid))
                results = item._data
                self.set_header('Content-Type', 'application/json')
                self.write(jsonify(results))
            except self.container.DoesNotExist:
                results = {'transid' : None}
                self.write(jsonify(results))
        else:
            all_item = self.container.select().dicts()
            results = [item for item in all_item]
            self.set_header('Content-Type', 'application/json')
            self.write(jsonify(results))


    def post(self):
        """Post new data to our rest service as a JSON"""
        data = json.loads(self.request.body.decode('utf-8'))
        self.write(data)


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


class EditTipeTransaksiHandler(BaseHandler):
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

