#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle login logout process"""

from dompetku import model
from dompetku.handler import base
from dompetku.form import LoginForm
from dompetku.utils import jsonify, generate_hash, verify_password


class LoginHandler(base.BaseHandler):
    """ Class untuk menghandle login process """

    def get(self):
        """Render form login"""
        form = LoginForm()
        self.render('login.html', form=form)

    def post(self):
        """ Check login process """
        # username = self.get_argument("name", "")
        # password = self.get_argument("password", "")
        form = LoginForm(self.request.arguments)

        if form.validate():
            username = form.data['name']
            password = form.data['password']
            auth = self._authenticate(username, password)
            if auth:
                self.clear_all_cookies()
                self.set_secure_cookie("user", username)
                self.redirect(self.get_argument('next', '/'))
                #based on this, https://github.com/tornadoweb/tornado/issues/1315
                return # thanks ben darnell
            else:
                return

        self.render('login.html', form=form)

    @staticmethod
    def _authenticate(uname, passwd):
        """check jika user dan passwordnya match dengan db"""
        user_exists = model.User.select().where(model.User.name == uname).exists()
        if user_exists:  
            # get user instance                  
            user = model.User.get(model.User.name == uname)               
            # verify dengan password dan key yang ada di database
            if verify_password(passwd, user.password, user.passkey):
                return True

        return False


class LogoutHandler(base.BaseHandler):
    """Class untuk menghandle logout process """

    def get(self):
        """just clear all cookies and redirect to login page"""
        self.clear_all_cookies()
        self.redirect("/auth/login")


class CheckUserExistHandler(base.BaseHandler):
    """ to check user exist or not, and return {'valid: True or False}"""

    def get(self):
        username = self.get_argument("name", "")
        results = {}
        valid = model.User.select().where(model.User.name == username).exists()
        results['valid'] = valid
        self.write(jsonify(results))


class CheckIfUserAvailable(base.BaseHandler):
    """ to check user exist available or not, and return {'valid: True or False}"""

    def get(self):
        username = self.get_argument("name", "")
        results = {}
        exists = model.User.select().where(model.User.name == username).exists()
        results['valid'] = not exists
        self.write(jsonify(results))


class CheckPasswordHandler(base.BaseHandler):
    """ to check user password, and return {'valid: True or False}"""

    def get(self):
        username = self.get_argument("name", "")
        passwd = self.get_argument("password", "")
        results = {}
        valid = False
        sq = model.User.select(model.User.name == username)
        if sq.where(model.User.password == generate_hash(passwd)).exists():
            valid = True

        results['valid'] = valid
        self.write(jsonify(results))