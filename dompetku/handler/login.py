from dompetku import model
from dompetku.handler import base

__author__ = 'BKD Kab Kebumen'


class AuthLoginHandler(base.BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))  # Change this line
            return
        self.render('login.html')

    def post(self):
        try:
            uname = self.get_argument("username", "")
            passwd = self.get_argument("password", "")
            auth = self._authenticate(uname, passwd)

            if auth:
                self.set_current_user(uname)
                self.redirect(self.get_argument('next', '/'))
            else:
                self.render("login.html")
        except ValueError as errreason:
            errormessage = "Something wrong" + str(errreason)
            self.render("login.html")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", user)
        else:
            self.clear_cookie("user")

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


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument('next', '/'))