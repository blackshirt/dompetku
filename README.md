Dompetku
========


[Dompetku](http://blackshirt.pythonanywhere.com/ "Dompetku") adalah aplikasi berbasis web sederhana yang dibangun menggunakan python yang dimaksudkan sebagai  ***pencatat aktivitas keuangan pribadi*** (terutama pengeluaran pribadi, dan begitulah keadaannya :-( ). Pada awalnya digunakan 
untuk keperluan pribadi di halaman web [dompetku](http://blackshirt.pythonanywhere.com/ "your online pocket") . 
Dibuat dengan menggunakan beberapa stack python untuk web, 

* [Tornado web](https://tornadoweb.org/ "Tornado web framework"), Python web framework dan asynchronous networking library, yang dikembangkan oleh [FriendFeed](http://friendfeed.com/ "Online friendship sosial media") dan diakuisi oleh [Facebook](https://facebook.com/ "facebook"). 

* [Peewee ORM](http://docs.peewee-orm.com/en/latest/ "peewee"), Python based ORM, simpel dan mudah, yang support sqlite, mysql, dan postgres database. 

* [Wtforms library](https://wtforms.readthedocs.org/en/latest/ "wtforms"), Library untuk rendering dan validasi form berbasis python yang fleksibel. dan beberapa library lain, 

* [wtforms-tornado](https://pypi.python.org/pypi/wtforms-tornado/ "wtforms for tornado"), untuk kemudahan integrasi wtforms dan tornado.

* [wtf-peewee](https://pypi.python.org/pypi/wtf-peewee/ "wtforms peewee"), untuk kemudahan menggunakan peewee model dalam wtforms.

*****
>**Notes**: Beberapa fitur ini masih terbatas basic saja dan masih banyak kekurangannya.
*****

* Register 
![register](https://raw.githubusercontent.com/blackshirt/dompetku/pythonanywhere/data/pockets/register.PNG)
![register-sesuatu](https://raw.githubusercontent.com/blackshirt/dompetku/pythonanywhere/data/pockets/register-sesuatu.PNG)

* Transaksi baru
![register](https://raw.githubusercontent.com/blackshirt/dompetku/pythonanywhere/data/pockets/insert-new.PNG)

* Daftar transaksi (default bulan ini)
![register](https://raw.githubusercontent.com/blackshirt/dompetku/pythonanywhere/data/pockets/rekap.PNG)

Penggunaan
----------

**Penggunaan manual**: Download source code dari [Account blackshirt](https://github.com/blackshirt/dompetku.git "blackshirt"), dan pastikan git tools terinstall.

    $sudo apt-get install git-core (for debian based)
    $git clone https://github.com/blackshirt/dompetku.git
    $cd dompetku
    $python main.py
    
**Prerequisites**: Dompetku ditulis menggunakan Python 3, dan sama sekali belum dicoba dengan Python 2.

**Platforms**: Aplikasi ini seharusnya bisa jalan di any ***Unix-like platform*** yang support python, Windows, ataupun BSD

**Contact**: Saran dan ide silahkan contact ke <blackshirtmuslim@yahoo.com>
