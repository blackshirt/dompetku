import peewee
import hashlib
import datetime
import os

#from wtfpeewee.orm import model_form
from wtforms_tornado import Form

__all__ = ['database', 'User', 'Message', 'Category', 'Transaksi', 'TransaksiDetail']

data_path = os.path.join(os.path.dirname(__file__), 'data')
dbfile = 'dompetku.sqlite'
db = os.path.join(data_path, dbfile)

database = peewee.SqliteDatabase(db, threadlocals=True)


def gen_hash(password):
    return hashlib.sha512(str(password).encode('utf-8')).hexdigest()


class Base(peewee.Model):
    class Meta:
        database = database


class User(Base):
    uid = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    realname = peewee.CharField(default='guest')
    password = peewee.CharField()
    email = peewee.CharField()
    created = peewee.DateTimeField(default=datetime.datetime.now)
    active = peewee.BooleanField(default=False)
    lastactive = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('name',)

#UserForm = model_form(User, base_class=Form)

class Account(Base):
    acid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    amount = peewee.DecimalField()
    info = peewee.TextField()


class Hutang(Base):
    hid = peewee.PrimaryKeyField()
    tanggal = peewee.DateTimeField()
    tempo = peewee.DateTimeField()
    amount = peewee.DecimalField()
    sisa = peewee.DecimalField(default=0)
    hutanger = peewee.CharField()
    deskripsi = peewee.TextField()

    class Meta:
        order_by = ('-amount', 'tempo')


class Piutang(Base):
    pid = peewee.PrimaryKeyField()
    tanggal = peewee.DateTimeField()
    tempo = peewee.DateTimeField()
    amount = peewee.DecimalField()
    sisa = peewee.DecimalField(default=0)
    piutanger = peewee.CharField()
    deskripsi = peewee.TextField()

    class Meta:
        order_by = ('-amount', 'tempo')


class Investasi(Base):
    invid = peewee.PrimaryKeyField()
    jenis = peewee.CharField()
    amount = peewee.DecimalField()
    tanggal = peewee.DateField()


class Aset(Base):
    asid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    jenis = peewee.CharField()
    harga_sekarang = peewee.DecimalField()


class Message(Base):
    mid = peewee.PrimaryKeyField()
    title = peewee.CharField()
    body = peewee.TextField()
    author = peewee.ForeignKeyField(rel_model=User, db_column='author')
    created = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-created',)

#MessageForm = model_form(Message, base_class=Form)

class Category(Base):
    cid = peewee.PrimaryKeyField()
    category = peewee.CharField(unique=True)
    desc = peewee.CharField(default='Deskripsi')


class TipeTransaksi(Base):
    ttid = peewee.PrimaryKeyField()
    tipe = peewee.CharField()
    desc = peewee.CharField()

#TipeTransaksiForm = model_form(TipeTransaksi, base_class=Form)

class Transaksi(Base):
    tid = peewee.PrimaryKeyField()
    user = peewee.ForeignKeyField(rel_model=User)
    tipe = peewee.ForeignKeyField(rel_model=TipeTransaksi)
    info = peewee.CharField()
    amount = peewee.DecimalField(default=0)
    transdate = peewee.DateTimeField(default=datetime.datetime.now())
    memo = peewee.CharField()

    class Meta:
        order_by = ('-transdate',)

#TransaksiForm = model_form(Transaksi, allow_pk=True, base_class=Form)

class TransaksiDetail(Base):
    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(rel_model=Transaksi)
    item_transaksi = peewee.CharField()
    number_of_item = peewee.IntegerField(default=1)
    category = peewee.ForeignKeyField(rel_model=Category)
    prices = peewee.DecimalField(default=0)
    times = peewee.DateTimeField(default=datetime.datetime.now().time())
    notes = peewee.CharField()

def insert_data(dbase):
    with dbase.transaction():
        TipeTransaksi.insert_many(tipe_trans_data).execute()
        Category.insert_many(category_data).execute()
        Message.insert_many(msg_data).execute()
        User.insert_many(user_data).execute()
        Transaksi.insert_many(transaksi_data).execute()


all_model = [User, Message, Category, TipeTransaksi, Transaksi, TransaksiDetail, Hutang, Piutang, Investasi, Account,
             Aset]

def init():
    database.connect()
    peewee.create_model_tables(all_model, fail_silently=True)
