from dompetku import model
from dompetku.handler import basehandler
import tornado.web

__author__ = 'blackshirtmuslim@yahoo.com'


class AuthLoginHandler(basehandler.BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        try:
            uname = self.get_argument("username", "")
            passwd = self.get_argument("password", "")
            auth = self._authenticate(uname, passwd)

            if auth:
                self.set_secure_cookie("user_identity", uname)
                self.redirect(self.get_argument('next', '/'))
            else:
                self.clear_all_cookies()
                self.write("Error in login")
        except ValueError:
            self.clear_all_cookies()

    @staticmethod
    def _authenticate(uname, passwd):
        try:
            user = model.User.get(model.User.name == uname)
        except model.User.DoesNotExist:
            raise tornado.web.HTTPError(500)

        if user:
            if user.password == model.gen_hash(passwd):
                return True

        return False


class AuthLogoutHandler(basehandler.BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(self.get_argument('next', '/'))