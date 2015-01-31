#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Module to handle daily transaction activities."""
import peewee
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

    def get_transaksi_list(self, user, *filter):
        """Get transaksi data for current user with some filter"""
        active_user = model.User.get(model.User.name == user)
        data = model.Transaksi.select().where(model.Transaksi.user == active_user.uid, filter).dicts()
        
        return data
    
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
        #trans = self.get_all_data()
        active_user= model.User.get(model.User.name == self.current_user)
        # self.curent_user was available, because this method was decorated
        data = model.Transaksi.select().where(model.Transaksi.user == active_user.uid)
        
        if data:
            #trans = data._data
            self.render("transaksi/list.html", trans=data)
        else:
            self.write_error(403, message="Not found")

class TransaksiByIdHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, tid):
        if tid:
            #data = self.transaction.get(self.transaction.tid == tid)
            data = self.get_transaksi_list(self.current_user, model.Transaksi.tid == tid)
            #results = data._data
            #self.set_header('Content-Type', 'application/json')
            self.write(jsonify([item for item in data]))
        else:
            data = self.get_transaksi_list(self.current_user)
            self.write(jsonify([item for item in data]))


class TransaksiHandler(TransaksiBaseHandler):
    @tornado.web.authenticated
    def get(self, transid=None):
        transid = self.get_argument('transid', None)
        active_user= model.User.get(model.User.name == self.current_user)
            
        if transid:
            try:
                data = model.Transaksi.get(model.Transaksi.user == active_user.uid, model.Transaksi.tid == transid)
                self.render("transaksi/detail.html", item=data)
                return
            except peewee.DoesNotExist:
                raise tornado.web.HTTPError(403)
        else:
            data = model.Transaksi.select().where(model.Transaksi.user == active_user.uid)
            #trans = [item for item in data]
            self.render("transaksi/list.html", trans=data)

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
