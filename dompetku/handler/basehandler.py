import tornado.web
import tornado.escape
from dompetku import model

__author__ = 'BKD Kab Kebumen'


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user_id = self.get_secure_cookie("user_identity")
        if not user_id:
            return None
        return user_id

    def get(self):
        if not self.current_user:
            self.redirect("/auth/login")
        return
