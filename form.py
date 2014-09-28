from wtforms.fields import IntegerField, StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import Required
from wtforms_tornado import Form



class MessageForm(Form):

    title = TextField(validators=[Required()])
    body = TextAreaField(validators=[Required()])

class TransaksiForm(Form):
    type = TextField(validators=[Required()])
    info = TextField(validators=[Required()])
    amount = TextField(validators=[Required()])
    transdate = TextField(validators=[Required()])
    memo = TextField(validators=[Required()])