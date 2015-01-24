#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle login logout process"""

import tornado.web
import tornado.escape

from dompetku import model
from dompetku.handler import basehandler


class AuthLoginHandler(basehandler.BaseHandler):
    """ Class untuk menghandle login process """
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        
        auth = self._authenticate(username, password)
        if auth:
            self.set_secure_cookie("user", username)
            self.redirect('/trans')
        else:
            self.clear_cookie('user')
            self.redirect("/auth/login")

    @staticmethod
    def _authenticate(uname, passwd):
        '''check jika user dan passwordnya match dengan db'''
        try:
            user = model.User.get(model.User.name == uname)
        except model.User.DoesNotExist:
            user = None

        if user:
            if user.password == model.gen_hash(passwd):
                return True
        
        return False


class AuthLogoutHandler(basehandler.BaseHandler):
    """Class untuk menghandle logout process """
    def get(self):
        self.clear_all_cookies()
        self.redirect("/auth/login")