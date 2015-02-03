#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Core model represents data in the database"""

import datetime

import peewee
# from wtfpeewee.orm import model_form
# from wtforms_tornado import Form

from config import dbconfig

db = dbconfig['sqlite']['db']
database = peewee.SqliteDatabase(db)


class BaseModel(peewee.Model):
    """Base model"""
    class Meta:
        database = database


class User(BaseModel):
    """Model merepresentasikan user"""

    uid = peewee.PrimaryKeyField()
    name = peewee.CharField(max_length=255, unique=True)
    realname = peewee.CharField(max_length=255, default='guest')
    password = peewee.CharField()
    passkey = peewee.CharField()
    email = peewee.CharField(max_length=255)
    created = peewee.DateField(default=datetime.date.today)
    active = peewee.BooleanField(default=False)
    lastactive = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('name',)


# UserForm = model_form(User, base_class=Form)
class Account(BaseModel):
    """Model untuk account"""

    acid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    amount = peewee.DecimalField()
    info = peewee.TextField()


class Hutang(BaseModel):
    """Model untuk hutang"""

    hid = peewee.PrimaryKeyField()
    tanggal = peewee.DateField(default=datetime.date.today)
    tempo = peewee.DateField(default=datetime.date.today)
    amount = peewee.DecimalField(default=0)
    sisa = peewee.DecimalField(default=0)
    hutanger = peewee.CharField()
    deskripsi = peewee.TextField()

    class Meta:
        order_by = ('-amount', 'tempo')


class Piutang(BaseModel):
    """Model untuk piutang"""

    pid = peewee.PrimaryKeyField()
    tanggal = peewee.DateTimeField()
    tempo = peewee.DateTimeField()
    amount = peewee.DecimalField()
    sisa = peewee.DecimalField(default=0)
    piutanger = peewee.CharField()
    deskripsi = peewee.TextField()

    class Meta:
        order_by = ('-amount', 'tempo')


class Investasi(BaseModel):
    """Model untuk investasi"""

    invid = peewee.PrimaryKeyField()
    jenis = peewee.CharField()
    amount = peewee.DecimalField()
    tanggal = peewee.DateField()


class Aset(BaseModel):
    """Model buat aset"""

    asid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    jenis = peewee.CharField()
    harga_sekarang = peewee.DecimalField()


class Message(BaseModel):
    """Buat pesan dan info"""

    mid = peewee.PrimaryKeyField()
    title = peewee.CharField()
    body = peewee.TextField()
    author = peewee.ForeignKeyField(rel_model=User, db_column='author')
    created = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-created',)


# MessageForm = model_form(Message, base_class=Form)

class Category(BaseModel):
    """Category model untuk pengklasifikasian"""

    cid = peewee.PrimaryKeyField()
    category = peewee.CharField(unique=True)
    desc = peewee.CharField(default='Deskripsi')


class TipeTransaksi(BaseModel):
    """Tipe transaksi model"""

    ttid = peewee.PrimaryKeyField()
    tipe = peewee.CharField(default='Not defined')
    desc = peewee.TextField()


# TipeTransaksiForm = model_form(TipeTransaksi, base_class=Form)

class Transaksi(BaseModel):
    """Core model untuk aktifitas transaksi"""

    tid = peewee.PrimaryKeyField()
    user = peewee.ForeignKeyField(rel_model=User)
    tipe = peewee.ForeignKeyField(rel_model=TipeTransaksi, default=10)
    info = peewee.CharField()
    amount = peewee.DecimalField(default=0)
    transdate = peewee.DateTimeField(default=datetime.datetime.now, formats='%Y-%m-%d %H:%M:%S')
    memo = peewee.TextField()

    class Meta:
        order_by = ('-transdate',)


#TransaksiForm = model_form(Transaksi, base_class=Form, exclude=('tid', 'user', 'tipe', 'transdate',))


class TransaksiDetail(BaseModel):
    """Detail dari sebuah transaksi"""

    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(rel_model=Transaksi)
    item_transaksi = peewee.CharField()
    number_of_item = peewee.IntegerField(default=1)
    category = peewee.ForeignKeyField(rel_model=Category)
    prices = peewee.DecimalField(default=0)
    times = peewee.DateTimeField(default=datetime.datetime.now().time())
    notes = peewee.TextField()


all_model = [User, Message, Category, TipeTransaksi, Transaksi, TransaksiDetail, Hutang, Piutang, Investasi, Account,
             Aset]


def init():
    """utility function to initialize tables and database"""
    database.connect()
    peewee.create_model_tables(all_model, fail_silently=False)
