#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle user profile"""

import peewee
import tornado.web

from dompetku import model
from dompetku.handler import base
from dompetku.form import UserForm
from dompetku.utils import jsonify, generate_hash, verify_password


class UserHandler(base.BaseHandler):
    """ Class untuk menghandle login process """
    
    @tornado.web.authenticated
    def get(self, userid):
        try:
            user = model.User.get(model.User.uid == userid, model.User.name == self.current_user)
            form = UserForm(obj=user)
            self.render('user/edit.html', form=form)
            return
        except peewee.DoesNotExist:
            raise tornado.web.HTTPError(403)

    @tornado.web.authenticated
    def post(self, userid):
        user = model.User.get(model.User.uid == userid)
        if user:
            form = UserForm(self.request.arguments, obj=user)
            if form.validate():
                form.populate_obj(user)
                hashed_password = generate_hash(form.data['password'])
                user_entry = model.User.update(
                    password=hashed_password[0],
                    passkey=hashed_password[1]).where(model.User.name == self.current_user)
                user_entry.execute()
                return self.redirect('/trans')
        else:
            form = UserForm(obj=user)
        self.render('user/edit.html', form=form, obj=user)
