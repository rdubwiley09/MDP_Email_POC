from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from wtforms_alchemy import PhoneNumberField
from flask_admin.form.widgets import DatePickerWidget
from wtforms.fields.html5 import DateField

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Send Email')

class TextForm(FlaskForm):
    phone_number = PhoneNumberField(validators=[DataRequired()], render_kw={"placeholder": "Phone Number"})
    submit = SubmitField('Send Text')

