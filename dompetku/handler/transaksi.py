#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle daily transaction activities."""

import tornado.web

from dompetku import model
from dompetku.handler import base
from dompetku.utils import jsonify
from dompetku.form import TransaksiForm


class TransaksiBaseHandler(base.BaseHandler):
    """ Class dasar untuk Transaksi"""

    def initialize(self, transaction=model.Transaksi):
        self.transaction = transaction
        self.user = self.get_user_object()

    def get_data(self, id_data):
        if id_data:
            try:
                item = self.transaction.get(self.transaction.tid == id_data)
                results = item._data
                return results
            except self.transaction.DoesNotExist:
                pass

    def get_all_data(self):
        all_item = self.transaction.select().dicts()
        return [item for item in all_item]


class ListTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self):
        trans = self.get_all_data()
        self.render("transaksi/list.html", trans=trans)


class TransaksiByIdHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, tid):
        data = self.transaction.get(self.transaction.tid == tid)
        results = data._data
        self.set_header('Content-Type', 'application/json')
        self.write(jsonify(results))


class TransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, transid=None):
        transid = self.get_argument('transid', None)
        if transid:
            item = self.get_data(transid)
            self.render("transaksi/detail.html", item=item)
        else:
            trans = self.get_all_data()
            self.render("transaksi/list.html", trans=trans)

    @tornado.web.authenticated
    def post(self):
        """Post new data to our rpest service as a JSON"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = self.transaction.create(info=form.data['info'],
                                           amount=form.data['amount'],
                                           tipe=2,
                                           user=self.user.uid,
                                           memo=form.data['memo'], )
            post.save()
            self.write({'result': 'OK'})


class CreateTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/create.html", form=form)

    @tornado.web.authenticated
    def post(self):
        """Post data transaksi baru ke database"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = self.transaction.create(info=form.data['info'],
                                           amount=form.data['amount'],
                                           tipe=10,
                                           user=self.user.uid,
                                           memo=form.data['memo'], )
            post.save()
            # self.write({'result': 'OK'})
            self.redirect('/trans')
            return

        self.render('transaksi/create.html', form=form)


class InsertTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/create.html", form=form)

    @tornado.web.authenticated
    def post(self):
        """Insert data transaksi baru ke database"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            query = self.transaction.insert(info=form.data['info'],
                                            amount=form.data['amount'],
                                            user=self.user.uid,
                                            memo=form.data['memo'])
            query.execute()

            # self.write({'result': 'OK'})
            self.redirect('/trans')
            return

        self.render('transaksi/create.html', form=form)


class NewTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/new.html", form=form)

    @tornado.web.authenticated
    def post(self):
        """Post new data to our rpest service as a JSON"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = self.transaction.create(info=form.data['info'],
                                           amount=form.data['amount'],
                                           user=self.user.uid,
                                           memo=form.data['memo'])
            post.save()
            return
        self.render("transaksi/new.html", form=form)


class EditTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, transid):
        post = model.Transaksi.get(model.Transaksi.tid == transid)
        form = TransaksiForm(obj=post)
        self.render('transaksi/edit.html', form=form)

    @tornado.web.authenticated
    def post(self, transid):
        post = model.Transaksi.get(model.Transaksi.tid == transid)
        if post:
            form = TransaksiForm(self.request.arguments, obj=post)
            if form.validate():
                form.populate_obj(post)
                post.save()
                return self.redirect('/trans')
        else:
            form = TransaksiForm(obj=post)
        self.render('transaksi/edit.html', form=form, obj=post)


class DeleteTransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, tid):
        trans_id = model.Transaksi.get(model.Transaksi.tid == int(tid))
        if trans_id:
            try:
                trans_id.delete_instance()
            except model.Transaksi.DoesNotExist:
                return
        self.redirect('/trans')

    @tornado.web.authenticated
    def post(self, tid):
        trans_to_delete = self.get_argument('tid')
        trans_id = model.Transaksi.get(model.Transaksi.tid == int(trans_to_delete))
        if trans_id:
            try:
                trans_id.delete_instance()
            except model.Transaksi.DoesNotExist:
                return
        self.redirect('/trans')
