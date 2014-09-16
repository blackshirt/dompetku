import peewee
import hashlib
import datetime

__all__ = ['database', 'User', 'Message', 'Category', 'Transaksi', 'TransaksiDetail']

db = '/storage/sdcard1/database/dompetku.sqlite'
#db = r"D:\My Documents\db\dompetku.sqlite"
# db = config['dbpath']

database = peewee.SqliteDatabase(db)


def gen_hash(password):
    return hashlib.sha512(str(password).encode('utf-8')).hexdigest()


class Base(peewee.Model):
    class Meta:
        database = database


class User(Base):
    uid = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField()
    currentbalance = peewee.DecimalField(default=0)
    created = peewee.DateTimeField(default=datetime.datetime.now)
    lastactive = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('name',)


class Message(Base):
    mid = peewee.PrimaryKeyField()
    title = peewee.CharField()
    body = peewee.TextField()
    author = peewee.ForeignKeyField(User, db_column='author')
    created = peewee.DateTimeField()


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


class TransaksiDetail(Base):
    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(Transaksi)
    item = peewee.CharField()
    category = peewee.ForeignKeyField(Category)
    prices = peewee.DecimalField()
    times = peewee.DateTimeField(default=datetime.datetime.now)
    notes = peewee.CharField()


userdata = [
    {'name': 'paijo', 'password': gen_hash('paijo'), 'email': 'paijo@none'},
    {'name': 'black', 'password': gen_hash('black'), 'email': 'black@none'},
]


def insert_user(database):
    with database.transaction():
        User.insert_many(userdata).execute()


tipe_trans_data = [
    {'type': 'MSK', 'desc': 'Transaksi Masuk'},
    {'type': 'OUT', 'desc': 'Transaksi Keluar '},
    {'type': 'TRN', 'desc': 'Transaksi Transfer'},
    {'type': 'BLN', 'desc': 'Transaksi Balance'},
    {'type': 'OTH', 'desc': 'Transaksi Lain'},
]


def insert_tipe_trans(database):
    with database.transaction():
        TipeTransaksi.insert_many(tipe_trans_data).execute()


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


def insert_category_data(database):
    with database.transaction():
        Category.insert_many(category_data).execute()


def init():
    database.connect()
    peewee.create_model_tables([User, Message, Category, TipeTransaksi, Transaksi, TransaksiDetail], fail_silently=True)
