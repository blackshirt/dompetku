from wtforms_tornado import Form
from wtforms import StringField, DateTimeField, TextAreaField, DecimalField, TextField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

from dompetku import model

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
    email = StringField('Email Address', [Email()])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = model.User.select().where(model.User.name == self.name.data)
        if user.exists():
           self.name.errors.append('User exists')
           return False
        return True

class LoginForm(Form):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = model.User.select().where(model.User.name == self.name.data)
        if not user.exists():
           self.name.errors.append('User not exists')
           return False
        return True