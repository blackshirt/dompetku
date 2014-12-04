#/usr/bin/env python3.4
import os

_data_path = os.path.join(os.path.dirname(__file__), 'data') #relatif ke main script
_db_file = 'dompetku.sqlite'
_db = os.path.join(_data_path, _db_file)

dbconfig = {
    'sqlite':{
        'db_path':_data_path,
        'db_name':_db_file,
        'db': _db,
    },
    'mysql':{
        'host':'127.0.0.1',
        'user':'',
        'password':'',
        'db_name':'',
    },
    'postgre':{
        'host':'127.0.0.1',
        'user':'',
        'password':'',
        'db_name':'',
    }
}

