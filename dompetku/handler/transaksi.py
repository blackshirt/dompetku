#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle Transaction activities."""

import tornado.web
from dompetku import model
from dompetku.form import TransaksiForm
from dompetku.utils import jsonify

__author__ = 'blackshirt'


class BaseHandler(tornado.web.RequestHandler):
    pass


class TransaksiBaseHandler(BaseHandler):
    def initialize(self):
        self.transaksi = model.Transaksi

    def _get_data(self, id_data):
        if id_data:
            try:
                item = self.transaksi.get(self.transaksi.tid == id_data)
                results = item._data
                return results
            except self.transaksi.DoesNotExist:
                pass

    def _get_all_data(self):
        all_item = self.transaksi.select().dicts()
        return [item for item in all_item]


class ListTransaksiHandler(TransaksiBaseHandler):
    def get(self):
        trans = self._get_all_data()
        self.render("transaksi/list.html", trans=trans)


class TransaksiByIdHandler(TransaksiBaseHandler):
    def get(self, tid):
        data = self.transaksi.get(self.transaksi.tid == tid)
        results = data._data
        self.set_header('Content-Type', 'application/json')
        self.write(jsonify(results))


class TransaksiHandler(TransaksiBaseHandler):
    def get(self, transid=None):
        transid = self.get_argument('transid', None)
        if transid:
            item = self._get_data(transid)
            self.render("transaksi/detail.html", item=item)
        else:
            trans = self._get_all_data()
            self.render("transaksi/list.html", trans=trans)

    def post(self):
        """Post new data to our rpest service as a JSON"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = self.transaksi.create(info=form.data['info'],
                                         amount=form.data['amount'],
                                         type=2,
                                         user=1,
                                         memo=form.data['memo'], )
            post.save()
            self.write({'result': 'OK'})


class CreateTransaksiHandler(TransaksiBaseHandler):
    def get(self):
        form = TransaksiForm(self.request.arguments)
        self.render("transaksi/create.html", form=form)

    def post(self):
        """Post new data to our rpest service as a JSON"""
        form = TransaksiForm(self.request.arguments)
        if form.validate():
            post = self.transaksi.create(info=form.data['info'],
                                         amount=form.data['amount'],
                                         tipe=2,
                                         user=1,
                                         memo=form.data['memo'], )
            post.save()
            self.write({'result': 'OK'})


class EditTransaksiHandler(BaseHandler):
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


class DeleteTransaksiHandler(BaseHandler):
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
