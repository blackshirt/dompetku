#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Base handler module"""

import tornado.web
import tornado.escape

from dompetku import model


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        """Get current_user from cookies"""
        return self.get_secure_cookie('user')

    def get_user_object(self):
        try:
            user = model.User.get(model.User.name == self.current_user)
        except model.User.DoesNotExist:
            user = self.current_user

        return user
