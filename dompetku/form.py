from wtforms_tornado import Form
from wtforms import StringField, DateTimeField, TextAreaField, DecimalField, TextField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

__all__ = ["MessageForm", "TipeTransaksiForm", "TransaksiForm", "TransaksiDetailForm"]


class MessageForm(Form):
    title = StringField("Judul", validators=[DataRequired()])
    body = TextAreaField("Informasi", validators=[DataRequired()])
    created = DateTimeField()


class TipeTransaksiForm(Form):
    type = StringField(validators=[DataRequired()])
    desc = StringField(validators=[DataRequired()])

    def __unicode__(self):
        return self.desc


class TransaksiForm(Form):
    info = StringField("Kegunaan", validators=[DataRequired()])
    amount = DecimalField("Jumlah", validators=[DataRequired()])
    memo = TextAreaField("Catatan transaksi", validators=[DataRequired()])

    def __unicode__(self):
        return self.info


class TransaksiDetailForm(Form):
    item = StringField(validators=[DataRequired()])
    prices = DecimalField()
    times = DateTimeField
    notes = TextAreaField()

    def __unicode__(self):
        return self.item

class RegistrasiForm(Form):
    name = StringField('Username', [Length(min=3, max=25)])
    realname = StringField('Realname', [Length(min=3, max=50)])
    email = StringField('Email Address', [Length(min=3, max=35)])
    password = PasswordField('New Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    