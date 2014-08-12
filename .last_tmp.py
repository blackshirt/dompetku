from peewee import *

db = '/storage/sdcard1/database/test.sqlite'

dbs = SqliteDatabase(db)

class Tukon(Model):
    id = IntegerField()
    category = TextField()
    description = TextField()
    prices = IntegerField()
   
    class Meta:
        database = dbs

Tukon.create_table()

baju = Tukon.create(id=1, category='sandang', description='beli baju keperluan lebaran', prices=50000)
roti = Tukon.create(id=2, category='pangan', description='beli roti buat makan', prices=4000)
tempe = Tukon.create(id=3, category='lauk', description='lauk pauk', prices=500)