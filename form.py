from wtforms_tornado import Form
from wtforms import HiddenField, StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
from model import User, Message, TipeTransaksi, Transaksi, Category, TransaksiDetail

__all__ = ["MessageForm", "TipeTransaksiForm"]


class MessageForm(Form):
    title = StringField(validators=[DataRequired()])
    body = TextAreaField(validators=[DataRequired()])


class TipeTransaksiForm(Form):
    type = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])



