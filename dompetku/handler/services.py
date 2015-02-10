#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle json services."""
import tornado.web

from dompetku.model import Transaksi, User
from dompetku.utils import jsonify

class Transactions(tornado.web.RequestHandler):

    def get(self):
        user = User.get(User.name == self.current_user)
        all_item = Transaksi.select().where(Transaksi.user == user.uid).dicts()
        self.write(jsonify([item for item in all_item]))

    def post(self, *args, **kwargs):
        pass