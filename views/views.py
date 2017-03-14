from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from views.forms import EmailForm
from flask_bootstrap import Bootstrap
from datetime import datetime
from sqlalchemy_utils import PhoneNumberType
from views.send_email import sendMessage
from ast import literal_eval
from dateutil.relativedelta import relativedelta

app  = Flask(__name__)
app.config.from_object('config')
#app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
Bootstrap(app)

fail_message = """
This email is to inform you that we could not find you in our records.

Please sign up here: http://reformmidems.com/

Thanks,

Ryan Wiley (creator of the app)

"""



def successMessage(firstName, lastName, membershipLevel, expirationDate):
	success_message = """
	We found a record of your membership!

	Name: %s %s

	Membership Level: %s

	Your membership will expire on: %s

	Thanks,

	Ryan Wiley (creator of the app)

	""" %(firstName, lastName, membershipLevel, expirationDate)

	return success_message


class SignUpRecord(db.Model):
    __tablename__ = 'email_reminders'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    phone_number = db.Column(PhoneNumberType())
    email = db.Column(db.String(100))
    membership_level = db.Column(db.Text)
    sign_up_time = db.Column(db.DateTime)


    def __init__(self, first_name, last_name, phone_number, email, membership_level, sign_up_time):
    	self.first_name = first_name
    	self.last_name = last_name
    	self.phone_number = phone_number
    	self.email = email
    	self.membership_level = membership_level
    	self.sign_up_time = sign_up_time

    def __repr__(self):
        return "{'first_name': '%s', 'last_name': '%s', 'email': '%s', 'membership_level': '%s', 'sign_up_time':'%s'}" %(self.first_name,
                                                            															 self.last_name,
                                                            															 self.email,
                                                            															 self.membership_level,
                                                            															 self.sign_up_time)

@app.route("/", methods=['GET', 'POST'])
def sendEmail():
    emform = EmailForm()
    form_data = session.get('form_data')
    if emform.validate_on_submit():
        record = literal_eval(str(SignUpRecord.query.filter_by(email=emform.email.data).first()))
        if record:
            expiration = datetime.strptime(record['sign_up_time'].split(" ")[0], '%Y-%m-%d') + relativedelta(years=1)
            sendMessage(emform.email.data, successMessage(record['first_name'], record['last_name'], record['membership_level'], str(expiration.strftime('%m-%d-%Y'))))
        else:
            sendMessage(emform.email.data, fail_message)
        flash("Email Sent!")
    return render_template('/index.jade', response=emform, title = "Check Your MDP Registration Status")
