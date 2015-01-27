#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Main entry for Application"""

import os
import uuid
import base64

import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options

from dompetku.handler import transaksi
from dompetku.handler import login
from dompetku.handler import register

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handler = [
            (r"/", transaksi.ListTransaksiHandler),
            (r"/trans", transaksi.TransaksiHandler),
            (r"/trans/([0-9]*)", transaksi.TransaksiByIdHandler),
            (r"/trans/create", transaksi.CreateTransaksiHandler),
            (r"/trans/new", transaksi.NewTransaksiHandler),
            (r"/trans/([0-9]*)/edit", transaksi.EditTransaksiHandler),
            (r"/trans/([0-9]*)/delete", transaksi.DeleteTransaksiHandler),
            (r"/auth/login", login.LoginHandler),
            (r"/auth/logout", login.LogoutHandler),
            (r"/register", register.RegistrasiHandler),
            (r"/api/check/user", login.CheckUserExistHandler),
            (r"/api/check/user/available", login.CheckIfUserAvailable),
            (r"/api/check/password", login.CheckPasswordHandler),
        ]

        settings = dict(
            blog_title="Your online Pocket",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            login_url="/auth/login",
            debug=True,
        )

        tornado.wsgi.WSGIApplication.__init__(self, handler, **settings)

        # Have one global connection to the blog DB across all handlers
        # self.db = model.database


# Issue : locale.Error: local query failed
# based on this suggestion http://code.google.com/p/python-for-android/issues/detail?id=1
# and this snippet from http://code.google.com/p/python-for-android/issues/attachmentText?id=1&aid=8862727350419203445&
# name=monkey_locale.py&token=ABZ6GAcpG3dWuh_F9FOJ5TnNxsz3o_XeGA%3A1411486676371
def patch_locale():
    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def getlocale(*args, **kwargs):
        return None, None

    import locale

    locale.getlocale = getlocale


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


application = Application()

if __name__ == "__main__":
    patch_locale()
    main()
