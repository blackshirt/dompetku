from peewee import *
import hashlib
import datetime

db = '/storage/sdcard1/database/dompetku.sqlite'
#db = config['dbpath']

database = SqliteDatabase(db)


class ItemBase(Model):
    class Meta:
        database = database

class User(ItemBase):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    password = CharField()
    email = CharField()
    created = DateField()
    last = DateTimeField()
    
    class Meta:
        order_by = ('name',)

class Category(ItemBase):
    id = PrimaryKeyField()
    cat = CharField(unique=True)
    desc = CharField()

class Item(ItemBase):
    id = IntegerField(primary_key=True)
    name = ForeignKeyField(User)
    cat = ForeignKeyField(Category)
    prices = DecimalField()
   
def init():
    database.connect()
    database.create_table(User)
    database.create_table(Category)
    database.create_table(Item)

def gen_hash(password):
    return hashlib.sha512(str(password).encode('utf-8')).hexdigest()



#baju = Tukon.create(category='sandang', description='beli baju keperluan lebaran', prices=50000)
#roti = Tukon.create(category='pangan', description='beli roti buat makan', prices=4000)
#tempe = Tukon.create(category='lauk', description='lauk pauk', prices=500)

