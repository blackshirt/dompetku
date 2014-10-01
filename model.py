import peewee
import hashlib
import datetime

__all__ = ['database', 'User', 'Message', 'Category', 'Transaksi', 'TransaksiDetail']

# db = '/storage/sdcard1/database/dompetku.sqlite'
db = r"C:\Users\BKD Kab Kebumen\dompetku\data\dompetku.sqlite"
# db = config['dbpath']
#db = '/home/blackshirt/dompetku/data/dompetku.sqlite'
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
    created = peewee.DateTimeField(default=datetime.datetime.now)


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


class TransaksiDetail(Base):
    tdid = peewee.PrimaryKeyField()
    transid = peewee.ForeignKeyField(Transaksi)
    item = peewee.CharField()
    category = peewee.ForeignKeyField(Category)
    prices = peewee.DecimalField()
    times = peewee.DateTimeField(default=datetime.datetime.now)
    notes = peewee.CharField()


user_data = [
    {'name': 'paijo', 'password': gen_hash('paijo'), 'email': 'paijo@none'},
    {'name': 'black', 'password': gen_hash('black'), 'email': 'black@none'},
    {'name': 'xbunox', 'password': gen_hash('xbunox'), 'email': 'xbunox@none'},
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
    {'title': 'Introduction to Asynchronous python server', 'body': 'Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed. By using non-blocking network I/O, Tornado can scale to tens of thousands of open connections, making it ideal for long polling, WebSockets, and other applications that require a long-lived connection to each user.', 'author':1},
    {'title': 'wtf-peewee', 'body': 'WTForms integration for peewee, provides a bridge between peewee models and wtforms, mapping model fields to form fields', 'author':2},
]
def insert_data(dbase):
    with dbase.transaction():
        User.insert_many(user_data).execute()
        TipeTransaksi.insert_many(tipe_trans_data).execute()
        Category.insert_many(category_data).execute()
        Message.insert_many(msg_data).execute()


def init():
    database.connect()
    peewee.create_model_tables([User, Message, Category, TipeTransaksi, Transaksi, TransaksiDetail], fail_silently=True)
