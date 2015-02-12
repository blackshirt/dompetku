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


class TransaksiContainer(object):
    def __init__(self, user):
        self.user = user

    def find_one(self, tid):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            trn = Transaksi.select().where(Transaksi.tid == tid)
            if trn.exists():
                data = trn.get() # Transaksi instance
                return data

        return None

    def find_data(self, *kondisi):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            trn = Transaksi.select().where(*kondisi)
            if trn.exists():
                return trn # Transaksi QueryResultWrapper

        return None


class DataResponse(TransaksiContainer):
    def __init__(self, user):
        self.user = user
        super().__init__(self.user)

    def get_one(self, tid):
        data = self.find_one(tid)
        if data is not None:
            results = {'tid': data.tid, 'user': data.user.name, 'info': data.info,
                'amount': data.amount,
                'transdate': data.transdate,
                'memo': data.memo
            }

            return results # dict of transaksi item

    def get_data(self, *kondisi):
        temporary = {}
        results = []
        data = self.find_data(*kondisi)
        for item in data:
            temporary['tid'] = item.tid
            temporary['user'] = item.user.name  # !! remember!, this set to name, not uid
            temporary['info'] = item.info
            temporary['amount'] = item.amount
            temporary['transdate'] = item.transdate
            temporary['memo'] = item.memo
            results.append(temporary)

        return results # list of dict of transaksi item


class ApiTransactions(base.BaseHandler):
    def initialize(self):
        self.dsc = DataResponse(self.current_user)

    @tornado.web.authenticated
    def get(self, *kondisi):
        if kondisi:
            data = self.dsc.get_data(*kondisi)
        else:
            today = datetime.date.today()
            cur_month = today.month
            kondisi = (Transaksi.transdate.month == cur_month)
            data = self.dsc.get_data(kondisi)
        self.write(jsonify(data))

    def post(self, *args, **kwargs):
        pass