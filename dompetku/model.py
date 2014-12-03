import peewee
import hashlib
import datetime
import os

from wtfpeewee.orm import model_form
from wtforms_tornado import Form
from wtforms.validators import Length

__all__ = ['database', 'User', 'Message', 'Category', 'Transaksi', 'TransaksiDetail']

data_path = os.path.join(os.path.dirname(__file__), 'data')
dbfile = 'dompetku.sqlite'
db = os.path.join(data_path, dbfile)

database = peewee.SqliteDatabase(db, threadlocals=True)


def gen_hash(password):
    return hashlib.sha512(str(password).encode('utf-8')).hexdigest()


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    uid = peewee.PrimaryKeyField()
    name = peewee.CharField(max_length=255, unique=True)
    realname = peewee.CharField(max_length=255, default='guest')
    password = peewee.CharField()
    email = peewee.CharField(max_length=255)
    created = peewee.DateField(default=datetime.date.today)
    active = peewee.BooleanField(default=False)
    lastactive = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('name',)

#UserForm = model_form(User, base_class=Form)
class Account(BaseModel):
    acid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    amount = peewee.DecimalField()
    info = peewee.TextField()


class Hutang(BaseModel):
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
    invid = peewee.PrimaryKeyField()
    jenis = peewee.CharField()
    amount = peewee.DecimalField()
    tanggal = peewee.DateField()


class Aset(BaseModel):
    asid = peewee.PrimaryKeyField()
    name = peewee.CharField()
    jenis = peewee.CharField()
    harga_sekarang = peewee.DecimalField()


class Message(BaseModel):
    mid = peewee.PrimaryKeyField()
    title = peewee.CharField()
    body = peewee.TextField()
    author = peewee.ForeignKeyField(rel_model=User, db_column='author')
    created = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-created',)

#MessageForm = model_form(Message, base_class=Form)

class Category(BaseModel):
    cid = peewee.PrimaryKeyField()
    category = peewee.CharField(unique=True)
    desc = peewee.CharField(default='Deskripsi')


class TipeTransaksi(BaseModel):
    ttid = peewee.PrimaryKeyField()
    tipe = peewee.CharField()
    desc = peewee.TextField()

#TipeTransaksiForm = model_form(TipeTransaksi, base_class=Form)

class Transaksi(BaseModel):
    tid = peewee.PrimaryKeyField()
    user = peewee.ForeignKeyField(rel_model=User)
    tipe = peewee.ForeignKeyField(rel_model=TipeTransaksi)
    info = peewee.CharField()
    amount = peewee.DecimalField(default=0)
    transdate = peewee.DateTimeField(default=datetime.datetime.now)
    memo = peewee.TextField()

    class Meta:
        order_by = ('-transdate',)

TransaksiForm = model_form(Transaksi, base_class=Form, exclude=('tid','user','tipe','transdate',))

class TransaksiDetail(BaseModel):
    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(rel_model=Transaksi)
    item_transaksi = peewee.CharField()
    number_of_item = peewee.IntegerField(default=1)
    category = peewee.ForeignKeyField(rel_model=Category)
    prices = peewee.DecimalField(default=0)
    times = peewee.DateTimeField(default=datetime.datetime.now().time())
    notes = peewee.TextField()

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
