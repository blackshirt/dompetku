from dompetku import model
from dompetku.handler import basehandler
import tornado.web
import tornado.escape

__author__ = 'blackshirtmuslim@yahoo.com'


class AuthLoginHandler(basehandler.BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))  # Change this line
            return
        self.render('login.html')

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        # The authenticate method should match a username and password
        # to a username and password hash in the database users table.
        # Implementation left as an exercise for the reader.
        auth = self._authenticate(username, password)
        if auth:
            self.set_secure_cookie("user", username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            self.redirect(u"/auth/login")

    @staticmethod
    def _authenticate(username, passwd):
        try:
            user = model.User.get(model.User.name == username)
        except model.User.DoesNotExist:
            raise tornado.web.HTTPError(500)

        if user:
            if user.password == model.gen_hash(passwd):
                return True

        return False


class AuthLogoutHandler(basehandler.BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(u"/auth/login")