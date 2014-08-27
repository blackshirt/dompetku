from peewee import *
import hashlib
import datetime

db = '/storage/sdcard1/database/dompetku.sqlite'
#db = config['dbpath']

database = SqliteDatabase(db)

def gen_hash(password):
    return hashlib.sha512(str(password).encode('utf-8')).hexdigest()


class Base(Model):
    class Meta:
        database = database

class User(Base):
    uid = PrimaryKeyField()
    name = CharField(unique=True)
    password = CharField()
    email = CharField()
    currentbalance = DecimalField(default=0)
    created = DateTimeField(default=datetime.datetime.now)
    lastactive = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        order_by = ('name',)

class Message(Base):
    mid = PrimaryKeyField()
    title = CharField()
    body = TextField()
    author = CharField()
    created = DateTimeField()
    
class Category(Base):
    cid = PrimaryKeyField()
    category = CharField(unique=True)
    desc = CharField(default='Deskripsi')

class TipeTransaksi(Base):
    ttid = PrimaryKeyField()
    type = CharField()
    desc = CharField()

class Transaksi(Base):
    tid = PrimaryKeyField()
    user = ForeignKeyField(User)
    type = ForeignKeyField(TipeTransaksi)
    info = CharField()
    amount = DecimalField()
    transdate = DateTimeField(default=datetime.datetime.now)
    memo = CharField()

class TransaksiDetail(Base):
    tdid = PrimaryKeyField()
    transid = ForeignKeyField(Transaksi)
    item = CharField()
    category = ForeignKeyField(Category)
    prices = DecimalField()
    times = DateTimeField(default=datetime.datetime.now)
    notes = CharField()

userdata = [
    {'name':'paijo','password':gen_hash('paijo'),'email':'paijo@none'},
    {'name':'black','password':gen_hash('black'),'email':'black@none'},
]

def insert_user(db):
    with db.transaction():
        User.insert_many(userdata).execute()

tipe_trans_data= [
    {'type':'MSK', 'desc':'Transaksi Masuk'},
    {'type':'OUT', 'desc':'Transaksi Keluar '},
    {'type':'TRN', 'desc':'Transaksi Transfer'},
    {'type':'BLN', 'desc':'Transaksi Balance'},
    {'type':'OTH', 'desc':'Transaksi Lain'},
]

def insert_tipe_trans(db):
    with db.transaction():
        TipeTransaksi.insert_many(tipe_trans_data).execute()
   
category_data = [
    {'category':'sandang','desc':'kebutuhan sandang'},
    {'category':'pangan','desc':'kebutuhan pangan'},
    {'category':'papan','desc':'kebutuhan papan'},
    {'category':'rumahtangga','desc':'kebutuhan rumah tangga'},
    {'category':'transport','desc':'kebutuhan transportasi'},
    {'category':'jasa','desc':'kebutuhan jasa'},
    {'category':'kerja','desc':'kebutuhan kerja'},
    {'category':'masyarakat','desc':'kebutuhan masyarakat'},
    {'category':'umum','desc':'kebutuhan umum'},
    {'category':'lain','desc':'kebutuhan lain'},
] 

def insert_category_data(db):
    with db.transaction():
        Category.insert_many(category_data).execute()

def init():
    database.connect()
    peewee.create_model_tables([User, Message, Category, TipeTransaksi, Transaksi, TransaksiDetail],fail_silently=True)
    
