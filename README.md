Dompetku
========


`Dompetku <http://github.com/blackshirt/dompetku>`_ adalah aplikasi berbasis web sederhana yang dibangun menggunakan python yang dimaksudkan sebagai  *pencatat aktivitas keuangan pribadi* (terutama pengeluaran pribadi, dan begitulah keadaannya :-( ). Pada awalnya digunakan 
untuk keperluan pribadi di situs `Dompetku Online <http://blackshirt.pythonanywhere.com/>`_ . 
Dibuat dengan menggunakan beberapa stack python untuk web, 

- `Tornado web <https://tornadoweb.org/>`_, Python web framework dan asynchronous networking library, yang dikembangkan oleh `FriendFeed <http://friendfeed.com>`_ dan diakuisi oleh `Facebook <https://facebook.com>`_. Kemudian juga menggunakan, 

- `Peewee ORM <http://docs.peewee-orm.com/en/latest/>`_ , Python based ORM, simpel dan mudah, yang support sqlite, mysql, dan postgre database. 

- `Wtforms library, <https://wtforms.readthedocs.org/en/latest/>`_, Library untuk rendering dan validasi form berbasis python yang fleksibel. dan beberapa library lain, 

- `wtforms-tornado <https://pypi.python.org/pypi/wtforms-tornado/0.0.2>`_, untuk kemudahan integrasi wtforms dan tornado.

- `wtf-peewee <https://pypi.python.org/pypi/wtf-peewee>`_, untuk kemudahan menggunakan peewee model dalam wtforms.

.. note:: Beberapa fitur ini masih terbatas basic saja dan masih banyak kekurangannya.


Penggunaan
----------

**Penggunaan manual**: Download source code dari `Account github blackshirt <https://github.com/blackshirt/dompetku.git>`_, dan pastikan git tools terinstall.

.. parsed-literal::

    $sudo apt-get install git-core (for debian based)
    $git clone https://github.com/blackshirt/dompetku.git
    $cd dompetku
    $python main.py
    

**Prerequisites**: Dompetku ditulis menggunakan Python 3, dan sama sekali belum dicoba dengan Python 2.

**Platforms**: Aplikasi ini seharusnya bisa jalan di any Unix-like platform yang support python, Windows, ataupun BSD

**Contact**: Saran dan ide silahkan contact ke <``blackshirtmuslim@yahoo.com``> 
