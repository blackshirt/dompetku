#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
#

"""Form model for various purpose."""

from wtforms_tornado import Form
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import StringField, DateTimeField, TextAreaField, DecimalField, PasswordField

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
    """Form untuk input transaksi"""
    info = StringField("Kegunaan", validators=[DataRequired(), Length(min=10, max=100,
                                                                      message="Isi dengan kalimat lebih dari 10 huruf yang bermakna")])
    amount = DecimalField("Jumlah", validators=[DataRequired()])
    memo = TextAreaField("Catatan transaksi", validators=[DataRequired(), Length(min=5, max=255,
                                                                                 message="Isi dengan kalimat penjelasan yang bermakna")])

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
    """Form registrasi user"""
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
    """Form untuk login"""
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


class UserForm(Form):
    """Form registrasi user"""
    name = StringField('Username', [Length(min=3, max=25)])
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
        if not user.exists():
            self.name.errors.append('User not exists')
            return False
        return True