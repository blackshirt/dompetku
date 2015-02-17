#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle json services."""

import datetime
import json
import tornado.web
import tornado.escape

from dompetku.handler import base
from dompetku.utils import jsonify
from dompetku.model import Transaksi, User


class TransaksiContainer(object):
    def __init__(self, user):
        self.user = user

    def find_one(self, tid):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            user = cur_user.get()
            trn = Transaksi.select().where(Transaksi.user == user.uid, Transaksi.tid == tid)
            if trn.exists():
                data = trn.get() # Transaksi instance
                return data

        return None

    def find_data(self, *expr):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            user = cur_user.get()
            trn = Transaksi.select().where(Transaksi.user == user.uid, *expr)
            
            return trn # Transaksi QueryResultWrapper

        return None


class DataSources(TransaksiContainer):
    def __init__(self, user):
        self.user = user
        super().__init__(self.user)

    def get_one(self, tid):
        data = self.find_one(tid)
        if data is not None:
            results = {
                'tid': data.tid, 
                'user': data.user.name, 
                'info': data.info,
                'amount': data.amount,
                'transdate': data.transdate,
                'memo': data.memo
            }

            return results # dict of transaksi item

    def get_data(self, *expr):
        temporary = {}
        results = []
        data = self.find_data(*expr)
        
        for item in data:
            temporary = {
                  'tid': item.tid,
                  'user': item.user.name,
                  'info': item.info,
                  'transdate': item.transdate,
                  'amount': item.amount,
                  'memo': item.memo
                 }                
            results.append(temporary)

        return results # list of dict of transaksi item


class ApiTransactions(base.BaseHandler):
    def initialize(self):
        self.dsc = DataSources(self.current_user)

    @tornado.web.authenticated
    def get(self, *kondisi):
        if kondisi:
            data = self.dsc.get_data(*kondisi)
        else:
            # get data bulan sekarang
            today = datetime.date.today()
            cur_month = today.month
            expr = (Transaksi.transdate.month == cur_month,)
            data = self.dsc.get_data(expr)
        
        self.write(jsonify(data))

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        for row in data:
            info = data.get('info')
            amount = data.get('amount')
            memo = data.get('memo')

        user = self.current_user
        data.update({'user':user})
        self.write(jsonify(data))