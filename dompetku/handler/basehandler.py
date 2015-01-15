import tornado.web
import tornado.escape
from dompetku import model



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



