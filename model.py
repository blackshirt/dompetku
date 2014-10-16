import peewee
import hashlib
import datetime
import os

__all__ = ['database', 'User', 'Message', 'Category', 'Transaksi', 'TransaksiDetail']

data_path = os.path.join(os.path.dirname(__file__), 'data')
dbfile = 'dompetku.sqlite'
db = os.path.join(data_path, dbfile)

database = peewee.SqliteDatabase(db)


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
    lastactive = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('name',)


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
    author = peewee.ForeignKeyField(User, db_column='author')
    created = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-created',)


class Category(Base):
    cid = peewee.PrimaryKeyField()
    category = peewee.CharField(unique=True)
    desc = peewee.CharField(default='Deskripsi')


class TipeTransaksi(Base):
    ttid = peewee.PrimaryKeyField()
    type = peewee.CharField()
    desc = peewee.CharField()


class Transaksi(Base):
    tid = peewee.PrimaryKeyField()
    user = peewee.ForeignKeyField(User)
    type = peewee.ForeignKeyField(TipeTransaksi)
    info = peewee.CharField()
    amount = peewee.DecimalField()
    transdate = peewee.DateTimeField(default=datetime.datetime.now)
    memo = peewee.CharField()

    class Meta:
        order_by = ('-transdate',)


transaksi_data = [
    {'user': 1, 'type': 1, 'info': 'Pembelian kapal selam', 'amount': 50000, 'memo': 'Kapal selam nuklir bekas'},
    {'user': 2, 'type': 2, 'info': 'Pembelian kapal barang', 'amount': 54500, 'memo': 'Kapal selam barang bekas'},
    {'user': 1, 'type': 3, 'info': 'Pembelian pesawat tempur', 'amount': 42000, 'memo': 'pesawat tempur bekas'},
]


class TransaksiDetail(Base):
    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(Transaksi)
    item = peewee.CharField()
    category = peewee.ForeignKeyField(Category)
    prices = peewee.DecimalField()
    times = peewee.DateTimeField(default=datetime.datetime.now)
    notes = peewee.CharField()


user_data = [
    {'name': 'paijo', 'realname': 'Paijo Ganteng', 'password': gen_hash('paijo'), 'email': 'paijo@none'},
    {'name': 'black', 'realname': 'Blackshirt Ganteng', 'password': gen_hash('black'), 'email': 'black@none'},
    {'name': 'xbunox', 'realname': 'Xbunox', 'password': gen_hash('xbunox'), 'email': 'xbunox@none'},
]

tipe_trans_data = [
    {'type': 'MSK', 'desc': 'Transaksi Masuk'},
    {'type': 'OUT', 'desc': 'Transaksi Keluar '},
    {'type': 'TRN', 'desc': 'Transaksi Transfer'},
    {'type': 'BLN', 'desc': 'Transaksi Balance'},
    {'type': 'OTH', 'desc': 'Transaksi Lain'},
]

category_data = [
    {'category': 'sandang', 'desc': 'kebutuhan sandang'},
    {'category': 'pangan', 'desc': 'kebutuhan pangan'},
    {'category': 'papan', 'desc': 'kebutuhan papan'},
    {'category': 'rumahtangga', 'desc': 'kebutuhan rumah tangga'},
    {'category': 'transport', 'desc': 'kebutuhan transportasi'},
    {'category': 'jasa', 'desc': 'kebutuhan jasa'},
    {'category': 'kerja', 'desc': 'kebutuhan kerja'},
    {'category': 'masyarakat', 'desc': 'kebutuhan masyarakat'},
    {'category': 'umum', 'desc': 'kebutuhan umum'},
    {'category': 'lain', 'desc': 'kebutuhan lain'},
]

msg_data = [
    {'title': 'Introduction to Asynchronous python server',
     'body': 'Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed. By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets, and other applications that require a long-lived connection to each user.',
     'author': 1},
    {'title': 'wtf-peewee',
     'body': 'WTForms integration for peewee, provides a bridge between peewee models and wtforms, mapping model fields to form fields',
     'author': 2},
]


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
