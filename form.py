from wtforms_tornado import Form
from wtforms import HiddenField, StringField, TextField, DateTimeField
from model import User, Message, TipeTransaksi, Transaksi, Category, TransaksiDetail
from wtfpeewee.orm import model_form

MessageForm = model_form(Message, base_class=Form)
TipeTransaksiForm = model_form(TipeTransaksi, base_class=Form)

__all__ = ['MessageForm', 'TipeTransaksiForm']