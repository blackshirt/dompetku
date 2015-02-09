#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle json services."""

from tornado.web import RequestHandler
from dompetku.model import Transaksi
from dompetku.utils import jsonify

class Transactions(RequestHandler):
    def get(self, *args, **kwargs):
        all_item = Transaksi.select().dicts()
        self.write(jsonify([item for item in all_item]))

    def post(self, *args, **kwargs):
        pass