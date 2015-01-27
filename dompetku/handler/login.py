#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle login logout process"""

from dompetku import model
from dompetku.handler import basehandler
from dompetku.form import LoginForm
from dompetku.utils import jsonify, generate_hash, verify_password


class LoginHandler(basehandler.BaseHandler):
    """ Class untuk menghandle login process """

    def get(self):
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
                self.set_secure_cookie("user", username)
                self.redirect('/trans')
            else:
                self.clear_cookie('user')
        self.render('login.html', form=form)

    @staticmethod
    def _authenticate(uname, passwd):
        """check jika user dan passwordnya match dengan db"""
        try:
            user = model.User.get(model.User.name == uname)
        except model.User.DoesNotExist:
            user = None

        if user:
            if verify_password(passwd, user.password, user.passkey):
                return True

        return False


class LogoutHandler(basehandler.BaseHandler):
    """Class untuk menghandle logout process """

    def get(self):
        self.clear_all_cookies()
        self.redirect("/auth/login")


class CheckUserExistHandler(basehandler.BaseHandler):
    """ to check user exist or not, and return {'valid: True or False}"""

    def get(self):
        username = self.get_argument("name", "")
        results = {}
        valid = model.User.select().where(model.User.name == username).exists()
        results['valid'] = valid
        self.write(jsonify(results))


class CheckIfUserAvailable(basehandler.BaseHandler):
    """ to check user exist available or not, and return {'valid: True or False}"""

    def get(self):
        username = self.get_argument("name", "")
        results = {}
        exists = model.User.select().where(model.User.name == username).exists()
        results['valid'] = not exists
        self.write(jsonify(results))


class CheckPasswordHandler(basehandler.BaseHandler):
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