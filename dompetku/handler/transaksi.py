#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Module to handle daily transaction activities."""

import datetime

import peewee
import tornado.web
from tornado.web import HTTPError

from peewee import fn

from dompetku.handler import base
from dompetku.utils import jsonify
from dompetku.form import TransaksiForm
from dompetku.model import Transaksi, User



class TransaksiContainer(object):

    def __init__(self, user):
        self.user = user

    def find_one(self, tid):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            trn = Transaksi.select().where(Transaksi.tid == tid)
            if trn.exists():
                data = trn.get()
                return data

        return None

    def find_data(self, kondisi):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            trn = Transaksi.select().where(kondisi)
            if trn.exists():
                return trn

        return None

    def find_all(self):
        cur_user = User.select().where(User.name == self.user)
        if cur_user.exists():
            user = cur_user.get()
            kondisi = (Transaksi.user == user.uid)
            data = self.find_data(kondisi)
            
            if data:
                return data

        return None

class TransaksiBaseHandler(base.BaseHandler):
    """ Class dasar untuk Transaksi"""

    @staticmethod
    def get_transaksi_list(user, *query):
        """Get transaksi data for current user with some filter"""
        active_user = User.get(User.name == user)
        data = Transaksi.select().where(Transaksi.user == active_user.uid, query).dicts()

        return data

    @staticmethod
    def get_data(id_data):
        if id_data:
            try:
                item = Transaksi.get(Transaksi.tid == id_data)
                results = item._data
                return results
            except peewee.DoesNotExist:
                pass

    def get_all_data(self):
        active_user = User.get(User.name == self.current_user)
        all_item = Transaksi.select().where(Transaksi.user == active_user.uid).dicts()
        return [item for item in all_item]


class ListTrans(TransaksiBaseHandler):
    def get(self):
        self.render('transaksi/ko-list.html')


class ListTransaksiHandler(TransaksiBaseHandler):
    """Class untuk menampilkan data transaksi"""

    @tornado.web.authenticated
    def get(self):
        today = datetime.date.today()
        current_month = today.month

        d = self.get_argument('d', None)

        tot = self.get_argument('total', False)
        active_user = User.get(User.name == self.current_user)
        transaksi = Transaksi.select().where(Transaksi.user == active_user.uid)
        if tot:
            data = transaksi

            if d:
                days_ago = today - datetime.timedelta(days=int(d))
                data = transaksi.select().where(Transaksi.transdate > days_ago)
        else:
            data = transaksi.select().where(Transaksi.transdate.month == current_month)

        total = data.select(fn.sum(Transaksi.amount)).scalar()

        if data:
            self.render("transaksi/list.html", trans=data, total=total)
        else:
            self.write_error(403, message="Not found")


class TransaksiByIdHandler(TransaksiBaseHandler):
    """Class untuk menghandle data transaksi individual"""

    @tornado.web.authenticated
    def get(self, tid):
        if tid:
            data = self.get_transaksi_list(self.current_user, Transaksi.tid == tid)
            self.write(jsonify([item for item in data]))
        else:
            data = self.get_transaksi_list(self.current_user)
            self.write(jsonify([item for item in data]))


class TransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, transid=None):
        transid = self.get_argument('transid', None)
        active_user = User.get(User.name == self.current_user)
        if transid:
            try:
                data = Transaksi.get(Transaksi.user == active_user.uid, Transaksi.tid == transid)
                self.render("transaksi/detail.html", item=data)
                return
            except peewee.DoesNotExist:
                raise tornado.web.HTTPError(403)
        else:
            data = Transaksi.select().where(Transaksi.user == active_user.uid)
            self.render("transaksi/list.html", trans=data)

    @tornado.web.authenticated
    def post(self):
        form = TransaksiForm(self.request.arguments)
        active_user = User.get(User.name == self.current_user)
        if form.validate():
            item = Transaksi.create(info=form.data['info'],
                                    amount=form.data['amount'],
                                    tipe=2,
                                    user=active_user.uid,
                                    memo=form.data['memo'], )
            item.save()
            self.write({'result': 'OK'})


class CreateTransaksiHandler(TransaksiBaseHandler):
    """Class untuk menghandle create data transaksi, menggunakan peewee model.create """

    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/create.html", form=form)

    @tornado.web.authenticated
    def post(self):
        """Post data transaksi baru ke database"""
        form = TransaksiForm(self.request.arguments)
        active_user = User.get(User.name == self.current_user)
        if form.validate():
            item = Transaksi.create(info=form.data['info'],
                                    amount=form.data['amount'],
                                    tipe=10,
                                    user=active_user.uid,
                                    memo=form.data['memo'], )
            item.save()
            # self.write({'result': 'OK'})
            self.redirect('/trans')
            return

        self.render('transaksi/create.html', form=form)


class InsertTransaksiHandler(TransaksiBaseHandler):
    """Class untuk menghandle data transaksi menggunakan peewee model insert()"""

    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/create.html", form=form)

    @tornado.web.authenticated
    def post(self):
        """Insert data transaksi baru ke database"""
        form = TransaksiForm(self.request.arguments)
        active_user = User.get(User.name == self.current_user)
        if form.validate():
            query = Transaksi.insert(info=form.data['info'],
                                     amount=form.data['amount'],
                                     user=active_user.uid,
                                     memo=form.data['memo'])
            query.execute()
            # self.write({'result': 'OK'})
            self.redirect('/trans')
            return

        self.render('transaksi/create.html', form=form)


class EditTransaksiHandler(TransaksiBaseHandler):
    """Class untuk menghandle edit data transaksi"""

    @tornado.web.authenticated
    def get(self, transid):
        """get data with id 'transid' and populate form with that data"""
        item = Transaksi.get(Transaksi.tid == transid)
        form = TransaksiForm(obj=item)
        self.render('transaksi/edit.html', form=form)

    @tornado.web.authenticated
    def post(self, transid):
        item = Transaksi.get(Transaksi.tid == transid)
        if item:
            form = TransaksiForm(self.request.arguments, obj=item)
            if form.validate():
                form.populate_obj(item)
                item.save()
                return self.redirect('/trans')
        else:
            form = TransaksiForm(obj=item)
        self.render('transaksi/edit.html', form=form, obj=item)


class DeleteTransaksiHandler(TransaksiBaseHandler):
    """Class untuk menghandle delete data transaksi"""

    @tornado.web.authenticated
    def get(self, tid):
        trans_id = Transaksi.get(Transaksi.tid == int(tid))
        if trans_id:
            try:
                trans_id.delete_instance()
            except peewee.DoesNotExist:
                return
        self.redirect('/trans')

    @tornado.web.authenticated
    def post(self, tid):
        trans_to_delete = self.get_argument('tid')
        trans_id = Transaksi.get(Transaksi.tid == int(trans_to_delete))
        if trans_id:
            try:
                trans_id.delete_instance()
            except peewee.DoesNotExist:
                return
        self.redirect('/trans')