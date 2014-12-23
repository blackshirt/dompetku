import tornado.web

__author__ = 'BKD Kab Kebumen'


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