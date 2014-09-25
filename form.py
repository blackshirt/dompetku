from wtforms.fields import IntegerField, StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import Required
from wtforms_tornado import Form



class MessageForm(Form):

    title = TextField(validators=[Required()])
    body = TextAreaField(validators=[Required()])

