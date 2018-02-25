from flask import Flask, request, render_template
from amadeus import Flights
import smtplib
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email
import os
from boto import dynamodb2
from boto.dynamodb2.table import Table

app = Flask(__name__)

class FlightDataForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    depart = StringField('Origin (Airport Code)', validators=[DataRequired()])
    dest = StringField('Destination (Airport Code', validators=[DataRequired()])
    dates = StringField('Dates of Travel (YYYY-MM-DD--YYYY-MM-DD)', validators=[DataRequired()])

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@app.route('/')
def my_form():
    form = FlightDataForm(request.form)
    return render_template('my-form.html', form = form)

@app.route('/', methods=['POST'])
def my_form_post():
    form = FlightDataForm(request.form)
    email = form.email.data
    depart = form.depart.data.upper()
    dest = form.dest.data.upper()
    dates = form.dates.data
    key = 'uc3P6EbsIUyjwIfT9eQLyNdUp4CbWbem'
    flights = Flights(key)
    resp = flights.extensive_search(
        origin= depart,
        destination= dest,
        departure_date=dates)
    print(resp)
    a = resp['results'][0]['airline']
    b = resp['results'][0]['price']
    c = resp['results'][1]['airline']
    d = resp['results'][1]['price']
    e = resp['results'][2]['airline']
    f = resp['results'][2]['price']
    flight1 = f'{a} flight: {b}\n'
    flight2 = f'{c} flight: {d}\n'
    flight3 = f'{e} flight: {f}\n'
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    sendemail = 'flightsaleresponse@gmail.com'
    apppwd = 'kxgrfartdbtkdubf'
    smtp_server.login(sendemail, apppwd)
    #toaddr = 'izaankml@gmail.com' #CHANGE TO ACTUAL SENDER
    msg = "\r\n".join([
        "From: flightsaleresponse@gmail.com",
        "To: izaankml@gmail.com",
        "Subject: Your flight offers for the week",
        f"Your top 3 flights from {resp['origin']} to {resp['results'][3]['destination']}\n",
        flight1,
        flight2,
        flight3,
        "Thank You, and have a great day!"
        ])
    smtp_server.sendmail(sendemail, email, msg)
    return ('Congratulations! You have been subscribed to the mailing list.')


