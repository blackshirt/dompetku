#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle json services."""

import datetime
import tornado.web

from dompetku.model import Transaksi, User
from dompetku.utils import jsonify
from dompetku.handler import base


class ApiTransactions(base.BaseHandler):

    @tornado.web.authenticated
    def get(self):
        month = datetime.date.today().month
        data = []
        user = User.get(User.name == self.current_user)
        query = Transaksi.select().where(Transaksi.user == user.uid, Transaksi.transdate.month == month)
        for item in query.dicts():
            data.append(item)
        self.write(jsonify(data))

    def post(self, *args, **kwargs):
        pass