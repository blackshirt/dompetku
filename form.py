from wtforms_tornado import Form
from wtforms import HiddenField, StringField, DateTimeField, TextAreaField, DecimalField
from wtforms.validators import DataRequired
from model import User, Message, TipeTransaksi, Transaksi, Category, TransaksiDetail

__all__ = ["MessageForm", "TipeTransaksiForm", "TransaksiForm", "TransaksiDetailForm"]


class MessageForm(Form):
    title = StringField(validators=[DataRequired()])
    body = TextAreaField(validators=[DataRequired()])
    created = DateTimeField()

class TipeTransaksiForm(Form):
    type = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])

    def __unicode__(self):
        return self.desc


class TransaksiForm(Form):
    info = StringField("Kegunaan", validators=[DataRequired()])
    amount = DecimalField(validators=[DataRequired()])
    memo = TextAreaField(validators=[DataRequired()])

    def __unicode__(self):
        return self.info


class TransaksiDetailForm(Form):
    item = StringField(validators=[DataRequired()])
    prices = DecimalField()
    times = DateTimeField
    notes = TextAreaField()

    def __unicode__(self):
        return self.item