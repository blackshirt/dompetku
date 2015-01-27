#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle registration process."""

import tornado.web

from dompetku import model
from dompetku.form import RegistrasiForm
from dompetku.utils import jsonify, generate_hash
from dompetku.handler import basehandler



class RegistrasiBaseHandler(basehandler.BaseHandler):
    """ Class dasar untuk Registrasi"""
    def initialize(self):
        self.model = model.User
        self.user = self.get_user_object()


class RegistrasiHandler(RegistrasiBaseHandler):
    
    def get(self):
        form = RegistrasiForm(self.request.arguments)
        self.render("register.html", form=form)
    
    def post(self):
        """Post new data to our rpest service as a JSON"""
        form = RegistrasiForm(self.request.arguments)
        
        if form.validate():
            hashed_password = generate_hash(form.data['password'])
            reg_entry = model.User.create(
                        name = form.data['name'],
                        realname = form.data['realname'],
                        email = form.data['email'],
                        password = hashed_password[0],
                        passkey = hashed_password[1]
                        )
            reg_entry.save()
            #self.write({'result': 'OK'})
            self.redirect('/')
        self.render('register.html', form=form)
