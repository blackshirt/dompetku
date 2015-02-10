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
        all_item = Transaksi.select().dicts()
        self.write(jsonify([item for item in all_item]))

    def post(self, *args, **kwargs):
        pass